
from flask import Flask, request
import pandas as pd
import os
import requests
import re

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "plans.csv")


@app.route("/")
def home():

    return """

<!DOCTYPE html>

<html lang="zh-HK">

<head>

<meta charset="utf-8">

<title>香港手機及寬頻比較</title>

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
    background: linear-gradient(135deg,#0d6efd,#6610f2);
    color: white;
    padding: 80px 20px;
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

</style>

</head>

<body>

<div class="container py-5">

<div class="hero text-center shadow">

<h1 class="display-4 fw-bold mb-3">
香港手機及寬頻比較
</h1>

<p class="lead mb-4">
比較最新 5G 月費及家居寬頻優惠
</p>

<a
href="/mobile"
class="btn btn-light btn-lg btn-custom me-2">

手機月費

</a>

<a
href="/broadband"
class="btn btn-warning btn-lg btn-custom">

家居寬頻

</a>

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

立即查詢優惠

</button>

</form>

</div>

</div>

</div>

</body>

</html>

"""


@app.route("/mobile")
def mobile():

    try:

        df = pd.read_csv(CSV_PATH)

        df = df[df["category"] == "mobile"]

        df = df.sort_values("fee")

        html = """

<!DOCTYPE html>

<html lang="zh-HK">

<head>

<meta charset="utf-8">

<title>手機月費比較</title>

<meta name="viewport" content="width=device-width, initial-scale=1">

<link
href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
rel="stylesheet">

<style>

body {
    background: #f5f7fb;
}

.plan-card {
    border-radius: 20px;
    overflow: hidden;
    border: none;
}

.price {
    font-size: 42px;
    font-weight: bold;
    color: #0d6efd;
}

</style>

</head>

<body>

<div class="container py-5">

<h1 class="fw-bold mb-4">
手機月費比較
</h1>

<div class="row">

"""

        for index, row in df.iterrows():

            provider_class = "bg-dark text-white"

            if row["provider"] == "HGC":
                provider_class = "bg-danger text-white"

            elif row["provider"] == "HKBN":
                provider_class = "bg-primary text-white"

            elif row["provider"] in ["CSL", "網上行"]:
                provider_class = "bg-warning text-dark"

            badge = ""

            if index == df.index[0]:

                badge = """
<span class="badge bg-danger mb-3">
最平推薦
</span>
"""

            html += f"""

<div class="col-md-4 mb-4">

<div class="card shadow-lg plan-card h-100">

<div class="{provider_class} py-3 text-center fw-bold fs-4">

{row['provider']}

</div>

<div class="card-body text-center p-4">

{badge}

<div class="price">

${row['fee']}

</div>

<p class="text-muted">
每月月費
</p>

<hr>

<p class="fs-5">

{row['data']}

</p>

<a
href="https://wa.me/85291234567?text=我想申請/了解%20{row['provider']}%20{row['data']}%20月費計劃"
target="_blank"
class="btn btn-success w-100 rounded-pill">

WhatsApp 查詢

</a>

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

        return f"<pre>{str(e)}</pre>"


@app.route("/broadband")
def broadband():

    return "<h1>Broadband Page</h1>"


@app.route("/submit", methods=["POST"])
def submit():

    try:

        name = request.form.get("name")
        phone = request.form.get("phone")
        provider = request.form.get("provider")

        if not re.match(r"^[0-9]{8}$", phone):

            return "電話格式錯誤"

        payload = {
            "name": name,
            "phone": phone,
            "provider": provider
        }

        url = "你的 Google Apps Script URL"

        response = requests.post(
            url,
            json=payload,
            timeout=20
        )

        return f"""

<h2>成功提交</h2>

<pre>{response.text}</pre>

<a href="/">返回首頁</a>

"""

    except Exception as e:

        return f"<pre>{str(e)}</pre>"


@app.route("/health")
def health():

    return "OK"


if __name__ == "__main__":

    app.run(debug=True)

