<?php

$jsondata = file_get_contents('/opt/API/integrity.txt');
print($jsondata);


$fp = fopen('/opt/API/integrity.txt', 'w');
fwrite($fp, "");
fclose($fp);

$apache = shell_exec("/var/log/apache2/error.log");

$myFile = "../data/apache_token.txt";
$myFileLink = fopen($myFile, 'r');
$myFileContents = fread($myFileLink, filesize($myFile));
fclose($myFileLink);

if(sha1($apache) != $myFileContents){
    $_SESSION['logtab']=4;
    $apache_flag = 1;
    $myFile = "../data/apache_token.txt";
    $db = new SQLite3('../data/noti.sqlite');
	$db->exec("INSERT INTO noti(uptime,content,nottype) VALUES ('".date("Y/m/d h:i:s")."','Phát hiện tấn công ứng dụng web',0)");

    $myFileLink = fopen($myFile, 'w+') or die("Can't open file.");
    fwrite($myFileLink, sha1($waf));
    fclose($myFileLink);
}

$apache = shell_exec("sudo tac  /var/log/syslog | awk -F".'" "'." '{ printf(".'"%-50s<br>\n"'.", $0); }' |grep bkcs-");

$myFile = "../data/iptoken.txt";
$myFileLink = fopen($myFile, 'r');
$myFileContents = fread($myFileLink, filesize($myFile));
fclose($myFileLink);

	// print_r("it heresa");
	// print($myFileContents."<br>");
	// print_r(sha1($apache));
if(sha1($apache) != $myFileContents){
	// print_r("it heresa");
    $_SESSION['logtab']=4;
    $apache_flag = 1;
    $myFile = "../data/iptoken.txt";
    $db = new SQLite3('../data/noti.sqlite');
	$db->exec("INSERT INTO noti(uptime,content,nottype) VALUES ('".date("Y/m/d h:i:s")."','Phát hiện vi phạm tường lửa truy cập',4)");
	// print_r("INSERT INTO noti(uptime,content,nottype) VALUES ('".date("Y/m/d h:i:s")."','Phát hiện vi phạm tường lửa truy cập',4)");

    // $myFileLink = fopen($myFile, 'w+') or die("Can't open file.");
    // fwrite($myFileLink, sha1($waf));
    // fclose($myFileLink);
}


shell_exec("sudo python3 ../script/file_system_protection/demo_monitor.py -s_a");

shell_exec("sudo python3 ../script/file_system_protection/demo_integrity.py -s_a");

?>