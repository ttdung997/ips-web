<?php

include 'config.php';
    session_start();
    $myfile = fopen("../data/firewall.txt", "w");
    
    $txt = "threshold: ".$_POST["threshold"]."\n";
    fwrite($myfile, $txt);
    $txt = "CPU: ".$_POST["thresholdCPU"]."\n";
    fwrite($myfile, $txt);
    $txt = "thresholdRAM: ".$_POST["thresholdRAM"]."\n";
    fwrite($myfile, $txt);
    $txt = "paranoia: ".$_POST["paranoia"]."\n";
    fwrite($myfile, $txt);
    
    fclose($myfile);

$_SESSION['notification']="Cập nhật cấu hình tường lửa ứng dụng web thành công";    
$newURL = HOST;
header('Location: '.$newURL."firewall_module.php");
?>