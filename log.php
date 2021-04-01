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
                                                <a id="tab1" class="nav-link active color-a" onclick="tabFun(1)" data-toggle="tab" role="tab" href="#home">Nhật ký kiểm soát ứng dụng web</a>
                                            </li>
                                            <li class="nav-item margin_center">
                                                <a id="tab3" class="nav-link color-a" onclick="tabFun(3)"
                                                data-toggle="tab" role="tab" href="#menu2">Nhật ký phần mềm dịch vụ công</a>
                                            </li>
                                          
                                          </ul>  
<br>
  <div class="tab-content">
    <div id="home" class="tab-pane  in active">
    <hr>
    <form method="post" action="log.php">
       <div class="form-inline" >
        <div class="form-group">
          <label  for="input_IP1"></label>
          <input value="<?=$_POST['grep']?>" placeholder="Search" type="text" class="input-search form-control" name="grep">
        </div>
        <button type="submit" class="btn btn-add Disable"><i class="fa fa-search" aria-hidden="true"></i></button>

      </div>

    </form>
    <hr>
<?php
if(isset($_POST['grep'])){
  $shell = "sudo tac /var/log/syslog | awk -F".'" "'." '{ printf(".'"%-50s<br>\n"'.", $0); }'"."|grep ".$_POST['grep'];
  }else{
  $shell = "sudo tac  /var/log/syslog | awk -F".'" "'." '{ printf(".'"%-50s<br>\n"'.", $0); }' |grep bkcs-";

}
  // print_r($shell);
  $log = shell_exec($shell);
  $log = explode("<br>",$log);  
  $log[0]= preg_replace('/\s\s+/', ' ', $log[0]);
  $month = explode(" ",$log[0])[0];
  $day = explode(" ",$log[0])[1];
  $hour = explode(" ",$log[0])[2];
  $hour = explode(":",$hour)[0];
  $data =[];
  $time_series = [];
  for($i=0;$i<10;$i++){
    if($day < 10){
      $day = " ".$day;
    }
      // print("test123");
      $hourfliter = ($hour - $i +24) % 24;
    if($hourfliter < 10){
      $hour_str = "0".$hourfliter;
    }else{

      $hour_str = $hourfliter;
    }
    if(isset($_POST['grep'])){
       $minishell = "sudo tac /var/log/syslog | awk -F".'" "'." '{ printf(".'"%-50s<br>\n"'.", $0); }'"."|grep ".$_POST['grep'].' |grep "'.$month." ".$day." ".$hour_str.'"

      ';
  }else{
      $minishell = "sudo tac /var/log/syslog | awk -F".'" "'." '{ printf(".'"%-50s<br>\n"'.", $0); }'".'|grep bkcs-|grep "'.$month." ".$day." ".$hour_str.'"

    ';

}
      
      // print($minishell."<br>");
      $row = shell_exec($minishell);
      $row = explode("<br>",$row);
      if(count($row) >1){
        $data[] = count($row);
      }else{
         $data[] = 0;
      }

      
        $last_hour =$hourfliter+1;

      
      $time_series[] = (string)($hourfliter)."h-".(string)$last_hour."h";
  }
  $data = json_encode(array_reverse($data));
  $time_series = json_encode(array_reverse($time_series));
?>

  <h5>Phân tích gói tin bị chặn</h5>
<?php
if(count($log) >1){
  if(isset($_POST['grep'])){
    ?>
    <p>Đã phát hiện có <span style="color:#ff7504"><?=count($log)?></span> gói tin bị chặn có chứa từ khóa: <span style="color:blue"><?=$_POST['grep']?></span></p>
    <?php
     }else{
    ?>
    <p>Đã phát hiện có <span style="color:#ff7504"><?=count($log)?></span> gói tin bị chặn </p>
    <?php

  }
}

?>

  <div class="row">
                                        
        <div class="col-md-8">
                       
<canvas id="myChart" style="width: 100%; height: 400px;"></canvas>
                                 
        </div>
            <div class="col-md-4" style="padding-left: 20px;">
            <?php
$logview = shell_exec($shell);
?>
<h5 style="    background: #304c58;
    padding: 5px;">Chi tiết log</h5>
      <div class="info">
    <?=$logview?>
      </div>
    </div>
  </div>

<hr>
<br>
<h5>Chi tiết gói tin bị chặn</h5>
  <table id="processTable" class="table table-hover table-striped">
              <thead class="header-table">
                  <tr>      
                      <th>Thời gian</th>
                      <th>IP nguồn</th>
                      <th>IP đích</th>
                      <th>Cổng nguồn</th>
                      <th>Cổng đích</th>
                      <th>Phương thức</th>
                  </tr>
              </thead>
              <tbody>
<?php
	$i =0;
	foreach($log as $row){
    $i = $i+1;
    if ($i ==100){
      break;
    }
    $row= preg_replace('/\s\s+/', ' ', $row);


		$time = explode(" ",$row)[0]." ".explode(" ",$row)[1]." ".explode(" ",$row)[2];
		$input = explode("kernel",$row)[1];

		$src = explode("SRC=",$input)[1];
		$src = explode(" ",$src)[0];

		$dst = explode("DST=",$input)[1];
		$dst = explode(" ",$dst)[0];

		$proto = explode("PROTO=",$input)[1];
		$proto = explode(" ",$proto)[0];

		$dpt = explode("DPT=",$input)[1];
		$dpt = explode(" ",$dpt)[0];


		$spt = explode("SPT=",$input)[1];
		$spt = explode(" ",$spt)[0];


		//print($time."<br>");
		//print($input);
    if($src !== ""){
		 echo "<tr>";
		 echo "<td>".$time."</td>";
		 echo "<td>".$src."</td>";
		 echo "<td>".$dst."</td>";
		 echo "<td>".$dpt."</td>";
		 echo "<td>".$spt."</td>";
  		echo "<td>".$proto."</td>";
  		echo "</tr>";
    }
	}
?>

              </tbody>
       </table>

                            
    </div>
      <div id="menu1" class="tab-pane fade">
      <div class="info" style="padding: 15px;">
   <?php
  $iptable = shell_exec("sudo iptables -S"."| awk -F".'" "'." '{ printf(".'"%-50s<br>"'.", $0); }'");
  // echo $iptable;
?>
  <?=$iptable?>
  </div>
                            </div>

                            <div id="menu2" class="tab-pane fade">
 <div class="row">
            <div class="col-12">
              <div class="card" style="background: transparent;">
                <div class="card-header" style="padding: 0px;">
        
                <!-- /.card-header -->
                  <div class="wrapper">
                    <div class="row">
                      <div class="col-sm-4 chart-circle">
                        <h3>Thống kê truy vấn theo phương thức</h3>
                      <canvas id="method"></canvas>
                      </div>
                      <div class="col-sm-4 chart-circle">
                        <h3>Thống kê truy vấn theo cổng </h3>
                      <canvas id="port"></canvas>
                      </div>
                      <div class="col-sm-4 chart-circle">
                        <h3>Thống kê truy vấn theo respone</h3>
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
<script type="text/javascript">

document.getElementById("tab<?=$_SESSION['logtab']?>").click();

  function tabFun(i){
    document.getElementById("tabSelect").value = i;
  }
  x =  <?=$_POST['tab']?> +0;
  console.log(x)
  if(x == 2){
    document.getElementById("tab2").click();
  }
  if(x == 3){
    document.getElementById("tab3").click();
  }
  if(x == 4){
    // console.log("?????")
    document.getElementById("tab4").click();
  }
  if(x == 5){
    document.getElementById("tab5").click();
  }
</script>

<script src="admin_asset_web/plugins/js/Chart.js"></script>
<script type="text/javascript">
  var ctx = document.getElementById("myChart");
var myChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: <?=$time_series?>,
    datasets: [{
      label: 'Số lượng gói tin bị chặn',
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
          beginAtZero: true
        }
      }]
    }
  }
});

Chart.defaults.global.defaultFontColor = '#dcf3ff';

</script>

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
        text-align: center!important;
        padding: 20px!important;
      }

      .chart-circle canvas {
        display: inline!important;
        width: 100%!important;
        height: auto!important;
      }

      .chart_ {
        padding: 20px!important;
        text-align: center!important;
      }

      .card-header .wrapper {
        background: #2b3c46!important;
        margin-bottom: 15px!important;
      }

      .line-col {
        display: inline!important;
        width: 100%!important;
      }

    </style>