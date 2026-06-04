from flask import Flask, request
import pandas as pd
import os
import requests

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "plans.csv")


@app.route("/")
def home():

    return """
<!DOCTYPE html>
<html>
<head>

<meta charset="utf-8">

<title>香港手機及寬頻比較</title>

<meta name="viewport" content="width=device-width, initial-scale=1">

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

</head>

<body>

<div class="container mt-5">

<h1 class="mb-3">
香港手機及寬頻比較
</h1>

<p class="lead">
比較香港最新手機月費及家居寬頻優惠
</p>

<div class="row mt-4">

<div class="col-md-6 mb-3">

<div class="card">

<div class="card-body">

<h3>手機月費</h3>

<p>
比較各大電訊商月費計劃
</p>

<a href="/mobile" class="btn btn-primary">
查看手機計劃
</a>

</div>

</div>

</div>

<div class="col-md-6 mb-3">

<div class="card">

<div class="card-body">

<h3>家居寬頻</h3>

<p>
比較最新家居寬頻優惠
</p>

<a href="/broadband" class="btn btn-success">
查看寬頻計劃
</a>

</div>

</div>

</div>

</div>

<hr class="my-5">

<h2>免費獲取最新優惠</h2>

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
class="btn btn-warning">

立即查詢優惠

</button>

</form>

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
        <html>
        <head>
        <meta charset="utf-8">
        <title>手機月費比較</title>
        </head>

        <body>

        <h1>手機月費比較</h1>

        <table border="1" cellpadding="10">

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

        <br>

        <a href="/">返回首頁</a>

        </body>
        </html>
        """

        return html

    except Exception as e:
        return f"<h2>錯誤:</h2><pre>{str(e)}</pre>"


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
        </head>

        <body>

        <h1>家居寬頻比較</h1>

        <table border="1" cellpadding="10">

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

        <br>

        <a href="/">返回首頁</a>

        </body>
        </html>
        """

        return html

    except Exception as e:
        return f"<h2>錯誤:</h2><pre>{str(e)}</pre>"

@app.route("/submit", methods=["POST"])
def submit():

    name = request.form.get("name")
    phone = request.form.get("phone")
    provider = request.form.get("provider")

    payload = {
        "name": name,
        "phone": phone,
        "provider": provider
    }

    url = "https://script.google.com/macros/s/AKfycbzCofXWVKxzFa5-mUTh2ETEGQv_CB-ofTHJ0DA9uXQmMIjxc804AQxfUgyYWPIu6MH5/exec"

    try:

        response = requests.post(
            url,
            json=payload,
            timeout=10
        )

        return """
        <html>
        <head>
            <meta charset="utf-8">
            <title>提交成功</title>
        </head>
        <body>
            <h2>提交成功</h2>
            <p>我們已收到您的資料。</p>
            <a href="/">返回首頁</a>
        </body>
        </html>
        """

    except Exception as e:

        return f"""
        <html>
        <head>
            <meta charset="utf-8">
            <title>提交失敗</title>
        </head>
        <body>
            <h2>提交失敗</h2>
            <pre>{str(e)}</pre>
            <a href="/">返回首頁</a>
        </body>
        </html>
        """


@app.route("/health")
def health():
    return "OK"
@app.route("/test")
def test():
    import requests
    return requests.__version__

if __name__ == "__main__":
    app.run(debug=True)
