<?php

include 'include/header.php';

?>
            <div class="content-wrapper">
                <!-- Content Header (Page header) -->
                <section class="content-header">
                    <div class="container-fluid-header">
                        <div class="row mb-2">
                            <div class="col-sm-6">
                                <h1>Theo dõi tệp tin</h1>

                            </div>
                            <div class="col-sm-6">
                                <ol class="breadcrumb float-sm-right">
                                    <li class="breadcrumb-item"><a href="/"><i class="fa fa-home" aria-hidden="true"></i> Trang chủ</a></li>
                                    <li class="breadcrumb-item active">Theo dõi tệp tin</li>
                                </ol>
                            </div>
                        </div>
                    </div>
                    <!-- /.container-fluid -->
                </section>

                <!-- Main content -->
                <section class="content">
            
                             <div id="menu1">
<div class="row">
              <div class="col-sm-5">
                <h3>Chọn tệp</h3>
                <div id="files">

                </div>
                    <div class="row" style="margin: 10px 0px;">
    
            <button id="button1" type="button" class="btn btn-add" onclick="add()"><i class="fa fa-check"></i> Thêm đường dẫn </button>
            

              </div>
            </div>
              <div class="col-sm-7">

                <h3>Danh sách tệp bảo vệ </h3>
                   <div  id="list_error"  style="border: 1px solid #585858; border-radius: 5px; max-height: 500px;min-height: 500px;  overflow-y: auto; background-color: #00000045;padding: 10px;">
                   </div>
                    <div class="row float-right" style="margin: 10px 0px;">
            
             <button id="button1" type="button" class="btn btn-add" onclick="deletePath()"><i class="fa fa-check"></i> Xóa đường dân</button>
          </div>
                   
        </div>
              </div>
             
            </div>
            <br><br>
                             </div></div>
        <!-- /.row -->
        <input hidden  id="curpath" value="">
        <input hidden  id="choosepath" value="">
        <input hidden  id="deletepath" value="">
  <?php


$data = array_values($array);
$label = array_keys($array);
$data = json_encode(array_reverse($data));
$label = json_encode(array_reverse($label));
// print_r($data);
// print_r($label);
include 'include/footer.php';

?>
        <script src="admin_asset_web/dist/js/demo.js"></script>
<script src="admin_asset_web/plugins/js/Chart.js"></script>
        <script type="text/javascript">

function add(){
 var data = new FormData();
 var curpath = document.getElementById("curpath").value;
 var item = document.getElementById("choosepath").value;
 var path = curpath + "/" + item;
data.append('path', path);

  $.ajax({ 
  method: "POST",
  url: "/php/moniter_add.php",
  data: data,
  processData: false,
  contentType: false,
    async: false,
    cache: false,
   // url: "/check",
   // headers:  {'Access-Control-Allow-Origin' : 'http://192.168.218.138'},
   success: function (data) {
    console.log(data)
    alert("Đã thêm đương dẫn thành công");

  loadPath();
   }

 });
}


function deletePath(){
 var data = new FormData();
 var item = document.getElementById("deletepath").value;
 var path = item;
 console.log(path);
data.append('path', path);

  $.ajax({ 
  method: "POST",
  url: "/php/moniter_delete.php",
  data: data,
  processData: false,
  contentType: false,
    async: false,
    cache: false,
   // url: "/check",
   // headers:  {'Access-Control-Allow-Origin' : 'http://192.168.218.138'},
   success: function (data) {

    alert("Đã xóa đường dẫn");


  loadPath();
   }

 });
}


$(document).ready(function () {
  $('#DgaTable').DataTable();
  $('.dataTables_length').addClass('bs-select');
});
function getInfo(){
$(document).ready(function() {
    $.ajax({
        type: "GET",
        url: 'php/file_scan.php',
        success: function(response)
        {

            console.log("ending");

        }
       });
     });
   
}

// getInfo();

// window.setInterval(function () {
//   getInfo();
// }, 5000);




var ctx = document.getElementById("myChart");
var myChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: <?=$label?>,
    datasets: [{
      label: 'Thống kê loại file upload đến hệ thống',
      data: <?=$data?>,
     backgroundColor: '#638b94',
      borderWidth: 1
    }]
  },
  options: {
    responsive: false,
    scales: {
      xAxes: [{
        ticks: {
          maxRotation: 90,
          minRotation: 80
        }
      }],
      yAxes: [{
        ticks: {
          beginAtZero: false
        }
      }]
    }
  }
});

Chart.defaults.global.defaultFontColor = '#dcf3ff';



</script>

<script type="text/javascript">
  function getFile() {
  // checkErrors();
   var data = new FormData();

  data.append('path', '/');
  $.ajax({ 
  method: "POST",
  url: "/php/path_get.php",
  data: data,
  processData: false,
  contentType: false,
    async: false,
    cache: false,
   // url: "/check",
   // headers:  {'Access-Control-Allow-Origin' : 'http://192.168.218.138'},
   success: function (data) {
     console.log(data)
     list = JSON.parse(data)[0];
     folder = JSON.parse(data)[1];
   }
 });
  
  
    if (list != false){
     $("#files").empty()
    for(var i =0; i<list.length; i++){
      if (folder[i] == 1){
        var icon =  '<span><i class="fa fa-folder-o" aria-hidden="true"></i> '
      }else{
        var icon  = '<i class="fa fa-file-o" aria-hidden="true"> '
      }
      $("#files").append('<div class="file" id="'+list[i]+'"><span>'+icon+list[i]+'</span></div>')
     document.getElementById(list[i]).addEventListener("dblclick", function(){
        path = $(this).attr("id");
        readErrors(path)
      });
      document.getElementById(list[i]).addEventListener("click", function(){
        path = $(this).attr("id");
        $(".file").css('background-color', 'transparent');
        $(this).css('background-color', 'rgba(255,255,255,0.2)');
        document.getElementById("choosepath").value = path;

      });

    }
  
  

}
}
getFile()

function loadPath(){
  var data = new FormData();

  data.append('path', '/');
  $.ajax({ 
  method: "POST",
  url: "/php/moniter_get.php",
  data: data,
  processData: false,
  contentType: false,
    async: false,
    cache: false,
   // url: "/check",
   // headers:  {'Access-Control-Allow-Origin' : 'http://192.168.218.138'},
   success: function (data) {
     // console.log(data)
     list = JSON.parse(data)["check_list"];
     console.log(list);
     $("#list_error").empty()
   }
 });
    for(var i =0; i<list.length; i++){
      // console.log(i);
      $("#list_error").append('<div class="file" id="'+list[i][2]+"&"+list[i][1]+'"><span><i class="fa fa-file-o" aria-hidden="true"></i> '+list[i][2]+'</span></div>')
       document.getElementById(list[i][2]+"&"+list[i][1]).addEventListener("click", function(){
        path = $(this).attr("id");
        $(".file").css('background-color', 'transparent');
        $(this).css('background-color', 'rgba(255,255,255,0.2)');
        document.getElementById("deletepath").value = path;

      });

    }
}

loadPath();

   function clearFun(){
       console.log("clear");
     $("#list_error").empty();
     $("#error_content").empty();
     $("#error_des").empty();
     $("#error_total").empty();
   
   }
   function reload(){
   curpath =  document.getElementById("curpath").value;
 
   var data = new FormData();
  
  data.append('path', curpath);
   $.ajax({ 
  method: "POST",
  url: "/php/path_get.php",
  data: data,
  processData: false,
  contentType: false,
    async: false,
    cache: false,
   // url: "/check",
   // headers:  {'Access-Control-Allow-Origin' : 'http://192.168.218.138'},
   success: function (data) {
     console.log(data)
     list = JSON.parse(data)[0];
     folder = JSON.parse(data)[1];

   }
 });
  
    if (list != false){
     $("#files").empty()
    for(var i =0; i<list.length; i++){
      if (folder[i] == 1){
        var icon =  '<span><i class="fa fa-folder-o" aria-hidden="true"></i> '
      }else{
        var icon  = '<i class="fa fa-file-o" aria-hidden="true"> '
      }
      $("#files").append('<div class="file" id="'+list[i]+'"><span>'+icon+list[i]+'</span></div>')
      document.getElementById(list[i]).addEventListener("dblclick", function(){
        path = $(this).attr("id");
        readErrors(path)
      });
      document.getElementById(list[i]).addEventListener("click", function(){
        path = $(this).attr("id");
        $(".file").css('background-color', 'transparent');
        $(this).css('background-color', 'rgba(255,255,255,0.2)');
        document.getElementById("choosepath").value = path;

      });
    }
   
   }else{
    alert("Tệp đã chọn không là thư mục ");
    document.getElementById("curpath").value =  backup_path;
   }
 }
   
   function readErrors(path){
  curpath = document.getElementById("curpath").value;
  backup_path = curpath;
  if(path != ".."){
  if(curpath != "/"){
    curpath = curpath +  "/" +path;
  }else{
    curpath = curpath + path;
  }
  }else{
    newpath = curpath.split("/")[0]
    for (i = 1; i < curpath.split("/").length - 1; i ++){
      newpath = newpath + "/"+curpath.split("/")[i];
    }

    curpath = newpath
  }
  if (curpath == ""){
    curpath ="/"
  }

  document.getElementById("curpath").value = curpath;
  console.log(curpath)
   var data = new FormData();
  
  console.log(curpath);
  data.append('path', curpath);
   $.ajax({ 
  method: "POST",
  url: "/php/path_get.php",
  data: data,
  processData: false,
  contentType: false,
    async: false,
    cache: false,
   // url: "/check",
   // headers:  {'Access-Control-Allow-Origin' : 'http://192.168.218.138'},
   success: function (data) {
     console.log(data)
     list = JSON.parse(data)[0];
     folder = JSON.parse(data)[1];

   }
 });
  
    if (list != false){
     $("#files").empty()
     for(var i =0; i<list.length; i++){
      if (folder[i] == 1){
        var icon =  '<span><i class="fa fa-folder-o" aria-hidden="true"></i> '
      }else{
        var icon  = '<i class="fa fa-file-o" aria-hidden="true"> '
      }
      $("#files").append('<div class="file" id="'+list[i]+'"><span>'+icon+list[i]+'</span></div>')
      document.getElementById(list[i]).addEventListener("dblclick", function(){
        path = $(this).attr("id");
        readErrors(path)
      });
      document.getElementById(list[i]).addEventListener("click", function(){
        path = $(this).attr("id");
        $(".file").css('background-color', 'transparent');
        $(this).css('background-color', 'rgba(255,255,255,0.2)');
        document.getElementById("choosepath").value = path;

      });
    }
   
   }else{
    alert("Tệp đã chọn không là thư mục ");
    document.getElementById("curpath").value =  backup_path;
   }
 }
   
   
   
   
</script>
