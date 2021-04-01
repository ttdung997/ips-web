<?php

include 'include/header.php';

?>
            <div class="content-wrapper">
                <!-- Content Header (Page header) -->
                <section class="content-header">
                    <div class="container-fluid-header">
                        <div class="row mb-2">
                            <div class="col-sm-6">
                                <h1>Kiểm thử và đánh giá cơ sở dữ liệu</h1>
                            </div>
                            <div class="col-sm-6">
                                <ol class="breadcrumb float-sm-right">
                                    <li class="breadcrumb-item"><a href="/"><i class="fa fa-home" aria-hidden="true"></i> Trang chủ</a></li>
                                    <li class="breadcrumb-item active">Kiểm thử và đánh giá cơ sở dữ liệu</li>
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
      
    </div>
    <div class="row" style="margin-left:26px; margin-right:20px; padding-bottom: 10px;">
        <div id="list_error" class="col-md-9 col-sm-9" style="border: 1px solid #585858; border-radius: 5px; background-color:#000000ad; max-height: 500px; min-height: 500px; overflow-y: auto; padding: 0px;">
        </div>
        <div id="error_content" class="col-md-3 col-sm-3" style="border: 1px solid red; border-radius: 5px; background-color:#000000; max-height: 500px; min-height: 500px; padding: 0px; ">
            <div class="col-md-12 col-sm-12" style="color: #e00e0e; padding-top: 10px;">
                WARNING INFORMATION!!!
            </div>
        </div>
    </div>

    <div class="row" style="margin-left:26px; margin-right:20px; padding-bottom: 30px;">
        <div id="error_des" class="col-md-9 col-sm-9" style="background-color:#000000ad; border: 1px solid #585858; border-radius: 5px; max-height: 200px; min-height: 200px; overflow-y: auto; padding: 0px;">
            <div class="col-md-12 col-sm-12" style="color: #57a1bf; padding-top: 10px;">
                Description of vulnerability.
            </div>
        </div>

        <div id="error_total" class="col-md-3 col-sm-3" style="background-color:#000000; border: 1px solid #585858; border-radius: 5px; max-height: 200px; min-height: 200px; padding: 0px; ">
        </div>
    </div>

    <div class="row float-right" style="padding-bottom: 30px; margin-right: 20px;">
        <div class="">
            <button id="button1" type="button" class="btn btn-add" onclick="checkErrors()"><i class="fa fa-check"></i> Quét lỗi</button>
        </div>
        <div class="" style="padding: 0 0 0 15px;">
            <button id="button2" type="button" class="btn btn-add" onclick="fixErrors()"><i class="fa fa-chain-broken"></i> Sửa lỗi</button>
        </div>
    </div>        
                    </div>
                    <!-- /.card-body -->
            </div>
           
        </div>
        <!-- /.col -->
        </div>
        <!-- /.row -->
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
    function checkErrors(){
        var urlInput = "php/check_mysql.php";
        var totalError = "59";
  $.ajax({ 
    method:"GET", 
    url: urlInput,
    // url: "/check",
    // headers:  {'Access-Control-Allow-Origin' : 'http://192.168.218.138'},
    success: function (data) {
      var allData = JSON.parse(data);
      console.log(allData)
      Errors = allData;
      $("#list_error").empty();
      $("#error_content").empty();
      $("#error_des").empty();
      $("#error_total").empty();
      array=[];
      for (i = 0; i < allData.length; i++){
        $("#list_error").append('<div id="Error'+ i +'" class="col-md-12 col-sm-12" style="background-color:#333; color: #FFFFFF; border: 2px solid white; border-radius: 5px;" data-id="'+ i +'" onclick="onclickFunction(this.id)"><div class="row"><div class="col-md-6 colsm-6" style="margin-top:10px; margin-bottom:10px;"><h8>'+ allData[i].name +'</h8></div><div class="col-md-4 colsm-4" style="margin-top:10px; margin-bottom:10px;"><h9>'+ allData[i].group_error +'</h9></div><div class="col-md-1 colsm-1" style="text-align: center; padding-left: 95px; padding:5px;"><div class="checkbox" style="padding-left: 50px"><label><input type="checkbox" value="" data-id="'+ allData[i].id +'" class="checkbox_check"'+ allData[i].id +'"></label></div></div></div></div>');
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
// function fixErrors(){ 
//     var urlType =document.getElementById("CheckType").value;
//     console.log(urlType)
//     if (urlType == 0){
//         var urlInput = "php/fix_linux.php";
//     }
//     if (urlType == 1){
//         var urlInput = "php/fix_apache.php";
//     }
//     if (urlType ==2){
//         var urlInput = "php/fix_mysql.php";
//     } 
//   $.ajax({ 
//     method:"GET", 
//     url: urlInput,
//     success: function (response) {
//       if (response != 1) console.log(response);
//     }
// });

// checked = false;
// }


function fixErrors(){
    
  if (checked == false){
    alert('You must check errors before!!!');
    return;
  }
  $.ajaxSetup({
        headers: {
              'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
          }
  });
  if ($("input:checked").length != 0){
  $("input:checked").each(function(index){
  array.push($(this).attr("data-id"));
});
 
        var urlInput = "php/fixmysql.php";
    
  $.ajax({ 
    type: 'POST', 
    url: urlInput,
    data: {id : array},
    success: function (response) {
      if (response != 1) console.log(response);
    }
});
}else{
  
        var urlInput = "php/fix_mysql.php";
    
  $.ajax({ 
    method:"GET", 
    url: urlInput,
    success: function (response) {
      if (response != 1) console.log(response);
    }
});
}
checked = false;
}

</script>