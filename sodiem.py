from flask import Flask, abort, jsonify, redirect, request, url_for, make_response
from markupsafe import escape
from io import StringIO
import csv

app = Flask(__name__)
app.json.ensure_ascii = False
STUDENTS = {
    "23T1020001": {
        "name": "Nguyễn Văn An",
        "lop": "K47A",
        "scores": {"PMMNM": 8.5, "CSDL": 7.0, "MMT": 9.0},
    },
    "23T1020002": {
        "name": "Trần Thị Bình",
        "lop": "K47A",
        "scores": {"PMMNM": 6.0, "CSDL": 5.5, "MMT": 7.0},
    },
    "23T1020003": {
        "name": "Lê Hoàng Cường",
        "lop": "K47B",
        "scores": {"PMMNM": 9.5, "CSDL": 9.0},
    },
    "23T1020004": {
        "name": "Phạm Minh Dũng",
        "lop": "K47B",
        "scores": {"PMMNM": 4.0, "CSDL": 3.5, "MMT": 5.0},
    },
    "23T1020005": {"name": "Hoàng Thu Hà", "lop": "K47A", "scores": {}},
    "23T1020006": {
        "name": "Võ Quốc Khánh",
        "lop": "K47C",
        "scores": {"PMMNM": 7.5, "MMT": 8.0},
    },
}


def average(scores):
    if not scores:
        return None
    return round(sum(scores.values()) / len(scores), 2)


def rank(avg):
    if avg is None:
        return "Chưa có điểm"
    elif avg >= 8.5:
        return "Giỏi"
    elif avg >= 7.0:
        return "Khá"
    elif avg >= 5.0:
        return "Trung bình"
    else:
        return "Yếu"


def student_summary(mssv):
    student = STUDENTS[mssv]
    avg = average(student["scores"])
    return {
        "mssv": mssv,
        "name": student["name"],
        "lop": student["lop"],
        "scores": student["scores"],
        "average": avg,
        "rank": rank(avg),
    }


def layout(title, body):
    return f"""
<!doctype html>
<html lang="vi">
<head>
    <meta charset="utf-8">
    <title>{escape(title)} - Sổ điểm</title>
</head>
<body>
    <h1>{escape(title)}</h1>
    <nav>
        <a href="{escape(url_for("index"))}">Trang chủ</a> |
        <a href="{escape(url_for("student_list"))}">Sinh viên</a> |
        <a href="{escape(url_for("search"))}">Tìm kiếm</a>
    </nav>
    <hr>
    {body}
</body>
</html>"""

@app.route("/")
def index():
    total_students = len(STUDENTS)
    total_classes = len({s["lop"] for s in STUDENTS.values()})

    body = f"""
    <p>Tổng số sinh viên: {escape(total_students)}</p>
    <p>Số lớp: {escape(total_classes)}</p>
    <p><a href="{escape(url_for('student_list'))}">Danh sách sinh viên</a></p>
    <p><a href="{escape(url_for('api_student_list'))}">API danh sách sinh viên</a></p>
    """
    return layout("Trang chủ", body)


@app.route("/students")
def student_list():
    lop = request.args.get("lop", "")
    classes = sorted({s["lop"] for s in STUDENTS.values()})

    links = [
        f'<a href="{escape(url_for("student_list"))}">Tất cả</a>'
    ]
    for class_name in classes:
        link = url_for("student_list", lop=class_name)
        links.append(
            f'<a href="{escape(link)}">{escape(class_name)}</a>'
        )

    rows = ""
    for mssv, student in STUDENTS.items():
        if lop and student["lop"].lower() != lop.lower():
            continue

        info = student_summary(mssv)
        avg_text = (
            "—" if info["average"] is None
            else f"{info['average']:.2f}"
        )

        rows += f"""
        <tr>
            <td><a href="{escape(url_for('student_detail', mssv=mssv))}">{escape(mssv)}</a></td>
            <td>{escape(info['name'])}</td>
            <td>{escape(info['lop'])}</td>
            <td>{escape(avg_text)}</td>
            <td>{escape(info['rank'])}</td>
        </tr>
        """

    body = "<p>" + " | ".join(links) + "</p>"
    if rows:
        body += f"""
        <table border="1" cellpadding="6">
            <tr>
                <th>MSSV</th><th>Họ tên</th><th>Lớp</th>
                <th>Điểm TB</th><th>Xếp loại</th>
            </tr>
            {rows}
        </table>
        """
    else:
        body += "<p>Không có sinh viên phù hợp.</p>"

    return layout("Danh sách sinh viên", body)


@app.route("/search")
def search():
    q = request.args.get("q", "")
    keyword = q.lower()

    results = []
    for mssv, student in STUDENTS.items():
        if keyword in student["name"].lower() or keyword in mssv.lower():
            results.append((mssv, student))

    items = ""
    for mssv, student in results:
        detail_url = url_for("student_detail", mssv=mssv)
        items += f"""
        <li><a href="{escape(detail_url)}">{escape(mssv)} - {escape(student['name'])}</a></li>
        """

    body = f"""
    <form method="get" action="{escape(url_for('search'))}">
        <input type="text" name="q" value="{escape(q)}">
        <button type="submit">Tìm kiếm</button>
    </form>
    <p>Tìm thấy {escape(len(results))} kết quả cho “{escape(q)}”.</p>
    <ul>{items}</ul>
    """
    return layout("Tìm kiếm", body)


@app.route("/api/students")
def api_student_list():
    return jsonify([])

@app.route("/students/<mssv>")
def student_detail(mssv):
    if mssv not in STUDENTS:
        abort(404, description=f"Không có sinh viên với MSSV = {mssv}.")

    info = student_summary(mssv)
    avg_text = (
        "—" if info["average"] is None
        else f"{info['average']:.2f}"
    )

    rows = ""
    for course, score in info["scores"].items():
        rows += f"""
        <tr><td>{escape(course)}</td><td>{escape(score)}</td></tr>
        """

    class_url = url_for("student_list", lop=info["lop"])
    export_url = url_for("student_export", mssv=mssv)
    short_url = url_for("student_short", mssv=mssv)

    body = f"""
    <p>Họ tên: {escape(info['name'])}</p>
    <p>MSSV: {escape(mssv)}</p>
    <p>Lớp: <a href="{escape(class_url)}">{escape(info['lop'])}</a></p>
    <p>Điểm TB: {escape(avg_text)}</p>
    <p>Xếp loại: {escape(info['rank'])}</p>
    <table border="1" cellpadding="6">
        <tr><th>Học phần</th><th>Điểm</th></tr>
        {rows}
    </table>
    <p><a href="{escape(export_url)}">Tải bảng điểm (CSV)</a></p>
    <p>Link rút gọn: <a href="{escape(short_url)}">{escape(short_url)}</a></p>
    """
    return layout(info["name"], body)


@app.route("/sv/<mssv>")
def student_short(mssv):
    return redirect(
        url_for("student_detail", mssv=mssv), code=301
    )


@app.route("/students/<mssv>/export")
def student_export(mssv):
    if mssv not in STUDENTS:
        abort(404, description=f"Không có sinh viên với MSSV = {mssv}.")

    output = StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(["hoc_phan", "diem"])
    writer.writerows(STUDENTS[mssv]["scores"].items())

    response = make_response(output.getvalue())
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    response.headers["Content-Disposition"] = (
        f"attachment; filename=diem_{mssv}.csv"
    )
    return response