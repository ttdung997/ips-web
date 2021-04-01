<?php
// print("!@3123");
$dir    = '../data/history/';
$files = scandir($dir,1);

$jsonfile = [];
foreach ($files as $file) {
	if(strlen($file) > 3){
		$jsonfile[] = $file;
	}
}

print(json_encode($jsonfile));

?>