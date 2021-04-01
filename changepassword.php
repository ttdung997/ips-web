<?php

include 'include/header.php';

?>
            <div class="content-wrapper">
                <!-- Content Header (Page header) -->
                <section class="content-header">
                    <div class="container-fluid-header">
                        <div class="row mb-2">
                            <div class="col-sm-6">
                                <h1>Thay đổi mật khẩu</h1>
                            </div>
                            <div class="col-sm-6">
                                <ol class="breadcrumb float-sm-right">
                                    <li class="breadcrumb-item"><a href="/"><i class="fa fa-home" aria-hidden="true"></i> Trang chủ</a></li>
                                    <li class="breadcrumb-item active">Thay đổi mật khẩu</li>
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
             <form action="php/changepass.php" method="POST">
            <input type="hidden" name="form" value="1">
            <div class="form-group">

                <table>
                    <tbody>
                   
                        <tr>
                            <td><label style="width: 200px" for="input_IP1"> Mật khẩu cũ</label></td>
                            <td><input  type="password"  class="form-control" name="oldpass"></td>
                        </tr>
                        <tr>
                            <td><label style="width: 200px" for="input_IP1">Mật khẩu mới</label></td>
                            <td><input type="password"  class="form-control" id="newpass" name="newpass"></td>
                        </tr>


            </tbody>
            </table>
            </div>
            <button type="submit" class="btn btn-add Disable"><i class="fa fa-plus" aria-hidden="true"></i> Thay mật khẩu</button>
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