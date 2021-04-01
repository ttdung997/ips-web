<?php
 
include 'config.php';

session_start();
$myFile = "pass.txt";
$myFileLink = fopen($myFile, 'r');
$myFileContents = fread($myFileLink, filesize($myFile));
fclose($myFileLink);


	// print($_POST["password"]."<br>");
	// print(sha1($_POST["password"]."AlleNN996g"));
	// echo "<br>";
	// print($myFileContents);

	// hash Char: AlleNN996g
	// $myFile = "pass.txt";
	// $myFileLink = fopen($myFile, 'w+') or die("Can't open file.");
	// fwrite($myFileLink, sha1($_POST["password"]."AlleNN996g"));
	// fclose($myFileLink);

	// echo $myFileContents;
	print($_POST["oldpass"]."<br>");
	print($_POST["newpass"]."<br>");

	if(sha1($_POST["oldpass"]."AlleNN996g") == $myFileContents ){
		$myFile = "pass.txt";
		$myFileLink = fopen($myFile, 'w+') or die("Can't open file.");
		fwrite($myFileLink, sha1($_POST["newpass"]."AlleNN996g"));
		fclose($myFileLink);

		setcookie("token",sha1($_POST["newpass"]."AlleNN996g"), time() + (3600), "/");

		$_SESSION['notification']="Thay đổi mật khẩu thành công";
	}else{

		$_SESSION['error']="Thay đổi mật khẩu thật bại";
		print("Login false");
	}
		$newURL = HOST;
		header('Location: '.$newURL."changepassword.php");
	// echo "Cookies Not Set";
  
?>
 