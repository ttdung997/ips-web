<?php
// print("!@3123");
$dir    = $_POST['path'];
$files = scandir($dir,1);
$key = 0;

$fileArr = [];
$folderArr =[];


$typeFile = [];
$typeFolder = [];

if($files !== false){
	foreach ($files as $file) {
		if ($dir == "/"){
			$check = scandir($_POST['path'].$file,1);
		}else{
			$check = scandir($_POST['path']."/".$file,1);

		}
	if($check == false){
		$fileArr[]=$file;
		$typeFile[] = 0;
	}else{
		$folderArr[]=$file;
 		$typeFolder[] = 1;
	}
} 
}
print(json_encode([array_merge(array_reverse($folderArr),array_reverse($fileArr)),array_merge($typeFolder,$typeFile)]));

?>