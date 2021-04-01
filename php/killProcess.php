<?php
shell_exec("sudo kill -9 ".$_POST["id"]);
print_r("Đã xóa tiến trình")
?>