<html><head>

	<?php

include 'php/config.php';


$myFile = "php/pass.txt";
$myFileLink = fopen($myFile, 'r');
$myFileContents = fread($myFileLink, filesize($myFile));
fclose($myFileLink);
   
   
if($_COOKIE["token"] == $myFileContents) {
  $newURL = HOST;
  header('Location: '.$newURL);
} 

?>


<title>BKCS</title>
<!-- <script src="js/jquery.min.js"></script> -->
<!-- Custom Theme files -->
<link href="admin_asset_web/style.css" rel="stylesheet" type="text/css" media="all">
<!-- Font Awesome -->
<link rel="stylesheet" href="admin_asset_web/dist/css/font-awesome.min.css">

<!-- for-mobile-apps -->
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta name="keywords" content="Classy Login form Responsive, Login form web template, Sign up Web Templates, Flat Web Templates, Login signup Responsive web template, Smartphone Compatible web template, free webdesigns for Nokia, Samsung, LG, SonyEricsson, Motorola web design">


<!-- //for-mobile-apps -->
<!--Google Fonts-->
<link href="//fonts.googleapis.com/css?family=Roboto+Condensed:400,700" rel="stylesheet" type="text/css">
 </head>
<body>
  <div class="login-header">
      
  </div>
<!--header start here-->
 <div class="header">
	<div class="header-main">
		<div class="form-login">
			<div>
				<div class="header-left-bottom agileinfo">
														</div>
				<div class="avatar"><span class="span-avatar"><img style="border-radius: 25%" src="admin_asset_web/dist/img/bkcs-logo.png"></span></div>
				<div class="header-left-bottom">
					<div class="size-cutom"><span   class="css-color-blue span-header">IPS DASHBROAD</span></div>
					<form action="php/login.php" method="POST">
						<div class="input-custom">
							<span class="span-custom"><i class="fa fa-user color-icon"></i></span>
							<input type="text" name="username" placeholder="Nhập tài khoản đăng nhập">
						</div>
						<div class="input-custom">
							<span class="span-custom"><i class="fa fa-briefcase color-icon"></i></span>
							<input type="password" name="password" placeholder="Nhập mật khẩu">
						</div>
						<div class="input-custom">
							<input class="button-login" type="submit" value="Login" name="dangnhap">
						</div>
						<!-- <div class="forgotpassword">
							<a href="/password/reset"><h2>Forgot password?</h2></a>
						</div> -->
					</form>
				</div>
			</div>
		</div>
	</div>
</div>
<!--header end here-->
<!--footer end here-->
  
</body></html>