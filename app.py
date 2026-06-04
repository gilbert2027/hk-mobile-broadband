from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>香港手機及寬頻比較</h1>

    <a href="/mobile">
    手機月費比較
    </a>

    <br><br>

    <a href="/broadband">
    家居寬頻比較
    </a>
    """

if __name__ == "__main__":
    app.run()
