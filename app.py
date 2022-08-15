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

dict = {}
searched_ids = set()



@app.route("/")
@app.route("/home")
@app.route("/index")
def index():
    global dict

    with open("list_of_keys.txt", "r") as file:
        for line in file:
            dict[line.strip()] = 0


    return render_template("index.html", dict=dict)

@app.route("/search", methods=['GET', 'POST'])
def start_search():
    global dict
    if request.method == 'POST':
        place = request.form['place']
        job = request.form['job_search']
        jobList = extract_from_page(place=place, job_search=job)
        ordered_result = {}
        ok = ""

        for j in jobList:
            if j['id'] not in searched_ids:
                # add it to the set
                searched_ids.add(j['id'])
                # pull the listing for the offer
                page_object = pull_listing_data('https://it.indeed.com' + j['job_link'])
                try:
                    description = get_description(page_object)
                    ok = "ok"
                except AttributeError:
                    return render_template("error_page.html", error="There was an error on line 45 after page_object")


                # for every job page that has not yet been analized
                #  call analisis to do string match

                # ordered_result= percent_calc(sort_dictionary(analisis(description)))

                ordered_result = {'a':2, 'b': 5, 'c':6}
        # instead of passing various arguments, i put them in a dict and passed to render templates an **unpacked_dict
                print(ordered_result, flush=True)
                app.logger.info('This is info output')
        variables = {"place": place, "job":job, "dict":dict, "result_dict":ordered_result}
        # time.sleep(22)
        # return render_template("result.html", **variables)
        return render_template("result.html", place=place, job=job, dict=dict, result_dict=ordered_result, ok=ok)
    else:
        return error("There was an error on line 55 else>method!=post")

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
        sleep(1)
        app.run()