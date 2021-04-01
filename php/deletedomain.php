<?php
 
include 'config.php';
  $db = new SQLite3('../tool/dga/data.db');
  print_r($_POST["id"]);
  
$rule_encode = base64_encode($_POST["rule"]);               
  $db->exec('DELETE FROM bkcs_custom_domain where id = '.$_POST["id"]);
               
$newURL = HOST;
header('Location: '.$newURL."dga_custom.php"); 
?>
 