cat /etc/issue
echo "|||"
sudo lshw -short | awk -F " " '{ printf("%-50s|||\n", $0); }'

