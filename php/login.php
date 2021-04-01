<?php
 
include 'config.php';

$myFile = "pass.txt";
$myFileLink = fopen($myFile, 'r');
$myFileContents = fread($myFileLink, filesize($myFile));
fclose($myFileLink);

if(!empty($_COOKIE["token123"])) {
	print("Login Successfuly");
	 $newURL = HOST;
	 header('Location: '.$newURL);
} else {
	print($_POST["password"]."<br>");
	print(sha1($_POST["password"]."AlleNN996g"));
	echo "<br>";
	print($myFileContents);

	// hash Char: AlleNN996g
	// $myFile = "pass.txt";
	// $myFileLink = fopen($myFile, 'w+') or die("Can't open file.");
	// fwrite($myFileLink, sha1($_POST["password"]."AlleNN996g"));
	// fclose($myFileLink);

	// echo $myFileContents;

	if(sha1($_POST["password"]."AlleNN996g") == $myFileContents && $_POST["username"]=="admin"){
		print("Login Successfuly");
		setcookie("token",sha1($_POST["password"]."AlleNN996g"), time() + (3600), "/");
	}else{
		print("Login false");
	}
		$newURL = HOST;
		header('Location: '.$newURL);
	// echo "Cookies Not Set";
  
}
?>
 