<?php

include 'include/header.php';

?>
            <div class="content-wrapper">
                <!-- Content Header (Page header) -->
                <section class="content-header">
                    <div class="container-fluid-header">
                        <div class="row mb-2">
                            <div class="col-sm-6">
                                <h1>Thêm tên miền tự định nghĩa</h1>
                            </div>
                            <div class="col-sm-6">
                                <ol class="breadcrumb float-sm-right">
                                    <li class="breadcrumb-item"><a href="/"><i class="fa fa-home" aria-hidden="true"></i> Trang chủ</a></li>
                                    <li class="breadcrumb-item active">Thêm tên miền tự định nghĩa</li>
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
              <?php
              if(isset($_SESSION['error'])){
                       ?>
                                    <center><div style="background-color: #f8d7da!important;" class="alert alert-danger">
                                       <?=$_SESSION['error']?> <br>
                                    </div></center>
              <?php
                }
    
              ?>

                               <!-- /.card -->
             <form action="php/adddomain.php" method="POST">
            <input type="hidden" name="form" value="1">
            <div class="form-group">

                <table>
                    <tbody>
                   
                        <tr>
                            <td><label style="width: 200px" for="input_IP1">Tên miền </label></td>
                            <td><input  class="form-control" name="Domain"></td>
                        </tr>
                        <tr>
                            <td><label style="width: 200px" for="input_IP1"> Loại tên miền  </label></td>
                             <td><select class="form-control Disable" name="Type" id="input_protocol">
                                <option value="1"> Tên miền sạch</option>
                                <option value="2">Tên miền độc hại</option>
                            </select></td>
                        </tr>


            </tbody>
            </table>
            </div>
            <button type="submit" class="btn btn-add Disable"><i class="fa fa-plus" aria-hidden="true"></i> Thêm tên miền</button>
        </form>             
                    </div>
                    <!-- /.card-body -->
            </div>
           
        </div>
        <!-- /.col -->
        </div>
        <!-- /.row -->
      <?php

include 'include/footer.php';

?>