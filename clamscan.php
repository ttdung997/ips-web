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
               <div class="card-header card-header-cus">
                                         <form method="post" style="float: right;">
                 <input value="1" type="hidden" name="tab" id="tabSelect">
                 <button type="button" onclick="clamUpdate()" class="btn btn-add Disable" style="margin-top: 10px;"><i class="fa fa-refresh" aria-hidden="true"></i>  Cập nhật tập luật clamAV </button>
              </form></div>
                                        
                             <div id="menu1">
<div class="row">
              <div class="col-sm-12">
                <h3>Chọn tệp</h3>
                <div id="files" style="border: 1px solid #585858; border-radius: 5px; background-color:#000000ad; max-height: 500px; min-height: 500px; overflow-y: auto; padding: 0px;">
                      <br><br>


                </div>
                    

              </div>
          

                   
              </div>
             
            </div>
                   <br>
            <div class="row float-right" style="padding-bottom: 30px; margin-right: 20px;">
    
            <button id="button1" type="button" class="btn btn-add" onclick="ScanSel()"><i class="fa fa-check"></i>Quét </button>

         
          </div>
            <br><br>
          </section>
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


function ScanAll(){
  $.ajax({ 
    method:"GET", 
    url: "php/clamall.php",
    // url: "/check",
    // headers:  {'Access-Control-Allow-Origin' : 'http://192.168.218.138'},
    success: function (data) {
        console.log(data)
        $("#list_error").html(data);
      
    }
});

}


function ScanSel(){
 var data = new FormData();
 var curpath = document.getElementById("curpath").value;
 var item = document.getElementById("choosepath").value;
 if(item == ""){
    alert("Bạn chưa chọn tệp tin, thư mục.");
 }
 else{
  var path = curpath + "/" + item;
  data.append('folder', path);
  var data = new FormData();

    data.append('folder', path);
    
      $.ajax({ 
        method:"POST", 
        url: "php/file_scan.php",
        data: data,
        processData: false,
        contentType: false,
        // url: "/check",
        // headers:  {'Access-Control-Allow-Origin' : 'http://192.168.218.138'},
        success: function (data) {
            console.log(data)
            alert("Đã gửi yếu cầu quét thư mục, kết quả trả về sẽ được lưu tại phân hệ mã độc thống kê");
            // $("#list_error").html(data);
          
        },
        error: function (request, status, error) {
            alert("Quét không thành công. Đã có lỗi trong quá trình xử lý.");
        }
    });

 }
  
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
        $(".file").css('background-color', 'black');
        $(this).css('background-color', 'red');
        document.getElementById("choosepath").value = path;

      });

    }
  
  

}
getFile()


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
        console.log("it in");
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
   
    function clamUpdate(){
                $.ajax({
                    url : "php/clamUpdate.php",
                    type : "get",
                    dataType:"text",
                    success : function (result){
                         console.log(result);
                         alert("Đã cập nhật tập luật clamAV từ IPS-manager")
                    }
                });
            }
   
   
</script>
