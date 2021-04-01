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
                                <div class="card-body">
                                <section class="content">





<h5 style="margin-bottom: 15px;">Chỉnh sửa bộ luật tùy biến</h5>

<?php

include 'include/ip.php';

// include 'include/url.php';

include 'include/custom.php';

?>
<script>
$body = $("body");

$(document).on({
    ajaxStart: function() { $body.addClass("loading");    },
     ajaxStop: function() { $body.removeClass("loading"); }    
});

</script>
</div>
  </div>
            <!-- /.container-fluid -->
        </section>

<?php

include 'include/footer.php';

?>