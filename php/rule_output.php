<?php
include 'config.php';
	session_start();
	$command = "sudo python ../tool/python-iptables/manual_output.py -d ".$_POST['id'];
	print_r($command);
	// die();
	$shell = shell_exec($command);
	$shell = shell_exec("sudo iptables-save > /opt/iptables.conf");
	$_SESSION['notification']="Đã xóa luật thành công";

	$newURL = HOST."rule.php";
	header('Location: '.$newURL);
	
?>