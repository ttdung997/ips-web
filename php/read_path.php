<?php
	// echo ("data/clam/".$_POST["path"]);
    echo  shell_exec("sudo cat ../data/clam/".$_POST["path"]."| awk -F".'" "'." '{ printf(".'"%-25s<br>"'.", $0); }'");
?>