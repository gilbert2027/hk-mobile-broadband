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


...
@app.route("/submit", methods=["POST"])
def submit():
    return """
    <h2>提交成功</h2>
    <a href="/">返回首頁</a>
    """

if __name__ == "__main__":
    app.run()
