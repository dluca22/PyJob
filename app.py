from crypt import methods
from distutils.log import debug
from glob import glob
import time
from flask import Flask, render_template, request, redirect, url_for, flash
import look_module
from analize_module import analisis, elaborate, percent_calc, sort_dictionary
import sys
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

default_dict = {}
user_dict = {}
# ????  searched_ids = set()

# =============================================================


@app.route("/")
@app.route("/index")
def index():
    global default_dict
    global user_dict

    default_dict = build_dict()


    return render_template("index.html", dict=default_dict)

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
        place = request.form['place']
        job = request.form['job_search']

        ordered_result = {}
        ordered_result = look_module.search(place=place, job_search=job, default_dict=default_dict)
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



@app.route("/add_keywords", methods=["POST"])
def add_keywords():
    global user_dict
    if request.method == "POST":
        global default_dict

        # new_keyword = request.get["keyword"]  ???
        # what user adds
        new_keywords = ["AAAAAA", "BBBBB", "c"]

        for key in new_keywords:
            if key not in default_dict:
                default_dict[key] = 0

        flash("Your keywords were added!")
        # return index()
        # return redirect(url_for("/"))
        # oppure
        return redirect("/")
    else:
        return user_dict

# =============================================================

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)


    # TEMP - reload every second
    while True:
        time.sleep(1)
        app.run()
