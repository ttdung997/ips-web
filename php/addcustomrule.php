<?php
 
include 'config.php';
  $db = new SQLite3('../data/check.sqlite');
  // print("INSERT INTO bkcs_custom_domain(domain,type) VALUES ('".$_POST["Domain"]."','".$_POST["Type"]."')");
  $content = str_replace('"','&bdquo;',$_POST["description"]);
  $content = str_replace("'",'&sbquo;;',$_POST["description"]);
  $db->exec("INSERT INTO mod_custom_rule(rule,description) VALUES ('".$_POST["rule"]."','".$content."')");
$rule_encode = base64_encode($content);               
$rows = $db->query("SELECT COUNT(*) as count FROM mod_ip_deny");
$row = $rows->fetchArray();
$numRows = $row['count'];
print("sudo python ../tool/core_waf/add_rule_custom.py 1 ".$rule_encode." 2>&1");
print(shell_exec("sudo python ../tool/core_waf/add_rule_custom.py 1 ".$rule_encode." 2>&1"));
// print(1);

// $newURL = HOST;
// header('Location: '.$newURL."firewall_module.php");

?>
 