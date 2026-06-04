
from flask import Flask, request
import pandas as pd
import os
import sqlite3
import re

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# 防 spam
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["10 per minute"]
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "plans.csv")
DB_PATH = os.path.join(BASE_DIR, "leads.db")


# =========================
# 建立 Database
# =========================

def init_db():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leads (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        name TEXT,
        phone TEXT,
        provider TEXT,

        status TEXT DEFAULT 'new'
    )
    """)

    conn.commit()
    conn.close()


init_db()


# =========================
# Home
# =========================

@app.route("/")
def home():

    return """
<!DOCTYPE html>

<html>

<head>

<meta charset="utf-8">

<title>香港手機月費及家居寬頻比較</title>

<meta
name="description"
content="比較香港最新5G手機月費及家居寬頻優惠">

<meta
name="viewport"
content="width=device-width, initial-scale=1">

<link
href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
rel="stylesheet">

</head>

<body class="bg-light">

<div class="container py-5">

<div class="text-center mb-5">

<h1 class="display-5 fw-bold">
香港手機及寬頻比較
</h1>

<p class="lead">
比較香港最新手機月費及家居寬頻優惠
</p>

</div>

<div class="row">

<div class="col-md-6 mb-4">

<div class="card shadow h-100">

<div class="card-body text-center">

<h3>手機月費</h3>

<p>
比較各大電訊商月費計劃
</p>

<a
href="/mobile"
class="btn btn-primary">

查看手機計劃

</a>

</div>

</div>

</div>

<div class="col-md-6 mb-4">

<div class="card shadow h-100">

<div class="card-body text-center">

<h3>家居寬頻</h3>

<p>
比較最新家居寬頻優惠
</p>

<a
href="/broadband"
class="btn btn-success">

查看寬頻計劃

</a>

</div>

</div>

</div>

</div>

<hr class="my-5">

<div class="card shadow">

<div class="card-body">

<h2 class="mb-4">
免費獲取最新優惠
</h2>

<form action="/submit" method="POST">

<div class="mb-3">

<label class="form-label">
姓名
</label>

<input
type="text"
name="name"
class="form-control"
required>

</div>

<div class="mb-3">

<label class="form-label">
電話
</label>

<input
type="text"
name="phone"
class="form-control"
required>

</div>

<div class="mb-3">

<label class="form-label">
現用供應商
</label>

<select
name="provider"
class="form-select">

<option>CMHK</option>
<option>3HK</option>
<option>CSL</option>
<option>SmarTone</option>
<option>HKBN</option>
<option>HGC</option>

</select>

</div>

<button
type="submit"
class="btn btn-warning w-100">

立即查詢優惠

</button>

</form>

</div>

</div>

</div>

</body>

</html>
"""


# =========================
# Mobile Plans
# =========================

@app.route("/mobile")
def mobile():

    try:

        provider = request.args.get("provider")

        df = pd.read_csv(CSV_PATH)

        df = df[df["category"] == "mobile"]

        if provider:
            df = df[df["provider"] == provider]

        df = df.sort_values("fee")

        html = """
        <html>

        <head>

        <meta charset="utf-8">

        <title>手機月費比較</title>

        <link
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
        rel="stylesheet">

        </head>

        <body class="bg-light">

        <div class="container py-5">

        <h1 class="mb-4">
        手機月費比較
        </h1>

        <table class="table table-bordered table-striped bg-white">

        <tr>
            <th>供應商</th>
            <th>月費</th>
            <th>數據</th>
        </tr>
        """

        for _, row in df.iterrows():

            html += f"""
            <tr>
                <td>{row['provider']}</td>
                <td>${row['fee']}</td>
                <td>{row['data']}</td>
            </tr>
            """

        html += """
        </table>

        <a href="/" class="btn btn-secondary">
        返回首頁
        </a>

        </div>

        </body>

        </html>
        """

        return html

    except Exception as e:

        return f"<h2>錯誤:</h2><pre>{str(e)}</pre>"


# =========================
# Broadband
# =========================

@app.route("/broadband")
def broadband():

    try:

        df = pd.read_csv(CSV_PATH)

        df = df[df["category"] == "broadband"]

        df = df.sort_values("fee")

        html = """
        <html>

        <head>

        <meta charset="utf-8">

        <title>家居寬頻比較</title>

        <link
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
        rel="stylesheet">

        </head>

        <body class="bg-light">

        <div class="container py-5">

        <h1 class="mb-4">
        家居寬頻比較
        </h1>

        <table class="table table-bordered table-striped bg-white">

        <tr>
            <th>供應商</th>
            <th>月費</th>
            <th>速度</th>
        </tr>
        """

        for _, row in df.iterrows():

            html += f"""
            <tr>
                <td>{row['provider']}</td>
                <td>${row['fee']}</td>
                <td>{row['speed']}</td>
            </tr>
            """

        html += """
        </table>

        <a href="/" class="btn btn-secondary">
        返回首頁
        </a>

        </div>

        </body>

        </html>
        """

        return html

    except Exception as e:

        return f"<h2>錯誤:</h2><pre>{str(e)}</pre>"


# =========================
# Submit Lead
# =========================

@app.route("/submit", methods=["POST"])
@limiter.limit("5 per minute")
def submit():

    try:

        name = request.form.get("name")
        phone = request.form.get("phone")
        provider = request.form.get("provider")

        # 電話驗證
        if not re.match(r"^[0-9]{8}$", phone):

            return """
            <html>

            <head>
            <meta charset="utf-8">
            </head>

            <body>

            <h2>電話格式錯誤</h2>

            <a href="/">返回首頁</a>

            </body>

            </html>
            """

        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()

        cursor.execute("""

        INSERT INTO leads (

            name,
            phone,
            provider

        ) VALUES (?, ?, ?)

        """, (name, phone, provider))

        conn.commit()

        conn.close()

        return f"""

        <html>

        <head>
        <meta charset="utf-8">
        </head>

        <body>

        <h2>成功提交</h2>

        <p>姓名：{name}</p>

        <p>電話：{phone}</p>

        <p>供應商：{provider}</p>

        <a href="/">返回首頁</a>

        </body>

        </html>

        """

    except Exception as e:

        return f"""

        <html>

        <head>
        <meta charset="utf-8">
        </head>

        <body>

        <h2>提交失敗</h2>

        <pre>{str(e)}</pre>

        <a href="/">返回首頁</a>

        </body>

        </html>

        """


# =========================
# Admin Dashboard
# =========================

@app.route("/admin")
def admin():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM leads

    ORDER BY id DESC

    """)

    leads = cursor.fetchall()

    conn.close()

    html = """

    <html>

    <head>

    <meta charset="utf-8">

    <title>Admin Dashboard</title>

    <link
    href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
    rel="stylesheet">

    </head>

    <body class="bg-light">

    <div class="container py-5">

    <h1 class="mb-4">
    Leads Dashboard
    </h1>

    <table class="table table-bordered table-striped bg-white">

    <tr>

        <th>ID</th>
        <th>時間</th>
        <th>姓名</th>
        <th>電話</th>
        <th>供應商</th>
        <th>狀態</th>

    </tr>

    """

    for lead in leads:

        html += f"""

        <tr>

            <td>{lead[0]}</td>
            <td>{lead[1]}</td>
            <td>{lead[2]}</td>
            <td>{lead[3]}</td>
            <td>{lead[4]}</td>
            <td>{lead[5]}</td>

        </tr>

        """

    html += """

    </table>

    <a href="/" class="btn btn-secondary">
    返回首頁
    </a>

    </div>

    </body>

    </html>

    """

    return html


# =========================
# Health Check
# =========================

@app.route("/health")
def health():
    return "OK"


@app.route("/test")
def test():

    import requests

    return requests.__version__


# =========================
# Run
# =========================

if __name__ == "__main__":
    app.run(debug=True)

