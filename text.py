from flask import Flask
import pandas as pd
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "plans.csv")

@app.route("/")
def home():

    return """
    <!DOCTYPE html>

    <html>

    <head>

        <title>香港手機及寬頻比較</title>

        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/css/bootstrap.min.css" rel="stylesheet">

    </head>

    <body>

    <div class="container mt-5">

        <h1 class="mb-4">
            香港手機及寬頻比較
        </h1>

        <p>
            比較全港最新月費計劃及寬頻優惠
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

    </body>

    </html>
    """

@app.route("/mobile")
def mobile():

    df = pd.read_csv(CSV_PATH)

    df = df[df["category"] == "mobile"]

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

    html += "</table><br><a href='/'>返回首頁</a>"

    return html


@app.route("/broadband")
def broadband():

    df = pd.read_csv(CSV_PATH)

    df = df[df["category"] == "broadband"]

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

    html += "</table><br><a href='/'>返回首頁</a>"

    return html


if __name__ == "__main__":
    app.run(debug=True)