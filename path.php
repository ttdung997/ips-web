<?php

include 'include/header.php';

?>
            <div class="content-wrapper">
                <!-- Content Header (Page header) -->
                <section class="content-header">
                    <div class="container-fluid-header">
                        <div class="row mb-2">
                            <div class="col-sm-6">
                                <h1>Rà soát tập tin mã độc</h1>

                            </div>
                            <div class="col-sm-6">
                                <ol class="breadcrumb float-sm-right">
                                    <li class="breadcrumb-item"><a href="/"><i class="fa fa-home" aria-hidden="true"></i> Trang chủ</a></li>
                                    <li class="breadcrumb-item active">Rà soát tập tin mã độc</li>
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
              <div class="col-sm-3">
                <h3>Thời gian quét</h3>
                <div id="files" style="border: 1px solid #585858; border-radius: 5px; background-color:#000000ad; max-height: 660px; min-height: 660px; overflow-y: auto; padding: 0px;">
                  
                </div>
              </div>
              <div class="col-sm-9">
                   <div class="info" id="list_error"  style="border: 1px solid #585858; border-radius: 5px; background-color:#000000ad; max-height: 650px;min-height: 700px;  overflow-y: auto; padding: 0px;">
                   </div>
                   <br><br>
                   
        </div>
              </div>
              <div class="row float-right" style="padding-bottom: 30px; margin-right: 20px;">
            <label>Mật khẩu</label>
            <input id="pass" class="form-control">
            <button id="button1" type="button" class="btn btn-add" onclick="encrype()"><i class="fa fa-check"></i> Mã hóa</button>
             <button id="button1" type="button" class="btn btn-add" onclick="decrype()"><i class="fa fa-check"></i> Giải mã</button>
          </div>
            </div>
            <br><br>
                             </div></div>
        <!-- /.row -->
        <input hidden  id="curpath" value="">
        <input hidden  id="choosepath" value="">
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

function encrype(){
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
    console.log(data)
    if (data == "false"){
    alert("Đã mã hóa tệp tin thành công");

    }else{
      alert("Đã mã hóa thư mục thành công");
    }

  reload();
   }

 });
}

function decrype(){
  
 var data = new FormData();

 var curpath = document.getElementById("curpath").value;
 var item = document.getElementById("choosepath").value;
 var path = curpath  + "/" +  item
 var pass = document.getElementById("pass").value;
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
    if (data == "false"){
    alert("Đã giải mã hóa tệp tin thành công");

    }else{
      alert("Đã giải mã thư mục thành công");  
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
   }
 });
  
  
    for(var i =0; i<list.length; i++){
      $("#files").append('<div class="file" id="'+list[i]+'"><span><i class="fa fa-file-o" aria-hidden="true"></i> '+list[i].split("-")[0]+'</span></div>')
      document.getElementById(list[i]).addEventListener("dblclick", function(){
        path = $(this).attr("id");
        readErrors(path)

        // function show log
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

   }
 });
  
    if (list != false){
     $("#files").empty()
    for(var i =0; i<list.length; i++){
      $("#files").append('<div class="file" id="'+list[i]+'"><span><i class="fa fa-file-o" aria-hidden="true"></i> '+list[i].split("-")[0]+'</span></div>')
      document.getElementById(list[i]).addEventListener("dblclick", function(){
        path = $(this).attr("id");
        readErrors(path)
      });
      document.getElementById(list[i]).addEventListener("click", function(){
        path = $(this).attr("id");
        $(".file").css('background-color', 'black');
        $(this).css('background-color', 'red');
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

   }
 });
  
    if (list != false){
     $("#files").empty()
    for(var i =0; i<list.length; i++){
      $("#files").append('<div class="file" id="'+list[i]+'"><span><i class="fa fa-file-o" aria-hidden="true"></i> '+list[i].split("-")[0]+'</span></div>')
      document.getElementById(list[i]).addEventListener("dblclick", function(){
        path = $(this).attr("id");
        readErrors(path)
      });
      document.getElementById(list[i]).addEventListener("click", function(){
        path = $(this).attr("id");
        $(".file").css('background-color', 'black');
        $(this).css('background-color', 'red');
        document.getElementById("choosepath").value = path;

      });
    }
   
   }else{
    alert("Tệp đã chọn không là thư mục ");
    document.getElementById("curpath").value =  backup_path;
   }
 }
   
   
   
   
</script>
