<?php

include 'include/header.php';

?>
            <div class="content-wrapper">
                <!-- Content Header (Page header) -->
                <section class="content-header">
                    <div class="container-fluid-header">
                        <div class="row mb-2">
                            <div class="col-sm-6">
                                <h1>Mã hóa tệp tin</h1>

                            </div>
                            <div class="col-sm-6">
                                <ol class="breadcrumb float-sm-right">
                                    <li class="breadcrumb-item"><a href="/"><i class="fa fa-home" aria-hidden="true"></i> Trang chủ</a></li>
                                    <li class="breadcrumb-item active">Mã hóa tệp tin</li>
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
              <div class="col-sm-12">
                <h3>Chọn tệp</h3>
                <div id="files">
                  
                </div>
              </div>
        </div>
              </div>
              <br>
              <div class="col-sm-4">
              <div class="row" style="padding-bottom: 30px; margin-right: 20px;">
            <button id="button1" type="button" class="btn btn-add" data-toggle="modal" data-target="#myModal" style="margin: 0px 10px 10px 0px;"><i class="fa fa-lock" aria-hidden="true"></i> Mã hóa</button>
             <button id="button1" type="button" class="btn btn-add" data-toggle="modal" data-target="#myModalDecrypt" style="margin: 0px 10px 10px 0px;"><i class="fa fa-unlock" aria-hidden="true"></i> Giải mã</button>
          </div>
            </div>
            <br><br>
                             </div></div>
        <!-- /.row -->
        <input hidden  id="curpath" value="">
        <input hidden  id="choosepath" value="">

          <!-- Modal -->
  <div class="modal fade" id="myModal" role="dialog">
    <div class="modal-dialog" style="max-width: 500px; color: white;">
    
      <!-- Modal content-->
      <div class="modal-content" style="background: #404b56;">
        <div class="modal-body">
          <label>Nhập mật khẩu mã hóa</label>
            <input id="pass" class="form-control">
        </div>
        <div class="modal-footer" style="border-top: 0px;">
          <button type="button" class="btn btn-add" data-dismiss="modal" onclick="encrype()">Bắt đầu mã hóa</button>
        </div>
      </div>
      
    </div>
  </div>

  <!-- Modal -->
  <div class="modal fade" id="myModalDecrypt" role="dialog">
    <div class="modal-dialog" style="max-width: 500px; color: white;">
    
      <!-- Modal content-->
      <div class="modal-content" style="background: #404b56;">
        <div class="modal-body">
          <label>Nhập mật khẩu giải mã</label>
            <input id="pass2" class="form-control">
        </div>
        <div class="modal-footer" style="border-top: 0px;">
          <button type="button" class="btn btn-add" data-dismiss="modal" onclick="decrype()">Bắt đầu giải mã</button>
        </div>
      </div>
      
    </div>
  </div>

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

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}


async function encrype(){
 loading_nomal();
 await sleep(100);

 var data = new FormData();

 var curpath = document.getElementById("curpath").value;
 var item = document.getElementById("choosepath").value;
 var path = curpath + "/" + item
 var pass = document.getElementById("pass").value;
  data.append('path', path);
  data.append('pass', pass);
  $.ajax({ 
  method: "POST",
  url: "/php/encrype.php",
  data: data,
  processData: false,
  contentType: false,
    async: false,
    cache: false,
   // url: "/check",
   // headers:  {'Access-Control-Allow-Origin' : 'http://192.168.218.138'},
   success: function (data) {
    data = JSON.parse(data)
    console.log(data[0])
    if (data[0] ==1){
    if (data[1] == false){
    clearLoading();
    alert("Đã mã hóa tệp tin thành công");

    }else{
      clearLoading();
      alert("Đã mã hóa thư mục thành công");
    }
    }else{
      clearLoading();
        alert("Đã có lỗi xảy ra trong quá trình mã hóa ");

        }

  reload();
   }

 });
}

async function decrype(){
 loading_nomal();
 await sleep(100);
 var data = new FormData();

 var curpath = document.getElementById("curpath").value;
 var item = document.getElementById("choosepath").value;
 var path = curpath  + "/" +  item
 var pass = document.getElementById("pass2").value;
  data.append('path', path);
  data.append('pass', pass);
  $.ajax({ 
  method: "POST",
  url: "/php/decrype.php",
  data: data,
  processData: false,
  contentType: false,
    async: false,
    cache: false,
   // url: "/check",
   // headers:  {'Access-Control-Allow-Origin' : 'http://192.168.218.138'},
   success: function (data) {
    console.log(data)
    data = JSON.parse(data)
    if (data[0] ==1){
      if (data[1] == false){
        clearLoading();
      alert("Đã giải mã hóa tệp tin thành công");

      }else{
        clearLoading();
        alert("Đã giải mã thư mục thành công");  
          }
        }else{
        clearLoading();
        alert("Đã có lỗi xảy ra trong quá trình giải mã ");

        }
  reload();
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
getFile()


   function clearFun(){
       console.log("clear");
     $("#list_error").empty();
     $("#error_content").empty();
     $("#error_des").empty();
     $("#error_total").empty();
   
   }
   function reload(){
   curpath =  document.getElementById("curpath").value;
   // backup_path = curpath
  console.log(curpath)
  console.log("213123")
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
    // alert("Tệp đã chọn không là thư mục ");
    document.getElementById("curpath").value =  "/";
    reload()
   }
 }
   
   function readErrors(path){
  curpath = document.getElementById("curpath").value;
  backup_path = curpath;
  if(path != ".."){
    curpath =curpath +  "/"+path;
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
