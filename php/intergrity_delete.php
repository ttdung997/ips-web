<?php

$path = explode("&", $_POST['path'])[0] ;
$type = explode("&", $_POST['path'])[1] ;

$add = shell_exec("sudo python3 ../script/file_system_protection/demo_integrity.py -r ".$path." ".$type);
// print("sudo python3 ../script/file_system_protection/integrity_check_linux.py -r ".$path." ".$type);

print_r($add);
?>