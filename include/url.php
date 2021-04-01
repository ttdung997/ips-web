<header class="panel-heading" data-toggle="collapse" href="#RuleTableURL"  aria-expanded="false" aria-controls="RuleTable" style="margin-left: 20px; margin-top:50px; margin-right: 1px; height: 50px; background-color:#343a40; border-top-left-radius: 5px; border-top-right-radius: 5px;">
<i class="fa fa-globe" style="margin-top:17px; margin-left: 10px; color: white;">  URL</i>
</header>
<?php

    $db = new SQLite3('data/check.sqlite');

    $res = $db->query('SELECT * FROM mod_url_deny');
?>
<div class="collapse multi-collapse" id="RuleTableURL" style="overflow:auto; margin-top: 10px;">
<table id="RuleTableurl" class="table table-striped table-bordered thead-dark" style="width:98%; margin-left: 20px;">
        <thead>
            <tr>
                <th>Url</th>
                <th>Chi tiết</th>
                <th id="tbedit_u"></th>
            </tr>
        </thead>
         <tbody>
                <?php
                    while ($row = $res->fetchArray()) {
                                        echo "<tr>";
                                        echo "<td>".$row['url']."</td>";
                                        echo "<td>".$row['description']."</td>";
                                        
                                      ?>
                                       <td>
                                       <form style="float: left;" method="post" action="dga_malware_detail.php">
                                <input name = "id" type="hidden" value="<?=$row['id']?>">
                                <button type="submit" class="btn btn-del Disable"><i class="fa fa-search" aria-hidden="true" style="font-size: 1.2rem;"></i></button>
                              </form>
                                       <form style="float: left;" method="post" action="php/deleteurldeny.php">
                                <input name = "id" type="hidden" value="<?=$row['id']?>">
                                <button type="submit" class="btn btn-del Disable"><i class="fa fa-trash-o" aria-hidden="true" style="font-size: 1.2rem;"></i></button>
                              </form></td>
                              </tr>
                            <?php
                                }
                            ?>
        </tbody>
    </table>
<button class="btn btn-info" style="float:right; margin-top: 10px; margin-right:15px;" id="addUrl" onclick="AppendUrl()"><i class="fa fa-plus" style="padding-right:10px;"></i><span class="glyphicon glyphicon-plus-sign"></span> Thêm mới</button>
</div>



<script>
var isEdit = false;
var table_url;


function AppendUrl() {
    tr = $(".fa-check");
    if (!tr.length){
        $('#RuleTableurl').append('<tr id="URLRuleAppend" role="row" class="even"><td class="sorting_1"><input id="addUrlRule" style="width: 100%;" value=""></td><td><input id="addUrlRuleDescription" style="width: 100%;" value=""></td><td><i style="margin-left:13px;" class="fa fa-lg fa-check" title="Save" aria-hidden="true" id="saveIpRule" onclick="SaveUrl()"></i><i style="margin-left: 20px;" class="fa fa-lg fa-close" title="Delete" aria-hidden="true" id="deleteUrl" onclick="reloadUrlRuleTable()"></i></td></tr>');    
    }
}

function reloadUrlRuleTable() {
      location.reload();
}

var value=[];

function EditUrl(id) {
    check = $('.fa-check');
    if (!check.length){
    $("#editUrl_"+id).toggleClass('fa-edit fa-check');
    $("#deleteUrl_"+id).toggleClass('fa-trash-o fa-close');
    $("#editUrl_"+id).attr("onclick", "UpdateUrl(\'"+ id +"\')");
    $("#deleteUrl_"+id).attr("onclick", "reloadUrlRuleTable()");
    var column = $("#editUrl_"+id).parent().parent().children();
    for (i = 0; i < column.length - 2; i++) {
        value[i] = column[i].innerText;
        column[i].innerHTML="<input id='input_data_"+ (i+1) +"' style='width: 100%;' value='" + value[i] + "'>";
    }
    value[column.length - 2] = column[column.length - 2].innerText;
    column[column.length - 2].innerHTML='<td><select id="addGroupRule"> <option></option>' + '<?php foreach ($group_rule as $value) {echo "<option value=\"$value->id\">$value->name</option>";} ?>'+'</select></td>';

}
}



function SaveUrl() {
    Url = $('#addUrlRule').val();
    var re = /(http:\/\/|https:\/\/)?((\w|\d)+(\.(\w|\d)+)+)\/(.*)/;
    var new_string = Url.replace(re, "$2,$6");
    console.log(new_string);
    var array = new_string.split(",");
    if (array.length != 2){
        url = array[0];
        host = '0';
    } else {
        host = array[0];
        url = array[1];
    }
    if (url.charAt(0) == "/") {
        url = url.substr(1);
    }
    console.log(url);
    console.log(host);
    description = $('#addUrlRuleDescription').val();
    group_rule = $('#addGroupRule').val();
    if (description == '' || url == ''){
        alert('Please fill the url and description !!!');
        return 0;
    }
    var data = new FormData();
    data.append('host', host);
    data.append('url', url);
    data.append('description', description);
    data.append('group_rule', group_rule);
    $.ajaxSetup({
        headers: {
            'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
        }
    });
    $.ajax({
        method: "POST",
        url: "php/addurldeny.php",
        data: data,
        processData: false,
        contentType: false,
        success : function(a){
            // if (a != 1) alert(a);
            
            alert("Đã thêm luật thành công");
            reloadUrlRuleTable();
            something_change = 1;
        },
    });
}

function UpdateUrl(id) {
    Url = $("#input_data_1").val();
    // Url = $('#addUrlRule').val();
    var re = /(http:\/\/|https:\/\/)?((\w|\d)+(\.(\w|\d)+)+)\/(.*)/;
    var new_string = Url.replace(re, "$2,$6");
    var array = new_string.split(",");
    if (array.length != 2){
        url = array[0];
        host = '0';
    } else {
        host = array[0];
        url = array[1];
    }
    if (url.charAt(0) == "/") {
        url = url.substr(1);
    }
    description = $("#input_data_2").val();
    group_rule = $('#addGroupRule').val();
    id_num = id;
    if (url == '' || description == '') {
        alert('Please fill the host, url and description !!!');
    } else {
    $("#editUrl_"+id).toggleClass('fa-check fa-edit');
    $("#deleteUrl_"+id).toggleClass('fa-close fa-trash-o');
    $("#editUrl_"+id).attr("onclick", "EditUrl(\'"+ id +"\')");
    $("#deleteUrl_"+id).attr("onclick", "DeleteUrl(\'"+ id +"\')");
    var data = new FormData();
    data.append('id', id_num);
    data.append('host', host);
    data.append('url', url);
    data.append('description', description);
    data.append('group_rule', group_rule);
    var re = /(http:\/\/|https:\/\/)?((\w|\d)+(\.(\w|\d)+)+)\/(.*)/;
    var new_string = value[0].replace(re, "$2,$6");
    var array = new_string.split(",");
    if (array.length != 2){
        old_url = array[0];
        old_host = '0';
    } else {
        old_host = array[0];
        old_url = array[1];
    }
    if (old_url.charAt(0) == "/") {
        old_url = old_url.substr(1);
    }
    data.append('old_host', old_host);
    data.append('old_url', old_url);
    data.append('old_description', value[1]);
    data.append('old_group_rule', value[2]);
    console.log(host);
    console.log(url);
    console.log(description);
    console.log(group_rule);
    console.log(old_host);
    console.log(old_url);
    console.log(value[1]);
    console.log(value[2]);
    $.ajaxSetup({
        headers: {
            'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
        }
    });
    $.ajax({
        method: "POST",
        url: "{{route('update-url-rule')}}",
        data: data,
        processData: false,
        contentType: false,
        success : function(a){
            if (a != 1) alert(a);
            reloadUrlRuleTable();
            something_change = 1;
            value = [];
        },
    });
    }   
}

function DeleteUrl(id) {
    check = $('.fa-check');
    if (!check.length){
    $("#editUrl_"+id).toggleClass('fa-edit fa-check');
    $("#deleteUrl_"+id).toggleClass('fa-trash-o fa-close');
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
        url: "{{route('delete-url-rule')}}",
        data: data,
        processData: false,
        contentType: false,
        success : function(a){
            if (a != 1) alert(a);
            reloadUrlRuleTable();
            something_change = 1;
        },
    });
    }
    reloadUrlRuleTable();
    }
}
</script>