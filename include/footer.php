 </section>
                    </div>
                    <!-- /.card-body -->
            </div>
           
        </div>
        <!-- /.col -->
        </div>
        <!-- /.row -->
        </sect
ion>
        <!-- /.content -->
        </div>

        <footer class="main-footer">
            <strong>Copyright &copy; 2020 An toàn an ninh thông tin Bách Khoa</a>.</strong> All rights reserved.
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

function readNoti(path){
   $.ajax({ 
  method: "GET",
  url: "/include/noti_read.php",
  processData: false,
  contentType: false,
   // url: "/check",
   // headers:  {'Access-Control-Allow-Origin' : 'http://192.168.218.138'},
   success: function (data) {
     var allData = JSON.parse(data);
     console.log(allData)

     for (i = 0; i < allData.length; i++){
        if(allData[i][2].includes("deleted")){
            alert("Tệp tin " + allData[i][3] + " đã bị xóa vào lúc "+ allData[i][1]) 
        }
        else{
            alert("Tệp tin " + allData[i][3] + " đã bị thay đổi vào lúc "+ allData[i][1]) 
        }
     }
   }
   });
}
readNoti();
</script>
    </body>

    </html>