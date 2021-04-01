



# Cấu hình cài đặt


## Cài đặt web frontend
- dùng git clone repo về máy tình được thư mục HOST-IPS, truy cập thư mục cần cài đặt 

### Một số lưu ý
- Có thể tùy chỉnh tên miền trong file /php/config.php

## Cài đặt bộ lệnh hệ thống linux
### Cài đăt cho hệ điều hành ubuntu 

- Cài đặt module python cho hệ thống
```sh
sudo cp network.py /opt/
sudo cp rc.local /etc/
sudo service rc.local restart
sudo apt install python-pip
pip install python-iptables
cd ~
sudo cp .local/lib/python2.7/site-packages /usr/lib/python2.7/dist-packages
sudo cp -r .local/lib/python2.7/site-packages /usr/lib/python2.7/dist-packages


```

- Cài đặt module mã hóa dữ liệu
```sh
sudo pip install -r requirements_linux.txt
sudo apt-get install auditd -y
sudo systemctl start auditd & sudo systemctl enable auditd
```

- Cài đặt Php và chaỵ ứng dụng
```sh
sudo apt-get install php -y
sudo apt-get install php-sqlite3 
sudo apt-get install php-{bcmath,bz2,intl,gd,mbstring,mysql,zip,fpm} -y
php -S 0.0.0.0:8080 >/dev/null 2>&1 &
```

### Cài đặt cho hệ điều hành CentOS 

- Cài đặt các phần mềm cần thiết
```sh
sudo yum makecache
sudo yum install git

sudo yum install epel-release
sudo yum install python
sudo yum install python-pip
sudo yum install python-devel
sudo yum install -y python3-devel.x86_64

sudo yum install python3
sudo yum install python-pip
 
sudo pip install python-iptables
sudo pip3 install psuti
```


- Cài đặt module mã hóa dữ liệu
```sh
sudo pip install -r requirements_linux.txt
sudo yum install auditd -y
sudo systemctl start auditd & sudo systemctl enable auditd
```

- Cài đặt Php và chaỵ ứng dụng
```sh
sudo yum install php7.3-sqlite3 
sudo yum install php -y
sudo  install php-{bcmath,bz2,intl,gd,mbstring,mysql,zip,fpm} -y
php -S 0.0.0.0:8080 >/dev/null 2>&1 &
```

