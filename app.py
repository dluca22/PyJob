from crypt import methods
from distutils.log import debug
import time
from flask import Flask, render_template, request
from look_module import extract_from_page, pull_listing_data, get_description
from analize_module import analisis, percent_calc, sort_dictionary
import sys
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

dict_from_text = {}
searched_ids = set()



@app.route("/")
@app.route("/home")
@app.route("/index")
def index():
    global dict_from_text

    with open("list_of_keys.txt", "r") as file:
        for line in file:
            dict_from_text[line.strip()] = 0


    return render_template("index.html", dict=dict_from_text)

@app.route("/search", methods=['GET', 'POST'])
def start_search():


    if request.method == 'POST':
        # setting variables
        start_time = time.time()
        dev_mode = False # False DEFAULT VAL
        searched_ids = set()
        chart = False

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
                ordered_result= percent_calc(sort_dictionary(analisis(description)))


        # instead of passing various arguments,  put them in a dict and pass that to render templates as an **unpacked_dict

        time.sleep(10)

        return render_template("result.html", place=place, job=job, dict=dict_from_text, result_dict=ordered_result, jobList=jobList)
    else:
        return error("There was an error on line 55 else > method !=post")

@app.route("/error")
def error(error):

    return render_template("error_page.html", error=error)


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
        time.sleep(1)
        app.run()