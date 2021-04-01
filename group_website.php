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
                                <section class="content">
           <div class="col-md-12">
            <div class="card card-primary card-outline">
                <table id="GroupWebsiteTable" class="table table-striped table-bordered thead-dark" style="width:100%;">
                        <thead class="header-table">
                            <tr>
                                <th>Name</th>
                                <th>Description</th>
                                <th style="width: 60px;">Edit</th>
                            </tr>
                        </thead>
                </table>
                <div class="float-right">
                <button class="btn btn-add" style="float:right; margin-top: 10px; margin-bottom:15px; margin-right:10px; width: 140px;" id="add" onclick="AppendGW()"><i class="fa fa-plus" style="padding-right:10px;"></i><span class="glyphicon glyphicon-plus-sign">Add New</span></button>
                </div>
            </div>
            </div>
        </section>
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