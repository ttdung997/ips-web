<?php

include 'config.php';
  $output = json_decode(shell_exec("sudo python ../tool/core_waf/check_security/check_secure_server.py check"));
  // print("123123");
  // print_r($output);
$url= ips_manager; 

$ch = curl_init();
curl_setopt($ch, CURLOPT_HEADER, 0);
curl_setopt($ch, CURLOPT_VERBOSE, 0);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_POST, true);
$postData = array(
    "time" => date("M,d,Y h:i:s A"),
    'name' => "DungPC",
    'type' => "Quét lỗ hổng phần mềm cung cấp dịch vụ công",
    'content' => "Số lỗ hổng: ".count($output)
);
curl_setopt($ch, CURLOPT_POSTFIELDS, $postData);
$response = curl_exec($ch);

// echo $response;
// die();

            $a = array('0');
            $b = array('0');
            for ($x = 0; $x < count($output); $x++){
                if ($output[$x][0] != 0){
                    array_push($a, $output[$x][0]);
                    array_push($b, $output[$x]);
                }
            }
            
            // array_sort($b, 0, SORT_DESC);
            // sort($a);
            unset($a[0]);
            unset($b[0]);
            // $error = DB::table('information')->whereIn('id', $a)->get();

            // print_r($b);
            $db = new SQLite3('../data/check.sqlite');

            $res = $db->query('SELECT * FROM mod_information');
            // // return json_encode($b);
            // for ($i = 0; $i < count($error); $i++){
            //     $error[$i]->l_error = $b[$i + 1];
            // }
            $warn = [];
            foreach ($b as $b) {
                $warn[$b[0]] = $b[1]; 
            }
            // print_r($warn);
            $count = 0;
            $error = [];
            while($row = $res->fetchArray()){
                $count = $count + 1;
                if(in_array($count,$a)){
                    // print_r($row);
                    // print_r("<br>");

                    $row["l_error"] = $warn[$count];
                    $error[] = $row;
                }
            }            
            // print("<br>");
            // print_r($error);

$db = new SQLite3('../data/noti.sqlite');
$db->exec("INSERT INTO noti(uptime,content,nottype) VALUES ('".date("Y/m/d h:i:s")."','Đã thực hiện quét lỗ hổng phần mềm web',1)");

            $fp = fopen('../data/history/'.date("M,d,Y h:i:s A").'-web.json', 'w');
            fwrite($fp, json_encode($error));
            fclose($fp);
            print_r(json_encode($error));
            // return json_encode($error);
// $jsondata = file_get_contents('../data/history/results.json');
// print($jsondata);

?>