<?php
// print_r($_POST);
$sel = str_replace("/","-",$_POST["sel"]);

$output = shell_exec('echo "" > /var/www/html/waf/data/clam/final.log');
$output = shell_exec("sudo clamscan ".$_POST["sel"]." --log /var/www/html/waf/data/clam/final.log");
$output = shell_exec("sudo cp /var/www/html/waf/data/clam/final.log  /var/www/html/waf/data/clam/".date("M,d,Y").".".$sel.".log");
// print_r("/var/www/html/waf/data/clam/".date("M,d,Y").".".$_POST["sel"].".log");
$res =   shell_exec("sudo cat ../data/clam/final.log"."| awk -F".'" "'." '{ printf(".'"%-25s<br>"'.", $0); }'");
echo $res;
?>