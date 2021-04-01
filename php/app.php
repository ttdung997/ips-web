<?php

        $output = shell_exec('sudo apt list --upgradeable');
        $output = explode( "\n", $output);
        // print_r($output); 
   
        $i = 0;
        foreach ($output as $key => $line) {
                if($i == 0){
                    $i = 1;
                    continue;
                }
                $line = explode( " ", $line);
                $app_name = explode( "/", $line[0])[0] . " (".$line[2].")";
                $cur_version = substr($line[5], 0, -1);
                $new_version = $line[1];
                print_r($app_name."<br>");
                print_r($cur_version."<br>");
                print_r($new_version."<br>");
              }     

?>