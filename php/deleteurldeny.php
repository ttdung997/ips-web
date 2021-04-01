<?php
include 'config.php';
$db = new SQLite3('../data/check.sqlite');
  // print("INSERT INTO bkcs_custom_domain(domain,type) VALUES ('".$_POST["Domain"]."','".$_POST["Type"]."')");
$db->exec("DELETE FROM mod_url_deny WHERE id = ". $_POST["id"]);
shell_exec("sudo python  ../tool/core_waf/delete_rule_url.py 1 ".$_POST["id"]." 2>&1");

               
$newURL = HOST;
header('Location: '.$newURL."firewall_module.php"); 

?>