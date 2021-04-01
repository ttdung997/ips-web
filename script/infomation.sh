uptime
echo "|||"
free -m |tail -2|awk '{ printf("%-8s||  %-8s|||\n",$2, $3); }' | head -n 20 
lscpu |grep MHz | awk -F" " '{ printf("%-50s ??? ", $0); }'

#grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage "%"}'

echo "|||"
top -bn1 | grep 'Tasks' | tail -1 


