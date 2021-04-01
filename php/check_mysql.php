<?php
  // print("123123");
include 'config.php';
  $output = json_decode(shell_exec("sudo python ../tool/core_waf/check_security_mysql/check_secure_server.py check"));
  
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
    'type' => "Quét lỗ hổng cơ sở dữ liệu máy chủ dịch vụ",
    'content' => "Số lỗ hổng: ".count($output)
);
curl_setopt($ch, CURLOPT_POSTFIELDS, $postData);
$response = curl_exec($ch);

// echo $response;
// die();
  // print_r($output);
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
            $db = new SQLite3('../data/info.sqlite');

            $res = $db->query('SELECT * FROM information where type ="MySQL 5.7 Community Linux"');
            // // return json_encode($b);
            // for ($i = 0; $i < count($error); $i++){
            //     $error[$i]->l_error = $b[$i + 1];
            // }
            $warn = [];
            foreach ($b as $b) {
                $warn[$b[0]] = $b[1]; 
            }
            // print_r($warn);
            // $count = 0;
            $error = [];
            // print_r($a);
            while($row = $res->fetchArray()){
                // $count = $count + 1;
                if(in_array($row[0],$a)){
                    $row["l_error"] = $warn[$row[0]];
                    $error[] = $row;
                }
                // if(isset($warn[$count])){
                //         $row["l_error"] = $warn[$count];
                //     }else{
                //          $row["l_error"] = "";
                //     }
                //     $error[] = $row;
            }            
            // print("<br>");
            // print_r($error);
            // print_r(json_encode($error));$db = new SQLite3('../data/noti.sqlite');
$db->exec("INSERT INTO noti(uptime,content,nottype) VALUES ('".date("Y/m/d h:i:s")."','Đã thực hiện quét lỗ hổng cơ sở dữ liệu',1)");
            $fp = fopen('../data/history/'.date("M,d,Y h:i:s A").'-mysql.json', 'w');
            fwrite($fp, json_encode($error));
            fclose($fp);
            print_r(json_encode($error));
            return json_encode($error);

            // return json_encode($error);

?>