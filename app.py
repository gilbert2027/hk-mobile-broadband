from flask import Flask

app = Flask(__name__)

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

</body>

</html>
"""


@app.route("/mobile")
def mobile():

    return """
    <h1>手機月費比較</h1>

    <table border='1'>

    <tr>
        <th>供應商</th>
        <th>月費</th>
    </tr>

    <tr>
        <td>CMHK</td>
        <td>$128</td>
    </tr>

    <tr>
        <td>3HK</td>
        <td>$138</td>
    </tr>

    </table>

    <br>

    <a href="/">返回首頁</a>
    """


@app.route("/broadband")
def broadband():

    return """
    <h1>家居寬頻比較</h1>

    <table border='1'>

    <tr>
        <th>供應商</th>
        <th>月費</th>
    </tr>

    <tr>
        <td>HKBN</td>
        <td>$109</td>
    </tr>

    <tr>
        <td>HGC</td>
        <td>$99</td>
    </tr>

    </table>

    <br>

    <a href="/">返回首頁</a>
    """


if __name__ == "__main__":
    app.run()
