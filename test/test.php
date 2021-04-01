<?php
$it = new RecursiveTreeIterator(new RecursiveDirectoryIterator("/", RecursiveDirectoryIterator::SKIP_DOTS));
foreach($it as $path) {
  echo $path."<br>";
}

