<?php

include 'include/header.php';

?>
<?php
print_r($_SESSION);
?>
      <div class="content-wrapper">
    <!-- Content Header (Page header) -->
    <section class="content-header">
      <div class="container-fluid-header">
        <div class="row mb-2">
          <div class="col-sm-6">   <div class="form-inline" >

            <h1>Thống kê hệ thống tệp</h1>
            </div>
          </div>
          <div class="col-sm-6">
            <ol class="breadcrumb float-sm-right">
              <li class="breadcrumb-item"><a href="/"><i class="fa fa-home" aria-hidden="true"></i> Trang chủ</a></li>
              <li class="breadcrumb-item active">Thống kê hệ thống tệp</li>
            </ol>
          </div>
        </div>
      </div><!-- /.container-fluid -->
    </section>

    <!-- Main content -->
    <section class="content">
      <div class="row">
        <div class="col-12">
          <div class="card">
            <div class="card-header">
    
            <!-- /.card-header -->
            <div class="card-body" >

  
           
  <ul class="nav nav-tabs" id="example-tabs" role="tablist">
                                            <li class="nav-item margin_center">
                                                <a id="tab1" class="nav-link active color-a"  data-toggle="tab" role="tab" href="#home">
                                                Nhật kỹ mã hóa tệp
                                                </a>
                                            </li>
                                            <li class="nav-item margin_center">
                                                <a id="tab3" class="nav-link color-a"
                                                data-toggle="tab" role="tab" href="#menu1">Nhật ký kiếm soát tính toàn vẹn</a>
                                            </li>
                                          <li class="nav-item margin_center">
                                                <a id="tab3" class="nav-link color-a" 
                                                data-toggle="tab" role="tab" href="#menu2">Nhật ký kiếm soát truy cập</a>
                                            </li>
                                          </ul>  
<br>
<?php          // print_r($_POST);
    $dt1 = "";
    $dt2 = "";
    if(isset($_POST['dt1']) && $_POST['dt1'] !== ""){
      $dt1 = $_POST['dt1'];
      $dt2 = $_POST['dt2'];
       $output = shell_exec('python3 ./script/file_system_protection/demo_crypto.py -l "'.str_replace("T", " " ,$_POST['dt1']).'" "'.str_replace("T", " " ,$_POST['dt2']).'"');
    }else{
        $output = shell_exec("python3 ./script/file_system_protection/demo_crypto.py -l_7");
}
      ?>
    <form action = "/reg_static.php" method="POST" class="form-inline">
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
 <?php
    // print_r(explode(".",$output,2));
    $data = (json_decode(explode(".",$output,2)[1]))->events;
    // print_r($data);
    ?>
</form>  


    <br><br>
  <div class="tab-content">
    <div id="home" class="tab-pane  in active">
    <hr>

    <table id="Table" class="table table-hover table-striped">
                              <thead class="header-table">
                                  <tr>      
                                      <th>Thời gian</th>
                                      <th>Tệp tin</th>
                                      <th>Hành động</th>
                                      <th>Trạng thái</th>
                                  </tr>
                              </thead>
                              <tbody>
                                <?php
                                    foreach ($data as $data) {
                                      echo "<tr>";
                                      echo "<td>".$data[0]."</td>";
                                      echo "<td>".$data[3]."</td>";
                                      if($data[2] == "-d"){
                                        echo "<td>Giải mã</td>";
                                      }else{
                                        echo "<td>Mã hóa</td>";
                                      }

                                      if($data[1] == "Success"){
                                        echo "<td>Thành công</td>";
                                      }else{
                                        echo "<td>Thất bại</td>";
                                      }
                                      
                                      echo "</tr>";
                                    }
                                      ?>
                                 
                          
                              </tbody>
              </table>
                            
    </div>
      <div id="menu1" class="tab-pane fade">
      
<table id="Table1" class="table table-hover table-striped"> 

 <?php       
    if(isset($_POST['dt1']) && $_POST['dt1'] !== ""){
       $output = shell_exec('python3 ./script/file_system_protection/demo_integrity.py -l "'.str_replace("T", " " ,$_POST['dt1']).'" "'.str_replace("T", " " ,$_POST['dt2']).'"');
    }else{
        $output = shell_exec("python3 ./script/file_system_protection/demo_integrity.py -l_7");
}
// print_r(json_decode($output));
    $data = (json_decode($output))->alert_list;
      ?>
                              <thead class="header-table">
                                  <tr>      
                                      <th>Thời gian</th>
                                      <th>Tệp tin</th>
                                      <th></th>
                                  </tr>
                              </thead>
                              <tbody>
                                <?php
                                    
                  foreach ($data as $row)  {
                                        echo "<tr>";
                                        echo "<td>".$row[1]."</td>";
                                        echo "<td>".$row[3]."</td>";
                                        echo "<td>".$row[2]."</td>";
                                        echo "</tr>";

                                      }
                                      ?>
                                 
                          
                              </tbody>
              </table>
                    </div>  

                     <div id="menu2" class="tab-pane fade">
     <?php    
    if(isset($_POST['dt1']) && $_POST['dt1'] !== ""){
       $output = shell_exec('python3 ./script/file_system_protection/demo_monitor.py -a "'.str_replace("T", " " ,$_POST['dt1']).'" "'.str_replace("T", " " ,$_POST['dt2']).'"');
    }else{
        $output = shell_exec("python3 ./script/file_system_protection/demo_monitor.py -a_7");
}
  // print_r($output);
    $data = (json_decode($output))->alert_list;
      ?>

<table id="Table2" class="table table-hover table-striped">
                              <thead class="header-table">
                                  <tr>      
                                      <th>Thời gian</th>
                                      <th>Người thao tác</th>
                                      <th>Tệp tin</th>
                                      <th>Hành động</th>
                                      <th>Lời gọi</th>
                                      <th>Trạng thái</th>

                                  </tr>
                              </thead>
                              <tbody>
        <?php
              foreach ($data as $row)  {
                                        echo "<tr>";
                                        echo "<td>".$row[1]."</td>";
                                        echo "<td>".$row[2]."</td>";
                                        echo "<td>".$row[4]."</td>";
                                        echo "<td>".$row[3]."</td>";
                                        echo "<td>".$row[5]."</td>";
                                        echo "<td>".$row[6]."</td>";
                                        echo "</tr>";

                                      }
                                      
        ?>
                          
                              </tbody>
              </table>
                    </div>
                    </div>       
                            </div>
                        </div>
                        <!-- /.row -->
                    </div>

                <!-- /.card-body -->
              </div>
                            </div>
                          

                          </div>
                        </div>
                           
                            <a id="background-loading">
                              <img id="gif_load" hidden="" style="position: fixed; top: 50%;" src="admin_asset_web/dist/img/loading1.gif">
                            </a>
                        </div>
                    </div>
                    <!-- /.row -->
                </div>
            </div>
            <!-- /.card-body -->
          </div>
          <!-- /.card -->

        </div>
        <!-- /.col -->
      </div>
      <!-- /.row -->
   <?php

include 'include/footer.php';

?>
<!-- AdminLTE for demo purposes -->
<script src="admin_asset_web/dist/js/demo.js"></script>

<script src="admin_asset_web/plugins/js/Chart.js"></script>
<script type="text/javascript">
  $(document).ready(function () {
  $('#Table').DataTable();
  $('#Table1').DataTable();
  $('#Table2').DataTable();
  $('.dataTables_length').addClass('bs-select');
});
 function reload(){
    document.getElementById("dt1").value = "";
    document.getElementById("dt2").value  = "";
    $("#SubmitButton").click();

  
   }

</script>
