from flask import Flask

app = Flask(__name__)


@app.route("/")
def imgResp():
    return "Hello World!"
