<?php
include 'config.php';
session_start();
// print_r($_POST);
// die();
$ip1Array = explode(",", $_POST['ip1']);
$ip2Array = explode(",", $_POST['ip2']);
$port1Array = explode(",", $_POST['port1']);
$port2Array = explode(",", $_POST['port2']);

// if(strlen($_POST['ip1']) ==0){
// 	// $ip1Error = "IP đích không được rỗng";
// 		$e = 1;

// }
// else{
// 	foreach ($ip1Array as $ip) {
// 		if(substr_count($ip, ".") != 3){
// 			$ip1Error = "Không đúng định dạng IP nguồn";	
// 			$eflag = 1;
// 			break;
// 		}
// 	}
// }



if (strlen($_POST['port1']) == 0) {
	// $port1Error = "Cổng đích không được rỗng";
	$e = 1;
} else {
	foreach ($port1Array as $port) {
		// print_r($port);
		// die();
		if ((int) $port > 65000) {
			$port1Error = "Port phải nhỏ hơn 65000";
			$eflag = 1;
			break;
		}
		if ((int) $port < 1) {
			$port1Error = "Port phải là số";
			$eflag = 1;
			break;
		}
	}
}

if (strlen($_POST['ip2']) == 0) {
	// $ip2Error = "IP nguồn không được rỗng";
	$e = 1;
} else {
	foreach ($ip2Array as $ip) {
		if (substr_count($ip, ".") != 3) {
			$ip1Error = "Không đúng định dạng IP nguồn";
			$eflag = 1;
			break;
		}
	}
}

if (strlen($_POST['port2']) == 0) {
	// $port1Error = "Cổng nguồn không được rỗng";
	$e = 1;
} else {
	foreach ($port2Array as $port) {
		if ((int) $port > 65000) {
			$port2Error = "Port phải nhỏ hơn 65000";
			$eflag = 1;
			break;
		}
		if ((int) $port < 1) {
			$port1Error = "Port phải là số";
			$eflag = 1;
			break;
		}
	}
}

if (substr_count($_POST['ip1'], ",") > 4) {
	$ip1Error = "IP đích chỉ chứa tối đa 5 lựa chọn";
	$eflag = 1;
}
if (substr_count($_POST['port1'], ",") > 4) {
	$port1Error = "Cổng đích chỉ chứa tối đa 5 lựa chọn";
	$eflag = 1;
}

if (substr_count($_POST['ip2'], ",") > 4) {
	$ip2Error = "IP nguồn chỉ chứa tối đa 5 lựa chọn";
	$eflag = 1;
}
if (substr_count($_POST['port2'], ",") > 4) {
	$port2Error = "Cổng nguồn chỉ chứa tối đa 5 lựa chọn";
	$eflag = 1;
}
if (strlen($_POST['prefix']) > 64) {
	$prefixError = "Prefix phải từ 1 đến  64 kí tự";
	$eflag = 1;
}

if ($eflag == 0) {
	//call script
	$a = 1;

	// python blacklist_input.py --dst-port 80 --src-ip 192.168.1.22

	// usage: blacklist_input.py [-h] [--protocol PROTOCOL] [--src-ip SRC_IP]
	//                           [--dst-ip DST_IP] [--src-port SRC_PORT]
	//                           [--dst-port DST_PORT] [--port PORT] [--ip IP]
	//                           [--comment COMMENT] [-f]

	$command = "sudo python ../tool/python-iptables/blacklist_output.py --protocol " . $_POST['Protocol'];
	if (strlen($_POST['ip1']) != 0) {
		$command = $command . " --src-ip " . $_POST['ip1'];
	}

	if (strlen($_POST['ip2']) != 0) {
		$command = $command . " --dst-ip " . $_POST['ip2'];
	}

	if (strlen($_POST['port']) != 0) {
		$command = $command . " --port " . $_POST['port'];
	} else {
		if (strlen($_POST['port1']) != 0) {
			$command = $command . " --src-port " . $_POST['port1'];
		}

		if (strlen($_POST['port2']) != 0) {
			$command = $command . " --dst-port " . $_POST['port2'];
		}
	}

	if (strlen($_POST['prefix']) != 0) {
		$command = $command . " --log bkcs-" . $_POST['prefix'];
	} else {

		$command = $command . " --log bkcs-";
	}

	print($command . "<br>");
	// $command = "l";
	$shell = shell_exec($command);

	print_r($shell);
	// sleep(2);
	$shell = shell_exec("sudo iptables-save > /opt/iptables.conf");



	session_destroy();
	session_start();

	$_SESSION['notification'] = "Thêm luật thành công vào IPS";
	$newURL = HOST . "firewall.php";
	header('Location: ' . $newURL);
} else {

	$_SESSION['ip1Error'] = $ip1Error;
	$_SESSION['ip2Error'] = $ip2Error;
	$_SESSION['port1Error'] = $port1Error;
	$_SESSION['port2Error'] = $port2Error;
	$_SESSION['prefixError'] = $prefixError;
	$_SESSION['val'] = $_POST;

	$newURL = HOST . "firewall.php";
	header('Location: ' . $newURL);
}
