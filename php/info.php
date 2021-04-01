<?php

        $output = shell_exec('bash ../script/infomation.sh');
                                               
        $output = explode( '|||', $output);
        // print_r($output[3]);
        $data['time'] = explode( 'up', $output['0'])[0];
        $data['uptime'] = explode( 'up', $output['0'])[1];
        $data['uptime'] = explode( ',', $data['uptime'])[0];

        $data['process'] = $output[4];

        $cpuContent = str_replace(',','.',$output[3]);
        $cpuContent = explode( '???', ($cpuContent));

        // print((float)explode( ':', $cpuContent[0])[1]);
        // print("<br>");
        // print((float)explode( ':', $cpuContent[1])[1]);
        $cpuPercent = (float)explode( ':', $cpuContent[0])[1]*100/(float)explode( ':', $cpuContent[1])[1];


        $data['cpuPercent'] = round((float)$cpuPercent,2);
       

        $data['ramTotal'] = explode( '||', explode( ':', $output[1])[0])[0];
        
        $data['ramUsed'] =  explode('||', explode( ':', $output[1])[0])[1];
      
        $data['swapTotal'] = explode( '||', explode( ':', $output[2])[0])[0];
        $data['swapUsed'] = explode( '||', explode( ':', $output[2])[0])[1];

       $status = $data;
        // print_r($data);


$data = json_encode($data);

echo($data);
?>