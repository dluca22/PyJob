from glob import glob
import logging
import time
from flask import Flask, render_template, request, redirect, flash, url_for
from look_module import build_dict, format_entry, search
from analize_module import elaborate, get_count


app = Flask(__name__)
app.secret_key = '01101100'
# app.config['PROPAGATE_EXCEPTIONS'] = True REMOVE??

logging.basicConfig(level=logging.DEBUG)

default_dict = {}
user_dict = {}


# =============================================================


@app.route("/")
@app.route("/index")
def index():

    if request.method == "GET":
        global default_dict

        # maybe do it as a list? since gets built already in look_module
        default_dict = build_dict()
        # can't join user dict here because would be merged in the main dict and not display as separate keys


    return render_template("index.html", dict=default_dict, user_dict=user_dict)

# =============================================================

@app.route("/remove_custom")
def remove_custom():
    user_dict.clear()
    return redirect(url_for("index"))

# =============================================================

@app.route("/search", methods=['GET', 'POST'])
def start_search():

    if request.method == 'POST':
        # setting variables

        start_time = time.time()

        global user_dict

        # get values from request form
        place = format_entry(request.form['place'])
        job = format_entry(request.form['job_search'])
        if request.form['country'] == 'www':
            country = 'www'
        else:
            country = 'it'
        # page 1 returns value 0 that extract_from_page uses to display
        # works even if not converted to int() ?!?
        page = int(request.form['page'])

        # if user keywords are defined
        if not user_dict:
            ordered_result = search(country=country, place=place, job_search=job, page=page)
        else:
            ordered_result = search(country=country, place=place, job_search=job, user_dict=user_dict, page=page)

        if ordered_result == "400 - Invalid search":
            return error(400, msg="Your search was invalid :(")

        ordered_result = elaborate()

        total_time = round((time.time() - start_time),2)


        return render_template("result.html", place=place, job=job, dict=default_dict, result_dict=ordered_result,total_time=total_time, counter=get_count(), pageX=page, countryX=country)

    # if method 'get'
    else:
        return error(403, msg="You can't do THAT /: ")


# =============================================================


@app.route("/error")
def error(code, msg="error"):

    return render_template("error.html", code=code, msg=msg)

# =============================================================



@app.route("/add_keywords", methods=["POST"])
def add_keywords():

    if request.method == "POST":
        global default_dict
        global user_dict

        # gets list of inserted keys from input, split on ","
        new_keywords = request.form["custom_keys"].split(",")
        # inline loop to strip whitespace from keys
        new_keywords = [i.strip() for i in new_keywords]
        # removes keys already present
        if len(new_keywords) > 0:
            for key in new_keywords:
                if key in default_dict or key in user_dict:
                    continue
                else:
                    user_dict[key] = 0

            flash("The keywords have been updated!")
            return redirect(url_for("index"))
        else:
            flash("No additions.")
            return redirect(url_for("index"))

        # return index()
        # return redirect(url_for("/"))
        # oppure
        # return redirect(url_for('index'), method="POST")

# =============================================================
@app.route("/new_search")
def new_search():
    global default_dict
    default_dict.clear()
    return redirect(url_for("index"))
# =============================================================

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)


    # TEMP - reload every second
    while True:
        time.sleep(1)
        app.run()
