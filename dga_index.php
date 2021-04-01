<?php

include 'include/header.php';

?>
            <div class="content-wrapper">
                <!-- Content Header (Page header) -->
                <section class="content-header">
                    <div class="container-fluid-header">
                        <div class="row mb-2">
                            <div class="col-sm-6">
                                <h1>Thông tin máy trạm</h1>
                            </div>
                            <div class="col-sm-6">
                                <ol class="breadcrumb float-sm-right">
                                    <li class="breadcrumb-item"><a href="/"><i class="fa fa-home" aria-hidden="true"></i> Trang chủ</a></li>
                                    <li class="breadcrumb-item active">Thông tin máy trạm</li>
                                </ol>
                            </div>
                        </div>
                    </div>
                    <!-- /.container-fluid -->
                </section>

                <!-- Main content -->
                <section class="content">
                    <div class="row">
                                        
                                <div class="col-md-5">
                                               
                                      <div class="card card-custom">

                                      <div class="card-header card-header-cus">
                                        <h3 class="card-title">Thông tin máy trạm</h3>

                                      </div>
                                      <div class="card-body">
                                          
                                           <ul id="server-list" class="list-group">

                                          <li class="list-group-item">
                                          <a >
                                          <b class="color-b">Time:</b>
                                          </a>  <i id="timeInfo"></i> 
                                          
                                          <b class="color-b" style="margin-left: 20px">Uptime:</b><i id="uptimeInfo"></i> 
                                          </li>
                                          <li class="list-group-item">
                                          <a>
                                          <b class="color-b">SWAP:</b>
                                          </a>  <i id ="swapInfo"> </i> 
                                         
                                          </li>
                                          <li class="list-group-item">
                                          <a>
                                          <b class="color-b">Processes:</b>
                                          </a>  <i id = "processInfo"></i> 
                                          
                                          </li>
                                          <li class="list-group-item">
                                          <a>
                                          <?php
                    $db = new SQLite3('tool/dga/data.db');

                    $res = $db->querySingle('SELECT Safe FROM bkcs_host_moniter');
               
                                          ?>
                                          <b class="color-b">Độ an toàn:</b>
                                          </a> <?=$res ?>
                                          
                                          </li>

                                          </ul>


                                   
                                        
                                        </div>
                                    </div>                         
                                </div>
                                    <div class="col-md-7">
                                      <div class="card card-custom">
                                      <div class="card-header">
                                        <h3 class="card-title">Biểu đồ thống kê</h3>
                                      </div>
                                      <div class="card-body"> 
                                        <?php 
                                        $res = $db->query('SELECT * FROM bkcs_history_daily ORDER BY count DESC LIMIT 10');

                                         $domainArr =[];
                                         $countArr = [];
                                        while ($row = $res->fetchArray()) {
                                            $domainArr[] = $row["domain"];
                                            $countArr[] = $row["count"];
                                       }

                                        $domainArr = json_encode(array_reverse($domainArr));
                                        $countArr = json_encode(array_reverse($countArr));
                                        ?>

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

                                         $res = $db->query('SELECT * FROM bkcs_host_history');
                   
            ?>
                   
           <table id="DgaTable" class="table table-hover table-striped">
                              <thead class="header-table">
                                  <tr>      
                                      <th>Địa chỉ DGA</th>
                                      <th>Thời gian truy cập</th>
                                      <th>Chỉ số nhiễm độc</th>
                                  </tr>
                              </thead>
                              <tbody>
                                    <?php
                    while ($row = $res->fetchArray()) {
                                        echo "<tr>";
                                        echo "<td>".$row['Domain']."</td>";
                                        echo "<td>".$row['Date']."-".$row['Time']."</td>";
                                        echo "<td>".$row['Safe']."</td>";
                                     
                                      ?>
                                 
                            </tr>
                            <?php
                                }
                            ?>
                              </tbody>
              </table>
          
            </div>
        </section>
                    </div>
                    <!-- /.card-body -->
            </div>
           
        </div>
        <!-- /.col -->
        </div>
        <!-- /.row -->
  <?php
// print_r($domainArr);
// print_r($countArr);
include 'include/footer.php';

?>
        <script src="admin_asset_web/dist/js/demo.js"></script>
<script src="admin_asset_web/plugins/js/Chart.js"></script>
        <script type="text/javascript">

$(document).ready(function () {
  $('#DgaTable').DataTable();
  $('.dataTables_length').addClass('bs-select');
});
function getInfo(){
$(document).ready(function() {
    $.ajax({
        type: "GET",
        url: 'php/info.php',
        success: function(response)
        {

            var Data = JSON.parse(response);
            console.log(Data);

            document.getElementById("timeInfo").innerHTML = Data.time;
            document.getElementById("uptimeInfo").innerHTML = Data.uptime;
            document.getElementById("swapInfo").innerHTML = Data.swapUsed+"/"+Data.swapTotal;
            document.getElementById("processInfo").innerHTML = Data.process;

        }
       });
     });
   
}

getInfo();

window.setInterval(function () {
  getInfo();
}, 5000);


var ctx = document.getElementById("myChart");
var myChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: <?=$domainArr?>,
    datasets: [{
      label: 'Thống kê truy vấn từ máy trạm',
      data: <?=$countArr?>,
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