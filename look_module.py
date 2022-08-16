from analize_module import analisis, elaborate
from bs4 import BeautifulSoup
import requests
import re
import sys
import app

# then sends to the helper function the description to analize and store relevant data
agent = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36 Vivaldi/5.3.2679.70.'}
#  Estrae la HomePage e tira fuori un "object" che rappresenta il DOM della webpage

# ===========================================================

def search(place, job_search, default_dict, user_dict=None, page=0):
    # empty set
    searched_ids = set()

    jobList = extract_from_page(place=place, job_search=job_search)

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
                return app.error("Service on Indeed is temporarily unavailable")


            # for every job page that has not yet been analized
            #  call analisis to do string match

            analisis(description, default_dict)

    elaborate()

# ===========================================================

# formats user input to match url specifications
def format_entry(entry):
    # replace space with '+' with regular expression
    # strip trailing whitespaces
    formatted = re.sub(r"\s+", '+', entry.strip())

    return formatted

# ===========================================================

def extract_from_page(place, job_search, page=0):
    # empty job list to be filled with dicts
    jobList = []
    if page == 0:
        jobList = transform(extract(0, place, job_search))
            #if page argument given >1 , loop over and .extend the jobList adding all job dictionaries
    elif page != 0:
        # in range da page 0 a page +1(8)inclusive page) step 10
        for p in range(0, page +1, 10):
            jobList.extend(transform(extract(p, place, job_search)))
    return jobList

# ===========================================================


# returns the HTML of the page
def extract(page, place, job_search):
    # global url

    # page 1 starts at 0, then increments of 10
    url = f'http://it.indeed.com/jobs?q={job_search}&l={place}&start={page}&vjk=ab0f880e61368268'
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

    return jobList

# ===========================================================


# extracts the DOM from every job link page
def pull_listing_data(job_link):
    global agent
    r = requests.get(job_link, headers=agent)

    jobSoup = BeautifulSoup(r.content, 'html.parser')

    return jobSoup


# ===========================================================

# returns the text for the job offer description
def get_description(jobSoup):

    description = jobSoup.find('div', {'id': 'jobDescriptionText'}).text.strip()

    return description.strip().lower()


