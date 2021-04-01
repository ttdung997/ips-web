<?php
include 'config.php';
$db = new SQLite3('../data/check.sqlite');
  // print("INSERT INTO bkcs_custom_domain(domain,type) VALUES ('".$_POST["Domain"]."','".$_POST["Type"]."')");
$db->exec("DELETE FROM mod_custom_rule WHERE id = ". $_POST["id"]);

$rule_encode = base64_encode($_POST["rule"]);               
shell_exec("sudo python  ../tool/core_waf/delete_rule_custom.py 1 ".$rule_encode." 2>&1");

               
$newURL = HOST;
header('Location: '.$newURL."firewall_module.php"); 

?>