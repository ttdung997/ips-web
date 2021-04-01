<?php
// print("!@3123");
$dir    = $_POST['path'];
// print($dir);
$password  = $_POST['pass'];
$files = scandir($dir,1);
$key = 0;

// print_r($files);
if ($files == false){
	$encrype = shell_exec("sudo python3 ../script/file_system_protection/demo_crypto.py -d -f ".'"'.$dir.'" '.'"'.$password.'" 2');
	// print_r($encrype);
	if(strpos($encrype,"Done")>0){
				$check =1;
		}
}else{
	foreach ($files as $file) {
		if($file != ".." or $file !="."){	
			// print($dir."/".$file);
			$encrype = shell_exec("sudo python3 ../script/file_system_protection/demo_crypto.py -d -d ".'"'.$dir.'"'.' "'.$password.'" 2');
		// print_r($encrype);
			if(strpos($encrype,"Done")>0){
				$check =1;
		}

		}
	}
}
  // cmd = "python3 script/file_system_protection/demo.py -f -p 3 -d " "'"+path+"'" + " '"+password+"'"
              
                // encrype
  // cmd = "python3 script/file_system_protection/demo.py -f -e " "'"+path+"'" + " '"+password+"'"
                

print(json_encode([$check,$files]));


?>