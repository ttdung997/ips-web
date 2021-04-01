<?php
include 'config.php';
        $filename = '../data/hardware.json';
       
            $output = shell_exec('sudo bash ../script/hardware.sh');
            // print($output);
             while(strpos($output,'||||') > 0){
                $output = str_replace('||||', '|||', $output);
            }

            $output = (explode( '|||', $output));
            print_r($output[0]);
            if(strpos("abc ".$output[0],'Windows') > 0){
                $data = [];
                $data[] = array(array('Operating system'),1);
                $data[] = array(array($output[0]),0);
                $row =0;
                $tem = 0;
                foreach ($output as $line) {
                    if ($row >0){
                        while(strpos($line,'  ') > 0){
                            $line = str_replace('  ', ' ', $line);
                        } 
                        if(strpos($line,'*****') > 0){
                            $flag = 1;
                            $line = str_replace('*****', '', $line);
                        }else
                            $flag = 0;
                        
                        $word_list = explode("||",$line);
                        if($flag == 1){
                            $tem = count($word_list);
                        }
                        if($tem == count($word_list)){
                            $data[] = array($word_list,$flag);
                        }
                    }
                    $row = $row +1;
                }
            }
            else{
                $data = [];
                $result = array_reverse(array_map('strrev', explode(" ", strrev($output[0]),3)));
                
                $os = ['','','system',$result[0]];
                $data[] = $os;
                $row =0;
                foreach ($output as $line) {
                    if ($row >2){
                        while(strpos($line,'  ') > 0){
                            $line = str_replace('  ', ' ', $line);
                        }
                        $word_list = explode(" ",$line,4);
                        $i = 0;
                        foreach ($word_list as $word) {
                            if(isset($word[0])){
                                if(isset($word[1])){
                                    if(ctype_upper($word[1])){
                                        break;
                                    }
                                }
                                if(ctype_upper($word[0]) or is_numeric($word[0])){
                                    break;
                                }
                            }

                            $i = $i + 1;

                        }
                        $word_list = explode(" ",$line,$i+1);
                        if ($i < 1){
                            $line =$word_list;
                        }
                        else if ($i < 2){
                            $line = ['','',$word_list[0],''];
                        }else if ($i < 3){
                            $line = [$word_list[0],'',$word_list[1],$word_list[2]];
                        }else{
                            $line =$word_list;
                        }
                        $data[] = $line;
                    }
                    $row = $row + 1;
                }
            }
            
        file_put_contents($filename,json_encode($data));
        $newURL = HOST;
        header('Location: '.$newURL);

?>