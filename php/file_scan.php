<?php



 
function iterateDirectory($i)
{	
		$db = new SQLite3('../data/check.sqlite');
    foreach ($i as $path) {
        if ($path->isDir())
        {
            iterateDirectory($path);
        }
        else
        {
        $row = shell_exec('stat  -c "%y|| %s|| %n|||" "'.$path.'"');
        $time = substr(explode("||",$row)[0],0,19);
		$large = intval(explode("||",$row)[1])/1024;
		$name = trim(explode("||",$row)[2]);
		

		$res = $db->querySingle('SELECT count(name) FROM check_file where name = "'.$name.'"');

		if($res > 0){
			continue;
		}


	    // print('python ../tool/o-checker/o-checker.py "'.$path.'"');
		$output = shell_exec('sudo clamdscan "'.$path.'"');
		// print_r($output."<br>");

		if(strpos($output,"FOUND") == false) {
			$db = new SQLite3('../data/noti.sqlite');
$db->exec("INSERT INTO noti(uptime,content,nottype) VALUES ('".date("Y/m/d h:i:s")."','Tệp ".$path." Đã bị nhiễm mã độc',2)");
			$check =0;
		}else{
			$check = 1;
		// }
		$db = new SQLite3('../data/check.sqlite');
		// print("INSERT INTO check_file(name,large_file,date_check,check_value) VALUES ('".$path."','".intval($large)."','".$time."','".$check."')");
		$db->exec("INSERT INTO check_file(name,large_file,date_check,check_value) VALUES ('".$path."','".intval($large)."','".date("Y/m/d h:i:s")."','".$check."')");
		// dd();
	        }
	    }
	}
}


include 'config.php';

$files = scandir($_POST["folder"],1);
 if ($files !== false)
        {
$iterator = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($_POST["folder"]));
iterateDirectory($iterator);
}else{
		$db = new SQLite3('../data/check.sqlite');
	$path = $_POST["folder"];
        $row = shell_exec('stat  -c "%y|| %s|| %n|||" "'.$path.'"');
        // print("***************<br>");
        // print('stat  -c "%y|| %s|| %n||| "'.$path);
        // print($row);
        // print("***************<br>");
        $time = substr(explode("||",$row)[0],0,19);
		$large = floatval(explode("||",$row)[1])/1024.0;
		$name = trim(explode("||",$row)[2]);
		

		$res = $db->querySingle('SELECT count(name) FROM check_file where name = "'.$name.'"');
		// print("it on");
		// print_r($res);
		if($res <=  0){
			// print_r("it in");

	    // print('python ../tool/o-checker/o-checker.py "'.$path.'"');
		// $output = shell_exec('sudo python ../tool/o-checker/o-checker.py "'.$path.'"');
			$output = shell_exec('sudo clamdscan "'.$path.'"');
		print_r($output."<br>");

		if(strpos($output,"FOUND") !== false) {
			$check =0;
			$db = new SQLite3('../data/noti.sqlite');
$db->exec("INSERT INTO noti(uptime,content,nottype) VALUES ('".date("Y/m/d h:i:s")."','Tệp ".$path." Đã bị nhiễm mã độc',2)");
		}else{
			$check = 1;
		}
		

		$db = new SQLite3('../data/check.sqlite');
		print("INSERT INTO check_file(name,large_file,date_check,check_value) VALUES ('".$path."','".round(floatval($large),2)."','".date("Y/m/d h:i:s")."','".$check."')");
		$db->exec("INSERT INTO check_file(name,large_file,date_check,check_value) VALUES ('".$path."','".round(floatval($large),2)."','".date("Y/m/d h:i:s")."','".$check."')");
		// dd();
		
		}

}

?>

