import logging
import time
from flask import Flask, render_template, request, redirect, flash, url_for
from look_module import format_entry, search
from analize_module import elaborate


app = Flask(__name__)
app.secret_key = '01101100'

logging.basicConfig(level=logging.DEBUG)

default_dict = {}
user_dict = {}
# ????  searched_ids = set()

# =============================================================


@app.route("/")
@app.route("/add_keywords", methods=["POST"])
@app.route("/index")
def index():

    global default_dict
    global user_dict

    if request.method == "GET":
        default_dict = build_dict()
    elif request.method == "POST":


        # new_keyword = request.get["keyword"]  ???
        # what user adds
        new_keywords = ["AAAAAA", "BBBBB", "c"]
        if len(new_keywords) != 0:
            for key in new_keywords:
                if key not in default_dict:
                    user_dict[key] = 0

            flash("Your keywords were added!")
            # return index()
            # return redirect(url_for("/"))
            # oppure
            return redirect("/index")
        else:
            flash("No additions.")
            return redirect("/index")




    return render_template("index.html", dict=default_dict, user_dict=user_dict)

# =============================================================
def build_dict():
    global default_dict
    default_dict = {}

    with open("list_of_keys.txt", "r") as file:
        for line in file:
            default_dict[line.strip()] = 0

    return default_dict


# =============================================================



@app.route("/search", methods=['GET', 'POST'])
def start_search():


    if request.method == 'POST':
        # setting variables
        dev_mode = False # False DEFAULT VAL

        start_time = time.time()
        searched_ids = set()
        chart = False
        global default_dict
        global user_dict
        build_dict()

        # test to call function
        # add_keywords()

        # get values from request form
        place = format_entry(request.form['place'])
        job = format_entry(request.form['job_search'])

        ordered_result = {}
        ordered_result = search(place=place, job_search=job, default_dict=default_dict)
        # chiama funzione e ritorna lista (page e logica è definito dentro la funzione )
        # jobList = extract_from_page(place = place, job_search = job)

        ordered_result, finish_time, counter = elaborate()

        timing = round((finish_time - start_time),2)
        return render_template("result.html", place=place, job=job, dict=default_dict, result_dict=ordered_result,timing=timing, counter=counter)
    else:
        return error("There was an error on line 55 else > method !=post")

# =============================================================



@app.route("/error")
def error(error):

    return render_template("error_page.html", error=error)

# =============================================================



# @app.route("/add_keywords", methods=["POST"])
# def add_keywords():
#     global user_dict
#     if request.method == "POST":
#         global default_dict

#         # new_keyword = request.get["keyword"]  ???
#         # what user adds
#         new_keywords = ["AAAAAA", "BBBBB", "c"]

#         for key in new_keywords:
#             if key not in default_dict:
#                 default_dict[key] = 0

#         flash("Your keywords were added!")
#         # return index()
#         # return redirect(url_for("/"))
#         # oppure
#         return redirect(url_for('index'), method="POST")
#     else:
#         return user_dict

# # =============================================================

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)


    # TEMP - reload every second
    while True:
        time.sleep(1)
        app.run()
