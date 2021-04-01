<?php

include 'include/header.php';

?>
   
      <div class="content-wrapper">
    <!-- Content Header (Page header) -->
    <section class="content-header">
      <div class="container-fluid-header">
        <div class="row mb-2">
          <div class="col-sm-6">
            <h1>Danh sách ứng dụng</h1>
          </div>
          <div class="col-sm-6">
            <ol class="breadcrumb float-sm-right">
              <li class="breadcrumb-item"><a href="/"><i class="fa fa-home" aria-hidden="true"></i> Trang chủ</a></li>
              <li class="breadcrumb-item active">Danh sách ứng dụng</li>
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
    
        $output = shell_exec('python3 tool/applications/app.py');
                                               
        $output = explode( "\n", $output);
    ?>
        <table id="appTable" class="table table-hover table-striped">
              <thead class="header-table">
                  <tr>      
                      <th>Tên ứng dụng</th>
                      <th>Phiên bản</th>
                      <th style="min-width:80px">Kiến trúc</th>
                      <th>Mô tả</th>
                      <th style="min-width:50px"></th>

                  </tr>
              </thead>
              <tbody>
              <?php
                  foreach($output as $key=>$line){
                    $line = json_decode(str_replace("'",'"',$line));
                      if($line->application_name != ""){
                    echo "<tr>";
                    echo "<td><img src='admin_asset_web/dist/img/app.png'> ".$line->application_name."</td>";
                    echo "<td>".$line->version."</td>";
                    echo "<td>".$line->architect."</td>";
                    echo "<td>".$line->description."</td>";
                    ?>
                    <td>
                        <button onclick="deleteApp(<?=$line->application_name?>)" class="btn-del Disable"><i class="fa fa-trash-o" aria-hidden="true"></i> Xóa</button>
                    </td>
                    <?php
                    echo "</tr>";
                  }
                  }
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
  
    

<?php

include 'include/footer.php';
?>
<script>
 
$(document).ready(function () {
  $('#appTable').DataTable();
 
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
  location.reload();
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

