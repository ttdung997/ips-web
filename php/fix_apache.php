<?php
   $output = shell_exec("sudo python ../tool/core_waf/check_security/check_secure_server.py fix");
   print_r($output); 
?>