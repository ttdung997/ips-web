<?php
$db = new SQLite3('../data/noti.sqlite');
$db->exec("INSERT INTO noti(uptime,content,nottype) VALUES ('".date("Y/m/d h:i:s")."','Đã cập nhật ứng dụng ".$_POST["app"]."',1)");
 // print_r("INSERT INTO noti(uptime,content,nottype) VALUES ('".date("Y/m/d h:i:s")."','Đã cập nhật ứng dụng ".$_POST["app"]."',1)");
shell_exec("sudo apt install ".$_POST["app"]." -y");
print_r("Đã cập nhật ứng dụng ")
?>