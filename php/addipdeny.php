<?php
 
include 'config.php';
  $db = new SQLite3('../data/check.sqlite');
  // print("INSERT INTO bkcs_custom_domain(domain,type) VALUES ('".$_POST["Domain"]."','".$_POST["Type"]."')");
  $db->exec("INSERT INTO mod_ip_deny(ip,description) VALUES ('".$_POST["ip"]."','".$_POST["description"]."')");
               
$rows = $db->query("select max(id) as count from mod_ip_deny");
$row = $rows->fetchArray();
$numRows = $row['count'];
shell_exec("sudo python  ../tool/core_waf/add_rules.py 1 ".$_POST["ip"]." ".$numRows." 2>&1");
// print(1);

// $newURL = HOST;
// header('Location: '.$newURL."firewall_module.php");

?>
 