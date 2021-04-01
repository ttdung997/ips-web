<?php

include 'include/header.php';

?>
<div class="content-wrapper">
    <!-- Content Header (Page header) -->
    <section class="content-header">
        <div class="container-fluid-header">
            <div class="row mb-2">
                <div class="col-sm-6">
                    <h1>Cấu hình tường lửa kiểm soát truy cập</h1>
                </div>
                <div class="col-sm-6">
                    <ol class="breadcrumb float-sm-right">
                        <li class="breadcrumb-item"><a href="/"><i class="fa fa-home" aria-hidden="true"></i> Trang chủ</a></li>
                        <li class="breadcrumb-item active">Cấu hình tường lửa kiểm soát truy cập</li>
                    </ol>
                </div>
            </div>
        </div>
        <!-- /.container-fluid -->
    </section>

    <!-- Main content -->
    <section class="content">
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <!-- /.card-header -->
                    <div class="card-body">
                        <?php
                        if (isset($_SESSION['notification'])) {
                        ?>
                            <center>
                                <div class="alert alert-success">
                                    <?= $_SESSION['notification'] ?>
                                    <br>
                                </div>
                            </center>
                        <?php
                        }
                        session_destroy();
                        session_start();

                        ?>
                        <div class="container">

                            <ul class="nav nav-tabs" id="example-tabs" role="tablist">
                                <li class="nav-item margin_center">
                                    <a id="tab1" class="nav-link active color-a" data-toggle="tab" role="tab" href="#home">Thêm luật </a>
                                </li>

                                <li class="nav-item margin_center">
                                    <a id="tab2" class="nav-link color-a" data-toggle="tab" role="tab" href="#menu2">Danh sách luật</a>
                                </li>
                                <li class="nav-item margin_center">
                                    <a id="tab3" class="nav-link color-a" data-toggle="tab" role="tab" href="#menu3">Profile</a>
                                </li>
                            </ul>
                            <br>
                            <div class="tab-content">
                                <?php
                                $NetworkArray = shell_exec("ip link show | cut -d: -f2,2" . "| awk -F" . '" "' . " '{ printf(" . '"%-5s|||"' . ", $0); }'");
                                $NetworkArray = (explode('|||', $NetworkArray));

                                $data = [];
                                $row = 0;
                                $i = 0;
                                foreach ($NetworkArray as $nw) {
                                    $i = $i + 1;
                                    if ($i % 2 == 0) {
                                        continue;
                                    }
                                    $nw = str_replace(' ', '', $nw);
                                    $data[] = $nw;
                                }

                                ?>

                                <div id="home" class="tab-pane in active show">
                                    <ul class="nav nav-tabs" id="example-tabs" role="tablist">
                                        <li class="nav-item margin_center">
                                            <a id="tab1" class="nav-link active color-a" data-toggle="tab" role="tab" href="#add1">Lưu lượng vào </a>
                                        </li>

                                        <li class="nav-item margin_center">
                                            <a id="tab2" class="nav-link color-a" data-toggle="tab" role="tab" href="#add2">Lưu lượng ra</a>
                                        </li>


                                    </ul>
                                    <br><br>

                                    <div class="tab-content">

                                        <div id="add1" class="tab-pane fade active show">
                                            <?php
                                            $jsondata1 = file_get_contents('input.json');
                                            $arr_data1 = json_decode($jsondata1, true)['flag'];
                                            ?>
                                            <?php
                                            // print_r($arr_data)
                                            if ($arr_data1 == 0) {
                                                echo '<button type="button" id="0"  onclick="convert1(0)" class="btn btn-secondary">Chuyển sang Whitelist</button>';
                                            } else {
                                                echo '<button type="button" id="1"  onclick="convert1(1)" class="btn btn-secondary">Chuyển sang Blacklist</button>';
                                            }
                                            ?>

                                            <?php
                                            if ($arr_data1 == 0) {
                                                echo '<form id="input" action="php/firewall_input.php" method="POST">';
                                            } else {
                                                echo '<form id="input" action="php/firewall_whitelist_input.php" method="POST">';
                                            }
                                            ?>

                                            <input type="hidden" name="form" value="1">
                                            <div class="form-group">

                                                <table>
                                                    <tbody>
                                                        <tr>
                                                            <td><label><i class="fa fa-ticket"></i> &nbsp;Card mạng</label></td>
                                                            <td><select class="form-control Disable" name="network" id="input_protocol" style="width: 300px;">
                                                                    <option value=>Tất cả</option>
                                                                    <?php

                                                                    foreach ($data as $nw) {
                                                                        if ($nw != "lo")
                                                                            echo '<option value="' . $nw . '">' . $nw . '</option>';
                                                                    }
                                                                    ?>
                                                                </select></td>
                                                        </tr>
                                                        <tr>
                                                            <td><label><i class="fa fa-ticket"></i> &nbsp;Giao thức</label></td>
                                                            <td><select class="form-control Disable" name="Protocol" id="input_protocol">
                                                                    <option value="tcp">TCP</option>
                                                                    <option value="udp">UDP</option>
                                                                    <option value="icmp">ICMP</option>
                                                                    <option value="">ANY</option>
                                                                </select>
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <td><label>Thông tin luật (
                                                                    <label style="color: red;">*</label>)</label></td>
                                                            <td></td>
                                                        </tr>
                                                        <tr>
                                                            <td><label style="width: 120px" for="input_IP1">Địa chỉ IP nguồn:</label></td>
                                                            <td><input placeholder="Nhập địa chỉ (VD: 192.168.2.22)" value="<?= $_SESSION['val']['ip1'] ?>" type="text" class="form-control" id="input_ip1" name="ip1"></td>
                                                        </tr>
                                                        <tr>
                                                            <td><label style="width: 170px" for="pwd">Cổng dịch vụ nguồn:</label></td>
                                                            <td><input placeholder="Nhập cổng (VD: 80,80:88)" value="<?= $_SESSION['val']['port1'] ?>" type="text" class="form-control" id="input_port1" name="port1"></td>
                                                        </tr>
                                                        <tr>
                                                            <td><label style="width: 120px" for="input_IP1">Địa chỉ IP đích:</label></td>
                                                            <td><input placeholder="Nhập địa chỉ (VD: 192.168.2.22)" value="<?= $_SESSION['val']['ip2'] ?>" type="text" class="form-control" id="input_ip2" name="ip2"></td>
                                                        </tr>
                                                        <tr>
                                                            <td><label style="width: 170px" for="pwd">Cổng dịch vụ đích:</label></td>
                                                            <td><input placeholder="Nhập cổng (VD: 80,80:88)" value="<?= $_SESSION['val']['port2'] ?>" type="text" class="form-control" id="input_port2" name="port2"></td>
                                                        </tr>
                                                        <tr>
                                                            <td></td>
                                                            <td></td>
                                                        </tr>
                                                        <tr>
                                                            <td><label><i class="fa fa-ticket"></i>&nbsp; Hành vi thực hiện</label></td>
                                                            <td><select class="form-control Disable" name="action" id="input_action">
                                                                    <option value="DROP">DROP</option>
                                                                    <option value="ACCEPT">ACCEPT</option>
                                                                    <option value="DENY">DENY</option>
                                                                </select></td>
                                                        </tr>
                                                        <tr>
                                                            <td>
                                                                <label style="width: 70px" for="input_IP1">Log</label>
                                                                <input type="checkbox" class="form-check-input" id="checklog1" onclick="checklog()" style="margin-top: 7px;">
                                                                <label style="margin-left: 15px;" for="input_IP1">Prefix</label>
                                                            </td>
                                                            <td><input id="prefix1" value="<?= $_SESSION['val']['[prefix'] ?>" type="text" disabled class="form-control" id="input_prefix" name="prefix"></td>
                                                        </tr>
                                                    </tbody>
                                                </table>

                                                <p style="color: red">
                                                    <?= $_SESSION['ip1Error'] ?>
                                                </p>
                                                <p style="color: red">
                                                    <?= $_SESSION['port1Error'] ?>
                                                </p>

                                                <p style="color: red">
                                                    <?= $_SESSION['ip2Error'] ?>
                                                </p>
                                                <p style="color: red">
                                                    <?= $_SESSION['port2Error'] ?>
                                                </p>
                                                <div class="form-inline">
                                                    <div class="form-group">
                                                        <label style="width: 120px" for="input_IP1"></label>
                                                        <label style="width: 300px" for="input_IP1"></label>
                                                    </div>
                                                    <!-- <div class="form-group">
                                          <label style="width: 120px" for="pwd">Cổng :</label>
                                          <input type="text" style="width: 340px" class="form-control" id="input_port" placeholder="port" name="port">
                                        </div> -->
                                                    <p style="color: red">
                                                        <?= $_SESSION['portError'] ?>
                                                    </p>
                                                </div>
                                            </div>
                                            <p style="color: red">
                                                <?= $_SESSION['prefixError'] ?>
                                            </p>
                                            <button type="submit" class="btn btn-add Disable"><i class="fa fa-plus" aria-hidden="true"></i> Thêm luật</button>

                                            </form>

                                        </div>

                                        <div id="add2" class="tab-pane fade">
                                            <?php
                                            $jsondata2 = file_get_contents('output.json');
                                            $arr_data2 = json_decode($jsondata2, true)['flag'];
                                            ?>
                                            <?php
                                            // print_r($arr_data)
                                            if ($arr_data2 == 0) {
                                                echo '<button type="button" id="0"  onclick="convert2(0)" class="btn btn-secondary">Chuyển sang Whitelist</button>';
                                            } else {
                                                echo '<button type="button" id="1"  onclick="convert2(1)" class="btn btn-secondary">Chuyển sang Blacklist</button>';
                                            }
                                            ?>

                                            <?php
                                            if ($arr_data2 == 0) {
                                                echo '<form id="input" action="php/firewall_output.php" method="POST">';
                                            } else {
                                                echo '<form id="input" action="php/firewall_whitelist_output.php" method="POST">';
                                            }
                                            ?>
                                            <input type="hidden" name="form" value="2">
                                            <div class="form-group">
                                                <table>
                                                    <tbody>
                                                        <tr>
                                                            <td><label><i class="fa fa-ticket"></i>&nbsp; Card mạng
                                                                </label></td>
                                                            <td><select class="form-control Disable" name="network" id="input_protocol" style="width: 300px;">
                                                                    <option value=>Tất cả</option>
                                                                    <?php
                                                                    foreach ($data as $nw) {
                                                                        echo '<option value="' . $nw . '">' . $nw . '</option>';
                                                                    }
                                                                    ?>
                                                                </select></td>
                                                        </tr>
                                                        <tr>
                                                            <td><label><i class="fa fa-ticket"></i>&nbsp; Giao thức</label></td>
                                                            <td><select class="form-control Disable" name="Protocol" id="input_protocol">
                                                                    <option value="tcp">TCP</option>
                                                                    <option value="udp">UDP</option>

                                                                    <option value="icmp">ICMP</option>
                                                                    <option value="">ANY</option>
                                                                </select></td>
                                                        </tr>
                                                        <tr>
                                                            <td><label>Thông tin luật (
                                                                    <label style="color: red;">*</label>)</label></td>
                                                            <td></td>
                                                        </tr>
                                                        <tr>
                                                            <td><label style="width: 120px" for="input_IP1">Địa chỉ IP nguồn:</label></td>
                                                            <td> <input value="<?= $_SESSION['val']['ip1'] ?>" type="text" class="form-control" id="input_ip1" name="ip1"></td>
                                                        </tr>
                                                        <tr>
                                                            <td><label style="width: 170px" for="pwd">Cổng dịch vụ nguồn:</label></td>
                                                            <td><input value="<?= $_SESSION['val']['port1'] ?>" type="text" class="form-control" id="input_port1" name="port1"></td>
                                                        </tr>
                                                        <tr>
                                                            <td><label style="width: 120px" for="input_IP1">Địa chỉ IP đích:</label></td>
                                                            <td><input value="<?= $_SESSION['val']['ip2'] ?>" type="text" class="form-control" id="input_ip2" name="ip2"></td>
                                                        </tr>
                                                        <tr>
                                                            <td><label style="width: 170px" for="pwd">Cổng dịch vụ đích:</label></td>
                                                            <td><input value="<?= $_SESSION['val']['port2'] ?>" type="text" class="form-control" id="input_port2" name="port2"></td>
                                                        </tr>
                                                        <tr>
                                                            <td></td>
                                                            <td></td>
                                                        </tr>
                                                        <tr>
                                                            <td><label><i class="fa fa-ticket"></i>&nbsp; Hành vi thực hiện</label></td>
                                                            <td><select class="form-control Disable" name="action" id="input_action">
                                                                    <option value="DROP">DROP</option>
                                                                    <option value="ACCEPT">ACCEPT</option>
                                                                    <option value="DENY">DENY</option>
                                                                </select></td>
                                                        </tr>
                                                        <tr>
                                                            <td>
                                                                <label style="width: 70px" for="input_IP1">Log</label>

                                                                <input type="checkbox" class="form-check-input" id="checklog2" onclick="checklog()" style="margin-top: 7px;">

                                                                <label style="margin-left: 15px;" for="input_IP1">Prefix</label>
                                                            </td>
                                                            <td>
                                                                <input id="prefix2" value="<?= $_SESSION['val']['[prefix'] ?>" type="text" disabled class="form-control" id="input_prefix" placeholder="prefix" name="prefix">
                                                            </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </div>

                                            <div class="row">
                                                <p style="color: red">
                                                    <?= $_SESSION['ip1Error'] ?>
                                                </p>
                                                <p style="color: red">
                                                    <?= $_SESSION['port1Error'] ?>
                                                </p>

                                                <p style="color: red">
                                                    <?= $_SESSION['ip2Error'] ?>
                                                </p>
                                                <p style="color: red">
                                                    <?= $_SESSION['port2Error'] ?>
                                                </p>
                                                <div class="form-inline">
                                                    <div class="form-group">
                                                        <label style="" for="input_IP1"></label>
                                                        <label style="" for="input_IP1"></label>
                                                    </div>
                                                    <!--   <div class="form-group">
                                          <label style="width: 120px" for="pwd">Cổng :</label>
                                          <input type="text" style="width: 340px" class="form-control" id="input_port" placeholder="port" name="port">
                                        </div> -->
                                                    <p style="color: red">
                                                        <?= $_SESSION['portError'] ?>
                                                    </p>
                                                </div>
                                            </div>

                                            <p style="color: red">
                                                <?= $_SESSION['prefixError'] ?>
                                            </p>
                                            <button id="addRule" type="submit" class="btn btn-add Disable"><i class="fa fa-plus" aria-hidden="true"></i> Thêm luật</button>
                                            </form>
                                        </div>
                                    </div>
                                </div>

                                <div id="menu2" class="tab-pane fade">
                                    <ul class="nav nav-tabs" id="example-tabs" role="tablist">
                                        <li class="nav-item margin_center">
                                            <a id="tab1" class="nav-link active color-a" data-toggle="tab" role="tab" href="#submenu1">Lưu lượng vào</a>
                                        </li>
                                        <li class="nav-item margin_center">
                                            <a id="tab2" class="nav-link color-a" data-toggle="tab" role="tab" href="#submenu2">Lưu lượng ra</a>
                                        </li>
                                        <li class="nav-item margin_center">
                                            <button onclick="exportFileJson()" type="button" class="btn btn-add"><i class="fa fa-download" aria-hidden="true"></i> Export</button>
                                        </li>

                                    </ul>
                                    <br>

                                    <div class="tab-content">
                                        <?php
                                        $command = "sudo python tool/python-iptables/manual_input.py -L";
                                        // print_r($command);  
                                        $string = shell_exec($command);
                                        //   print($string);
                                        // print_r(explode(')',$string)[1]);
                                        $string = explode(')', $string)[1];
                                        $data = json_decode($string, true);
                                        // print_r($data);
                                        $input = $data[0]["chain_rules"];
                                        // print_r($input);
                                        $output = $data[2]['chain_rules'];
                                        // print(count($data['INPUT']));

                                        ?>
                                        <div id="submenu1" class="tab-pane  in active">
                                            <table id="processTable1" class="table table-hover table-striped">
                                                <thead class="header-table">
                                                    <tr>
                                                        <th>Phương thức</th>
                                                        <th>Địa chỉ IP</th>
                                                        <th>Cổng kết nối</th>
                                                        <th>Prefix</th>
                                                        <th>Hành vi</th>
                                                        <th></th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    <?php
                                                    $i = 0;
                                                    foreach ($input as $key => $line) {
                                                        $ip = "";
                                                        if (!isset($line['target']['LOG'])) {
                                                            if (isset($line['iprange']['dst-range'])) {
                                                                $ip = $line['iprange']['dst-range'];
                                                            }
                                                            if (isset($line['iprange']['dst-range']) && isset($line['iprange']['src-range'])) {
                                                                $ip = $ip . ",";
                                                            }
                                                            if (isset($line['iprange']['src-range'])) {
                                                                $ip = $ip . $line['iprange']['src-range'];
                                                            }

                                                            $port = "";
                                                            if (isset($line[$line['protocol']]['dport'])) {
                                                                $port = $line[$line['protocol']]['dport'];
                                                            }
                                                            if (isset($line[$line['protocol']]['dport']) && isset($line['iprange']['sport'])) {
                                                                $port = $port . ",";
                                                            }
                                                            if (isset($line[$line['protocol']]['sport'])) {
                                                                $port = $port . $line[$line['protocol']]['sport'];
                                                            }


                                                            echo "<tr>";
                                                            echo "<td>" . $line['protocol'] . "</td>";
                                                            echo "<td>" . $ip . "</td>";
                                                            echo "<td>" . $port . "</td>";
                                                            echo "<td>" . $log . "</td>";
                                                            echo "<td>" . $line['target'] . "</td>";
                                                    ?>
                                                            <td>
                                                                <form method="post" action="php/rule_input.php">
                                                                    <input name="id" type="hidden" value="<?= $i ?>">
                                                                    <button type="submit" class="btn-del Disable"><i class="fa fa-trash-o" style="font-size: 1.2rem;" aria-hidden="true"></i></button>
                                                                </form>
                                                            </td>
                                                    <?php
                                                            echo "</tr>";
                                                        } else {
                                                            $log = $line['target']['LOG']['log-prefix'];
                                                        }

                                                        $i = $i + 1;
                                                    }
                                                    ?>
                                                </tbody>
                                            </table>

                                        </div>

                                        <div id="submenu2" class="tab-pane fade">
                                            <table id="processTable2" class="table table-hover table-striped">
                                                <thead class="header-table">
                                                    <tr>
                                                        <th>Phương thức</th>
                                                        <th>Địa chỉ IP</th>
                                                        <th>Cổng kết nối</th>
                                                        <th>Hành vi</th>
                                                        <th></th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    <?php
                                                    $i = 0;
                                                    // print_r($output);
                                                    foreach ($output as $key => $line) {
                                                        $ip = "";

                                                        if (!isset($line['target']['LOG'])) {
                                                            if (isset($line['iprange']['dst-range'])) {
                                                                $ip = $line['iprange']['dst-range'];
                                                            }
                                                            if (isset($line['iprange']['dst-range']) && isset($line['iprange']['src-range'])) {
                                                                $ip = $ip . ",";
                                                            }
                                                            if (isset($line['iprange']['src-range'])) {
                                                                $ip = $ip . $line['iprange']['src-range'];
                                                            }

                                                            $port = "";
                                                            if (isset($line[$line['protocol']]['dport'])) {
                                                                $port = $line[$line['protocol']]['dport'];
                                                            }
                                                            if (isset($line[$line['protocol']]['dport']) && isset($line['iprange']['sport'])) {
                                                                $port = $port . ",";
                                                            }
                                                            if (isset($line[$line['protocol']]['sport'])) {
                                                                $port = $port . $line[$line['protocol']]['sport'];
                                                            }

                                                            echo "<tr>";
                                                            echo "<td>" . $line['protocol'] . "</td>";
                                                            echo "<td>" . $ip . "</td>";
                                                            echo "<td>" . $port . "</td>";
                                                            echo "<td>" . $line['target'] . "</td>";
                                                    ?>
                                                            <td>
                                                                <form method="post" action="php/rule_output.php">
                                                                    <input name="id" type="hidden" value="<?= $i ?>">
                                                                    <button type="submit" class="btn-del Disable"><i class="fa fa-trash-o" style="font-size: 1.2rem;" aria-hidden="true"></i></button>
                                                                </form>
                                                            </td>
                                                    <?php
                                                            echo "</tr>";
                                                        }
                                                        $i = $i + 1;
                                                    }
                                                    ?>
                                                </tbody>
                                            </table>
                                        </div>
                                    </div>
                                </div>
                                <?php
                                $string = file_get_contents("service.json");
                                $service = json_decode($string, true);
                                $getContent = file_get_contents("manual_service.json");
                                $manual_service = json_decode($getContent, true);
                                ?>
                                <div id="menu3" class="tab-pane fade">
                                    <form action="php/addService.php" method="POST">
                                        <div class="form-group">
                                            <label>Dịch vụ</label>
                                            <input type="" name="service" class="form-control" id="" aria-describedby="" placeholder="Service">
                                        </div>
                                        <div class="form-group">
                                            <label for="exampleInputPassword1">Protocol</label>
                                            <select class="form-control Disable" name="protocol" id="input_action">
                                                <option value="TCP">TCP</option>
                                                <option value="UDP">UDP</option>
                                                <option value="ICMP">ICMP</option>
                                            </select>
                                        </div>
                                        <div class="form-group">
                                            <label for="exampleInputPassword1">Port</label>
                                            <input type="" name="port" class="form-control" id="" placeholder="Port">
                                        </div>
                                        <div class="form-group">
                                            <label for="exampleInputPassword1">I/O</label>
                                            <select class="form-control Disable" name="i/o" id="input_action">
                                                <option value="Input">Input</option>
                                                <option value="Output">Output</option>
                                            </select>
                                        </div>
                                        <div class="form-group">
                                            <label for="exampleInputPassword1">Target</label>
                                            <select class="form-control Disable" name="target" id="input_action">
                                                <option value="ACCEPT">ACCEPT</option>
                                                <option value="DROP">DROP</option>
                                            </select>
                                        </div>
                                        <button type="submit" class="btn btn-add">Tạo luật</button>
                                    </form>
                                    <table class="table" id="profile">
                                        <thead>
                                            <tr>
                                                <th scope="col"></th>
                                                <th scope="col">Dịch vụ</th>
                                                <th scope="col">Protocol</th>
                                                <th scope="col">Port</th>
                                                <th scope="col">I/O</th>
                                                <th scope="col">Target</th>
                                                <th scope="col">Xóa</th>
                                            </tr>
                                        </thead>
                                        <tbody>

                                            <?php

                                            foreach ($service as $key => $serv) {
                                                echo '<tr>';
                                                $cnt = 0;
                                                if ($serv['i_o'] == 'Input') {
                                                    if (count($input) == 0) {
                                                        echo '<th scope="row"><input type="checkbox" name="checkbox" aria-label="Checkbox for following text input" ></th>';
                                                    } else {
                                                        $i = 0;
                                                        foreach ($input as $key => $line) {
                                                            if ($line[$line['protocol']]['dport'] == $serv['port']) {
                                                                echo '<th target=' . $i . ' scope="row"><input target=' . $i . '  type="checkbox" name="checkbox" aria-label="Checkbox for following text input" checked></th>';
                                                                $cnt = 0;
                                                                break;
                                                            } else {
                                                                $cnt++;
                                                            }
                                                            $i++;
                                                        }

                                                        if ($cnt > 0) {
                                                            echo '<th scope="row"><input type="checkbox" name="checkbox" aria-label="Checkbox for following text input"></th>';
                                                        }
                                                    }
                                                } else {
                                                    if (count($output) == 0) {
                                                        echo '<th scope="row"><input type="checkbox" name="checkbox" aria-label="Checkbox for following text input" ></th>';
                                                    } else {
                                                        $i = 0;
                                                        foreach ($output as $key => $line) {
                                                            if ($line[$line['protocol']]['dport'] == $serv['port']) {
                                                                echo '<th target=' . $i . ' scope="row"><input target=' . $i . ' type="checkbox" name="checkbox" aria-label="Checkbox for following text input" checked></th>';
                                                                $cnt = 0;
                                                                break;
                                                            } else {
                                                                $cnt++;
                                                            }
                                                            $i++;
                                                        }

                                                        if ($cnt > 0) {
                                                            echo '<th scope="row"><input type="checkbox" name="checkbox" aria-label="Checkbox for following text input"></th>';
                                                        }
                                                    }
                                                }
                                                echo '<td>' . $serv['service'] . '</td>';
                                                echo '<td>' . $serv['protocol'] . '</td>';
                                                echo '<td>' . $serv['port'] . '</td>';
                                                echo '<td>' . $serv['i_o'] . '</td>';
                                                echo '<td>' . $serv['target'] . '</td>';
                                                echo '<td><button type="button" id="1"  onclick="deleteService(' . $serv['port'] . ')" class="btn btn-secondary" disabled>delete</button></td>';
                                                echo "</tr>";
                                            }
                                            foreach ($manual_service as $key => $serv) {
                                                echo '<tr>';
                                                $cnt = 0;
                                                if ($serv['i_o'] == 'Input') {
                                                    if (count($input) == 0) {
                                                        echo '<th scope="row"><input type="checkbox" name="checkbox" aria-label="Checkbox for following text input" ></th>';
                                                    } else {
                                                        $i = 0;
                                                        foreach ($input as $key => $line) {
                                                            if ($line[$line['protocol']]['dport'] == $serv['port']) {
                                                                echo '<th target=' . $i . ' scope="row"><input target=' . $i . ' type="checkbox" name="checkbox" aria-label="Checkbox for following text input" checked></th>';
                                                                $cnt = 0;
                                                                break;
                                                            } else {
                                                                $cnt++;
                                                            }
                                                            $i++;
                                                        }

                                                        if ($cnt > 0) {
                                                            echo '<th scope="row"><input type="checkbox" name="checkbox" aria-label="Checkbox for following text input"></th>';
                                                        }
                                                    }
                                                } else {
                                                    if (count($output) == 0) {
                                                        echo '<th scope="row"><input type="checkbox" name="checkbox" aria-label="Checkbox for following text input" ></th>';
                                                    } else {
                                                        $i = 0;
                                                        foreach ($output as $key => $line) {
                                                            if ($line[$line['protocol']]['dport'] == $serv['port']) {
                                                                echo '<th target=' . $i . ' scope="row"><input target=' . $i . ' type="checkbox" name="checkbox" aria-label="Checkbox for following text input" checked></th>';
                                                                $cnt = 0;
                                                                break;
                                                            } else {
                                                                $cnt++;
                                                            }
                                                            $i++;
                                                        }
                                                        if ($cnt > 0) {
                                                            echo '<th scope="row"><input type="checkbox" name="checkbox" aria-label="Checkbox for following text input"></th>';
                                                        }
                                                    }
                                                }
                                                echo '<td>' . $serv['service'] . '</td>';
                                                echo '<td>' . $serv['protocol'] . '</td>';
                                                echo '<td>' . $serv['port'] . '</td>';
                                                echo '<td>' . $serv['i_o'] . '</td>';
                                                echo '<td>' . $serv['target'] . '</td>';
                                                echo '<td><button type="button" id="1"  onclick="deleteService(' . $serv['port'] . ')" class="btn btn-secondary" >delete</button></td>';
                                                echo "</tr>";
                                            }
                                            ?>
                                        </tbody>
                                    </table>
                                    <button id="update" onclick="update()" type="button" class="btn btn-secondary">Cập nhật</button>
                                </div>
                            </div>
                        </div>
                    </div>

                    <a id="background-loading">
                        <img id="gif_load" hidden="" style="position: fixed; top: 50%;" src="admin_asset_web/dist/img/loading1.gif">
                    </a>

                </div>

            </div>
            <!-- /.row -->
        </div>
</div>
<!-- /.card-body -->
</div>
<!-- /.card -->

</div>
<!-- /.col -->
</div>
<!-- /.row -->
<?php

include 'include/footer.php';

?>
<script>
    <?php
    if (isset($_SESSION['val']['form'])) {
    ?>
        if (<?= $_SESSION['val']['form'] ?> == 2) {
            document.getElementById("tab2").click();
        }

    <?php
    }
    ?>

    function checklog() {
        var prefix1 = document.getElementById("prefix1");
        var prefix2 = document.getElementById("prefix2");

        if (document.getElementById("checklog1").checked) {
            prefix1.disabled = false;
        } else {
            prefix1.disabled = true;

        }

        if (document.getElementById("checklog2").checked) {
            prefix2.disabled = false;
        } else {
            prefix2.disabled = true;

        }

    }

    var checked = [],
        unchecked = [];
    update = () => {
        $.ajax({
            type: "POST",
            url: 'php/profile.php',
            data: {
                check: checked,
                uncheck: unchecked
            },
            success: function(response) {
                // console.log(response)
                self.location = "/firewall.php"
            }
        }, false)
    }
    sendAjax = (tr, port, protocol, i, input_output, target) => {
        if (tr.checked == false && tr.getAttribute('target') != null) {
            checked.push({
                index: tr.getAttribute('target'),
                inout: input_output
            });
        }
        if (tr.checked == true && tr.getAttribute('target') == null) {
            unchecked.push({
                service: service,
                protocol: protocol,
                port: port,
                input_output: input_output,
                target: target
            })
        }
    }
    let table = document.getElementById("profile");
    let tr;
    let length = table.rows.length
    for (let i = 1; i <= length - 1; i++) {
        tr = table.rows[i];
        for (let j = 1; j <= tr.cells.length - 1; j++) {
            switch (j) {
                case 1:
                    var service = tr.cells[j].innerHTML;
                    break;
                case 2:
                    var protocol = tr.cells[j].innerHTML;
                    break;
                case 3:
                    var port = tr.cells[j].innerHTML;
                    break;
                case 4:
                    var inout = tr.cells[j].innerHTML;
                    break;
                case 5:
                    var target = tr.cells[j].innerHTML;
                    break;
            }
        }
        var index = tr.cells[0].querySelector("input[name=checkbox]").getAttribute('target')
        tr.cells[0].addEventListener('click', sendAjax.bind(this, tr.cells[0].querySelector("input[name=checkbox]"), port, protocol, index, inout, target), false)
    }


    $(document).ready(function() {
        $('#processTable1').DataTable({
            dom: 'Bfrtip',
            buttons: [
                'copy', 'csv', 'excel', 'pdf', 'print'
            ]
        });
    });

    $(document).ready(function() {
        $('#processTable2').DataTable({
            dom: 'Bfrtip',
            buttons: [
                'copy', 'csv', 'excel', 'pdf', 'print'
            ]
        });
    });

    $(document).ready(function() {
        $('#profile').DataTable({
            dom: 'Bfrtip',
            buttons: [
                'copy', 'csv', 'excel', 'pdf', 'print'
            ]
        });
    });

    exportFileJson = () => {
        $.ajax({
            type: "GET",
            url: 'php/exportJson.php',
            success: function(response) {
                self.location = "/firewall.php"
            }
        }, false)
    }

    convert1 = (index) => {
        $.ajax({
            type: "POST",
            url: 'php/deleteInput.php',
            data: {
                index: index
            },
            success: function(response) {
                self.location = "/firewall.php"
            }
        }, false)

    }

    convert2 = (index) => {
        $.ajax({
            type: "POST",
            url: 'php/deleteOutput.php',
            data: {
                index: index
            },
            success: function(response) {
                self.location = "/firewall.php"
            }
        }, false)
    }

    deleteService = (port) => {
        $.ajax({
            type: "POST",
            url: 'php/deletePort.php',
            data: {
                port: port
            },
            success: function(response) {
                self.location = "/firewall.php"
            }
        }, false)

    }
</script>