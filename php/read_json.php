<?php
// print("123123123");
$jsondata = file_get_contents('../data/history/'.$_POST["path"]);
print($jsondata);
?>