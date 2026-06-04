from flask import Flask, request
import pandas as pd
import os
import requests
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


# =========================
# Home
# =========================


@app.route("/")
def home():

    return """

<!DOCTYPE html>

<html lang="zh-HK">

<head>

<meta charset="utf-8">

<title>香港手機月費及寬頻比較</title>

<meta
name="description"
content="比較香港最新5G手機月費及家居寬頻優惠">

<meta
name="viewport"
content="width=device-width, initial-scale=1">

<link
href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
rel="stylesheet">

<link
href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css"
rel="stylesheet">

<style>

body {

    background: #f5f7fb;

}

.hero {

    background:
    linear-gradient(
        135deg,
        #0d6efd,
        #6610f2
    );

    color: white;

    padding: 100px 20px;

    border-radius: 25px;

}

.card-custom {

    border: none;

    border-radius: 20px;

    transition: 0.3s;

}

.card-custom:hover {

    transform: translateY(-5px);

}

.btn-custom {

    border-radius: 50px;

    padding: 12px 24px;

    font-weight: bold;

}

.footer {

    color: #777;

    font-size: 14px;

}

</style>

</head>

<body>

<nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">

<div class="container">

<a class="navbar-brand fw-bold" href="/">
HK Plan Compare
</a>

</div>

</nav>

<div class="container py-5">

<div class="hero text-center shadow">

<h1 class="display-4 fw-bold mb-3">
香港手機及寬頻比較
</h1>

<p class="lead mb-4">

比較最新：

5G 月費｜
手機優惠｜
家居寬頻

</p>

<a
href="/mobile"
class="btn btn-light btn-lg btn-custom me-2">

<i class="bi bi-phone"></i>

手機月費

</a>

<a
href="/broadband"
class="btn btn-warning btn-lg btn-custom">

<i class="bi bi-wifi"></i>

家居寬頻

</a>

</div>

<div class="row mt-5">

<div class="col-md-6 mb-4">

<div class="card shadow-lg card-custom h-100">

<div class="card-body text-center p-5">

<div class="mb-4">

<i
class="bi bi-phone"
style="font-size:60px;color:#0d6efd;">
</i>

</div>

<h3 class="fw-bold">
手機月費比較
</h3>

<p class="text-muted">

比較：

CMHK｜
3HK｜
CSL｜
SmarTone

最新 5G 月費優惠

</p>

<a
href="/mobile"
class="btn btn-primary btn-custom">

立即比較

</a>

</div>

</div>

</div>

<div class="col-md-6 mb-4">

<div class="card shadow-lg card-custom h-100">

<div class="card-body text-center p-5">

<div class="mb-4">

<i
class="bi bi-router"
style="font-size:60px;color:#198754;">
</i>

</div>

<h3 class="fw-bold">
家居寬頻比較
</h3>

<p class="text-muted">

比較：

HKBN｜
HGC｜
網上行

最新光纖寬頻優惠

</p>

<a
href="/broadband"
class="btn btn-success btn-custom">

查看寬頻

</a>

</div>

</div>

</div>

</div>

<div class="card shadow-lg border-0 mt-5">

<div class="card-body p-5">

<h2 class="fw-bold mb-4 text-center">

免費獲取最新優惠

</h2>

<form action="/submit" method="POST">

<div class="row">

<div class="col-md-6 mb-3">

<label class="form-label fw-bold">
姓名
</label>

<input
type="text"
name="name"
class="form-control form-control-lg"
required>

</div>

<div class="col-md-6 mb-3">

<label class="form-label fw-bold">
電話
</label>

<input
type="text"
name="phone"
class="form-control form-control-lg"
required>

</div>

</div>

<div class="mb-4">

<label class="form-label fw-bold">
現用供應商
</label>

<select
name="provider"
class="form-select form-select-lg">

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
class="btn btn-warning btn-lg w-100 btn-custom">

<i class="bi bi-lightning-charge-fill"></i>

立即查詢優惠

</button>

</form>

</div>

</div>

<div class="text-center mt-5 footer">

© 2026 HK Plan Compare

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

<!DOCTYPE html>

<html lang="zh-HK">

<head>

<meta charset="utf-8">

<title>手機月費比較</title>

<meta
name="viewport"
content="width=device-width, initial-scale=1">

<link
href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
rel="stylesheet">

<link
href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css"
rel="stylesheet">

<style>

body {

    background: #f5f7fb;

}

.plan-card {

    border: none;

    border-radius: 20px;

    transition: 0.3s;

}

.plan-card:hover {

    transform: translateY(-5px);

}

.price {

    font-size: 40px;

    font-weight: bold;

    color: #0d6efd;

}

.data {

    font-size: 18px;

}

.badge-best {

    font-size: 14px;

}

</style>

</head>

<body>

<nav class="navbar navbar-dark bg-primary shadow-sm">

<div class="container">

<a class="navbar-brand fw-bold" href="/">
HK Plan Compare
</a>

</div>

</nav>

<div class="container py-5">

<div class="d-flex justify-content-between align-items-center mb-4">

<h1 class="fw-bold">

<i class="bi bi-phone"></i>

手機月費比較

</h1>

<a href="/" class="btn btn-outline-secondary">
返回首頁
</a>

</div>

<div class="row">

"""

        for index, row in df.iterrows():

            badge = ""

            if index == df.index[0]:

                badge = """

                <span class="badge bg-danger badge-best mb-3">
                最平推薦
                </span>

                """

            html += f"""

<div class="col-md-4 mb-4">

<div class="card shadow-lg plan-card h-100">

<div class="card-body p-4 text-center">

{badge}

<h4 class="fw-bold mb-3">

{row['provider']}

</h4>

<div class="price">

${row['fee']}

</div>

<p class="text-muted">
每月月費
</p>

<hr>

<div class="data mb-3">

<i class="bi bi-wifi"></i>

{row['data']}

</div>

<button class="btn btn-primary w-100 rounded-pill">

立即申請

</button>

</div>

</div>

</div>

"""

        html += """

</div>

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

<!DOCTYPE html>

<html lang="zh-HK">

<head>

<meta charset="utf-8">

<title>家居寬頻比較</title>

<meta
name="viewport"
content="width=device-width, initial-scale=1">

<link
href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
rel="stylesheet">

<link
href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css"
rel="stylesheet">

<style>

body {

    background: #f5f7fb;

}

.plan-card {

    border: none;

    border-radius: 20px;

    transition: 0.3s;

}

.plan-card:hover {

    transform: translateY(-5px);

}

.price {

    font-size: 40px;

    font-weight: bold;

    color: #198754;

}

.speed {

    font-size: 18px;

}

.badge-best {

    font-size: 14px;

}

</style>

</head>

<body>

<nav class="navbar navbar-dark bg-success shadow-sm">

<div class="container">

<a class="navbar-brand fw-bold" href="/">
HK Plan Compare
</a>

</div>

</nav>

<div class="container py-5">

<div class="d-flex justify-content-between align-items-center mb-4">

<h1 class="fw-bold">

<i class="bi bi-router"></i>

家居寬頻比較

</h1>

<a href="/" class="btn btn-outline-secondary">
返回首頁
</a>

</div>

<div class="row">

"""

        for index, row in df.iterrows():

            badge = ""

            if index == df.index[0]:

                badge = """

                <span class="badge bg-danger badge-best mb-3">
                最平推薦
                </span>

                """

            html += f"""

<div class="col-md-4 mb-4">

<div class="card shadow-lg plan-card h-100">

<div class="card-body p-4 text-center">

{badge}

<h4 class="fw-bold mb-3">

{row['provider']}

</h4>

<div class="price">

${row['fee']}

</div>

<p class="text-muted">
每月月費
</p>

<hr>

<div class="speed mb-3">

<i class="bi bi-lightning-charge-fill"></i>

{row['speed']}

</div>

<button class="btn btn-success w-100 rounded-pill">

立即申請

</button>

</div>

</div>

</div>

"""

        html += """

</div>

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

        payload = {
            "name": name,
            "phone": phone,
            "provider": provider
        }

        # 你的 Google Apps Script Web App URL
        url = "https://script.google.com/macros/s/AKfycbyCaFVQsTMEiU1C4rMRD8yGxYr5DI_5Z563BrMJejmSwOFngIuibN2G0GsxW-HSs5Fu/exec"

        response = requests.post(
            url,
            json=payload,
            timeout=20
        )

        return f"""

        <html>

        <head>
        <meta charset="utf-8">
        </head>

        <body>

        <h2>成功提交</h2>

        <p>Status Code: {response.status_code}</p>

        <pre>{response.text}</pre>

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
# Health
# =========================

@app.route("/health")
def health():
    return "OK"


@app.route("/test")
def test():

    return requests.__version__


# =========================
# Run
# =========================

if __name__ == "__main__":
    app.run(debug=True)
