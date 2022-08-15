from distutils.log import debug
from flask import Flask, render_template


app = Flask(__name__)



@app.route("/")
@app.route("/home")
@app.route("/index")
def index():
    list = []
    with open("list_of_keys.txt", "r") as file:

        for line in file:
            list.append(line)
            
    return render_template("index.html", list=list)

# @app.route("/test")
# def test():

#     return render_template("test.html", visibility="hidden")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)

    # TEMP - reload every secondss
    while True:
        sleep(1)
        app.run()