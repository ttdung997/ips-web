<?php


 // $url= "http://localhost/test/test.php"; 

// $ch = curl_init();
// curl_setopt($ch, CURLOPT_HEADER, 0);
// curl_setopt($ch, CURLOPT_VERBOSE, 0);
// curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
// curl_setopt($ch, CURLOPT_URL, $url);
// curl_setopt($ch, CURLOPT_POST, true);
// curl_setopt($ch, CURLOPT_POSTFIELDS, $postData);
// $response = curl_exec($ch);




 $url= "http://dascam.com.vn:8000/checkservice";
$postData = array(
    "time" => date("M,d,Y h:i:s A"),
    'name' => "DungPC",
    'type' => "Quét lỗ hổng cơ sở dữ liệu máy chủ dịch vụ",
    'content' => "Số lỗ hổng: ".count($output)
);               
$data_string = json_encode($postData);                                                                                   
                                                                                                                     
$ch = curl_init($url);                                                                      
curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");                                                                     
curl_setopt($ch, CURLOPT_POSTFIELDS, $data_string);                                                                  
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);                                                                      
curl_setopt($ch, CURLOPT_HTTPHEADER, array(                                                                          
    'Content-Type: application/json',                                                                                
    'Content-Length: ' . strlen($data_string))                                                                       
);                                                                                                                   
                                                                                                                     
$result = curl_exec($ch);

echo $response;

// 4.- dump result
echo $result;
die();