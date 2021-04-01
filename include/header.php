<?php

include 'php/config.php';

// include 'incule/noti_read.php';

$myFile = "php/pass.txt";
$myFileLink = fopen($myFile, 'r');
$myFileContents = fread($myFileLink, filesize($myFile));
fclose($myFileLink);
   
// $db = new SQLite3('data/noti.sqlite');
// $db->exec("INSERT INTO noti(uptime,content,nottype) VALUES ('".date("Y/m/d h:i:s")."','Phát hiện tấn công ứng dụng web',0)");
// print_r("INSERT INTO noti(uptime,content,nottype) VALUES ('".date("Y/m/d h:i:s")."','Phát hiện tấn công ứng dụng web',0)");
// quit();
   
if($_COOKIE["token"] != $myFileContents) {
  $newURL = HOST."login.php";
  header('Location: '.$newURL);
} 
session_start();


// $waf = shell_exec("sudo tail -n 10 /opt/siem-log/denytem");

// $myFile = "data/waf_token.txt";
// $myFileLink = fopen($myFile, 'r');
// $myFileContents = fread($myFileLink, filesize($myFile));
// fclose($myFileLink);

// if(sha1($waf) != $myFileContents){
//     $_SESSION['logtab']=5;
//     $waf_flag = 1;
//     $myFile = "data/waf_token.txt";
//     $myFileLink = fopen($myFile, 'w+') or die("Can't open file.");
//     fwrite($myFileLink, sha1($waf));
//     fclose($myFileLink);

//  $url= ips_manager+"/notifi";
//   $postData = array(
//       "time" => date("M,d,Y h:i:s A"),
//       'name' => "DungPC",
//       'type' => "Phát hiện tấn công dịch vụ công trực tuyến ",
//       'content' => shell_exec("sudo tail -n 10 /opt/siem-log/denytem")
//   );               
//   $data_string = json_encode($postData);                                                                                   
                                                                                                                       
//   $ch = curl_init($url);                                                                      
//   curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");                                                                     
//   curl_setopt($ch, CURLOPT_POSTFIELDS, $data_string);                                                                  
//   curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);                                                                      
//   curl_setopt($ch, CURLOPT_HTTPHEADER, array(                                                                          
//       'Content-Type: application/json',                                                                                
//       'Content-Length: ' . strlen($data_string))                                                                       
//   );                                                                                                                   
                                                                                                                       
//   $result = curl_exec($ch);
// }
  
// $apache = shell_exec("sudo tail -n 10 /var/log/apache2/error.log");

// $myFile = "data/apache_token.txt";
// $myFileLink = fopen($myFile, 'r');
// $myFileContents = fread($myFileLink, filesize($myFile));
// fclose($myFileLink);

// if(sha1($apache) != $myFileContents){
//     $_SESSION['logtab']=4;
//     $apache_flag = 1;
//     $myFile = "data/apache_token.txt";
//     $myFileLink = fopen($myFile, 'w+') or die("Can't open file.");
//     fwrite($myFileLink, sha1($waf));
//     fclose($myFileLink);
//     $url= ips_manager + "/notifi";
//   $postData = array(
//       "time" => date("M,d,Y h:i:s A"),
//       'name' => "DungPC",
//       'type' => "Phát hiện lỗi trên máy chủ dịch vụ công ",
//       'content' => shell_exec("sudo tail -n 10 /var/log/apache2/error.log")
//   );               
//   $data_string = json_encode($postData);                                                                                   
                                                                                                                       
//   $ch = curl_init($url);                                                                      
//   curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");                                                                     
//   curl_setopt($ch, CURLOPT_POSTFIELDS, $data_string);                                                                  
//   curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);                                                                      
//   curl_setopt($ch, CURLOPT_HTTPHEADER, array(                                                                          
//       'Content-Type: application/json',                                                                                
//       'Content-Length: ' . strlen($data_string))                                                                       
//   );                                                                                                                   
                                                                                                                       
//   $result = curl_exec($ch);
// }
// $_SESSION['logtab']=44;
?>
    <!DOCTYPE html>
    <html style="background-color: #1e2a31;">

    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <title>HOST IPS | BKCS</title>
        <!-- Tell the browser to be responsive to screen width -->
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <!-- Font Awesome -->
        <link rel="stylesheet" href="admin_asset_web/dist/css/font-awesome.min.css">
        <!-- Ionicons -->
        <link rel="stylesheet" href="admin_asset_web/dist/css/ionicons.min.css">
        <!-- DataTables -->
        <link rel="stylesheet" href="admin_asset_web/plugins/datatables/dataTables.bootstrap4.css">
        <!-- Theme style -->
        <link rel="stylesheet" href="admin_asset_web/dist/css/adminlte1.css">
        <!-- iCheck -->
        <link rel="stylesheet" href="admin_asset_web/plugins/iCheck/flat/blue.css">
        <!-- Google Font: Source Sans Pro -->
        <link rel="stylesheet" href="admin_asset_web/dist/css/google_font.css">
        <!-- passtrength -->
        <link rel="stylesheet" type="text/css" href="admin_asset_web/dist/css/passtrength.css">
        <!-- anomay css -->
        <link rel="stylesheet" href="admin_asset_web/dist/css/anomaly.css">
        <script  type="text/javascript">
          function check(){
              if( '1'  == '<?=$apache_flag?>'){
                 $("#LogModel").modal()
            }
               if( '1'  == '<?=$waf_flag?>'){
                  $("#LogModel").modal()
            }
            if(window.location.href.includes("log.php") == true){
              document.getElementById("loglink").href = "#";
              document.getElementById("loglink").setAttribute("data-dismiss", "modal");
            }
          }
          window.onload = function(){
        //time is set in milliseconds
              setTimeout(check, 1000)
          };
        </script>
        <script src="admin_asset_web/plugins/jquery/loading.js"></script>
    </head>

    <body class="hold-transition sidebar-mini" id="main-body">
      <div class="lds-roller-div">
            <div class="lds-roller"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div>
        </div>
        <div id="background-black"></div>

        <div class="wrapper" id="main">
            <!-- Navbar -->
            <nav class="main-header navbar navbar-expand bg-white navbar-light header-custom page-topbar">
                <!-- Left navbar links -->
                <a href="php/logout.php" class="nav-link" style="position: fixed;right: 30px; top: 15px;" title="Đăng xuất">
                 <p><i class="fa fa-sign-out" aria-hidden="true"></i> &nbsp;Đăng xuất</p>
                </a>
                <!-- Main Sidebar Container -->
                <aside class="main-sidebar elevation-4">
                    <!-- Brand Logo -->
                    <a class="brand-link">
                        <img src="admin_asset_web/dist/img/bkcs-logo.png" alt="BKCS" class="brand-image img-circle elevation-3" style="opacity: .8; margin-left: 6px;">
                        <span class="brand-text font-weight-light"><strong class="css-color-blue"><b>IPS DASHBOARD</b></strong></span>
                    </a>

                    <!-- Sidebar -->
                    <div class="sidebar">
                        <!-- Sidebar Menu -->
                        <nav class="mt-2">
      <ul class="nav nav-pills nav-sidebar flex-column" data-widget="treeview" role="menu" data-accordion="false">
        <!-- Add icons to the links using the .nav-icon class
             with font-awesome or any other icon font library -->

        <li class="menusection">Main</li>
         <li class="nav-item has-treeview">
          <a href="/" class="nav-link">
           <p><i class="fa fa-home" aria-hidden="true"></i> &nbsp;Trang chủ</p>
          </a>
        </li>
         <li class="nav-item has-treeview">
          <a href="noti.php" class="nav-link">
           <p><i class="fa fa-home" aria-hidden="true"></i> &nbsp;Cảnh báo</p>
          </a>
        </li>
         <li class="nav-item has-treeview">
              <a href="#" class="nav-link">
                <i class="fa fa-archive"></i><p> &nbsp;Bảo vệ hệ thống tệp tin<i class="fa fa-angle-left right"></i></p>
              </a>
              <ul class="nav nav-treeview">

        <li class="nav-item has-treeview">
          <a href="crypto.php" class="nav-link">
           <p><i class="fa fa-circle-o nav-ico" aria-hidden="true"></i> &nbsp;Mã hóa tệp tin</p>
          </a>
        </li> 
  <li class="nav-item has-treeview">
          <a href="integrity.php" class="nav-link">
           <p><i class="fa fa-circle-o nav-ico" aria-hidden="true"></i> &nbsp;Kiểm tra toàn vẹn </p>
          </a>
        </li>   
          <li class="nav-item has-treeview">
          <a href="moniter.php" class="nav-link">
           <p><i class="fa fa-circle-o nav-ico" aria-hidden="true"></i> &nbsp;Kiểm soát truy cập</p>
          </a>
        </li> 
          <li class="nav-item has-treeview">
          <a href="reg_static.php" class="nav-link">
           <p><i class="fa fa-circle-o nav-ico" aria-hidden="true"></i> &nbsp;Báo cáo thống kê </p>
          </a>
        </li> 
      </ul>
      </li>
      <li class="nav-item has-treeview">
              <a href="#" class="nav-link">
                <i class="fa fa-archive"></i><p> &nbsp;Quản lý tường lửa<i class="fa fa-angle-left right"></i></p>
              </a>
              <ul class="nav nav-treeview">


        <li class="nav-item has-treeview">
          <a href="firewall.php" class="nav-link">
           <p><i class="fa fa-circle-o nav-ico" aria-hidden="true"></i> &nbsp;Tường lửa kiểm soát truy cập</p>
          </a>
        </li> 
  <li class="nav-item has-treeview">
          <a href="firewall_module.php" class="nav-link">
           <p><i class="fa fa-circle-o nav-ico" aria-hidden="true"></i> &nbsp; Tường lửa ứng dụng Web</p>
          </a>
        </li>   
         
         <li class="nav-item has-treeview">
          <a href="log.php" class="nav-link">
           <p><i class="fa fa-circle-o nav-ico" aria-hidden="true"></i> &nbsp; Báo cáo thống kê</p>
          </a>
        </li>  
          <!--  <li class="nav-item has-treeview">
          <a href="firewall_log.php" class="nav-link">
           <p><i class="fa fa-circle-o nav-ico" aria-hidden="true"></i> &nbsp; Nhật ký tường lửa ứng dụng</p>
          </a>
        </li>  -->
      </ul>
      </li>


        <!--   <li class="nav-item has-treeview">
              <a href="#" class="nav-link">
                <i class="fa fa-archive"></i><p> &nbsp;Tương lửa truy cập <i class="fa fa-angle-left right"></i></p>
              </a>
              <ul class="nav nav-treeview">

        <li class="nav-item has-treeview">
          <a href="firewall.php" class="nav-link">
           <p><i class="fa fa-circle-o nav-ico" aria-hidden="true"></i> &nbsp;Cấu hình luật</p>
          </a>
        </li> 
  <li class="nav-item has-treeview">
          <a href="firewall_module.php" class="nav-link">
           <p><i class="fa fa-circle-o nav-ico" aria-hidden="true"></i> &nbsp;Quản lý luật</p>
          </a>
        </li>   
      </ul>
      </li>
          -->
      <!--    <li class="nav-item has-treeview">
              <a href="#" class="nav-link">
                <i class="fa fa-archive"></i><p> &nbsp;Tương lửa ứng dụng web <i class="fa fa-angle-left right"></i></p>
              </a>
              <ul class="nav nav-treeview">
                <li class="nav-item">
                  <a href="firewall_module.php" class="nav-link">
                    <i class="fa fa-circle-o nav-icon"></i><p>Cấu hinh tương lửa </p>
                  </a>
                </li>
                <li class="nav-item has-treeview">
          <a href="wafrule.php" class="nav-link">
           <p><i class="fa fa-circle-o nav-icon" aria-hidden="true"></i> Quản lý luật Modsecurity</p>
          </a>
        </li>
              </ul>
      </li> -->

           
      <!--   <li class="nav-item has-treeview">
          <a href="app.php" class="nav-link">
            <p><i class="fa fa-bookmark" aria-hidden="true"></i> &nbsp;Quản lý ứng dụng</i></p>
          </a>
        </li> -->

        
     
      <li class="nav-item has-treeview">
              <a href="#" class="nav-link">
                <i class="fa fa-archive"></i><p> &nbsp;Kiểm thử và đánh giá<i class="fa fa-angle-left right"></i></p>
              </a>
              <ul class="nav nav-treeview">

        <li class="nav-item has-treeview">
          <a href="web_test.php" class="nav-link">
           <p><i class="fa fa-circle-o nav-ico" aria-hidden="true"></i> &nbsp; Phần mềm dịch vụ công </p>
          </a>
        </li> 
  
  <li class="nav-item has-treeview">
          <a href="sql_test.php" class="nav-link">
           <p><i class="fa fa-circle-o nav-ico" aria-hidden="true"></i> &nbsp; Cơ sở dữ liệu </p>
           
          </a>
        </li>   
        <li class="nav-item has-treeview">
          <a href="os_test.php" class="nav-link">
           <p><i class="fa fa-circle-o nav-ico" aria-hidden="true"></i> &nbsp;Hệ điều hành</p>
           
          </a>
        </li> 
        <li class="nav-item has-treeview">
          <a href="testing_history.php" class="nav-link">
           <p><i class="fa fa-circle-o nav-ico" aria-hidden="true"></i> &nbsp; Báo cáo thống kê</p>
           
          </a>
        </li> 

      </ul>
      </li>


    <!--    <li class="nav-item has-treeview">
          <a href="service_testing_and_evaluation.php" class="nav-link">
            <p><i class="fa fa-archive" aria-hidden="true"></i> &nbsp;Kiểm thử và đánh giá dịch vụ</i></p>
          </a>
        </li>
 -->

      <li class="nav-item has-treeview">
              <a href="#" class="nav-link">
                <i class="fa fa-archive"></i><p> &nbsp;Rà soát mã độc<i class="fa fa-angle-left right"></i></p>
              </a>
              <ul class="nav nav-treeview">

        <li class="nav-item has-treeview">
          <a href="clamscan.php" class="nav-link">
           <p><i class="fa fa-circle-o nav-ico" aria-hidden="true"></i> &nbsp;Tệp tin hệ thống </p>
          </a>
        </li> 
  
 <!--  <li class="nav-item has-treeview">
          <a href="file_secure.php" class="nav-link">
           <p><i class="fa fa-circle-o nav-ico" aria-hidden="true"></i> &nbsp; Tệp tin dịch vụ công</p>
           
          </a>
        </li>  -->  
        <li class="nav-item has-treeview">
          <a href="file_secure.php" class="nav-link">
           <p><i class="fa fa-circle-o nav-ico" aria-hidden="true"></i> &nbsp; Báo cáo thống kê</p>
           
          </a>
        </li> 

        <!--  <li class="nav-item has-treeview">
          <a href="file_secure.php" class="nav-link">
           <p><i class="fa fa-circle-o nav-ico" aria-hidden="true"></i> &nbsp; Báo cáo thống kê</p>
           
          </a>
        </li>   -->
      </ul>
      </li>
       <li class="nav-item has-treeview">
              <a href="#" class="nav-link">
                <i class="fa fa-archive"></i><p> &nbsp;Quản lý ứng dụng <i class="fa fa-angle-left right"></i></p>
              </a>
              <ul class="nav nav-treeview">

        <li class="nav-item has-treeview">
          <a href="app.php" class="nav-link">
           <p><i class="fa fa-circle-o nav-ico" aria-hidden="true"></i> &nbsp;Danh sách ứng dụng </p>
          </a>
        </li> 
  <li class="nav-item has-treeview">
          <a href="update_app.php" class="nav-link">
           <p><i class="fa fa-circle-o nav-ico" aria-hidden="true"></i> &nbsp;Cập nhật ứng dụng</p>
          </a>
        </li>   
      </ul>
      </li>


    <!--     <li class="nav-item has-treeview">
          <a href="clamav.php" class="nav-link">
            <p><i class="fa fa-bookmark" aria-hidden="true"></i> &nbsp;Rà soát mã độc hệ thống</i></p>
          </a>
        </li>
        <li class="nav-item has-treeview">
          <a href="file_secure.php" class="nav-link">
            <p><i class="fa fa-bookmark" aria-hidden="true"></i> &nbsp;Rà soát tập tin mã độc</i></p>
          </a>
        </li> -->

       <!--  <li class="nav-item has-treeview">
          <a href="log.php" class="nav-link">
            <p><i class="fa fa-bookmark" aria-hidden="true"></i> &nbsp;Quản lý lưu nhật ký</i></p>
          </a>
        </li> -->

     <!--  <li class="nav-item has-treeview">
              <a href="#" class="nav-link">
                <i class="fa fa-archive"></i><p> &nbsp;Phân hệ mã độc DGA<i class="fa fa-angle-left right"></i></p>
              </a>
              <ul class="nav nav-treeview">
                <li class="nav-item">
                  <a href="dga_index.php" class="nav-link">
                    <i class="fa fa-circle-o nav-icon"></i><p>Thông tin máy trạm</p>
                  </a>
                </li>
                <li class="nav-item">
                  <a href="dga_list.php" class="nav-link">
                    <i class="fa fa-circle-o nav-icon"></i><p>Danh sách tên miền DGA</p>
                  </a>
                </li>
                <li class="nav-item">
                  <a href="dga_custom.php" class="nav-link">
                    <i class="fa fa-circle-o nav-icon"></i><p>Tên miền tự định nghĩa</p>
                  </a>
                </li> <li class="nav-item">
                  <a href="dga_malware.php" class="nav-link">
                    <i class="fa fa-circle-o nav-icon"></i><p>Thông tin mã độc</p>
                  </a>
                </li>
              </ul>
      </li> -->

                              <!--   <li class="nav-item has-treeview">
                                    <a href="firewall_module.php" class="nav-link">
                                        <p><i class="fa fa-sitemap" aria-hidden="true"></i> &nbsp;Phân hệ tường lửa </i>
                                        </p>
                                    </a>
                                </li> -->
                               <li class="nav-item has-treeview">
              <a href="#" class="nav-link">
                <i class="fa fa-archive"></i><p> &nbsp; Tùy chọn hệ thống<i class="fa fa-angle-left right"></i></p>
              </a>
              <ul class="nav nav-treeview">

        <li class="nav-item has-treeview">
          <a href="changepassword.php" class="nav-link">
           <p><i class="fa fa-circle-o nav-ico" aria-hidden="true"></i> &nbsp;Thay đổi mật khẩu </p>
          </a>
        </li> 
  

                              <!--   <li class="nav-item has-treeview">
                                    <a href="changepassword.php" class="nav-link">
                                        <p><i class="fa fa-lock" aria-hidden="true"></i> &nbsp;Thay đổi mật khẩu </i>
                                        </p>
                                    </a>
                                </li>
                                <li class="nav-item has-treeview">
                                    <a href="php/logout.php" class="nav-link">
                                        <p><i class="fa fa-sign-out" aria-hidden="true"></i> &nbsp;Đăng xuất </i>
                                        </p>
                                    </a>
                                </li>

 -->

      
      </ul>
    </nav>
                        <!-- /.sidebar-menu -->
                    </div>
                    <!-- /.sidebar -->
                </aside>

            </nav>
            <!-- /.navbar -->
            <!-- jQuery -->
            <script src="admin_asset_web/plugins/jquery/jquery.min.js"></script>

         
            <div class="modal" tabindex="-1" role="dialog" id="LogModel">
          <div class="modal-dialog" role="document">
            <div class="modal-content">
              <div class="modal-header">
                <h5 style="color: black" class="modal-title">Cảnh báo tấn công</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                  <span aria-hidden="true">&times;</span>
                </button>
              </div>
              <div class="modal-body">
                <p style="color: black">đã phát hiện tấn công đến máy chủ dịch vụ công trực tuyến!</p>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">Thoát</button>
                <a id="loglink" href="/log.php" class="btn btn-primary" >Chi tiết</a>
              </div>
            </div>
          </div>
          </div>
            <!-- -->
           