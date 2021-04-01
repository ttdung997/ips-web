Win32:
script: moniter.py

Reset CSDL: run script: reset_db.py

Linux:
script: moniter_linux.py

Reset CSDL: run script: reset_db_linux.py

API:

1. Thêm vào danh sách theo dõi:
script -i [Đường dẫn tuyệt đối file, thư mục] [Loại đường dẫn]

Loại đường dẫn: 0 - file, 1- thư mục

Kết quả in ra dạng json: {"result": true/false, "moniter_list":[]}
    result: true- không có lỗi
            false - có lỗi
    moniter_list: danh sách theo dõi lưu trong csdl, mỗi phần tử dạng:
        [id, type, path, , state]
        state = 0: mới thêm vào, chưa quét

2. Xóa khỏi danh sách kiểm tra
script -r [Đường dẫn tuyệt đối file, thư mục] [Loại đường dẫn]
Kết quả tương tự 1.

3. Truy vấn danh sách theo dõi
script -l

Kết quả tương tự 1.

4. Truy vấn thông báo
script -a 

Kết quả in ra dạng json: {"alert_list":alert_list}
    alert_list: danh sách thông báo lưu trong csdl, đã xắp xếp giảm dần theo thời gian quét,
    mỗi phần tử dạng:
        [id, time, mess, path]
    time: chuỗi thời gian: 'Y-M-D' h:m:s
    mess: Thông điệp thông báo dạng chuỗi:

        FILE được tạo mới = "File created."
        FILE đã chỉnh sửa = "File changed."
        File đã truy cập = "File access."
        File đã bị xóa = "File deleted."
        Thư mục bị xóa = "Folder deleted."
    path: đường dẫn kiểm tra

5. Quét 1 đường dẫn
script -s [Đường dẫn] [loại đường dẫn]

Kết quả in ra dạng json:
Nếu có lỗi: {"result": false, "error_msg": err_mess}
Nếu không có lỗi: {"result": false, "message": {info_dic}}

    result: true- không có lỗi
    info_dic: dictionary (python) chứa các kết quả tóm lược quá trình quét path

6. Truy vấn id của alert mới nhất
script -e
Kết quả in ra dạng json:
Nếu có lỗi: {"last_alert_id": id}

7. Truy vấn danh sách alert từ id trở đi
script -a id
Kết quả trả về như 4.
