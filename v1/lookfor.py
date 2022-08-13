from analize import analisis, print_to_file, pie_chart
from bs4 import BeautifulSoup
import requests
import re
import sys
import time

# this one gets user input and scrapes the website for job offers
# then sends to the helper function the description to analize and store relevant data

# define brower agent to show
agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0'}

#  Estrae la HomePage e tira fuori un "object" che rappresenta il DOM della webpage

# ===========================================================
if __name__ == '__main__':
    def main():

        start_time = time.time()
        page = 0
        dev_mode = False # False DEFAULT VAL
        searched_ids = set()
        chart = False

        if len(sys.argv) > 1:
            page, dev_mode, chart= argv_commands(sys.argv)


        # ask for user input and formats it
        place = format_entry(input('Where to search? '))
        job_search = format_entry(input('What to search for? '))

        # creates a lists from function
        jobList = extract_from_page(page, place, job_search)

        # for every element of the list open the job page and extract the description as lowercase text
        for j in jobList:
            # if the job 'id' is not in the set of already searched
            if j['id'] not in searched_ids:
                # add it to the set
                searched_ids.add(j['id'])
                # pull the listing for the offer
                page_object = pull_listing_data('https://it.indeed.com' + j['job_link'])
                try:
                    description = get_description(page_object)
                except AttributeError:
                    sys.exit("Service on Indeed temporarily unavailable")
                # for every job page that has not yet been analized
                #  call analisis to do string match
                analisis(description)

        # dev_mode trigger
        if dev_mode == True:
            timing = time.time() - start_time
            print_to_file(dev_mode, timing, searched_ids, jobList, url, job_search, place)
        elif chart == True:
            pie_chart()
        else:
            #if no dev_mode, function has default parameters
            print_to_file(ids=searched_ids)

# end of main()
# ===========================================================
    def argv_commands(args, dev_mode=False, chart=False):
        usage_message = "Usage: $ python3 lookfor.py [pages 1-5, default=1] [dev_mode, default=OFF]"

        # if 1 argum is "help" print help message
        if len(args) == 2 and args[1].lower() in ('help', '--help'):
            sys.exit(help())

        # if more than 2 arguments
        elif len(args) > 3:
            sys.exit(f"Invalid number of arguments!!!! \n{usage_message}")
        # if 1 or 2 arguments passed

        elif len(args) >= 2:
            # but if arguments are 2 and the second is 'dev_mode'
            if len(args) == 3 and args[2].lower() in ('-g', '-c', '--graph', '--chart'):
                chart = True
            if len(args) == 3 and args[2] == 'dev_mode':
                    # set developer mode as True
                dev_mode = True
            # if argv[1] is a number convert as page int
            try:
                page = int(args[1])
                # if dev_mode active, list up to 15 pages
                if dev_mode == True:
                    if page in range(1, 16):
                        page = (page - 1) * 10
                    else:
                        sys.exit("Error: Dev_mode only accept numbers 1 to 15")
                # only accept 1-5
                else: #if dev_mode is off
                    if page in range(1, 6):
                        page = (page - 1) * 10
                    else:
                        sys.exit("Error: can only accept numbers 1 to 5")
            # if argv[1] not a number
            except ValueError:
                sys.exit(f"!!! ERROR - not a number!!! \n{usage_message}")

        return page, dev_mode, chart

# ===========================================================

    # formats user input to match url specifications
    def format_entry(entry):
        # replace space with '+' with regular expression
        # strip trailing whitespaces
        formatted = re.sub(r"\s+", '+', entry.strip())

        return formatted
# ===========================================================
    def extract_from_page(page, place, job_search):
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
        global url
        # page 1 starts at 0, then increments of 10
        url = f'https://it.indeed.com/jobs?q={job_search}&l={place}&start={page}&vjk=ab0f880e61368268'
        # url_usa = f'https://www.indeed.com/jobs?q={job_search}&l={place}&start={page}&vjk=ab0f880e61368268'

        r = requests.get(url, agent)
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

        r = requests.get(job_link, agent)
        jobSoup = BeautifulSoup(r.content, 'html.parser')

        return jobSoup

# ===========================================================
    # returns the text for the job offer description
    def get_description(jobSoup):

        description = jobSoup.find('div', {'id': 'jobDescriptionText'}).text.strip()

        return description.strip().lower()

# ===========================================================

    def help():
        print("usage: python3 lookfor.py [number of pages, default=1][dev_mode, default=OFF]")
        print("dev_mode logs number of matches, number of offers searched and expands the limit to 15 pages")

main()