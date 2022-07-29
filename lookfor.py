from bs4 import BeautifulSoup
import requests
import re
from analize import analisis

# this one gets user input and scrapes the website for job offers
# then sends to the helper function the description to analize and store relevant data


# define brower agent to show
agent = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0'}

#  Estrae la HomePage e tira fuori un "object" che rappresenta il DOM della webpage
if __name__ == '__main__':
    def main():

        job = transform(extract(0))
        with open('block_of_text.txt', 'w') as raw_text:
            for j in job:
                # print(j)
                # print('\n')
                # print(retreive_description(pull_listing_data('https://it.indeed.com' + j['job_link'])))
                # count_desc += 1
                # print('\n')
                # print('=======================================')
                # print('\n')
                raw_text.write(retreive_description(pull_listing_data('https://it.indeed.com' + j['job_link'])))

        analisis()

    def format_entry(entry):
        # replace space with '+' from regEx
        formatted = re.sub(r"\s+", '+', entry)
        return formatted

    def extract(page):

        # ask for user input and formats it
        # TEMPORARY COMMENT
        # place = format_entry(input('Where to search? '))
        # job_search = format_entry(input('What to search for? '))

        # REMOVE THIS AUTOMATION
        place = 'Besana+in+brianza'
        job_search = 'developer+junior'

        # page 1 starts at 0, then increments of 10
        # ad user input variables for job Position & area as func param
        url = f'https://it.indeed.com/jobs?q={job_search}&l={place}%2C+Lombardia&start={page}&pp=gQAPAAAAAAAAAAAAAAAB3d8PgwAUAQAEbIA5ge2ct_D9OUJ6C26CwdAAAA&vjk=1034e4c2c9378470'

        r = requests.get(url, agent)
        # returns the DOM object
        soup = BeautifulSoup(r.content, 'html.parser')
        return soup

    def transform(soup):
        jobList = []
        # all the card divs
        divs = soup.find_all('div', class_='job_seen_beacon')

        for item in divs:
            # job title is in the <a> tag as text
            jobTitle = item.find('a').text.strip()
            companyName = item.find('span', class_='companyName').text.strip()
            description = item.find('div', class_='job-snippet').text.strip()
            location = item.find('div', class_='companyLocation').text.strip()
            # link is in the <a> tag as the title but as an href attribute
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

        description = jobSoup.find(
            'div', {'id': 'jobDescriptionText'}).text.strip()

        return description.strip().lower()
        #  TODO call for analizing the text in the description


main()