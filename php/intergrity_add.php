<?php

include 'config.php';

$path = $_POST['path'];
// print($path);
$files = scandir($path,1);
$key = 1;

// print_r($files);

if ($files == false){
	$key = 0;
}else{
	$key = 1;
}

// print_r("sudo python3 ../script/file_system_protection/demo_integrity.py -i ".$path." ".$key);
$add = shell_exec("sudo python3 ../script/file_system_protection/demo_integrity.py -i ".$path." ".$key);
print_r($add);
?>