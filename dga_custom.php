<?php

include 'include/header.php';

?>
            <div class="content-wrapper">
                <!-- Content Header (Page header) -->
                <section class="content-header">

                    <div class="container-fluid-header">
                        <div class="row mb-2">
                            <div class="col-sm-6">
                                <h1>Tên miền tự định nghĩa</h1>
                            </div>
                            <div class="col-sm-6">
                                <ol class="breadcrumb float-sm-right">
                                    <li class="breadcrumb-item"><a href="/"><i class="fa fa-home" aria-hidden="true"></i> Trang chủ</a></li>
                                    <li class="breadcrumb-item active">Tên miền tự định nghĩa</li>
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
                                <div class="card-body">    <?php
              if(isset($_SESSION['notification'])){
             ?>
                                        <center>
                                            <div class="alert alert-success">
                                                <?=$_SESSION['notification']?>
                                                    <br>
                                            </div>
                                        </center>
                                        <?php
                }
                session_destroy();
                session_start();

              ?>
                                <section class="content">
           <div class="col-md-12">
           <?php

                    $db = new SQLite3('tool/dga/data.db');

                    $res = $db->query('SELECT * FROM bkcs_custom_domain');
            ?>
                   
           <table id="DgaTable" class="table table-hover table-striped"><a href="/add_domain.php" style="float: right" type="submit" class="btn btn-add Disable" style="margin-top: 10px;"><i class="fa fa-plus" aria-hidden="true"></i> Thêm mới</a>
                              <thead class="header-table">
                                  <tr>      
                                      <th>Tên miền</th>
                                      <th>Loại tên miền</th>
                                      <th></th>
                                  </tr>
                              </thead>
                              <tbody>
                                    <?php
                    while ($row = $res->fetchArray()) {
                                        echo "<tr>";
                                        echo "<td>".$row['domain']."</td>";
                                        if($row['type'] == 1){
                                            echo "<td>Tên miền sạch</td>";
                                        }else{
                                            echo "<td>Tên miền độc hại</td>";
                                        }
                                     
                                      ?>
                                       <td><form method="post" action="php/deletedomain.php">
                                <input name = "id" type="hidden" value="<?=$row['id']?>">
                                <button type="submit" class="btn btn-del Disable"><i class="fa fa-trash-o" aria-hidden="true" style="font-size: 1.2rem;"></i></button>
                              </form></td>
                              </tr>
                                      <td>
                             
                            </tr>
                            <?php
                                }
                            ?>
                              </tbody>
              </table>
          
            </div>
       <?php

include 'include/footer.php';

?>
        <script type="text/javascript">

$(document).ready(function () {
  $('#DgaTable').DataTable();
  $('.dataTables_length').addClass('bs-select');
});

</script>