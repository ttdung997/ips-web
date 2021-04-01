<?php
include 'config.php';
setcookie("token","", time() + (3600), "/");

// print($_COOKIE["token"]);
$newURL = HOST."login.php";
header('Location: '.$newURL);
