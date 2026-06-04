from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "網站成功運行"

if __name__ == "__main__":
    app.run()
