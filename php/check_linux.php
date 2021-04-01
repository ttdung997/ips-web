<?php
  // print("123123");
include 'config.php';
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
    'type' => "Quét lỗ hổng máy chủ dịch vụ",
    'content' => "Số lỗ hổng: ".count($output)
);
curl_setopt($ch, CURLOPT_POSTFIELDS, $postData);
$response = curl_exec($ch);

// echo $response;
// die();
            // print_r($b);
            $db = new SQLite3('../data/linux.sqlite');

            $res = $db->query('SELECT * FROM info');
            // // return json_encode($b);
            // for ($i = 0; $i < count($error); $i++){
            //     $error[$i]->l_error = $b[$i + 1];
            // }
            $warn = [];
            // foreach ($b as $b) {
            //     $warn[$b[0]] = $b[1]; 
            // }
            // print_r($warn);
            // $count = 0;
            $error = [];
            // print_r($a);
            while($row = $res->fetchArray()){
                // $count = $count + 1;
                // if(in_array($row[0],$a)){
                $row["l_error"]="[WARNING] Linux Secure are not strong enough";
                    // $row["l_error"] = $warn[$row[0]];
                    $error[] = $row;
                // }
            }            
            // print("<br>");
            // print_r($error);
            // print_r(json_encode($error));
            $db = new SQLite3('../data/noti.sqlite');
$db->exec("INSERT INTO noti(uptime,content,nottype) VALUES ('".date("Y/m/d h:i:s")."','Đã thực hiện quét lỗ hổng phần mềm hệ điều hành ',1)");
            $fp = fopen('../data/history/'.date("M,d,Y h:i:s A").'-os.json', 'w');
            fwrite($fp, json_encode($error));
            fclose($fp);
            print_r(json_encode($error));
            // return json_encode($error);

            // return json_encode($error);

?>