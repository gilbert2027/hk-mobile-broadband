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

流通通訊

</a>

<button
class="navbar-toggler"
type="button"
data-bs-toggle="collapse"
data-bs-target="#navbarNav">

<span class="navbar-toggler-icon"></span>

</button>

<div
class="collapse navbar-collapse"
id="navbarNav">

<ul class="navbar-nav ms-auto">

<li class="nav-item">

<a class="nav-link" href="/">

主頁

</a>

</li>

<li class="nav-item">

<a class="nav-link" href="/mobile">

手機月費

</a>

</li>

<li class="nav-item">

<a class="nav-link" href="/broadband">

家居寬頻

</a>

</li>

<li class="nav-item">

<a class="nav-link" href="https://wa.me/85254838282?text=我想查詢" target="_blank">

聯絡我們

</a>

</li>

</ul>

</div>

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

即時獲取最新轉台優惠

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
    
        df = pd.read_csv(CSV_PATH)
    
        df = df[df["category"] == "mobile"].copy()
    
        df["fee"] = pd.to_numeric(df["fee"], errors="coerce")
    
        df = df.dropna(subset=["fee"])
    
        provider = request.args.get("provider")
        max_fee = request.args.get("max_fee")
    
        providers = sorted(df["provider"].dropna().unique())
    
        if provider:
            df = df[df["provider"] == provider]
    
        if max_fee:
            df = df[df["fee"] <= int(max_fee)]
    
        df = df.sort_values("fee")
    
        html = """


<!DOCTYPE html>

<html lang="zh-HK">

<head>

<meta charset="utf-8">

<title>香港手機月費比較</title>

<meta name="viewport"
content="width=device-width, initial-scale=1">

<meta name="description"
content="比較香港最新5G手機月費優惠">

<link
href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
rel="stylesheet">

<link
href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css"
rel="stylesheet">

<style>

body{
    background:#f5f7fb;
}

.table-card{
    background:white;
    border-radius:20px;
    padding:25px;
}

</style>

</head>

<body>

<nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">

<div class="container">

<a class="navbar-brand fw-bold" href="/">
流通通訊
</a>

<div class="navbar-nav ms-auto">

<a class="nav-link text-white" href="/">
主頁
</a>

<a class="nav-link text-white" href="/mobile">
手機月費
</a>

<a class="nav-link text-white" href="/broadband">
家居寬頻
</a>

</div>

</div>

</nav>

<div class="container py-5">

<h1 class="fw-bold mb-4">

<i class="bi bi-phone"></i>

手機月費比較

</h1>

<div class="alert alert-primary">

現時比較中的手機計劃： <b>
"""


        html += str(len(df))

        html += """


</b>
個

</div>

<form method="GET" class="row g-3 mb-4">

<div class="col-md-6">

<select
name="provider"
class="form-select"
onchange="this.form.submit()">

<option value="">
所有供應商
</option>

"""


        for p in providers:

            selected = ""

            if p == provider:
                selected = "selected"

            html += f"""


<option value="{p}" {selected}>
{p}
</option>

"""


        html += """


</select>

</div>

<div class="col-md-6">

<select
name="max_fee"
class="form-select"
onchange="this.form.submit()">

<option value="">
所有價錢
</option>

<option value="100">
$100以下
</option>

<option value="150">
$150以下
</option>

<option value="200">
$200以下
</option>

<option value="300">
$300以下
</option>

</select>

</div>

</form>

<div class="table-card shadow">

<div class="table-responsive">

<table class="table table-striped table-hover align-middle">

<thead class="table-dark">

<tr>

<th>供應商</th>

<th>計劃</th>

<th>月費</th>

<th>數據</th>

<th>合約</th>

<th>特色</th>

<th>查詢</th>

</tr>

</thead>

<tbody>

"""


        for row in df.itertuples(index=False):

            html += f"""


<tr>

<td>{row.provider}</td>

<td>{row.plan_name}</td>

<td>${int(row.fee)}</td>

<td>{row.data}</td>

<td>{row.contract}</td>

<td>{row.remark}</td>

<td>

<a
href="https://wa.me/85254838282?text=我想了解 {row.provider} {row.plan_name}"
target="_blank"
class="btn btn-success btn-sm">

<i class="bi bi-whatsapp"></i>

WhatsApp

</a>

</td>

</tr>

"""


        html += """


</tbody>

</table>

</div>

</div>

</div>

</body>

</html>

"""


        return html

    except Exception as e:

        return f"<pre>{str(e)}</pre>"







# =========================
# Broadband
# =========================

@app.route("/broadband")
def broadband():

    try:

    df = pd.read_csv(CSV_PATH)

    df = df[df["category"] == "broadband"].copy()

    df["fee"] = pd.to_numeric(df["fee"], errors="coerce")

    df = df.dropna(subset=["fee"])

    provider = request.args.get("provider")
    max_fee = request.args.get("max_fee")

    providers = sorted(df["provider"].dropna().unique())

    if provider:
        df = df[df["provider"] == provider]

    if max_fee:
        df = df[df["fee"] <= int(max_fee)]

    df = df.sort_values("fee")

    html = """


<!DOCTYPE html>

<html lang="zh-HK">

<head>

<meta charset="utf-8">

<title>香港家居寬頻比較</title>

<meta name="viewport"
content="width=device-width, initial-scale=1">

<meta name="description"
content="比較香港最新家居寬頻優惠">

<link
href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
rel="stylesheet">

<link
href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css"
rel="stylesheet">

<style>

body{
    background:#f5f7fb;
}

.table-card{
    background:white;
    border-radius:20px;
    padding:25px;
}

</style>

</head>

<body>

<nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">

<div class="container">

<a class="navbar-brand fw-bold" href="/">
流通通訊
</a>

<div class="navbar-nav ms-auto">

<a class="nav-link text-white" href="/">
主頁
</a>

<a class="nav-link text-white" href="/mobile">
手機月費
</a>

<a class="nav-link text-white" href="/broadband">
家居寬頻
</a>

</div>

</div>

</nav>

<div class="container py-5">

<h1 class="fw-bold mb-4">

<i class="bi bi-router"></i>

家居寬頻比較

</h1>

<div class="alert alert-success">

現時比較中的寬頻計劃： <b>
"""


        html += str(len(df))

        html += """


</b>
個

</div>

<form method="GET" class="row g-3 mb-4">

<div class="col-md-6">

<select
name="provider"
class="form-select"
onchange="this.form.submit()">

<option value="">
所有供應商
</option>

"""


    for p in providers:

        selected = ""

        if p == provider:
            selected = "selected"

        html += f"""


<option value="{p}" {selected}>
{p}
</option>

"""


    html += """


</select>

</div>

<div class="col-md-6">

<select
name="max_fee"
class="form-select"
onchange="this.form.submit()">

<option value="">
所有價錢
</option>

<option value="100">
$100以下
</option>

<option value="150">
$150以下
</option>

<option value="200">
$200以下
</option>

</select>

</div>

</form>

<div class="table-card shadow">

<div class="table-responsive">

<table class="table table-striped table-hover align-middle">

<thead class="table-dark">

<tr>

<th>供應商</th>

<th>計劃</th>

<th>月費</th>

<th>速度</th>

<th>合約</th>

<th>特色</th>

<th>查詢</th>

</tr>

</thead>

<tbody>

"""


    for row in df.itertuples(index=False):

        html += f"""


<tr>

<td>{row.provider}</td>

<td>{row.plan_name}</td>

<td>${int(row.fee)}</td>

<td>{row.speed}</td>

<td>{row.contract}</td>

<td>{row.remark}</td>

<td>

<a
href="https://wa.me/85254838282?text=我想了解 {row.provider} {row.plan_name}"
target="_blank"
class="btn btn-success btn-sm">

WhatsApp

</a>

</td>

</tr>

"""


    html += """


</tbody>

</table>

</div>

</div>

</div>

</body>

</html>

"""


    return html

except Exception as e:

    return f"<pre>{str(e)}</pre>"









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

            <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">

            <div class="container">

            <a class="navbar-brand fw-bold" href="/">

            流通通訊

            </a>

            <button
            class="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNav">

            <span class="navbar-toggler-icon"></span>

            </button>

            <div
            class="collapse navbar-collapse"
            id="navbarNav">

            <ul class="navbar-nav ms-auto">

            <li class="nav-item">

            <a class="nav-link" href="/">

            主頁

            </a>

            </li>

            <li class="nav-item">

            <a class="nav-link" href="/mobile">

            手機月費

            </a>

            </li>

            <li class="nav-item">

            <a class="nav-link" href="/broadband">

            家居寬頻

            </a>

            </li>

            <li class="nav-item">

            <a class="nav-link" href="https://wa.me/85254838282?text=我想查詢" target="_blank">

            聯絡我們

            </a>

            </li>

            </ul>

            </div>

            </div>

            </nav>

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


        return """

        <!DOCTYPE html>

        <html lang="zh-HK">

        <head>

        <meta charset="utf-8">

        <title>提交成功</title>

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

        .success-card {

            max-width: 600px;
    
            margin: auto;

            border-radius: 25px;
    
        }

        .success-icon {

            font-size: 80px;

            color: #198754;

        }

        </style>

        </head>

        <body>

        <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">

        <div class="container">

        <a class="navbar-brand fw-bold" href="/">

        流通通訊

        </a>

        <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav">

        <span class="navbar-toggler-icon"></span>

        </button>

        <div
        class="collapse navbar-collapse"
        id="navbarNav">

        <ul class="navbar-nav ms-auto">

        <li class="nav-item">

        <a class="nav-link" href="/">

        主頁

        </a>

        </li>

        <li class="nav-item">

        <a class="nav-link" href="/mobile">

        手機月費

        </a>

        </li>

        <li class="nav-item">

        <a class="nav-link" href="/broadband">

        家居寬頻

        </a>

        </li>

        <li class="nav-item">

        <a class="nav-link" href="https://wa.me/85254838282?text=我想查詢" target="_blank">

        聯絡我們

        </a>

        </li>

        </ul>

        </div>

        </div>

        </nav>

        <div class="container py-5">

        <div class="card shadow-lg border-0 success-card">

        <div class="card-body text-center p-5">

        <div class="success-icon mb-4">

        <i class="bi bi-check-circle-fill"></i>

        </div>

        <h1 class="fw-bold mb-3">
        成功提交查詢
        </h1>

        <p class="lead text-muted mb-4">

        我們已收到你的資料，
        將會盡快聯絡你。

        </p>

        <div class="d-grid gap-3">

        <a
        href="https://wa.me/85254838282"
        target="_blank"
        class="btn btn-success btn-lg rounded-pill">

        <i class="bi bi-whatsapp"></i>

        立即 WhatsApp 查詢

        </a>

        <a
        href="/"
        class="btn btn-outline-secondary rounded-pill">

        返回首頁

        </a>

        </div>

        </div>

        </div>

        </div>

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

        <nav class="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm">

        <div class="container">

        <a class="navbar-brand fw-bold" href="/">

        流通通訊

        </a>

        <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav">

        <span class="navbar-toggler-icon"></span>

        </button>

        <div
        class="collapse navbar-collapse"
        id="navbarNav">

        <ul class="navbar-nav ms-auto">

        <li class="nav-item">

        <a class="nav-link" href="/">

        主頁

        </a>

        </li>

        <li class="nav-item">

        <a class="nav-link" href="/mobile">

        手機月費

        </a>

        </li>

        <li class="nav-item">

        <a class="nav-link" href="/broadband">

        家居寬頻

        </a>

        </li>

        <li class="nav-item">

        <a class="nav-link" href="https://wa.me/85254838282?text=我想查詢" target="_blank">

        聯絡我們

        </a>

        </li>

        </ul>

        </div>

        </div>

        </nav>

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

