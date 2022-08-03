from analize import analisis, print_to_file
from arguments import help
from bs4 import BeautifulSoup
import requests
import re
import sys

# this one gets user input and scrapes the website for job offers
# then sends to the helper function the description to analize and store relevant data

# define brower agent to show
agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0'}

#  Estrae la HomePage e tira fuori un "object" che rappresenta il DOM della webpage
if __name__ == '__main__':
    def main():

        page = 0
        usage_message = "Usage: $ python3 lookfor.py [pages 1-5, default=1] [dev_mode, default=OFF]"
        dev_mode = False
        jobList = []

        # if 1 argum is help print help message
        if len(sys.argv) == 2 and sys.argv[1].lower() == 'help':
            sys.exit(usage_message)

        # if 1 or 2 arguments passed
        elif len(sys.argv) >= 2:

            if len(sys.argv) == 3 and sys.argv[2] == 'dev_mode':
                    # set developer mode as True
                dev_mode = True
            # if argv[1] is a number convert as page int
            try:
                page = int(sys.argv[1])
                # only accept 1-5
                if page in range(1, 6):
                    page = (page - 1) * 10
                else:
                    sys.exit("Error: can only accept numbers 1 to 5")
            # if argv[1] not a number
            except ValueError:
                sys.exit(f"!!! ERROR - not a number!!! \n{usage_message}")

            # but if arguments are 2 and the second is 'dev_mode'

        # if more than 2 arguments
        if len(sys.argv) > 3:
            sys.exit(f"Invalid number of arguments!!!! \n{usage_message}")


        # returns a list of dictionary for every job listing in the page
        if page == 0:
            jobList = transform(extract(0))
            print(jobList)
            print(len(jobList))
            sys.exit("1")
        elif page != 0:
            # in range da page 0 a page +1(8)inclusive page) step 10
            for p in range(0, page +1, 10):
                
                jobList.extend(transform(extract(p)))
            print(jobList)
            print(len(jobList))
            sys.exit("2+")


        # for every element of the list open the job page and extract the description as lowercase text
        for j in jobList:
            page_object = pull_listing_data('https://it.indeed.com' + j['job_link'])
            try:
                description = retreive_description(page_object)
            except AttributeError:
                sys.exit("Service on Indeed temporarily unavailable")
            # for every job page, call analize to do string match
            analisis(description)

        # after logging data to the dict, send command to print to file
        # optional arguments (formatted=yes/no)
        print_to_file()

# end of main()



    # formats user input to match url specifications
    def format_entry(entry):
        # replace space with '+' with regular expression
        formatted = re.sub(r"\s+", '+', entry)
        return formatted

    # returns the HTML of the page
    def extract(page):

        # TEMPORARY COMMENTED =========
        # CHIAMARLO IN FUNZIONE MAIN SE NO LO CHIEDE AD OGNI LOOP
        # ask for user input and formats it
        # place = format_entry(input('Where to search? '))
        # job_search = format_entry(input('What to search for? '))
        # TEMPORARY COMMENTED =========

        # REMOVE THIS AUTOMATION
        # place = 'Besana+in+brianza'
        place = 'Milano'
        job_search = 'developer+junior'

        # page 1 starts at 0, then increments of 10
        # ad user input variables for job Position & area as func param
        url = f'https://it.indeed.com/jobs?q={job_search}&l={place}%2C+Lombardia&start={page}&pp=gQAPAAAAAAAAAAAAAAAB3d8PgwAUAQAEbIA5ge2ct_D9OUJ6C26CwdAAAA&vjk=1034e4c2c9378470'

        r = requests.get(url, agent)
        # returns the DOM object
        soup = BeautifulSoup(r.content, 'html.parser')
        return soup

    # retrieves all the divs
    def transform(soup):
        jobList = []
        # all the card divs
        divs = soup.find_all('div', class_='job_seen_beacon')

        for item in divs:

            # as of now only job_link is relevant, other elements can be integrated later for added functionalities
            # job title is in the <a> tag as text
            jobTitle = item.find('a').text.strip()
            companyName = item.find('span', class_='companyName').text.strip()
            description = item.find('div', class_='job-snippet').text.strip()
            location = item.find('div', class_='companyLocation').text.strip()
            # link is in the <a> tag as the title BUT as an href attribute
            job_link = item.find('a').get('href')
            # create a job dictionary
            job = {
                'title': jobTitle,
                'company': companyName,
                # rarely defined but also field is shared with contract duration
                # 'salary' : salary,
                'location': location,
                'short_description': description,
                'job_link': job_link
            }
            # every loop appends a dictionary to the list
            jobList.append(job)

        return jobList

    # extracts the DOM from every job link page
    def pull_listing_data(job_link):

        r = requests.get(job_link, agent)
        jobSoup = BeautifulSoup(r.content, 'html.parser')

        return jobSoup

    # returns the text for the job offer description
    def retreive_description(jobSoup):

        description = jobSoup.find('div', {'id': 'jobDescriptionText'}).text.strip()

        return description.strip().lower()
        #  TODO call for analizing the text in the description


main()