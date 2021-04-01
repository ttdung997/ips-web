cd "/tmp"

unzip -o "$1.zip"
cp /tmp/$1/* /opt/modsecurity/etc/custom
cp -r /tmp/$1/* /opt/modsecurity/etc/custom