from flask import Flask, request
import pandas as pd
import os

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "plans.csv")
LEADS_PATH = os.path.join(BASE_DIR, "leads.csv")

@app.route("/")
def home():

    return """
<!DOCTYPE html>

<html>

<head>

<title>香港手機及寬頻比較</title>

<meta name="viewport" content="width=device-width, initial-scale=1">

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/css/bootstrap.min.css" rel="stylesheet">

</head>

<body>

<div class="container mt-5">

<h1>
香港手機及寬頻比較
</h1>

<p>
比較香港最新手機月費及家居寬頻優惠
</p>

<div class="row">

<div class="col-md-6">

<div class="card">

<div class="card-body">

<h3>手機月費</h3>

<a class="btn btn-primary"
href="/mobile">

查看手機計劃

</a>

</div>

</div>

</div>

<div class="col-md-6">

<div class="card">

<div class="card-body">

<h3>家居寬頻</h3>

<a class="btn btn-success"
href="/broadband">

查看寬頻計劃

</a>

</div>

</div>

</div>

</div>

</div>

<hr>

<h2>免費獲取最新優惠</h2>

<form action="/submit" method="POST">

姓名:<br>
<input type="text" name="name"><br><br>

電話:<br>
<input type="text" name="phone"><br><br>

現用供應商:<br>

<select name="provider">
<option>CMHK</option>
<option>3HK</option>
<option>CSL</option>
<option>SmarTone</option>
<option>HKBN</option>
<option>HGC</option>
</select>

<br><br>

<button type="submit">
立即查詢優惠
</button>

</form>
"""


@app.route("/mobile")
def mobile():

    df = pd.read_csv(CSV_PATH)

    df = df[df["category"] == "mobile"]

    df = df.sort_values("fee")

    html = """
    <h1>手機月費比較</h1>

    <table border='1'>

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

    html += "</table>"

    return html


@app.route("/broadband")
def broadband():

    df = pd.read_csv(CSV_PATH)

    df = df[df["category"] == "broadband"]

    df = df.sort_values("fee")

    html = """
    <h1>家居寬頻比較</h1>

    <table border='1'>

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

    html += "</table>"

    return html

@app.route("/submit", methods=["POST"])
def submit():

    name = request.form.get("name")
    phone = request.form.get("phone")
    provider = request.form.get("provider")

    if not os.path.exists(LEADS_PATH):

        with open(
            LEADS_PATH,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                "name,phone,provider\n"
            )

    with open(
        LEADS_PATH,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            f"{name},{phone},{provider}\n"
        )

    return """
    <h1>提交成功</h1>

    <p>
    我們已收到你的查詢，
    將盡快聯絡你。
    </p>

    <a href="/">返回首頁</a>
    """

if __name__ == "__main__":
    app.run()
