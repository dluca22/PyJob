from distutils.log import debug
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/home")
@app.route("/index")
def index():

    return render_template("index.html")

@app.route("/test")
def test():

    return render_template("test.html", visibility="hidden")
    ''
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)