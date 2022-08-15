from distutils.log import debug
from flask import Flask, render_template


app = Flask(__name__)



@app.route("/")
@app.route("/home")
@app.route("/index")
def index():

    dict = {}
    with open("list_of_keys.txt", "r") as file:
        for line in file:
            dict[line.strip()] = 0


    return render_template("index.html", dict=dict)

# @app.route("/test")
# def test():

#     return render_template("test.html", visibility="hidden")

# IDEA per dopo
# def user_added_keys():
            # possiamo creare un dictionary da una list che chiediamo all'user, popolare la list
    # user_input = ["JINJA2", "COBOL", "POSTGRES", "FLAKS"]
            # e con questo metodo creare keys:values con pre-defined value
    # user_custom_dict = dict.fromkeys(user_input, 0)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)

    # TEMP - reload every secondss
    while True:
        sleep(1)
        app.run()