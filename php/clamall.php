
<?php

$output = shell_exec('echo "" > /var/www/html/waf/data/clam/final.log');

$output = shell_exec("clamscan /home/ --log /var/www/html/waf/data/clam/final.log");
$output = shell_exec("sudo cp /var/www/html/waf/data/clam/final.log /var/www/html/waf/data/clam/".date("M,d,Y").".log");
$res =   shell_exec("sudo cat ../data/clam/final.log"."| awk -F".'" "'." '{ printf(".'"%-25s<br>"'.", $0); }'");
echo $res;
?>