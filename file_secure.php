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
                   <ul class="nav nav-tabs" id="example-tabs" role="tablist">
                                                    <li class="nav-item margin_center">
                                                        <a id="tab1" class="nav-link active color-a" data-toggle="tab" role="tab" href="#home">Thống kê chi tiết mã độc </a>
                                                    </li>
                                                    
                                                    <li class="nav-item margin_center">
                                                        <a id="tab2" class="nav-link color-a" data-toggle="tab" role="tab" href="#menu1">Lịch sử quét mã độc hệ thống</a>
                                                    </li>
                                                </ul>
                                                <br>

                                                    <div class="tab-content">
                                                        <div id="home" class="tab-pane in active show">
      <div>
    <h5>&nbsp;&nbsp;Bộ lọc tệp tin</h5>
    <?php

    $db = new SQLite3('data/check.sqlite');
    // print_r($_POST);
    $dt1 = "";
    $dt2 = "";
    if(isset($_POST['dt1']) && $_POST['dt1'] !== ""){
      $dt1 = $_POST['dt1'];
      $dt2 = $_POST['dt2'];
      // echo str_replace("T", " " ,$_POST['dt1']);
        $res = $db->query('select DISTINCT * from check_file where check_value = 0 and date_check > "'.str_replace("T", " " ,$_POST['dt1']).'" and date_check < "'.str_replace("T", " " ,$_POST['dt2']).'" ORDER BY name');
        // echo 'select DISTINCT * from check_file where check_value = 0 and date_check > "'.str_replace("T", " " ,$_POST['dt1']).'" and date_check < "'.str_replace("T", " " ,$_POST['dt2']).'" ORDER BY name';
    }else{
      $res = $db->query('select DISTINCT * from check_file where check_value = 0 ORDER BY name');
    }

      ?>
    <form action = "/file_secure.php" method="POST" class="form-inline">
  <div class="form-group row">
  <label for="example-datetime-local-input" class="col-2 col-form-label">Từ </label>
  <div class="col-10">
    <input class="form-control" type="datetime-local" name="dt1" id="dt1" value="<?=$dt1?>">
  </div>
</div>
<div style="margin-left: 5%" class="form-group row">
  <label for="example-datetime-local-input" class="col-2 col-form-label">Đến </label>
  <div class="col-10">
    <input class="form-control" type="datetime-local" name="dt2" id="dt2" value="<?=$dt2?>">
  </div>
</div>

 <button style="margin-left: 5%"  type="submit" id="SubmitButton" class="btn btn-add"><i class="fa fa-refresh" aria-hidden="true"></i> Tìm kiếm</button>
 <button style="margin-left: 5%"  type="button" onclick="reload()" class="btn btn-add"> <i class="fa fa-refresh" aria-hidden="true"></i> Tải lại </button>
</form>
<br>
  </div>
                    <div class="row">
   
                                        

                                
                                    <div class="col-md-12">
                                      <div class="card card-custom">
         
                                      <div class="card-header">
                                        <h3 class="card-title">Biểu đồ thống kê</h3>
                                      </div>
                                      <div class="card-body"> 
                                        
                                        <canvas id="myChart" width="800" height="300"></canvas>
                                 
                                     </div>
                                  </div>
                                </div>
                        <div class="col-12">
                            <div class="card">
                                <!-- /.card-header -->
                                <div class="card-body">
                                <section class="content">
                                           <div class="col-md-12">
           <?php

                                       
                   
            ?>
  
  <br>
   <ul class="nav nav-tabs" id="example-tabs" role="tablist">
              <li class="nav-item margin_center">
                  <a id="tab1" class="nav-link active color-a" data-toggle="tab" role="tab" href="#menu2">Danh sách têp tin mã độc</a>
              </li>
              
              <li class="nav-item margin_center">
                  <a id="tab2" class="nav-link color-a" data-toggle="tab" role="tab" href="#menu3">Danh sách tệp tin an toàn</a>
              </li>
          </ul>
          <br>

              <div class="tab-content">
                  <div id="menu2" class="tab-pane in active show">                 
           <table id="DgaTable" class="table table-hover table-striped">
                              <thead class="header-table">
                                  <tr>      
                                      <th>Tên tệp</th>
                                      <th>Kích thước</th>
                                      <th>Thời gian khởi tạo</th>
                                      <th>Kết quả quét mã</th>
                                  </tr>
                              </thead>
                              <tbody>
                                    <?php
                    $array = [];
                    while ($row = $res->fetchArray()) {
                                      if($curname == $row['name']){
                                        continue;
                                      }
                                        $kbs = $row['large_file'];
                                        echo "<tr>";
                                        echo "<td>".$row['name']."</td>";
                                        echo "<td>".$kbs."KB</td>";
                                        echo "<td>".$row['date_check']."</td>";
                                      if($row['check_value'] == 0){
                                        	echo "<td>Tệp tin mã độc</td>";
                                    	}else{
                                        	echo "<td>Tệp tin an toàn</td>";	
                                    	}
                                        echo "</tr>";
                                        $curname  = $row['name'];
                                      ?>
                                 
                            <?php
                                if(isset(explode(".",$row['name'])[1])){
                                  $file = end(explode(".",$row['name']));
                                    // if(!in_array($file,$label)){
                                    //   $label[] = $file;
                                    // }
                                  $array[$file] = $array[$file] + 1;
                                 }
                              }
                            ?>
                              </tbody>
              </table>
              <br><br>
              <button style="float: right;"  type="button" onclick="removeVirus()" class="btn btn-add"> <i class="fa fa-refresh" aria-hidden="true"></i> Xử lý tệp mã độc </button>
          </div>
            <div id="menu3" class="tab-pane fade">                 
           <table id="DgaTable2" class="table table-hover table-striped">
                              <thead class="header-table">
                                  <tr>      
                                      <th>Tên tệp</th>
                                      <th>Kích thước</th>
                                      <th>Thời gian khởi tạo</th>
                                      <th>Kết quả quét mã</th>
                                  </tr>
                              </thead>
                              <tbody>
                                    <?php 
                                    if(isset($_POST['dt1']) && $_POST['dt1'] !== ""){
                                      $res = $db->query('select DISTINCT * from check_file where large_file > 0 and date_check > "'.str_replace("T", " " ,$_POST['dt1']).'" and date_check < "'.str_replace("T", " " ,$_POST['dt2']).'" ORDER BY name');
                                    }else{
                                      $res = $db->query('select DISTINCT * from check_file where large_file > 0 ORDER BY name');
                                    }
                   
                    $array = [];
                    while ($row = $res->fetchArray()) {
                                      if($curname == $row['name']){
                                        continue;
                                      }
                                      if(0 != $row['check_value']){
                                        $kbs = $row['large_file'];
                                        echo "<tr>";
                                        echo "<td>".$row['name']."</td>";
                                        echo "<td>".$kbs."KB</td>";
                                        echo "<td>".$row['date_check']."</td>";
                                      if($row['check_value'] == 0){
                                          echo "<td>Tệp tin mã độc</td>";
                                      }else{
                                          echo "<td>Tệp tin an toàn</td>";  
                                      }
                                        echo "</tr>";
                                        $curname  = $row['name'];

                                      }
                                      ?>
                                 
                            <?php
                                if(isset(explode(".",$row['name'])[1])){
                                  $file = end(explode(".",$row['name']));
                                    // if(!in_array($file,$label)){
                                    //   $label[] = $file;
                                    // }
                                  $array[$file] = $array[$file] + 1;
                                 }
                              }
                            ?>
                              </tbody>
              </table>
          </div>


        </div>
            </div>
        </section>
                    </div>
                    <!-- /.card-body -->
            </div>
           
        </div>
        <!-- /.col -->
        </div>
      </div>
                             <div id="menu1" class="tab-pane fade">
<div class="row">
              <div class="col-sm-3">
                <h3>Thời gian quét</h3>
                <div id="files" style="border: 1px solid #585858; border-radius: 5px; background-color:#000000ad; max-height: 660px; min-height: 660px; overflow-y: auto; padding: 0px;">
                  
                </div>
              </div>
              <div class="col-sm-9">
                   <div class="info" id="list_error"  style="border: 1px solid #585858; border-radius: 5px; background-color:#000000ad; max-height: 650px;min-height: 700px;  overflow-y: auto; padding: 0px;">
                   </div>
                   
              </div>
            </div>
            <br><br>
                             </div></div>
        <!-- /.row -->
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

$(document).ready(function () {
  $('#DgaTable').DataTable();
  $('#DgaTable2').DataTable();
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
  $.ajax({ 
   method:"GET",
  async: false,
  cache: false, 
   url: "php/clam_get.php",
   // url: "/check",
   // headers:  {'Access-Control-Allow-Origin' : 'http://192.168.218.138'},
   success: function (data) {
     console.log(data)
     list = JSON.parse(data);
   }
 });
  
  
    for(var i =0; i<list.length; i++){
      $("#files").append('<div class="file" id="'+list[i]+'"><span><i class="fa fa-file-o" aria-hidden="true"></i> '+list[i]+'</span></div>')
      document.getElementById(list[i]).addEventListener("click", function(){
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
   function readErrors(path){
  
   var data = new FormData();

  data.append('path', path);
   $.ajax({ 
  method: "POST",
  url: "/php/read_path.php",
  data: data,
  processData: false,
  contentType: false,
   // url: "/check",
   // headers:  {'Access-Control-Allow-Origin' : 'http://192.168.218.138'},
   success: function (data) {
     console.log(data)
     // var allData = JSON.parse(data);
     // console.log(allData)

     // Errors = allData;
     $("#list_error").empty();
     $("#list_error").html(data);
    }
   });
   
   }
   
   function reload(){
    document.getElementById("dt1").value = "";
    document.getElementById("dt2").value  = "";
    $("#SubmitButton").click();

  
   }

function removeVirus(app){
      $.ajax({ 
        method:"GET", 
        url: "php/rmVirrus.php",
        // url: "/check",
        // headers:  {'Access-Control-Allow-Origin' : 'http://192.168.218.138'},
        success: function (data) {
            console.log(data)
            alert("Đã quét và xóa các tệp tin bị nhiệm mã độc");  
  location.reload();
        }
    });
}
   
</script>
