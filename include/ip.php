<header class="panel-heading" data-toggle="collapse" href="#RuleTableIP"  aria-expanded="false" aria-controls="RuleTable" style="height: 50px; background-color:#343a40; border-top-left-radius: 5px; border-top-right-radius: 5px;">
<i class="fa fa-globe" style="margin-top:17px; margin-left: 10px; color: white;">  IP</i>

</header>
<?php

                    $db = new SQLite3('data/check.sqlite');

                    $res = $db->query('SELECT * FROM mod_ip_deny');
            ?>
<div class="collapse multi-collapse" id="RuleTableIP" style="overflow:auto; margin-top: 10px;">
<table id="RuleTableip" class="table table-striped table-bordered thead-dark" style="width:100%; margin-left: 10px;">
        <thead>
            <tr>
                <th>IP</th>
                <th>Chi tiết</th>
                <th id="tbedit"></th>
            </tr>
        </thead>
        <tbody>
                <?php
                    while ($row = $res->fetchArray()) {
                                        echo "<tr>";
                                        echo "<td>".$row['ip']."</td>";
                                        echo "<td>".$row['description']."</td>";
                                        
                                      ?>
                                       <td>
                                    
                                       <form style="float: left;" method="post" action="php/deleteip.php">
                                <input name = "id" type="hidden" value="<?=$row['id']?>">
                                <button type="submit" class="btn btn-del Disable"><i class="fa fa-trash-o" aria-hidden="true" style="font-size: 1.2rem;"></i></button>
                              </form></td>
                              </tr>
                            <?php
                                }
                            ?>
        </tbody>
    </table>
<button class="btn btn-info" style="float:right; margin-top: 10px; margin-right:15px;" id="add" onclick="AppendIP()"><i class="fa fa-plus" style="padding-right:10px;"></i><span class="glyphicon glyphicon-plus-sign"></span> Thêm mới </button>
</div>


  <!--     <i style="margin-left:13px;" class="fa fa-lg fa-edit" title="Edit" aria-hidden="true" id="editIp_'+ data.id +'" onclick="EditIP(\''+ data.id +'\')"></i><i style="margin-left: 20px;" class="fa fa-lg fa-trash-o" title="Delete" aria-hidden="true" id="deleteIp_'+ data.id +'" onclick="DeleteIP(\''+ data.id +'\')"></i>
       -->
<script>
function AppendIP() {
    tr = $(".fa-check");
    if (!tr.length){
        $('#RuleTableip').append('<tr id="IPRuleAppend" role="row" class="even"><td class="sorting_1"><input id="addIPRuleName" style="width: 100%;" value=""></td><td><input id="addIpRuleDescription" style="width: 100%;" value=""></td><td><i style="margin-left:13px;" class="fa fa-lg fa-check" title="Save" aria-hidden="true" id="saveIpRule" onclick="SaveIP()"></i><i style="margin-left: 20px;" class="fa fa-lg fa-close" title="Delete" aria-hidden="true" id="deleteIp" onclick="reloadIPRuleTable()"></i></td></tr>');    
    }
}

function reloadIPRuleTable() {
  location.reload();
}

function EditIP(id) {
    check = $('.fa-check');
    if (!check.length){
    $("#editIp_"+id).toggleClass('fa-edit fa-check');
    $("#deleteIp_"+id).toggleClass('fa-trash-o fa-close');
    $("#editIp_"+id).attr("onclick", "UpdateIP(\'"+ id +"\')");
    $("#deleteIp_"+id).attr("onclick", "reloadIPRuleTable()");
    var column = $("#editIp_"+id).parent().parent().children();
    for (i = 0; i < column.length - 2; i++) {
        value = column[i].innerText;
        column[i].innerHTML="<input id='input_data_"+ (i+1) +"' style='width: 100%;' value='" + value + "'>";
    }
    column[column.length - 2].innerHTML='<select id="addGroupRule" style="min-width: 100%;"><option></option>' + '<?php foreach ($group_rule as $value) {echo "<option id=\"select$value->id\" value=\"$value->id\">$value->name</option>";} ?>'+'</select>';
}
}



function SaveIP() {
    ip = $('#addIPRuleName').val();
    description = $('#addIpRuleDescription').val();
    group_rule = $('#addGroupRule').val();
    var data = new FormData();
    data.append('ip', ip);
    data.append('description', description);
    data.append('group_rule', "1");
    console.log(data);
    $.ajaxSetup({
        headers: {
            'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
        }
    });
    $.ajax({
        method: "POST",
        url: "/php/addipdeny.php",
        data: data,
        processData: false,
        contentType: false,
        success : function(a){
            // if (a != 1) alert(a);
            alert("Đã thêm luật thành công");
            reloadIPRuleTable();
            something_change = 1;
        },
    });
}

function UpdateIP(id) {
    ip = $("#input_data_1").val();
    description = $("#input_data_2").val();
    group_rule = $("#addGroupRule").val();
    id_num = id;
    $("#editIp_"+id).toggleClass('fa-check fa-edit');
    $("#deleteIp_"+id).toggleClass('fa-close fa-trash-o');
    $("#editIp_"+id).attr("onclick", "EditIP(\'"+ id +"\')");
    $("#deleteIp_"+id).attr("onclick", "DeleteIP(\'"+ id +"\')");
    var data = new FormData();
    data.append('id', id_num);
    data.append('ip', ip);
    data.append('description', description);
    data.append('group_rule', group_rule);
    $.ajaxSetup({
        headers: {
            'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
        }
    });
    $.ajax({
        method: "POST",
        url: "{{route('update-ip-rule')}}",
        data: data,
        processData: false,
        contentType: false,
        success : function(a){
            if (a != 1) alert(a);
            reloadIPRuleTable();
            something_change = 1;
            value = [];
        },
    });
}

function DeleteIP(id) {
    check = $('.fa-check');
    if (!check.length){
    $("#editIp_"+id).toggleClass('fa-edit fa-check');
    $("#deleteIp_"+id).toggleClass('fa-trash-o fa-close');
    con = confirm ("Are you sure????");
    if (con == true){
        id_num = id;
        var data = new FormData();
        data.append('id', id_num);
        $.ajaxSetup({
        headers: {
            'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
        }
    });
    $.ajax({
        method: "POST",
        url: "{{route('delete-ip-rule')}}",
        data: data,
        processData: false,
        contentType: false,
        success : function(a){
            if (a != 1) alert(a);
            reloadIPRuleTable();
            something_change = 1;
        },
    });
    }
    reloadIPRuleTable();
    }
}
</script>

