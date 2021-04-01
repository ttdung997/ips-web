<?php
$data = file_get_contents('../manual_service.json');
$json_arr = json_decode($data, true);
$arr_index = [];
foreach ($json_arr as $key => $value) {
    if ($value['port'] == $_POST['port']) {
        $arr_index = $key;
    }
}
// echo $arr_index;
unset($json_arr[$arr_index]);

$json_arr = array_values($json_arr);
file_put_contents('../manual_service.json', json_encode($json_arr));
