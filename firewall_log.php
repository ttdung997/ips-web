
<?php

include 'include/header.php';

?>
      <div class="content-wrapper">
    <!-- Content Header (Page header) -->
    <section class="content-header">
      <div class="container-fluid-header">
        <div class="row mb-2">
          <div class="col-sm-6">   <div class="form-inline" >

            <h1>Báo cáo thống kê phân hệ tường lửa</h1>
            </div>
          </div>
          <div class="col-sm-6">
            <ol class="breadcrumb float-sm-right">
              <li class="breadcrumb-item"><a href="/"><i class="fa fa-home" aria-hidden="true"></i> Trang chủ</a></li>
              <li class="breadcrumb-item active">Báo cáo thống kê phân hệ tường lửa</li>
            </ol>
          </div>
        </div>
      </div><!-- /.container-fluid -->
    </section>
    
        <!-- Main content -->
        <section class="content">
          <div class="row">
            <div class="col-12">
              <div class="card" style="background: transparent;">
                <div class="card-header" style="padding: 0px;">
        
                <!-- /.card-header -->
                  <div class="wrapper">
                    <div class="row">
                      <div class="col-sm-4 chart-circle">
                      <canvas id="method"></canvas>
                      </div>
                      <div class="col-sm-4 chart-circle">
                      <canvas id="port"></canvas>
                      </div>
                      <div class="col-sm-4 chart-circle">
                      <canvas id="status"></canvas>
                      </div>
                    </div>
                  </div>
                  <div class="wrapper" style="padding: 25px;">
                    <div class="row">
                      <div class="col-sm-6 chart_">
                      <canvas id="hour" height="300" class="line-col"></canvas>
                      </div>
                      <div class="col-sm-6 chart_">
                      <canvas id="day" height="300" class="line-col"></canvas>
                      </div>
                    </div>
                  </div>
                  <div class="wrapper" style="padding: 20px;">
                    <div class=>
                      <table id="resTable" class="table table-hover table-striped">
              <thead class="header-table" >
                  <tr>      
                      <th>Thời gian</th>
                      <th>IP nguồn</th>
                      <th>IP đích</th>
                      <th>Nội dung</th>
                      <th>Kết quả trả về</th>
                      <th>Trạng thái</th>
                  </tr>
              </thead>
              <tbody>
                <?php
$output = shell_exec("sudo python3 tool/firewall_log.py");
$output = json_decode($output);
$i = 0; 
foreach($output as $res){
  // print("123123124");
  if( $i == 0){
    $i= $i +1;
    continue;
  }
  // print_r($res);
  // print_r("<br>");
   echo "<tr>";
 echo "<td>".$res[2]."</td>";
 echo "<td>".$res[0]."</td>";
 echo "<td>".$res[1]."</td>";
 echo "<td>".$res[3]."</td>";
 echo "<td>".$res[4]."</td>";
  echo "<td>".$res[5]."</td>";
  echo "</tr>";
  $i = $i +1;

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
<script src="admin_asset_web/plugins/js/canvasjs.min.js"></script>
    <script type="text/javascript">
      $(document).ready(function () {
  $('#resTable').DataTable();
 
  $('.dataTables_length').addClass('bs-select');
});

    function* iterate_object(o) {
    var keys = Object.keys(o).sort();
    console.log(keys)
    for (var i=0; i<keys.length; i++) {
        yield [keys[i], o[keys[i]]];
    }
}
    function getInfo() {
      $(document).ready(function () {
        $.ajax({
          type: "GET",
          url: 'php/read_audit.php',
          success: function (response) {
            console.log(response);
            let res = JSON.parse(response);
            let Data = res[0];
            let hourKey = res[1];
            let hourValue = res[2]
            let day = res[3];
            var colors = ['#81BEF7', '#604792', '#a98428', '#a98428', '#236ea9', '#604792'];
            /* 3 donut charts */
            var donutOptions = {
              cutoutPercentage: 85,
              legend: {
                position: 'bottom', padding: 5, labels: {
                  pointStyle: 'circle', usePointStyle: true
                }
              },
              responsive: false
            };

            // donut 3
            let methods = []
            let labels = []
            for(const [method, value] of Object.entries(Data.method)){
                methods.push(value);
                labels.push(`${method}: ${value}`)
            }
            console.log(methods, labels)
            var chDonutDataMethod = {
              labels: labels,
              datasets: [
                {
                  backgroundColor: colors.slice(4, 5),
                  borderWidth: 0,
                  data: methods
                }
              ]
            };
            var chDonutMethod = document.getElementById("method");
            if (chDonutMethod) {
              new Chart(chDonutMethod, {
                type: 'pie',
                data: chDonutDataMethod,
                options: donutOptions
              });
              Chart.defaults.global.defaultFontColor = '#dcf3ff';
            }
            // donnut
            methods = []
            labels = []
            for(const [method, value] of Object.entries(Data.port)){
                methods.push(value);
                labels.push(`${method}: ${value}`)
            }
            var chDonutDataPort = {
              labels: labels,
              datasets: [
                {
                  backgroundColor: colors.slice(3, 4),
                  borderWidth: 0,
                  data: methods
                }
              ]
            };
            var chDonutPort = document.getElementById("port");
            if (chDonutPort) {
              new Chart(chDonutPort, {
                type: 'pie',
                data: chDonutDataPort,
                options: donutOptions
              });
              Chart.defaults.global.defaultFontColor = '#dcf3ff';
            }
           // donnut
            methods = []
            labels = []
            for(const [method, value] of Object.entries(Data.status)){
                methods.push(value);
                labels.push(`${method}: ${value}`)
            }
            var chDonutDataStatus = {
              labels: labels,
              datasets: [
                {
                  backgroundColor: colors.slice(1),
                  borderWidth: 0,
                  data: methods
                }
              ]
            };
            var chDonutStatus = document.getElementById("status");
            if (chDonutStatus) {
              new Chart(chDonutStatus, {
                type: 'pie',
                data: chDonutDataStatus,
                options: donutOptions
              });
              Chart.defaults.global.defaultFontColor = '#dcf3ff';
            }

            methods = []
            labels = []
            console.log(hourKey, hourValue)
            for(const [method, value] of Object.entries(hourValue)){
                methods.push(value);
            }
            for(const [method, value] of Object.entries(hourKey)){
                labels.push(value);
            }
            var ctx = document.getElementById("hour");
            var myChart = new Chart(ctx, {
              type: 'bar',
              data: {
                labels: labels,
                datasets: [{
                  label: 'Thống kê loại truy vấn theo giờ',
                  data: methods,
                backgroundColor: '#23885a',
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


            methods = []
            labels = []
            for(const [method, value] of Object.entries(day)){
                methods.push(value);
                labels.push(`${method}`)
            }
            var ctx = document.getElementById("day");
            var myChart = new Chart(ctx, {
              type: 'bar',
              data: {
                labels: labels,
                datasets: [{
                  label: 'Thống kê loại truy vẫn theo ngày',
                  data: methods,
                backgroundColor: '#23885a',
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
          }

          
        });
      });
    }
    getInfo();    
    </script>
    
    
    <style type="text/css">
      .chart-circle {
        text-align: center;
        padding: 20px;
      }

      .chart-circle canvas {
        display: inline; 
        width: 100%; 
        height: auto;
      }

      .chart_ {
        padding: 20px;
        text-align: center;
      }

      .card-header .wrapper {
        background: #2b3c46;
        margin-bottom: 15px;
      }

      .line-col {
        display: inline; width: 100%;
      }
    </style>


</body>

