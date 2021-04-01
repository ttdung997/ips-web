<?php
$output = shell_exec("sudo python3  ../tool/firewall_log.py");
$output = json_decode($output);
$i = 0; 
foreach($output as $res){
	// print("123123124");
	if( $i == 0){
		$i= $i +1;
		continue;
	}
	print_r($res);
	print_r("<br>");
	$i = $i +1;

}
?>