<?php

include 'include/header.php';

?>
      <div class="content-wrapper">
    <!-- Content Header (Page header) -->
    <section class="content-header">
     
    </section>

    <!-- Main content -->
    <section class="content">
      <div class="row">
        <div class="col-12">
          <div>
            <!-- /.card-header -->
            <div>
                                <div class="session">
                                    
                                                                    </div>
                                <div class="row">
                                        
                                <div class="col-md-5">
                                               
                                      <div class="card card-custom" style="height: 717px;">

                                      <div class="card-header card-header-cus">
                                        <h3 class="card-title">Thông tin thiết bị</h3>

                                      </div>
                                      <div class="card-body">
                                           <?php
                                              $output = shell_exec('bash script/infomation.sh');
                                               
                                                $output = explode( '|||', $output);
                                                // print_r($output[3]);
                                                $data['time'] = explode( 'up', $output['0'])[0];
                                                $data['uptime'] = explode( 'up', $output['0'])[1];
                                                $data['uptime'] = explode( ',', $data['uptime'])[0];

                                                $data['process'] = $output[4];
                                                $data['cpuPercent'] = round((float)$output[3],2);
                                               
                                                $data['ramTotal'] = explode( '||', explode( ':', $output[1])[0])[0];
                                                
                                                $data['ramUsed'] =  explode('||', explode( ':', $output[1])[0])[1];
                                              
                                                $data['swapTotal'] = explode( '||', explode( ':', $output[2])[0])[0];
                                                $data['swapUsed'] = explode( '||', explode( ':', $output[2])[0])[1];
                                               $status = $data;
                                                // print_r($data);
                                           ?>

                                           <ul id="server-list" class="list-group">

                                          <li class="list-group-item">
                                          <a >
                                          <b class="color-b">Time:</b>
                                          </a>  <i id="timeInfo"></i> 
                                          </a>

                                          <b class="color-b" style="margin-left: 20px">Uptime:</b><i id="uptimeInfo"></i> 
                                          </li>
                                          <li class="list-group-item">
                                          <a>
                                          <b class="color-b">SWAP:</b>
                                          </a>  <i id ="swapInfo"> </i> 
                                          </a>
                                          </li>
                                          <li class="list-group-item">
                                          <a>
                                          <b class="color-b">Processes:</b>
                                          </a>  <i id = "processInfo"></i> 
                                          </a>
                                          </li>
                                          </ul>

                                     
                                    <br>

                                   
                                         <table id="processTable" class="table table-hover table-striped">
              <thead class="header-table">
                  <tr>      
                      <th>Tên card mạng</th>
                      <th>Trạng thái</th>
                      <th>Địa chỉ IP</th>

                  </tr>

              </thead>
              <tbody>
              <?php
                $net = shell_exec("python3 tool/netstat.py");
                $net = explode("|||", $net);
                foreach ($net as $nw) {
                    echo "<tr>";
                    echo "<td>".explode("||", $nw)[0]."</td>";
                    echo "<td>".explode("||", $nw)[2]."</td>";
                    echo "<td>".explode("||", $nw)[1]."</td>";
                    echo "</tr>";
                }
              
              
              ?>
              </tbody>
       </table>
                                        </div>
                                    </div>                         
                                </div>
                                    <div class="col-md-7">
                                      <div class="card card-custom">
                                      <div class="card-header">
                                        <h3 class="card-title">Biểu đồ thống kê</h3>
                                      </div>
                                      <div class="card-body"> 
                                        <div class="row">
                                          <div class="chart col-md-6 circle-chart">
                                            <div id="RAM" style="height: 250px; width: 100%;"></div>
                                            <div style="position: absolute;background-color: #2b3c46;height: 10px;width: 100%;bottom: 2px;"></div>
                                          </div>
                                          <div class="chart col-md-6 circle-chart">
                                            <div id="CPU" style="height: 250px; width: 100%;"></div>
                                            <div style="position: absolute;background-color: #2b3c46;height: 10px;width: 100%;bottom: 2px;"></div>
                                          </div>
                                          <div class="chart col-md-12" style="margin-top: 58px;">
                                            <div id="chartContainer" style="height: 320px; width: 100%;"></div>
                                            <div style="position: absolute;background-color: #2b3c46;height: 10px;width: 100%;bottom: 2px;"></div>
                                          </div>
                                        </div>
                                     </div>
                                  </div>
                                </div>
                                <div class="col-md-6">
                                      <div class="card card-custom">
                                                         
                                      <div class="card-header">
                                      <form action="php/hardware.php" method="post" style="float: right;">
                 <input value="1" type="hidden" name="tab" id="tabSelect">
                 <button type="submit" class="btn btn-add Disable"><i class="fa fa-refresh" aria-hidden="true"></i>  Làm mới</button>
              </form>
                                        <h3 class="card-title"> Cấu hình phần cứng </h3>
            
                                       
                                      </div>
                                      <div class="card-body">
                                      <?php
                                          $string = file_get_contents("data/hardware.json");
                                          $data = json_decode($string, true);
                                          // print_r($data);
                                      ?>
                                      <table id="processTable" class="table table-hover table-striped">
                                    <thead class="header-table">
                                        <tr>      
                                            <th>H/W path</th>
                                            <th>Thiết bị</th>
                                            <th>Phân lớp</th>
                                            <th>Mô tả</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                    <?php
                                        $i = 0;
                                        foreach($data as $key=>$line){
                                          // if($i == 15) break;
                                          $i = $i+1;
                                          if($i < 3) continue;
                                        echo "<tr>";
                                            echo "<td><img src='admin_asset_web/dist/img/hardware.png'> ".$line[0]."</td>";
                                            echo "<td>".$line[1]."</td>";
                                            echo "<td>".$line[2]."</td>";
                                            echo "<td>".$line[3]."</td>";
                                        echo "</tr>";
                                        }
                                     ?>
                                    </tbody>
                                   </table>
                                    </div>
                                                </div>
                                            </div>
                                <div class="col-md-6">
                                      <div class="card card-custom">
                                                         
                                      <div class="card-header">
                                        <h3 class="card-title"> Danh sách tiến trình</h3>

                                        <div class="card-tools">
                                         <button type="button" class="btn btn-tool" data-widget="collapse"><i class="fa fa-minus"></i>
                                          </button>
                                          <button type="button" class="btn btn-tool" data-widget="remove"><i class="fa fa-times"></i></button>
                                        </div>
                                      </div>
                                      <div class="card-body"> 
                                     <?php
                                        $output = shell_exec('sudo bash script/process.sh');
                                    // print_r($output);
                                        $begin_row = 1;
                                     $output = (explode( '|||', $output));
                                    
                                    $data = [];
                                    $row =0;
                                    foreach ($output as $line) {
                                        if ($row > $begin_row){
                                            while(strpos($line,'  ') > 0){
                                                $line = str_replace('  ', ' ', $line);
                                            }

                                        $word_list = explode("||",$line);
                                        if($os_flag == 1 && isset($word_list[3])){
                                            $time = $this->secondsToTime((int)$word_list[3]);
                                            $word_list[3] = $time['h'].":".$time['m'].":".$time['s'];
                                        }
                                        $data[] = $word_list;
                                        }
                                        $row = $row +1;
                                    }

                                     ?>
                                   <table class="table table-hover table-striped" id="Tabla">
                                            <thead class="header-table">
                                                <tr>
                                                    <th>Tên tiến trình</th>
                                                    <th>Dung lượng CPU (%)</th>
                                                    <th>Dung Lượng RAM (%)</th>
                                                    <th>Thời gian</th>
                                                </tr>
                                            </thead>
                                            <tbody id="TableBody">
                                            <?php
                                              foreach($data as $key=>$line){
                                                    echo "<tr>";
                                                    echo "<td><img src='admin_asset_web/dist/img/process.png'> ".$line[0]."</td>";
                                                    echo "<td>".$line[1]."</td>";
                                                    echo "<td>".$line[2]."</td>";
                                                    echo "<td>".$line[3]."</td>";
                                                    echo "<td>".$line[4]."</td>";                    
                                                    echo "</tr>";
                                              }
                                    ?>
                                     
                                        </tbody>
                                    </table>  

                                </div>

                                        </div>


                            </div>
                            <!--
                            <!-- /.card-body -->
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
<script src="admin_asset_web/dist/js/canvasjs.min.js"></script>

<style type="text/css">
  svg {
    display: block;
    width: 200px; height: 200px;
  }
  .axis1 text {
    font-size: 14px;
    fill: #f1f1f1;
  }

  .axis1 .domain, .axis1 .tick line {
    margin-left: 5px;
    stroke-width: 3px;
    stroke: #00cbf9;
  }
  .axis2 text {
    font-size: 14px;
    fill: #f1f1f1;
  }

  .axis2 .domain, .axis2 .tick line {
    margin-left: 5px;
    stroke-width: 3px;
    stroke: #ff8100;
  }
  

  .label{
    fill: #fff;
    stroke: #f00;
    stroke-width: 1px;
    font-size: 24px;
  }
  .circle-chart {
    display: flex; 
    justify-content: center; 
    flex-direction: column; 
    align-items: center;
  }
  </style>






<script type="text/javascript">
function getInfo(){
$(document).ready(function() {
    $.ajax({
        type: "GET",
        url: 'php/info.php',
        success: function(response)
        {
            var Data = JSON.parse(response);
            console.log(Data);

            var colors = ['#81BEF7','#28a745','#333333','#F5D0A9','#D0A9F5','#6c757d'];
            /* 3 donut charts */
            var donutOptions = {
              cutoutPercentage: 85, 
              legend: {
                position:'bottom', padding:5, labels: {
                  pointStyle:'circle', usePointStyle:true
                }
              },
              responsive: false
            };

            var ramTotal = Data.ramTotal;
            var ramUsed = Data.ramUsed;
            var ramFree = ramTotal - ramUsed;
            // donut 3
            var chDonutDataRAM = {
              labels: ['Used: '+ramUsed+'GiB', 'Free: '+ramFree+'GiB'],
              // labels: ['Used: 12GiB', 'Free: 38iB'],
              datasets: [
                {
                  backgroundColor: colors.slice(4,5),
                  borderWidth: 0,
                  data: [Data.ramUsed, ramFree]
                  // data: [12, 38]
                }
              ]
            };
            var chDonutRAM = document.getElementById("RamChart");
            if (chDonutRAM) {
            new Chart(chDonutRAM, {
                type: 'pie',
                data: chDonutDataRAM,
                options: donutOptions
            });
            Chart.defaults.global.defaultFontColor = '#dcf3ff';
            }
            cpuPercent = Data.cpuPercent;
            var CpuFree = 100 - cpuPercent
            // donut 3
            var chDonutDataCPU = {
              labels: ['Used: '+cpuPercent+'%', 'Free: '+CpuFree+'%'],
              datasets: [
                {
                  backgroundColor: colors.slice(3,4),
                  borderWidth: 0,
                  data: [cpuPercent, CpuFree]
                  // data: [1, 99]
                }
              ]
            };

            var chDonutCPU = document.getElementById("CpuChart");
            if (chDonutCPU) {
            new Chart(chDonutCPU, {
                type: 'pie',
                data: chDonutDataCPU,
                options: donutOptions
            });
            }
            swapTotal = Data.swapTotal;
            swapUsed = Data.swapUsed;

            var swapFree = swapTotal-swapUsed;

            var chDonutDataRAM = {
              labels: ['Used: '+swapUsed+'MiB', 'Free: '+swapFree+' MiB'],
              datasets: [
                {
                  backgroundColor: colors.slice(0,1),
                  borderWidth: 0,
                  data: [swapUsed, swapFree]
                  // data: [5, 95]
                }
              ]
            };
            var chDonutRAM = document.getElementById("SwapChart");
            if (chDonutRAM) {
            new Chart(chDonutRAM, {
                type: 'pie',
                data: chDonutDataRAM,
                options: donutOptions,
            });
            };
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
}, 5000)

</script>
<style>
    .gauge-chart {
  width: 100px;
}
.charts-circle {
  height: 100%;
  border-left: 1px solid #ccc; 
}
@media only screen and (max-width: 1100px) and (min-width: 576px) {
  .charts-circle {
    display: block;
  }
}
@media (max-width: 760px) {
  .charts-circle {
    border-left: 0px;
  }
}
</style>




<!-- */ =====================================  Network card ===================================/ -->

<script>
networkCardFunction()
function networkCardFunction() {

<?php
                $net = shell_exec("python3 tool/netup.py");
                $net = explode("|||", $net);
                $color = ['#81BEF7','#28a745','#333333','#F5D0A9','#D0A9F5','#6c757d'];
                $i = 0;
                foreach ($net as $nw) {
                    if($i ==0) {
                      $i = $i+1;
                      continue;
                    }
      ?>
        var dataPoints<?=$i?> = [];
        
      <?php
                      $i = $i+1;
    }
      ?>

var chart = new CanvasJS.Chart("chartContainer", {
  backgroundColor: "transparent",
    zoomEnabled: true,
    axisX: {
        labelFontColor: "transparent",
        valueFormatString:"0"
    },
    axisY:{
        prefix: "",
        includeZero: false,
        labelFontColor: "#dcf3ff",
        minimum: 0,
    }, 
    toolTip: {
        shared: true
    },
    legend: {
        cursor:"pointer",
        verticalAlign: "top",
        fontSize: 15,
        fontColor: "#dcf3ff",
        itemclick : toggleDataSeries
    },
    data: [
    <?php
                $net = shell_exec("python3 tool/netup.py");
                $net = explode("|||", $net);
                $color = ['#81BEF7','#28a745','#333333','#F5D0A9','#D0A9F5','#6c757d'];
                $i = 0;
                foreach ($net as $nw) {
                    if($i ==0) {
                      $i = $i+1;
                      continue;
                    }
      ?>
{ 
        type: "line",
        xValueType: "dateTime",
        yValueFormatString: "00.00",
        xValueFormatString: "hh:mm:ss TT",
        showInLegend: true,
        name: "<?=explode("||", trim($nw))[0]?>",
        dataPoints: dataPoints<?=$i?>,
        },
      <?php
                      $i = $i+1;
    }
      ?>
    // { 
    //     type: "line",
    //     xValueType: "dateTime",
    //     yValueFormatString: "$####.00",
    //     xValueFormatString: "hh:mm:ss TT",
    //     showInLegend: true,
    //     name: "Company A",
    //     dataPoints: dataPoints1,
    //     },
    //     {               
    //         type: "line",
    //         xValueType: "dateTime",
    //         yValueFormatString: "$####.00",
    //         showInLegend: true,
    //         name: "Company B" ,
    //         dataPoints: dataPoints2
    // },
    // {               
    //         type: "line",
    //         lineColor:"#ff7504",
    //         xValueType: "dateTime",
    //         yValueFormatString: "$####.00",
    //         showInLegend: true,
    //         name: "Company C" ,
    //         dataPoints: dataPoints3
    // }
    ]
});

function toggleDataSeries(e) {
    if (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
        e.dataSeries.visible = false;
    }
    else {
        e.dataSeries.visible = true;
    }
    chart.render();
}

var updateInterval = 2000;
// initial value
var yValue1 = 600; 
var yValue2 = 605;
var yValue2 = 607;

var time = new Date;
// starting at 9.30 am
time.setHours(9);
time.setMinutes(30);
time.setSeconds(00);
time.setMilliseconds(00);

function updateChart(count) {

    // count = count || 1;
    // var deltaY1, deltaY2, deltaY3;
    // for (var i = 0; i < count; i++) {
    //     deltaY1 = .5 + Math.random() *(-.5-.5);
    //     deltaY2 = .5 + Math.random() *(-.5-.5);
    //     deltaY3 = .5 + Math.random() *(-.5-.5);

    // // adding random value and rounding it to two digits. 
    // yValue1 = Math.random()*100;
    // yValue2 = Math.random()*100;
    // yValue3 = Math.random()*100;

    // pushing the new values
    // $(document).ready(function() {
        $.ajax({
            type: "GET",
            url: 'php/network.php',

            success: function(data)
            {
            var data = JSON.parse(data);
 
            var timenow = time.getTime()+ updateInterval;
  <?php
          $net = shell_exec("python3 tool/netup.py");
          $net = explode("|||", $net);
          $color = ['#81BEF7','#28a745','#333333','#F5D0A9','#D0A9F5','#6c757d'];
           array_pop($net);
          $i = 0;
          foreach ($net as $nw) {
              if($i ==0) {
                $i = $i+1;
                continue;
              }
              ?>
              netdata = data.<?=explode("||", trim($nw))[0]?>.in
              time.setTime(timenow);
              console.log(dataPoints<?=$i?>)
              if(dataPoints<?=$i?>.length == 0){
                for(var k=0; k<60; k++){
                  // console.log(time.getTime())
                  dataPoints<?=$i?>.push({
                    x: time.getTime()-60*2000+k*2000,
                    y: 0
                  });
                  chart.render();
                }


              }
              dataPoints<?=$i?>.push({
                  x: time.getTime(),
                  y: netdata*100
              });
              dataPoints<?=$i?>.shift()
              // console.log( dataPoints<?=$i?>);
              chart.options.data[<?=$i-1?>].legendText = "<?=explode("||", trim($nw))[0]?>  (Mbps)";
              <?php
              $i =$i +1;
            }
              ?>
 chart.render();
  
  // myLineChart.data.datasets[4].data[chartlen] = 90;
  // console.log("update")
  // myLineChart.update();
   }
       });
     // });
    // dataPoints1.push({
    //     x: time.getTime(),
    //     y: yValue1
    // });
    // dataPoints2.push({
    //     x: time.getTime(),
    //     y: yValue2
    // });
    // dataPoints3.push({
    //     x: time.getTime(),
    //     y: yValue3
    // });

    // }


    // updating legend text with  updated with y Value 
    // chart.options.data[0].legendText = " enp2s0  " + parseInt(yValue1) + " Mbps";
    // chart.options.data[1].legendText = " enp2s1  " + parseInt(yValue2) + " Mbps";
    // chart.options.data[2].legendText = " enp2s2  " + parseInt(yValue3) + " Mbps"; 
   
}
// generates first set of dataPoints 
updateChart(60);   
setInterval(function(){updateChart()}, updateInterval);

}
</script>




<!-- */ =====================================  RAM ===================================/ -->

<script>

ramFunction();
function ramFunction() {
var dataPoints1 = [];

var chart = new CanvasJS.Chart("RAM", {
  backgroundColor: "transparent",
    zoomEnabled: true,
    axisX: {
        labelFontColor: "transparent",
        valueFormatString:"0"
    },
    axisY:{
        prefix: "",
        includeZero: false,
        labelFontColor: "#dcf3ff",
        minimum: 0,
        maximum: 100
    }, 
    toolTip: {
        shared: true
    },
    legend: {
        cursor:"pointer",
        verticalAlign: "top",
        fontSize: 15,
        fontColor: "#dcf3ff",
        itemclick : toggleDataSeries
    },
    data: [{ 
        type: "line",
        xValueType: "dateTime",
        yValueFormatString: "00.00'%'",
        xValueFormatString: "hh:mm:ss TT",
        showInLegend: true,
        name: "RAM usage",
        dataPoints: dataPoints1,
        }]
});

function toggleDataSeries(e) {
    if (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
        e.dataSeries.visible = false;
    }
    else {
        e.dataSeries.visible = true;
    }
    chart.render();
}

var updateInterval = 1000;
// initial value
var yValue1 = 600; 

var time = new Date;
// starting at 9.30 am
time.setHours(9);
time.setMinutes(30);
time.setSeconds(00);
time.setMilliseconds(00);

async function updateChart(count) {
      
      if(count>0){
        count = count || 1;
        for (var i = 0; i < count; i++) {
            time.setTime(time.getTime()+ updateInterval);
                  dataPoints1.push({
                      x: time.getTime(),
                      y: 0
                  });
                  // updating legend text with  updated with y Value 
                  chart.options.data[0].legendText = " RAM Usage " + yValue1 + " %";
                  chart.render();
              }
        }
        else{
          count = count || 1;
          for (var i = 0; i < count; i++) {
              time.setTime(time.getTime()+ updateInterval);
              await $.ajax({
                  type: "GET",
                  url: 'php/info.php',
                  success: function(response)
                  {
                    var Data = JSON.parse(response)
                    // yValue1 = Math.random();
                    var ramTotal = parseInt(Data.ramTotal);
                    var ramUsed = parseInt(Data.ramUsed);
                    var ramValue = (ramUsed/ramTotal)*100
                    yValue1 = parseInt(ramValue);

                    // pushing the new values
                    dataPoints1.push({
                        x: time.getTime(),
                        y: yValue1
                    });

                    dataPoints1.shift()

                    // updating legend text with  updated with y Value 
                    chart.options.data[0].legendText = " RAM Usage " + yValue1 + " %";
                    chart.render();
                  }});
                }
        }
    

    
}
// generates first set of dataPoints 
updateChart(50);   
setInterval(function(){updateChart()}, updateInterval);

}
</script>



<!-- */ =====================================  CPU ===================================/ -->

<script>

ramFunction();
function ramFunction() {
var dataPoints1 = [];

var chart = new CanvasJS.Chart("CPU", {
  backgroundColor: "transparent",
    zoomEnabled: true,
    axisX: {
        labelFontColor: "transparent",
        valueFormatString:"0"
    },
    axisY:{
        prefix: "",
        includeZero: false,
        labelFontColor: "#dcf3ff",
        minimum: 0,
        maximum: 100
    }, 
    toolTip: {
        shared: true
    },
    legend: {
        cursor:"pointer",
        verticalAlign: "top",
        fontSize: 15,
        fontColor: "#dcf3ff",
        itemclick : toggleDataSeries
    },
    data: [{ 
        type: "line",
        lineColor:"#ff7504",
        xValueType: "dateTime",
        yValueFormatString: "00.00'%'",
        xValueFormatString: "hh:mm:ss TT",
        showInLegend: true,
        indexLabelFontColor: "ff7504",
        name: "CPU usage",
        dataPoints: dataPoints1,
        }]
});

function toggleDataSeries(e) {
    if (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
        e.dataSeries.visible = false;
    }
    else {
        e.dataSeries.visible = true;
    }
    chart.render();
}

var updateInterval = 1000;
// initial value
var yValue1 = 600; 

var time = new Date;
// starting at 9.30 am
time.setHours(9);
time.setMinutes(30);
time.setSeconds(00);
time.setMilliseconds(00);

async function updateChart(count) {
      
      if(count>0){
        count = count || 1;
        for (var i = 0; i < count; i++) {
            time.setTime(time.getTime()+ updateInterval);
                  dataPoints1.push({
                      x: time.getTime(),
                      y: 0
                  });
                  // updating legend text with  updated with y Value 
                  chart.options.data[0].legendText = " RAM Usage " + yValue1 + " %";
                  chart.render();
              }
        }
        else{
          count = count || 1;
          for (var i = 0; i < count; i++) {
              time.setTime(time.getTime()+ updateInterval);
              await $.ajax({
                  type: "GET",
                  url: 'php/info.php',
                  success: function(response)
                  {
                    var Data = JSON.parse(response)
                    cpuValue = parseInt(Data.cpuPercent)
                    yValue1 = parseInt(cpuValue);

                    // pushing the new values
                    dataPoints1.push({
                        x: time.getTime(),
                        y: yValue1
                    });

                    dataPoints1.shift()

                    // updating legend text with  updated with y Value 
                    chart.options.data[0].legendText = " CPU Usage " + yValue1 + " %";
                    chart.render();
                  }});
                }
        }
    

    
}
// generates first set of dataPoints 
updateChart(50);   
setInterval(function(){updateChart()}, updateInterval);

}
</script>