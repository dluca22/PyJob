from analize import analisis, print_to_file
from arguments import help
from bs4 import BeautifulSoup
import requests
import re
import sys
import time

agent = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}

def extract(page):
        place = 'Milano'
        job_search = 'junior+developer'

        url = f'https://it.indeed.com/jobs?q={job_search}&l={place}&start={page}&vjk=ab0f880e61368268'
        print(url)

        r = requests.get(url, agent)
        # print("r is ", type(r))
        # returns the DOM object
        soup = BeautifulSoup(r.content, 'html.parser')
        # print("soup is ", type(soup))
        time.sleep(3)
        divs = soup.find_all('div', class_='jobsearch-JobCountAndSortPane-jobCount')
        print("len of divs", len(divs))
        print(divs)

        # with open('test.txt', 'w') as test:
        #     for div in divs:
        #         test.write(div)
        # #         div.find('div', class_="jobsearch-LeftPane")
        # #         # print(div.text)
        # # #     total_listings = soup.find_all('div', class_='jobsearch-JobCountAndSortPane-jobCount')
        # #         # test.write(div.text)

        sys.exit("mio exit")
        # # sys.exit(f'this {len(total_listings)}')

        return soup

def main():
    extract(0)


main()