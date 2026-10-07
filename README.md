Endpoint            Methods           Rule                                
------------------  ----------------  ------------------------------------
api_score           DELETE, GET, PUT  /api/students/<mssv>/scores/<course>
api_student_detail  GET               /api/students/<mssv>                
api_student_list    GET               /api/students                       
index               GET               /                                   
search              GET               /search                             
static              GET               /static/<path:filename>             
student_detail      GET               /students/<mssv>                    
student_export      GET               /students/<mssv>/export             
student_list        GET               /students                           
student_short       GET               /sv/<mssv>

$B = "http://127.0.0.1:8000"

curl.exe -i "${B}/sv/23T1020001"
HTTP/1.1 301 MOVED PERMANENTLY
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Wed, 07 Oct 2026 13:04:07 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 227
Location: /students/23T1020001
Connection: close

<!doctype html>
<html lang=en>
<title>Redirecting...</title>
<h1>Redirecting...</h1>
<p>You should be redirected automatically to the target URL: <a href="/students/23T1020001">/students/23T1020001</a>. If not, click the link.


curl.exe -i ${B}/students/23T1020001/export
HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Wed, 07 Oct 2026 13:07:37 GMT
Content-Type: text/csv; charset=utf-8
Content-Length: 41
Content-Disposition: attachment; filename=diem_23T1020001.csv
Connection: close

hoc_phan,diem
PMMNM,8.5
CSDL,7.0
MMT,9.0


curl.exe -i "${B}/api/students?lop=k47a&min_avg=7"
HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Wed, 07 Oct 2026 13:10:32 GMT
Content-Type: application/json
Content-Length: 208
Connection: close

[
  {
    "average": 8.17,
    "lop": "K47A",
    "mssv": "23T1020001",
    "name": "Nguyễn Văn An",
    "rank": "Khá",
    "scores": {
      "CSDL": 7.0,
      "MMT": 9.0,
      "PMMNM": 8.5
    }
  }
]


curl.exe -i "${B}/api/students?min_avg=abc"
HTTP/1.1 400 BAD REQUEST
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Wed, 07 Oct 2026 13:12:42 GMT
Content-Type: application/json
Content-Length: 86
Connection: close

{"detail": "min_avg phải là một số.", "error": "Dữ liệu không hợp lệ"}


curl.exe -i "${B}/api/students/999"
HTTP/1.1 404 NOT FOUND
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Wed, 07 Oct 2026 13:16:11 GMT
Content-Type: application/json
Content-Length: 84
Connection: close

{"detail": "Không có sinh viên với MSSV = 999.", "error": "Không tìm thấy"}


curl.exe -i -X PUT "${S}/web?score=9"
HTTP/1.1 201 CREATED
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Wed, 07 Oct 2026 13:20:35 GMT
Content-Type: application/json
Content-Length: 80
Location: /api/students/23T1020005/scores/WEB
Connection: close

{
  "average": 9.0,
  "course": "WEB",
  "mssv": "23T1020005",
  "score": 9.0
}


curl.exe -i -X PUT "${S}/WEB?score=7.5"
HTTP/1.1 200 OK
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Wed, 07 Oct 2026 13:23:01 GMT
Content-Type: application/json
Content-Length: 80
Connection: close

{
  "average": 7.5,
  "course": "WEB",
  "mssv": "23T1020005",
  "score": 7.5
}


curl.exe -i -X PUT "${S}/WEB?score=11"
HTTP/1.1 400 BAD REQUEST
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Wed, 07 Oct 2026 13:24:04 GMT
Content-Type: application/json
Content-Length: 109
Connection: close

{"detail": "Điểm phải nằm trong khoảng từ 0 đến 10.", "error": "Dữ liệu không hợp lệ"}


curl.exe -i -X DELETE "${S}/WEB"
HTTP/1.1 204 NO CONTENT
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Wed, 07 Oct 2026 13:24:25 GMT
Content-Type: text/html; charset=utf-8
Connection: close


curl.exe -i -X POST "${S}/WEB"
HTTP/1.1 405 METHOD NOT ALLOWED
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Wed, 07 Oct 2026 13:26:02 GMT
Content-Type: application/json
Allow: HEAD, DELETE, GET, OPTIONS, PUT
Content-Length: 117
Connection: close

{"detail": "The method is not allowed for the requested URL.", "error": "Phương thức không được hỗ trợ"}


curl.exe -i -X POST "${B}/students"
HTTP/1.1 405 METHOD NOT ALLOWED
Server: Werkzeug/3.1.9 Python/3.14.8
Date: Wed, 07 Oct 2026 13:26:37 GMT
Content-Type: text/html; charset=utf-8
Allow: GET, OPTIONS, HEAD
Content-Length: 530
Connection: close


<!doctype html>
<html lang="vi">
<head>
    <meta charset="utf-8">
    <title>Phương thức không được hỗ trợ - Sổ điểm</title>
</head>
<body>
    <h1>Phương thức không được hỗ trợ</h1>
    <nav>
        <a href="/">Trang chủ</a> |
        <a href="/students">Sinh viên</a> |
        <a href="/search">Tìm kiếm</a>
    </nav>
    <hr>
    
        <h2>405 - Phương thức không được hỗ trợ</h2>
        <p>The method is not allowed for the requested URL.</p>
        
</body>
</html>

Vì sao Câu 4 dùng 301 còn Câu 8 trả 201 kèm Location?
-> Câu 4 dùng 301 vì chuyển hướng vĩnh viễn từ URL rút gọn /sv/<mssv> đến URL chuẩn /students/<mssv>. Câu 8 trả 201 khi thêm điểm cho một học phần chưa có. Header Location chỉ URL của tài nguyên điểm vừa tạo để client truy cập. Nếu sửa điểm đã tồn tại thì trả 200 OK.

Thêm điểm cho 23T1020005 rồi khởi động lại server, điểm đó còn không? Vì sao?
Không. Trong cách cài đặt của bài, điểm chỉ được lưu trong dictionary STUDENTS ở bộ nhớ RAM. Khi server khởi động lại, chương trình tạo lại dictionary từ dữ liệu mẫu, nên sinh viên 23T1020005 trở về trạng thái chưa có điểm.