<?php

include 'php/config.php';

$myFile = "php/pass.txt";
$myFileLink = fopen($myFile, 'r');
$myFileContents = fread($myFileLink, filesize($myFile));
fclose($myFileLink);

if($_COOKIE["token"] != $myFileContents) {
  $newURL = HOST."login.php";
  header('Location: '.$newURL);
} 
session_start();


$waf = shell_exec("sudo tail -n 100 /opt/siem-log/denytem");

$myFile = "data/waf_token.txt";
$myFileLink = fopen($myFile, 'r');
$myFileContents = fread($myFileLink, filesize($myFile));
fclose($myFileLink);

if(sha1($waf) != $myFileContents){
    $_SESSION['logtab']=5;
    $waf_flag = 1;
    $myFile = "data/waf_token.txt";
    $myFileLink = fopen($myFile, 'w+') or die("Can't open file.");
    fwrite($myFileLink, sha1($waf));
    fclose($myFileLink);
}
  
$apache = shell_exec("/var/log/apache2/error.log");

$myFile = "data/apache_token.txt";
$myFileLink = fopen($myFile, 'r');
$myFileContents = fread($myFileLink, filesize($myFile));
fclose($myFileLink);

if(sha1($apache) != $myFileContents){
    $_SESSION['logtab']=4;
    $apache_flag = 1;
    $myFile = "data/apache_token.txt";
    $db = new SQLite3('../data/noti.sqlite');
    $db->exec("INSERT INTO noti(uptime,content,type) VALUES ('".date("Y/m/d h:i:s")."','Phát hiện tấn công ứng dụng web,0')");

    $myFileLink = fopen($myFile, 'w+') or die("Can't open file.");
    fwrite($myFileLink, sha1($waf));
    fclose($myFileLink);
}

?>
    <!DOCTYPE html>
    <html>

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
        <script type="text/javascript">
          if( '1'  == '<?=$apache_flag?>'){
              if (confirm("Đã phát hiện tấn công vào dịch vụ công trực tuyến!")) {
                 window.location.href = '/log.php';
              } 
                  }
           if( '1'  == '<?=$waf_flag?>'){
              if (confirm("Đã phát hiện tấn công vào dịch vụ công trực tuyến!")) {
                 window.location.href = '/log.php';
              } 
                  }
        </script>
    </head>

    <body class="hold-transition sidebar-mini" id="main-body">
        <div class="wrapper" id="main">
            <!-- Navbar -->
            <nav class="main-header navbar navbar-expand bg-white navbar-light header-custom page-topbar">
                <!-- Left navbar links -->

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
          <a href="firewall.php" class="nav-link">
           <p><i class="fa fa-globe" aria-hidden="true"></i> &nbsp;Cấu hình tường lửa</p>
          </a>
        </li> 
         <li class="nav-item has-treeview">
          <a href="rule.php" class="nav-link">
           <p><i class="fa fa-list" aria-hidden="true"></i> &nbsp;Quản lý luật tường lửa</p>
          </a>
        </li>
             <li class="nav-item has-treeview">
          <a href="wafrule.php" class="nav-link">
           <p><i class="fa fa-list" aria-hidden="true"></i> &nbsp;Quản lý luật tự do</p>
          </a>
        </li>

        <li class="nav-item has-treeview">
          <a href="log.php" class="nav-link">
            <p><i class="fa fa-bookmark" aria-hidden="true"></i> &nbsp;Quản lý lưu nhật ký</i></p>
          </a>
        </li>
       <!--  <li class="nav-item has-treeview">
              <a href="#" class="nav-link">
                <i class="fa fa-archive"></i><p> &nbsp;Quản lý dịch vụ<i class="fa fa-angle-left right"></i></p>
              </a>
              <ul class="nav nav-treeview">
                <li class="nav-item">
                  <a href="group_website.php" class="nav-link">
                    <i class="fa fa-circle-o nav-icon"></i><p>Cấu hình dịch vụ</p>
                  </a>
                </li>
                <li class="nav-item">
                  <a href="service_testing_and_evaluation.php" class="nav-link">
                    <i class="fa fa-circle-o nav-icon"></i><p>Kiểm thử và đánh giá dịch vụ</p>
                  </a>
                </li>
              </ul>
      </li> -->
       <li class="nav-item has-treeview">
          <a href="service_testing_and_evaluation.php" class="nav-link">
            <p><i class="fa fa-archive" aria-hidden="true"></i> &nbsp;Kiểm thử và đánh giá dịch vụ</i></p>
          </a>
        </li>
      <li class="nav-item has-treeview">
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
      </li>

                                <li class="nav-item has-treeview">
                                    <a href="firewall_module.php" class="nav-link">
                                        <p><i class="fa fa-sitemap" aria-hidden="true"></i> &nbsp;Phân hệ tường lửa </i>
                                        </p>
                                    </a>
                                </li>
                                <li class="nav-item has-treeview">
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
            <!-- -->
           