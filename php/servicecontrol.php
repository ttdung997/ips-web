<?php
include 'config.php';
print_r($_POST["name"]);
print_r($_POST["action"]);
print('sudo service '.$_POST["name"]." ".$_POST["action"]);
       $output = shell_exec('sudo service '.$_POST["name"]." ".$_POST["action"]);
        // $newURL = HOST;
        // header('Location: '.$newURL."firewall_module.php");

?>