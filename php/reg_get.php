<?php
$list = shell_exec("sudo python3 ../script/file_system_protection/moniter/moniter_linux.py -a");
print_r($list);

?>