<?php
$data = ($_POST['id']);
	$checked = false;
                // $data = Request::get('id');
                $array = array(50, 28, 25, 10, 1, 7, 36);
                for ($x = 0; $x < count($array); $x++){
                    if (in_array($array[$x], $data)){
                        $checked = true;
                        break;
                    }
                }
            
            $db = new SQLite3('../data/check.sqlite');

            $res = $db->query('SELECT * FROM mod_information');

            $warn = [];

            $error = [];
            while($row = $res->fetchArray()){
            	// print_r($row['id']);
            	if (in_array($row['id'],$data)){
                        $checked = true;
                        print_r($row['id']."<br>");
                        $OUT = shell_exec("runp ../tool/core_waf/check_security_fix/".$row["group_c"]."/".$row["name_c"].".py fix_o");
                    }

            }            

                // for ($i = 0; $i < count($info); $i++){
                //     $OUT = shell_exec($zbx."[runp,".URL."/core_waf/check_security/".$info[$i]->group_c."/".$info[$i]->name_c.".py,fix_o]");
                // }
                if ($checked){
                    shell_exec("sudo service apache2 restart]");
                }
                return 1;

?>