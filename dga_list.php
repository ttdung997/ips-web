<?php

include 'include/header.php';

?>
            <div class="content-wrapper">
                <!-- Content Header (Page header) -->
                <section class="content-header">
                    <div class="container-fluid-header">
                        <div class="row mb-2">
                            <div class="col-sm-6">
                                <h1>Danh sách tên miền DGA</h1>
                            </div>
                            <div class="col-sm-6">
                                <ol class="breadcrumb float-sm-right">
                                    <li class="breadcrumb-item"><a href="/"><i class="fa fa-home" aria-hidden="true"></i> Trang chủ</a></li>
                                    <li class="breadcrumb-item active">Danh sách tên miền DGA</li>
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
                                <section class="content">
           <div class="col-md-12">
           <?php

                    $db = new SQLite3('tool/dga/data.db');

                    $res = $db->query('SELECT DISTINCT * FROM bkcs_dga_report group by domain');
            ?>
                   
           <table id="DgaTable" class="table table-hover table-striped">
                              <thead class="header-table">
                                  <tr>      
                                      <th>Địa chỉ DGA</th>
                                      <th>Thời gian truy cập</th>
                                      <th>Loại mã độc</th>
                                      <th></th>
                                  </tr>
                              </thead>
                              <tbody>
                                    <?php
                    while ($row = $res->fetchArray()) {
                                        echo "<tr>";
                                        echo "<td>".$row['domain']."</td>";
                                        echo "<td>".$row['time']."</td>";
                                        echo "<td>Banjori</td>";
                                     
                                      ?>
                                      <td>
                              <form method="post" action="php/vpn_status.php">
                                <input name = "id" type="hidden" value="<?=$i?>">
                                <button type="submit" class="btn btn-success Disable">Block</button>
                              </form>
                                        
                                         
                            </td>
                            </tr>
                            <?php
                                }
                            ?>
                              </tbody>
              </table>
          
            </div>
        </section>
                    </div>
                    <!-- /.card-body -->
            </div>
           
        </div>
        <!-- /.col -->
        </div>
        <!-- /.row -->
        </section>
        <!-- /.content -->
        </div>

        <footer class="main-footer">
            <strong>Copyright &copy; Viện hóa học môi trường</a>.</strong> All rights reserved.
        </footer>
        <!-- /.control-sidebar -->
        </div>
        <!-- ./wrapper -->

        <!-- jQuery -->
        <script src="admin_asset_web/plugins/jquery/jquery.min.js"></script>
        <!-- Bootstrap 4 -->
        <script src="admin_asset_web/plugins/bootstrap/js/bootstrap.bundle.min.js"></script>
        <!-- DataTables -->
        <script src="admin_asset_web/plugins/datatables/jquery.dataTables.js"></script>
        <script src="admin_asset_web/plugins/datatables/dataTables.bootstrap4.js"></script>
        <!-- SlimScroll -->
        <script src="admin_asset_web/plugins/slimScroll/jquery.slimscroll.min.js"></script>
        <!-- FastClick -->
        <script src="admin_asset_web/plugins/fastclick/fastclick.js"></script>
        <!-- AdminLTE App -->
        <script src="admin_asset_web/dist/js/adminlte.min.js"></script>
        <!-- AdminLTE for demo purposes -->
        <script src="admin_asset_web/dist/js/demo.js"></script>
        <!-- page script -->
        <script src="admin_asset_web/dist/js/Form.js"></script>
        <!-- iCheck -->
        <script src="admin_asset_web/plugins/iCheck/icheck.min.js"></script>
        <!-- pusher -->
        <!-- <script src="https://js.pusher.com/4.1/pusher.min.js"></script> -->
        <!-- datatable -->
        <script type="text/javascript" src="admin_asset_web/dist/js/jquery.passtrength.min.js"></script>
        <script type="text/javascript" src="admin_asset_web/dist/js/jquery.confirm.js"></script>

        <!-- AdminLTE for demo purposes -->
        <script src="admin_asset_web/dist/js/demo.js"></script>
        <script type="text/javascript">

$(document).ready(function () {
  $('#DgaTable').DataTable();
  $('.dataTables_length').addClass('bs-select');
});

<?php

include 'include/footer.php';

?>