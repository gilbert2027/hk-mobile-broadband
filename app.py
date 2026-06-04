from flask import Flask, request
import pandas as pd
import os

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "plans.csv")
LEADS_PATH = os.path.join(BASE_DIR, "leads.csv")

@app.route("/")

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
    
from flask import Flask, request
import pandas as pd
import os
import requests

...
@app.route("/submit", methods=["POST"])
def submit():

    name = request.form.get("name")
    phone = request.form.get("phone")
    provider = request.form.get("provider")

    GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzCofXWVKxzFa5-mUTh2ETEGQv_CB-ofTHJ0DA9uXQmMIjxc804AQxfUgyYWPIu6MH5/exec"

    payload = {
        "name": name,
        "phone": phone,
        "provider": provider
    }

    try:
        r = requests.post(
            GOOGLE_SCRIPT_URL,
            json=payload,
            timeout=10
        )

        return f"""
        <h2>成功</h2>
        <p>Status: {r.status_code}</p>
        <p>Response: {r.text}</p>
        <a href="/">返回首頁</a>
        """

    except Exception as e:
        return f"""
        <h2>錯誤</h2>
        <pre>{str(e)}</pre>
        """

if __name__ == "__main__":
    app.run()
