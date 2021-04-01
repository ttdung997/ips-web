<?php

$db = new SQLite3('../data/noti.sqlite');
$db->exec("INSERT INTO noti(uptime,content,nottype) VALUES ('".date("Y/m/d h:i:s")."','Đã xóa ứng dụng '"..$_POST["app"]..",2)");


shell_exec("sudo apt remove ".$_POST["app"]." -y");
print_r("Đã xóa ứng dụng ")
?>