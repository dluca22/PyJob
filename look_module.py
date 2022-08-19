from analize_module import analisis, elaborate
from bs4 import BeautifulSoup
import requests
import re
import sys
import app
from flask import abort

# then sends to the helper function the description to analize and store relevant data

#  Estrae la HomePage e tira fuori un "object" che rappresenta il DOM della webpage


# ===========================================================
def build_dict():

    default_dict = {}

    with open("list_of_keys.txt", "r") as file:
        for line in file:
            default_dict[line.strip()] = 0
    return  default_dict


# ===========================================================

def search(country , place, job_search, user_dict=None, page=1):
    # empty set

    searched_ids = set()

    default_dict = build_dict()

    jobList = extract_from_page(country=country, place=place, job_search=job_search)

    # se il job id non è nella lista, pull description dal suo link
    for j in jobList:
        if j['id'] not in searched_ids:
            # add it to the set
            searched_ids.add(j['id'])
            # pull the listing for the offer
            try:
                page_object = pull_listing_data(f'http://{country}.indeed.com' + j['job_link'])
                description = get_description(page_object)

            except requests.exceptions.ConnectionAbortedError:
                # chiama la funzione error importata da app
                app.error("Service on Indeed is temporarily unavailable")


            # for every job "id" page that has not yet been analized
            #  call analisis to do string match

            analisis(description, default_dict)

    elaborate()

# ===========================================================

# formats user input to match url specifications
def format_entry(entry):
    # replace space with '+' with regular expression
    # strip trailing whitespaces
    formatted = re.sub(r"\s+", '+', entry.strip())

    return formatted.lower()

# ===========================================================

def extract_from_page(country, place, job_search, page=1):
    # empty job list to be filled with dicts
    jobList = []
    if page == 1:
        # se si cerca pagina 1 il valore passato che accetta url è 0
        jobList = transform(extract(country=country, page=0, place=place, job_search=job_search))
            #if page argument given >1 , loop over and .extend the jobList adding all job dictionaries
    elif page != 1:
        # transform value *10 because url indeed uses 0, 10, 20, 30 to 40(=page 5)
        page = page * 10

        for p in range(1, page , 10):
            jobList.extend(transform(extract(country=country, page=p, place=place, job_search=job_search)))
        if not jobList:
            return app.error("something, something")
    return jobList

# ===========================================================


# returns the HTML of the page
def extract(country, page, place, job_search):
    # global url
    agent = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36 Vivaldi/5.3.2679.70.'}
    # page 1 starts at 0, then increments of 10
    url = f'http://{country}.indeed.com/jobs?q={job_search}&l={place}&start={page}&vjk=ab0f880e61368268'
    # url_usa = f'https://www.indeed.com/jobs?q={job_search}&l={place}&start={page}&vjk=ab0f880e61368268'

    r = requests.get(url, headers=agent)
    if r.status_code == 403:
        sys.exit("Request returned <403>")

    # returns the DOM object
    soup = BeautifulSoup(r.content, 'html.parser')

    return soup

# ===========================================================


# gets all the divs
def transform(soup):
    jobList = []
    # all the card divs
    divs = soup.find_all('div', class_='job_seen_beacon')

    for item in divs:

        # as of now only job_link is relevant, other elements can be integrated later for added functionalities
        # job title is in the <a> tag as text
        jobTitle = item.find('a').text.strip()
        companyName = item.find('span', class_='companyName').text.strip()
        snippet = item.find('div', class_='job-snippet').text.strip()
        location = item.find('div', class_='companyLocation').text.strip()
        id = item.find('a').get('id')
        # link is in the <a> tag as the title BUT as an href attribute
        job_link = item.find('a').get('href')
        # create a job dictionary
        job = {
            'id' : id,
            'title': jobTitle,
            'company': companyName,
            # 'location': location,
            # 'short_description': snippet,
            'job_link': job_link
        }
        # every loop appends a dictionary to the list
        jobList.append(job)
    if not jobList:
        abort("400")
    return jobList

# ===========================================================


# extracts the DOM from every job link page
def pull_listing_data(job_link):
    agent = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36 Vivaldi/5.3.2679.70.'}
    r = requests.get(job_link, headers=agent)

    jobSoup = BeautifulSoup(r.content, 'html.parser')

    return jobSoup


# ===========================================================

# returns the text for the job offer description
def get_description(jobSoup):

    description = jobSoup.find('div', {'id': 'jobDescriptionText'}).text.strip()

    return description.strip().lower()


