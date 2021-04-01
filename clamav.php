<?php

include 'include/header.php';

?>
            <div class="content-wrapper">
                <!-- Content Header (Page header) -->
                <section class="content-header">
                    <div class="container-fluid-header">
                        <div class="row mb-2">
                            <div class="col-sm-6">
                                <h1>Thiết lập quét mã độc </h1>
                            </div>
                            <div class="col-sm-6">
                                <ol class="breadcrumb float-sm-right">
                                    <li class="breadcrumb-item"><a href="/"><i class="fa fa-home" aria-hidden="true"></i> Trang chủ</a></li>
                                    <li class="breadcrumb-item active">Thiết lập quét mã độc</li>
                                </ol>
                            </div>
                        </div>
                    </div>
                    <!-- /.container-fluid -->
                </section>

                <!-- Main content -->
                <section class="content">
                    <div class="row">
                        <div class="col-12">
                            <div class="card">
                                <!-- /.card-header -->

                                <div class="card-header">
                                    <h5>Quét tệp tin hệ thống</h5>
                                </div>
                                <div class="card-body">
                        <div class="row" style="margin-bottom:20px;">
           </div>
    <div class="row" style="margin-left:26px; margin-right:20px; padding-bottom: 10px;">

                                    <h5>Kết quả lần quét gần nhất</h5>

        <div id="list_error" class="col-md-12 col-sm-12" style="border: 1px solid #585858; border-radius: 5px; background-color:#000000ad; max-height: 500px; min-height: 500px; overflow-y: auto; padding: 15px; color: #ff7504;">
           <?php 
           echo  shell_exec("sudo cat data/clam/final.log"."| awk -F".'" "'." '{ printf(".'"%-25s<br>"'.", $0); }'");
          
           ?>
        </div>
       
    </div>

    <div class="row float-right" style="padding-bottom: 30px; margin-right: 20px;">
        <div class="">
            <button id="button1" type="button" class="btn btn-add" onclick="ScanAll()"><i class="fa fa-check"></i>Quét toàn bộ hệ thống</button>
        </div>
        <div class="" style="padding: 0 0 0 15px;">
            <button id="button2"  class="btn btn-add"  data-toggle="modal" data-target="#exampleModalLong"><i class="fa fa-chain-broken"></i> Quét tùy chọn</button>
        </div>
    </div>        
                    </div>
                    <!-- /.card-body -->
            </div>
           <div id="exampleModalLong" class="modal" tabindex="-1" role="dialog">
  <div class="modal-dialog" role="document" style="max-width: 400px; margin: 20rem auto;">
    <div class="modal-content" style="background-color:#2b3c46">
      <div class="modal-header" style="    border-bottom: 1px solid rgba(255,255,255,0.1);">
        <h5 class="modal-title">Quét theo danh mục</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        <?php
         $output = shell_exec("ls /"."| awk -F".'" "'." '{ printf(".'"%-15s|||"'.", $1); }'");
         $output = (explode("|||",$output));
        ?>
        <select class="form-control Disable" name="disk" id="disk" style="width: 300px;">
                                        <?php

    foreach ($output as $nw) {
        echo '<option value="'.$nw.'">'.$nw.'</option>';
    }
    ?>
                                    </select>

      </div>
      <div class="modal-footer" style=" border-top: 1px solid rgba(255,255,255,0.1); justify-content: left">
        <button type="button" class="btn btn-add" onclick="ScanSel()">Quét</button>
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Thoát </button>
      </div>
    </div>
  </div>
</div>
        </div>
        <!-- /.col -->
        </div>
    </section>
    <section class="content">
                            <div class="card">
                                <!-- /.card-header -->
                                <div class="card-header">
                            <h5>Quét tệp tin hệ thống</h5>
                                   <?php
                                  $db = new SQLite3('data/check.sqlite');
                                  $count = $db->querySingle('SELECT count(distinct name) FROM check_file');
                                  $count_malware = $db->querySingle('SELECT count(distinct name) FROM check_file where check_value = 0');
                                  $large = $db->querySingle('SELECT AVG(large_file) FROM check_file');
                      ?>
</div>
                                <div class="card-body">

<div class="row">
                                <div class="col-md-12">
                                               
                                      <div class="card card-custom">

                                      <div class="card-header card-header-cus">
                                         <form action="php/file_scan.php" method="post" style="float: right;">
                 <input value="1" type="hidden" name="tab" id="tabSelect">
                 <button type="submit" class="btn btn-add Disable" style="margin-top: 10px;"><i class="fa fa-refresh" aria-hidden="true"></i>  Quét chủ động </button>
              </form>
                                        <h3 class="card-title">Thông tin tệp trên hệ thống </h3>

                                      </div>
                                      <div class="card-body">
                                          
                                           <ul id="server-list" class="list-group">

                                          <li class="list-group-item">
                                        
                                          
                                          <b class="color-b" >Số lượng file: </b><i><?=$count?> file</i> 
                                          </li>
                                          </li>
                                          <li class="list-group-item">
                                        
                                          <b class="color-b">Số file chứa mã độc: </b>
                                          </a>  <i><?=$count_malware?> file</i> 
                                          </li>
                                         
                                          <li class="list-group-item">
                                          <a>
                                          <b class="color-b">Kích thước trung bình: </b>
                                          </a>  <i><?=$large?> KB</i> 

                  

                                      </li>
                  </ul>
                  </div>

                                        </div>
                                    </div>                         
                                </div>
                        </div>
                    </div>
                </div>
            </div>
    </section>
</div>

        <!-- /.row -->
        <?php

include 'include/footer.php';

?>
        <!-- <script src="https://js.pusher.com/4.1/pusher.min.js"></script> -->
        <!-- datatable -->
        <script type="text/javascript" src="admin_asset_web/dist/js/jquery.passtrength.min.js"></script>
        <script type="text/javascript" src="admin_asset_web/dist/js/jquery.confirm.js"></script>

        <!-- AdminLTE for demo purposes -->
        <script src="admin_asset_web/dist/js/demo.js"></script>

<script type="text/javascript">
function ScanAll(){
  $.ajax({ 
    method:"GET", 
    url: "php/clamall.php",
    // url: "/check",
    // headers:  {'Access-Control-Allow-Origin' : 'http://192.168.218.138'},
    success: function (data) {
        console.log(data)
        $("#list_error").html(data);
      
    }
});

}

function ScanSel(){
    var sel = document.getElementById('disk');

    console.log(sel.value)
    if(sel.selectedIndex ==0){
        ScanAll();
    }else{

     var data = new FormData();

    data.append('sel', sel.value);
      $.ajax({ 
        method:"POST", 
        url: "php/clamav.php",
  data: data,
  processData: false,
  contentType: false,
        // url: "/check",
        // headers:  {'Access-Control-Allow-Origin' : 'http://192.168.218.138'},
        success: function (data) {
            console.log(data)
            $("#list_error").html(data);
          
        }
    });
  }
}
</script>
