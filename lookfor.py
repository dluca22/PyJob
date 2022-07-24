from bs4 import BeautifulSoup
import requests

# define brower agent to show
agent = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0'}

#  Estrae la HomePage e tira fuori un "object" che rappresenta il DOM della webpage

if __name__ == '__main__':
    def main():
        # do
        job = transform(extract(0))
        for j in job:
            print(j)
            print('\n')
            description = job_analizer(job['job_link'])
            print('\n')


    def extract(page):
        # page 1 starts at 0, then increments of 10
        # ad user input variables for job Position & area as func param
        url = f'https://it.indeed.com/jobs?q=developer+junior&l=Besana+in+Brianza%2C+Lombardia&start={page}&pp=gQAPAAAAAAAAAAAAAAAB3d8PgwAUAQAEbIA5ge2ct_D9OUJ6C26CwdAAAA&vjk=1034e4c2c9378470'

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
                'description': description,
                'job_link': job_link
            }
            # every loop appends the dictionary to a list
            jobList.append(job)

        return jobList


    def parse_job(job_link):

        r = requests.get(job_link, agent)
        jobSoup = BeautifulSoup(r.content, 'html.parser')

        return jobSoup


    def job_analizer(jobSoup):

        description = jobSoup.find(
            'div', {'id': 'jobDescriptionText'}).text.strip()
        print(description)
        #  TODO the count for analizing the text in the description


main()