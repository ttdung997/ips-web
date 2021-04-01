<?php

include 'include/header.php';

?>
   
      <div class="content-wrapper">
    <!-- Content Header (Page header) -->
    <section class="content-header">
      <div class="container-fluid-header">
        <div class="row mb-2">
          <div class="col-sm-6">
            <h1>Quản lý luật tường lửa</h1>
          </div>
          <div class="col-sm-6">
            <ol class="breadcrumb float-sm-right">
              <li class="breadcrumb-item"><a href="/"><i class="fa fa-home" aria-hidden="true"></i> Trang chủ</a></li>
              <li class="breadcrumb-item active">Quản lý luật tường lửa</li>
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
            <!-- /.card-header -->
            <div class="card-body" >
             <?php
              if(isset($_SESSION['notification'])){
             ?>
                                    <center><div class="alert alert-success">
                                       <?=$_SESSION['notification']?> <br>
                                    </div></center>
              <?php
                }
                session_destroy();
                session_start();
    
              ?>
          <div class="container">

  

  <ul class="nav nav-tabs" id="example-tabs" role="tablist">
                                            <li class="nav-item margin_center">
                                                <a id="tab1" class="nav-link active color-a" data-toggle="tab" role="tab" href="#home">Lưu lượng vào</a>
                                            </li>
                                            <li class="nav-item margin_center">
                                                <a id="tab2" class="nav-link color-a" data-toggle="tab" role="tab" href="#menu1">Lưu lượng ra</a>
                                            </li>
                                          </ul>  
<br>
  <?php
      $command = "sudo python tool/python-iptables/manual_input.py -L";
      // print_r($command);  
      $string = shell_exec($command);
      // print_r(explode(')',$string)[1]);
      $string = explode(')',$string)[1];
      $data = json_decode($string, true);
      // print_r($data);
      $input = $data['INPUT'];
      // print_r($input);
      $output =$data['OUTPUT'];
      // print(count($data['INPUT']));
 
    ?>
  <div class="tab-content">
    <div id="home" class="tab-pane  in active">
       <table id="processTable" class="table table-hover table-striped">
              <thead class="header-table">
                  <tr>      
                      <th>Phương thức</th>
                      <th>Địa chỉ IP</th>
                      <th>Cổng kết nối</th>
                      <th>Prefix</th>
                      <th>Hành vi</th>
                      <th></th>

                  </tr>
              </thead>
              <tbody>
              <?php
                  $i = 0;
                  foreach($input as $key=>$line){
                    $ip = "";
                    if(!isset($line['target']['LOG'])){
                    if(isset($line['iprange']['dst-range'])){
                      $ip = $line['iprange']['dst-range'];
                    }
                    if(isset($line['iprange']['dst-range']) && isset($line['iprange']['src-range'])){
                        $ip = $ip.",";
                    }
                    if(isset($line['iprange']['src-range'])){
                      $ip = $ip.$line['iprange']['src-range'];
                    }

                    $port = "";
                    if(isset($line[$line['protocol']]['dport'])){
                      $port = $line[$line['protocol']]['dport'];
                    }
                    if(isset($line[$line['protocol']]['dport']) && isset($line['iprange']['sport'])){
                        $port = $port.",";
                    }
                    if(isset($line[$line['protocol']]['sport'])){
                      $port = $port.$line[$line['protocol']]['sport'];
                    }


                    echo "<tr>";
                    echo "<td>".$line['protocol']."</td>";
                    echo "<td>".$ip."</td>";
                    echo "<td>".$port."</td>";
                    echo "<td>".$log."</td>";
                    echo "<td>".$line['target']."</td>";
                    ?>
                    <td>
                      <form method="post" action="php/rule_input.php">
                        <input name = "id" type="hidden" value="<?=$i?>">
                        <button type="submit" class="btn-del Disable"><i class="fa fa-trash-o" style="font-size: 1.2rem;" aria-hidden="true"></i></button>
                      </form>
                    </td>
                    <?php
                    echo "</tr>";
                                      }else{
                      $log = $line['target']['LOG']['log-prefix'];
                    }
                                      
                    $i = $i + 1;

                  }
               ?>
              </tbody>
       </table>

    </div>
    
                            <div id="menu1" class="tab-pane fade">
    <table id="processTable" class="table table-hover table-striped">
              <thead class="header-table">
                  <tr>      
                      <th>Phương thức</th>
                      <th>Địa chỉ IP</th>
                      <th>Cổng kết nối</th>
                      <th>Hành vi</th>
                      <th></th>

                  </tr>
              </thead>
              <tbody>
              <?php
                  $i = 0;
                  // print_r($output);
                  foreach($output as $key=>$line){
                     $ip = "";

                    if(!isset($line['target']['LOG'])){
                    if(isset($line['iprange']['dst-range'])){
                      $ip = $line['iprange']['dst-range'];
                    }
                    if(isset($line['iprange']['dst-range']) && isset($line['iprange']['src-range'])){
                        $ip = $ip.",";
                    }
                    if(isset($line['iprange']['src-range'])){
                      $ip = $ip.$line['iprange']['src-range'];
                    }

                    $port = "";
                    if(isset($line[$line['protocol']]['dport'])){
                      $port = $line[$line['protocol']]['dport'];
                    }
                    if(isset($line[$line['protocol']]['dport']) && isset($line['iprange']['sport'])){
                        $port = $port.",";
                    }
                    if(isset($line[$line['protocol']]['sport'])){
                      $port = $port.$line[$line['protocol']]['sport'];
                    }

                    echo "<tr>";
                    echo "<td>".$line['protocol']."</td>";
                    echo "<td>".$ip."</td>";
                    echo "<td>".$port."</td>";
                    echo "<td>".$line['target']."</td>";
                    ?>
                    <td>
                      <form method="post" action="php/rule_output.php">
                        <input name = "id" type="hidden" value="<?=$i?>">
                        <button type="submit" class="btn-del Disable"><i class="fa fa-trash-o" style="font-size: 1.2rem;" aria-hidden="true"></i></button>
                      </form>
                    </td>
                    <?php
                    echo "</tr>";
                    }
                    $i = $i + 1;
                  }
               ?>
              </tbody>
       </table>

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
    </section>
    <!-- /.content -->
  </div>
  
    
  <footer class="main-footer">
    <strong>Copyright &copy; Viện hóa học môi trường</a>.</strong> All rights
    reserved.
  </footer>
  <!-- /.control-sidebar -->
</div>
<!-- ./wrapper -->

<!-- jQuery -->
<script src="admin_asset_web/plugins/jquery/jquery.min.js"></script>
<!-- Bootstrap 4 -->
<script src="admin_asset_web/plugins/bootstrap/js/bootstrap.bundle.min.js"></script>
<!-- DataTables -->
<script src="admin_asset_web/plugins/datatables/jquery.dataTables.js"></script>
<script src="admin_asset_web/plugins/datatables/dataTables.bootstrap4.js"></script>
<!-- SlimScroll -->
<script src="admin_asset_web/plugins/slimScroll/jquery.slimscroll.min.js"></script>
<!-- FastClick -->
<script src="admin_asset_web/plugins/fastclick/fastclick.js"></script>
<!-- AdminLTE App -->
<script src="admin_asset_web/dist/js/adminlte.min.js"></script>
<!-- AdminLTE for demo purposes -->
<script src="admin_asset_web/dist/js/demo.js"></script>
<!-- page script -->
<script src="admin_asset_web/dist/js/Form.js"></script>
<!-- iCheck -->
<script src="admin_asset_web/plugins/iCheck/icheck.min.js"></script>
<!-- pusher -->
<!-- <script src="https://js.pusher.com/4.1/pusher.min.js"></script> -->
<!-- datatable -->
<script type="text/javascript" src="admin_asset_web/dist/js/jquery.passtrength.min.js"></script>
<script type="text/javascript" src="admin_asset_web/dist/js/jquery.confirm.js"></script>



<!-- AdminLTE for demo purposes -->
<script src="admin_asset_web/dist/js/demo.js"></script>
<script>
  if(<?=$_SESSION['val']['form']?> == 2){
    document.getElementById("tab2").click();
  }
</script>
</body>
</html>

