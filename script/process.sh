top  -o %MEM -bn 1 | grep "^ " | awk '{ printf("%-8s||  %-8s|| %-8s||  %-8s|||\n",$12, $9, $10,$11); }' | head -n 20

