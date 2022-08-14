from distutils.log import debug
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/home")
@app.route("/index")
def index():

    return render_template("home.html")

@app.route("/start")
def start():

    return render_template("start.html")
    ''
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)