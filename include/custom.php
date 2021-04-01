<header class="panel-heading" data-toggle="collapse" href="#RuleTableCustom"  aria-expanded="false" aria-controls="RuleTable" style="margin-top:50px; margin-right: 1px; height: 50px; background-color:#343a40; border-top-left-radius: 5px; border-top-right-radius: 5px;">
<i class="fa fa-globe" style="margin-top:17px; margin-left: 10px; color: white;">  CUSTOM RULE</i>
</header>
<?php

    $db = new SQLite3('data/check.sqlite');

    $res = $db->query('SELECT * FROM mod_custom_rule');
?>
<div class="collapse multi-collapse" id="RuleTableCustom" style="overflow:auto; margin-left: 20px; margin-top: 10px;">
<table id="RuleTablecustom" class="table table-striped table-bordered thead-dark" style="width:98%;">
        <thead>
            <tr>
                <th id="tbrule_c">Tên luật</th>
                <th id="tbdes_c">Nội dung</th>
                <th id="tbedit_c"></th>
            </tr>
        </thead>
         <tbody>
                <?php
                    while ($row = $res->fetchArray()) {
                                        echo "<tr>";
                                        echo "<td>".$row['rule']."</td>";
                                        echo "<td>".$row['description']."</td>";
                                        
                                      ?>
                                       <td>
                                       <form style="float: left;" method="post" action="dga_malware_detail.php">
                                <input name = "id" type="hidden" value="<?=$row['id']?>">
                                <button type="submit" class="btn btn-del Disable"><i class="fa fa-search" aria-hidden="true" style="font-size: 1.2rem;"></i></button>
                              </form>
                                       <form style="float: left;" method="post" action="php/deletecustomrule.php">
                                <input name = "id" type="hidden" value="<?=$row['id']?>">
                                <input name = "rule" type="hidden" value="<?=$row['description']?>">
                                <button type="submit" class="btn btn-del Disable"><i class="fa fa-trash-o" aria-hidden="true" style="font-size: 1.2rem;"></i></button>
                              </form></td>
                              </tr>
                            <?php
                                }
                            ?>
        </tbody>
    </table>
<button class="btn btn-info" style="float:right; margin-top: 10px; margin-right:15px;" id="add" onclick="AppendCustom()"><i class="fa fa-plus" style="padding-right:10px;"></i><span class="glyphicon glyphicon-plus-sign"></span>Thêm mới</button>
</div>

<script>
var isEdit = false;
var table_custom;

function AppendCustom() {
    tr = $(".fa-check");
    if (!tr.length){
        $('#RuleTablecustom').append('<tr id="CUSTOMRuleAppend" role="row" class="even"><td class="sorting_1"><input id="addCustomRule" style="width: 100%;" value=""></td><td><textarea id="addCustomRuleDescription" style="width: 520px;"></textarea></td><td><i style="margin-left:13px;" class="fa fa-lg fa-check" title="Save" aria-hidden="true" id="saveCustomRule" onclick="SaveCustom()"></i><i style="margin-left: 20px;" class="fa fa-lg fa-close" title="Delete" aria-hidden="true" id="deleteCustomRule" onclick="reloadCustomRuleTable()"></i></td></tr>');    
    }
}

function reloadCustomRuleTable() {
      location.reload();
}

var value=[];

function EditCustom(id) {
    check = $('.fa-check');
    if (!check.length){
    $("#editCustom_"+id).toggleClass('fa-edit fa-check');
    $("#deleteCustom_"+id).toggleClass('fa-trash-o fa-close');
    $("#editCustom_"+id).attr("onclick", "UpdateCustom(\'"+ id +"\')");
    $("#deleteCustom_"+id).attr("onclick", "reloadCustomRuleTable()");
    var column = $("#editCustom_"+id).parent().parent().children();
    value[0] = $(column[0]).text();
    console.log(value);
        column[0].innerHTML='<textarea id="textRule" name="comment" style="width: 520px;">' + value[0] + '</textarea>';
    for (i = 1; i < column.length - 2; i++) {
        value[i] = column[i].innerText;
        column[i].innerHTML="<input id='input_data_"+ (i+1) +"' style='width: 100%;' value='" + value[i] + "'>";
    }
    value[column.length - 2] = column[column.length - 2].innerText;
    column[column.length - 2].innerHTML='<td><select id="addGroupRuleCustom"> <option></option>' + '<?php foreach ($group_rule as $value) {echo "<option value=\"$value->id\">$value->name</option>";} ?>'+'</select></td>';
}
}



function SaveCustom() {
    rule = $('#addCustomRule').val();
    description = $('#addCustomRuleDescription').val();
    group_rule = $('#addGroupRuleCustom').val();
    var data = new FormData();
    data.append('rule', rule);
    data.append('description', description);
    data.append('group_rule', group_rule);
    $.ajaxSetup({
        headers: {
            'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
        }
    });
    $.ajax({
        method: "POST",
        url: "php/addcustomrule.php",
        data: data,
        processData: false,
        contentType: false,
        success : function(a){
            // if (a != 1) alert(a);
            
            alert("Đã thêm luật thành công");
            reloadCustomRuleTable();
            something_change = 1;
            $("#tbedit_c").css('width', '60');
        },
    });
}

function UpdateCustom(id) {
    rule = $("#textRule").val();
    description = $("#input_data_2").val();
    group_rule = $('#addGroupRuleCustom').val();
    id_num = id;
    $("#editCustom_"+id).toggleClass('fa-check fa-edit');
    $("#deleteCustom_"+id).toggleClass('fa-close fa-trash-o');
    $("#editCustom_"+id).attr("onclick", "EditCustom(\'"+ id +"\')");
    $("#deleteCustom_"+id).attr("onclick", "DeleteCustom(\'"+ id +"\')");
    var data = new FormData();
    data.append('id', id_num);
    data.append('rule', rule);
    data.append('description', description);
    data.append('group_rule', group_rule);
    data.append('old_rule', value[0]);
    data.append('old_description', value[1]);
    data.append('old_group_rule', value[2]);
    // console.log(id_num);
    // console.log(rule);
    // console.log(description);
    // console.log(group_rule);
    // console.log(value[0]);
    // console.log(value[1]);
    // console.log(value[2]);
    $.ajaxSetup({
        headers: {
            'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
        }
    });
    $.ajax({
        method: "POST",
        url: "{{route('update-custom-rule')}}",
        data: data,
        processData: false,
        contentType: false,
        success : function(a){
            if (a != 1) alert(a);
            reloadCustomRuleTable();
            value = [];
            something_change = 1;
            $("#tbedit_c").css('width', '60');
        },
    });
}

function DeleteCustom(id) {
    check = $('.fa-check');
    if (!check.length){
    $("#editCustom_"+id).toggleClass('fa-edit fa-check');
    $("#deleteCustom_"+id).toggleClass('fa-trash-o fa-close');
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
        url: "{{route('delete-custom-rule')}}",
        data: data,
        processData: false,
        contentType: false,
        success : function(a){
            if (a != 1) alert(a);
            reloadCustomRuleTable();
            something_change = 1;
            $("#tbedit_c").css('width', '60');
        },
    });
    }
    reloadCustomRuleTable();
    }
}
</script>