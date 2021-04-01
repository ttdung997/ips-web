<?php

include 'include/header.php';

?>
      <div class="content-wrapper">
    <!-- Content Header (Page header) -->
    <section class="content-header">
      <div class="container-fluid-header">
        <div class="row mb-2">
          <div class="col-sm-6">
            <h1>Cập nhật ứng dụng</h1>
          </div>
          <div class="col-sm-6">
            <ol class="breadcrumb float-sm-right">
              <li class="breadcrumb-item"><a href="/"><i class="fa fa-home" aria-hidden="true"></i> Trang chủ</a></li>
              <li class="breadcrumb-item active">Cập nhật ứng dụng</li>
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
          <div class="container-fluid">

  

    <?php

        $output = shell_exec('sudo apt list --upgradeable');
        $output = explode( "\n", $output);
        // print_r($output); 
   
      
?>
        <table id="updateTable" class="table table-hover table-striped">
              <thead class="header-table">
                  <tr>      
                      <th>Tên ứng dụng</th>
                      <th>Phiên bản hiện tại</th>
                      <th>Phiên bản nâng cấp</th>
                      <th></th>

                  </tr>
              </thead>
              <tbody>
              <?php
                    $i = 0;
                    foreach ($output as $key => $line) {
                            if($i == 0){
                                $i = 1;
                                continue;
                            }

                      $line = explode( " ", $line);
                      $app_name = explode( "/", $line[0])[0] . " (".$line[2].")";
                      $cur_version = substr($line[5], 0, -1);
                      $new_version = $line[1];
                      if($cur_version != ""){
                            // print_r($app_name."<br>");
                            // print_r($cur_version."<br>");
                            // print_r($new_version."<br>");
                            echo "<tr>";
                            echo "<td><img src='admin_asset_web/dist/img/app.png'> ".$app_name."</td>";
                            echo "<td>".$cur_version."</td>";
                            echo "<td>".$new_version."</td>";
                    ?>
                    <td>
                        <button onclick="updateApp('<?=explode( "/", $line[0])[0] ?>')" class="btn-update Disable"><i class="fa fa-upload" aria-hidden="true"></i> Cập nhật</button>
                    </td>
                    <?php
                    echo "</tr>";
                  }}
               ?>
              </tbody>
       </table>

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
  
    

  <!-- /.control-sidebar -->
</div>
<!-- ./wrapper -->

        <?php

include 'include/footer.php';

?>
<script>
 
$(document).ready(function () {
  $('#updateTable').DataTable();
  $('.dataTables_length').addClass('bs-select');
});
</script>
<script type="text/javascript">
function deleteApp(app){
      $.ajax({ 
        method:"POST", 
        url: "php/deleteApp.php",
        data: {"app": app},
        // url: "/check",
        // headers:  {'Access-Control-Allow-Origin' : 'http://192.168.218.138'},
        success: function (data) {
            console.log(data)
            alert(data);  
  location.reload();
            
        }
    });
}

function updateApp(app){
      $.ajax({ 
        method:"POST", 
        url: "php/updateApp.php",
        data: {"app": app},
        // url: "/check",
        // headers:  {'Access-Control-Allow-Origin' : 'http://192.168.218.138'},
        success: function (data) {
            console.log(data)
            alert(data);  
  // location.reload();
        }
    });
}

function killProcess(app){
      $.ajax({ 
        method:"POST", 
        url: "php/killProcess.php",
        data: {"id": app},
        // url: "/check",
        // headers:  {'Access-Control-Allow-Origin' : 'http://192.168.218.138'},
        success: function (data) {
            console.log(data)
            alert(data);  
  location.reload();
        }
    });
}
</script>
</body>
</html>

