<?php

    $db = new SQLite3('../data/check.sqlite');
 $res = $db->query('select DISTINCT * from check_file where check_value = 0 ORDER BY name');
 while ($row = $res->fetchArray()) {
 	$db->query('delete from check_file where name = "'.$row['name'].'"');
 	shell_exec("sudo rm ".$row['name']);
 }
?>