<?php
 print("123");
include 'config.php';
	session_start();
  $db = new SQLite3('../tool/dga/data.db');
  $db->exec("INSERT INTO bkcs_custom_domain(domain,type) VALUES ('".$_POST["Domain"]."','".$_POST["Type"]."')");

$_SESSION['notification']="Thêm tên miền tự định nghĩa thành công vào IPS";
$newURL = HOST;
header('Location: '.$newURL."dga_custom.php"); 
?>
 