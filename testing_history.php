<?php
   include 'include/header.php';
   
   ?>
<div class="content-wrapper">
<!-- Content Header (Page header) -->
<section class="content-header">
   <div class="container-fluid-header">
      <div class="row mb-2">
         <div class="col-sm-6">
            <h1>Kiểm thử và đánh giá dịch vụ</h1>
         </div>
         <div class="col-sm-6">
            <ol class="breadcrumb float-sm-right">
               <li class="breadcrumb-item"><a href="/"><i class="fa fa-home" aria-hidden="true"></i> Trang chủ</a></li>
               <li class="breadcrumb-item active">Kiểm thử và đánh giá dịch vụ</li>
            </ol>
         </div>
      </div>
   </div>
   <!-- /.container-fluid -->
</section>
<!-- Main content -->
<section class="content">
<div class="row">
   <div class="col-12">
      <div class="card">
         <!-- /.card-header -->
         <div class="card-body">
            <div class="row" style="margin-bottom:20px;">
               <label style="margin-left:10px; margin-top:10px;" for="ip">Loại lỗ hổng: </label>
               <select id="CheckType" style="margin-left:20px; width: 15%;color: wheat;" class="form-control-custom-size"  onchange="getFile()">
                  <option value="1">Lỗ hổng webserver</option>
                  <option value="2">Lỗ hổng MySql</option>
                  <option value="0">Lỗ hổng hệ điều hành  </option>
               </select>
            </div>
            <div class="row">
              <div class="col-sm-3">
                <div id="files" style="border: 1px solid #585858; border-radius: 5px; background-color:#000000ad; max-height: 700px; min-height: 700px; overflow-y: auto; padding: 0px;">
                  
                </div>
              </div>
              <div class="col-sm-9">
                <div class="row" style="margin-right:5px;">
                   <div id="list_error" class="col-md-9 col-sm-9" style="border: 1px solid #585858; border-radius: 5px; background-color:#000000ad; max-height: 500px; min-height: 500px; overflow-y: auto; padding: 0px;">
                   </div>
                   <div id="error_content" class="col-md-3 col-sm-3" style="border: 1px solid red; border-radius: 5px; background-color:#000000; max-height: 500px; min-height: 500px; padding: 0px; ">
                      <div class="col-md-12 col-sm-12" style="color: #e00e0e; padding-top: 10px;">
                         WARNING INFORMATION!!!
                      </div>
                   </div>
                </div>
                <div class="row" style="margin-right:5px; padding-bottom: 30px;">
                   <div id="error_des" class="col-md-9 col-sm-9" style="background-color:#000000ad; border: 1px solid #585858; border-radius: 5px; max-height: 200px; min-height: 200px; overflow-y: auto; padding: 0px;">
                      <div class="col-md-12 col-sm-12" style="color: #57a1bf; padding-top: 10px;">
                         Description of vulnerability.
                      </div>
                   </div>
                   <div id="error_total" class="col-md-3 col-sm-3" style="background-color:#000000; border: 1px solid #585858; border-radius: 5px; max-height: 200px; min-height: 200px; padding: 0px; ">
                   </div>
                </div>
              </div>
            </div>

         </div>
         <!-- /.card-body -->
      </div>
   </div>
   <!-- /.col -->
</div>
<!-- /.row -->



<script>
function getFile() {
  // checkErrors();
  var Type = document.getElementById("CheckType").value;
  $.ajax({ 
   method:"GET",
  async: false,
  cache: false, 
   url: "php/web_json.php",
   // url: "/check",
   // headers:  {'Access-Control-Allow-Origin' : 'http://192.168.218.138'},
   success: function (data) {
     console.log(data)
     list = JSON.parse(data);
   }
 });
  var urlType =document.getElementById("CheckType").value;
   console.log(urlType)
   var stingValue = "";
   if (urlType == 0){
       stingValue = "os";
   }
   
   if (urlType == 1){
       stingValue = "web";
   }
   if (urlType ==2){
       stingValue = "sql";
   }
  document.getElementById("files").innerHTML = "";
  
    for(var i =0; i<list.length; i++){
      if(list[i].includes(stingValue)){
      $("#files").append('<div class="file" id="'+list[i]+'"><span><i class="fa fa-file-o" aria-hidden="true"></i> '+list[i].split("-")[0]+'</span></div>')
      document.getElementById(list[i]).addEventListener("click", function(){
        path = $(this).attr("id");
        readErrors(path)

        // function show log
      });
    }
  }
  

}
</script>



<?php
   include 'include/footer.php';
   
   ?>
<!-- <script src="https://js.pusher.com/4.1/pusher.min.js"></script> -->
<!-- datatable -->
<script type="text/javascript" src="admin_asset_web/dist/js/jquery.passtrength.min.js"></script>
<script type="text/javascript" src="admin_asset_web/dist/js/jquery.confirm.js"></script>
<!-- AdminLTE for demo purposes -->
<script src="admin_asset_web/dist/js/demo.js"></script>
<script type="text/javascript">
   function clearFun(){
       console.log("clear");
     $("#list_error").empty();
     $("#error_content").empty();
     $("#error_des").empty();
     $("#error_total").empty();
   
   }
   function readErrors(path){
    var urlType =document.getElementById("CheckType").value;
   console.log(urlType)
   
   if (urlType == 0){
       var totalError = "213";
   }
   
   if (urlType == 1){
       var totalError = "54";
   }
   if (urlType ==2){
       var totalError = "59";
   }

   var data = new FormData();

  data.append('path', path);
   $.ajax({ 
  method: "POST",
  url: "/php/read_json.php",
  data: data,
  processData: false,
  contentType: false,
   // url: "/check",
   // headers:  {'Access-Control-Allow-Origin' : 'http://192.168.218.138'},
   success: function (data) {
     console.log(data)
     var allData = JSON.parse(data);
     console.log(allData)

     Errors = allData;
     $("#list_error").empty();
     $("#error_content").empty();
     $("#error_des").empty();
     $("#error_total").empty();
     array=[];
     for (i = 0; i < allData.length; i++){
       $("#list_error").append('<div id="Error'+ i +'" class="col-md-12 col-sm-12" style="background-color:#333; color: #FFFFFF; border: 2px solid white; border-radius: 5px;" data-id="'+ i +'" onclick="onclickFunction(this.id)"><div class="row"><div class="col-md-6 colsm-6" style="margin-top:10px; margin-bottom:10px;"><h8>'+ allData[i].name +'</h8></div><div class="col-md-4 colsm-4" style="margin-top:10px; margin-bottom:10px;"><h9>'+ allData[i].group_error +'</h9></div><div class="col-md-1 colsm-1" style="text-align: center; padding-left: 95px; padding:5px;"><div class="checkbox" style="padding-left: 50px"><label>');
     }
     $("#error_total").append('<div class="col-md-12 col-sm-12" style="color: #e00e0e; padding-top: 10px;"><h3>Statistics</h3></div><div class="col-md-12 col-sm-12" style="color: #e00e0e; padding-top: 10px;">Alert: '+ Errors.length +'</div><div class="col-md-12 col-sm-12" style="color: #e00e0e; padding-top: 10px;">Total: '+totalError+'</div>');
     checked = true;
   }
   });
   
   }
   
   
   
   function onclickFunction(div_id){
   error_id = $("#"+div_id).attr("data-id");
   $("#error_content").empty();
   $("#error_content").append('<div class="col-md-12 col-sm-12" style="padding-top: 10px; color: #FF3030;"><h3>Detail</h3></div>');
   $("#error_content").append('<div class="col-md-12 col-sm-12" style="padding-top: 10px; color: #FF3030;">'+ Errors[error_id].l_error +'</div>');
   
   $("#error_des").empty();
   $("#error_des").append('<div class="col-md-12 col-sm-12" style="padding-top: 10px; color: #000000;"><h3>Description</h3></div><div class="col-md-12 col-sm-12" style="padding-bottom: 10px; color: #FF3030;">'+ Errors[error_id].des +'</div>');
   }
</script>

<style type="text/css">
  .file {
    padding: 10px;
    cursor: pointer;
  }

  .file:hover {
    background: rgba(255,255,255,0.2);
  }

  .file span {
    /*white-space:nowrap*/
  }
</style>