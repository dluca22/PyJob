from crypt import methods
from distutils.log import debug
import time
from flask import Flask, render_template, request, redirect, url_for, flash
from look_module import extract_from_page, pull_listing_data, get_description
from analize_module import analisis, percent_calc, sort_dictionary
import sys
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

default_dict = {}
# ????  searched_ids = set()


@app.route("/")
@app.route("/index")
def index():
    global default_dict
    default_dict = build_dict()


    return render_template("index.html", dict=default_dict)


def build_dict():
    default_dict = {}

    with open("list_of_keys.txt", "r") as file:
        for line in file:
            default_dict[line.strip()] = 0

    return default_dict

@app.route("/search", methods=['GET', 'POST'])
def start_search():


    if request.method == 'POST':
        # setting variables
        start_time = time.time()
        dev_mode = False # False DEFAULT VAL
        searched_ids = set()
        chart = False
        global default_dict

        # test to call function
        add_keywords()

        # get values from request form
        place = request.form['place']
        job = request.form['job_search']

        # chiama funzione e ritorna lista (page e logica è definito dentro la funzione )
        jobList = extract_from_page(place = place, job_search = job)
        ordered_result = {}

        # se il job id non è nella lista, pull description dal suo link
        for j in jobList:
            if j['id'] not in searched_ids:
                # add it to the set
                searched_ids.add(j['id'])
                # pull the listing for the offer
                page_object = pull_listing_data('http://it.indeed.com' + j['job_link'])
                try:
                    description = get_description(page_object)

                except AttributeError:
                    return render_template("error_page.html", error="Service on Indeed is temporarily unavailable")


                # for every job page that has not yet been analized
                #  call analisis to do string match
                # with open("list_of_keys.txt", "r") as file:
                #     for line in file:
                #         default_dict[line.strip()] = 0
                ordered_result= sort_dictionary(analisis(description, default_dict))


        # instead of passing various arguments,  put them in a dict and pass that to render templates as an **unpacked_dict

        time.sleep(10)

        return render_template("result.html", place=place, job=job, dict=default_dict, result_dict=ordered_result, jobList=jobList)
    else:
        return error("There was an error on line 55 else > method !=post")

@app.route("/error")
def error(error):

    return render_template("error_page.html", error=error)


# @app.route("/add_keywords", methods=["POST"])
# def add_keywords():

#     if request.method == "POST":
#         global default_dict

#         # new_keyword = request.get["keyword"]  ???
#         # what user adds
#         new_keywords = ["AAAAAA", "BBBBB", "c"]

#         for key in new_keywords:
#             if key not in default_dict:
#                 default_dict[key] = 0

#         flash("Your keywords were added!")
#         return index()
#         # return redirect(url_for("/"))
#         # oppure
        # return redirect("/")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)


    # TEMP - reload every secondss
    while True:
        time.sleep(1)
        app.run()