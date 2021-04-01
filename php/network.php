<?php
    $net = shell_exec("python3 ../tool/netmoniter.py");
    $net = explode("|||", $net);
    // $net = array_pop($net);
    // print_r($net);
    foreach ($net as $net) {
    $data[explode("||", $net)[1]]['in']= explode("||", $net)[2];
    $data[explode("||", $net)[1]]['out']= explode("||", $net)[3];
    }

$data = json_encode($data);

echo($data);

?>