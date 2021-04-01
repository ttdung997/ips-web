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

            <h1>Quản lý lưu nhật ký</h1>
            </div>
          </div>
          <div class="col-sm-6">
            <ol class="breadcrumb float-sm-right">
              <li class="breadcrumb-item"><a href="/"><i class="fa fa-home" aria-hidden="true"></i> Trang chủ</a></li>
              <li class="breadcrumb-item active">Quản lý lưu nhật ký</li>
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

  
            <form action="log.php" method="post" style="float: right;">
                 <input value="1" type="hidden" name ="tab" id="tabSelect" >
                 <button type="submit" class="btn btn-add Disable" style="margin-top: 10px;"><i class="fa fa-refresh" aria-hidden="true"></i> Làm mới</button>
              </form>
  <ul class="nav nav-tabs" id="example-tabs" role="tablist">
                                            <li class="nav-item margin_center">
                                                <a id="tab1" class="nav-link active color-a" onclick="tabFun(1)" data-toggle="tab" role="tab" href="#home">
                                                  Cảnh báo tấn công ứng dụng web
                                                </a>
                                            </li>
                                            <li class="nav-item margin_center">
                                                <a id="tab3" class="nav-link color-a" onclick="tabFun(3)"
                                                data-toggle="tab" role="tab" href="#menu4">Cảnh báo tường lửa truy cập </a>
                                            </li>

                                            <li class="nav-item margin_center">
                                                <a id="tab3" class="nav-link color-a" onclick="tabFun(3)"
                                                data-toggle="tab" role="tab" href="#menu1">Cảnh báo cập nhật phần mềm  </a>
                                            </li>
                                          <li class="nav-item margin_center">
                                                <a id="tab3" class="nav-link color-a" onclick="tabFun(3)"
                                                data-toggle="tab" role="tab" href="#menu2">Cảnh báo mã độc</a>
                                            </li>
                                          </ul>  
<br>
<?php  
    $db = new SQLite3('data/noti.sqlite'); 
        // print_r($_POST);
    $dt1 = "";
    $dt2 = "";
    if(isset($_POST['dt1']) && $_POST['dt1'] !== ""){
      $dt1 = $_POST['dt1'];
      $dt2 = $_POST['dt2'];
      // echo str_replace("T", " " ,$_POST['dt1']);
        $res = $db->query('select * from noti where nottype = 0 and uptime > "'.str_replace("T", " " ,$_POST['dt1']).'" and uptime < "'.str_replace("T", " " ,$_POST['dt2']).'" ORDER BY uptime');
        // echo 'select DISTINCT * from check_file where check_value = 0 and date_check > "'.str_replace("T", " " ,$_POST['dt1']).'" and date_check < "'.str_replace("T", " " ,$_POST['dt2']).'" ORDER BY name';
    
    }

      ?>
    <form action = "/noti.php" method="POST" class="form-inline">
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
    <br><br>
  <div class="tab-content">
    <div id="home" class="tab-pane  in active">
    <hr>
    <?php
 if(isset($_POST['dt1']) && $_POST['dt1'] !== ""){
        $res = $db->query('select * from noti where nottype = 0 and uptime > "'.str_replace("T", " " ,$_POST['dt1']).'" and uptime < "'.str_replace("T", " " ,$_POST['dt2']).'" ORDER BY uptime');
    }else{
      $res = $db->query('select * from noti where nottype = 0 ORDER BY uptime');
    }
    ?>
    <table id="Table" class="table table-hover table-striped">
                              <thead class="header-table">
                                  <tr>      
                                      <th>Thời gian</th>
                                      <th>Nội dung</th>
                                  </tr>
                              </thead>
                              <tbody>
                                <?php
                                      // $res = $db->query('select * from noti where nottype = 0  ORDER BY uptime');
                    while ($row = $res->fetchArray()) {
                                        echo "<tr>";
                                        echo "<td>".$row['uptime']."</td>";
                                        echo "<td>".$row['content']."</td>";
                                        echo "</tr>";

                                      }
                                      ?>
                                 
                          
                              </tbody>
              </table>
                            
    </div>
    <div id="menu4" class="tab-pane fade">
      
<table id="Table1" class="table table-hover table-striped"> <?php
 if(isset($_POST['dt1']) && $_POST['dt1'] !== ""){
        $res = $db->query('select * from noti where nottype = 4 and uptime > "'.str_replace("T", " " ,$_POST['dt1']).'" and uptime < "'.str_replace("T", " " ,$_POST['dt2']).'" ORDER BY uptime');
    }else{
      $res = $db->query('select * from noti where nottype = 4 ORDER BY uptime');
    }
    ?>
                              <thead class="header-table">
                                  <tr>      
                                      <th>Thời gian</th>
                                      <th>Nội dung</th>
                                  </tr>
                              </thead>
                              <tbody>
                                <?php
                                    
                    while ($row = $res->fetchArray()) {
                                        echo "<tr>";
                                        echo "<td>".$row['uptime']."</td>";
                                        echo "<td>".$row['content']."</td>";
                                        echo "</tr>";

                                      }
                                      ?>
                                 
                          
                              </tbody>
              </table>
                    </div>

      <div id="menu1" class="tab-pane fade">
      
<table id="Table1" class="table table-hover table-striped"> <?php
 if(isset($_POST['dt1']) && $_POST['dt1'] !== ""){
        $res = $db->query('select * from noti where nottype = 1 and uptime > "'.str_replace("T", " " ,$_POST['dt1']).'" and uptime < "'.str_replace("T", " " ,$_POST['dt2']).'" ORDER BY uptime');
    }else{
      $res = $db->query('select * from noti where nottype = 1 ORDER BY uptime');
    }
    ?>
                              <thead class="header-table">
                                  <tr>      
                                      <th>Thời gian</th>
                                      <th>Nội dung</th>
                                  </tr>
                              </thead>
                              <tbody>
                                <?php
                                    
                    while ($row = $res->fetchArray()) {
                                        echo "<tr>";
                                        echo "<td>".$row['uptime']."</td>";
                                        echo "<td>".$row['content']."</td>";
                                        echo "</tr>";

                                      }
                                      ?>
                                 
                          
                              </tbody>
              </table>
                    </div>  

                     <div id="menu2" class="tab-pane fade">
       <?php
 if(isset($_POST['dt1']) && $_POST['dt1'] !== ""){
        $res = $db->query('select * from noti where nottype = 2 and uptime > "'.str_replace("T", " " ,$_POST['dt1']).'" and uptime < "'.str_replace("T", " " ,$_POST['dt2']).'" ORDER BY uptime');
    }else{
      $res = $db->query('select * from noti where nottype = 2 ORDER BY uptime');
    }
    ?>
<table id="Table2" class="table table-hover table-striped">
                              <thead class="header-table">
                                  <tr>      
                                      <th>Thời gian</th>
                                      <th>Nội dung</th>
                                  </tr>
                              </thead>
                              <tbody>
                                <?php
                                     
                    while ($row = $res->fetchArray()) {
                                        echo "<tr>";
                                        echo "<td>".$row['uptime']."</td>";
                                        echo "<td>".$row['content']."</td>";
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

</script>
