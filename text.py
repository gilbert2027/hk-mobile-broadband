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
    <html>

    <head>
        <title>香港手機及寬頻比較</title>
    </head>

    <body>

        <h1>香港手機及寬頻比較</h1>

        <p>
        比較香港最新手機月費及家居寬頻優惠
        </p>

        <hr>

        <h2>查看計劃</h2>

        <a href="/mobile">手機月費比較</a>

        <br><br>

        <a href="/broadband">家居寬頻比較</a>

        <hr>

        <h2>免費獲取最新優惠</h2>

        <form action="/submit" method="post">

            姓名：<br>
            <input type="text" name="name" required>

            <br><br>

            電話：<br>
            <input type="text" name="phone" required>

            <br><br>

            現時供應商：<br>

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
                立即查詢
            </button>

        </form>

    </body>

    </html>
    """


@app.route("/mobile")
def mobile():

    df = pd.read_csv(CSV_PATH)

    df = df[df["category"] == "mobile"]

    html = """
    <h1>手機月費比較</h1>

    <table border='1' cellpadding='10'>

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
    """

    return html


@app.route("/broadband")
def broadband():

    df = pd.read_csv(CSV_PATH)

    df = df[df["category"] == "broadband"]

    html = """
    <h1>家居寬頻比較</h1>

    <table border='1' cellpadding='10'>

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
    """

    return html


@app.route("/mobile/cmhk")
def cmhk():

    return """
    <h1>CMHK 5G 月費計劃比較</h1>

    <p>
    CMHK 提供多種 5G 月費計劃，
    適合一般上網、影片及遊戲用戶。
    </p>

    <a href="/">返回首頁</a>
    """


@app.route("/mobile/3hk")
def hk3():

    return """
    <h1>3HK 月費計劃比較</h1>

    <p>
    3HK 提供不同數據用量及漫遊優惠。
    </p>

    <a href="/">返回首頁</a>
    """


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

            f.write("name,phone,provider\n")

    with open(
        LEADS_PATH,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            f"{name},{phone},{provider}\n"
        )

    return """
    <h2>提交成功</h2>

    <p>
    我們稍後會與你聯絡。
    </p>

    <a href="/">返回首頁</a>
    """


if __name__ == "__main__":
    app.run(debug=True)
