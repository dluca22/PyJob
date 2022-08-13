from bs4 import BeautifulSoup
import requests
import sys


def request(page):
        place = 'Milano'
        job_search = 'junior+developer'
# global url
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36 Vivaldi/5.3.2679.70.'}
        # page 1 starts at 0, then increments of 10
        url2 = 'http://it.indeed.com'
        # only changed https to http
        url = f'http://it.indeed.com/jobs?q={job_search}&l={place}&start={page}&vjk=ab0f880e61368268'
        # url_usa = f'https://www.indeed.com/jobs?q={job_search}&l={place}&start={page}&vjk=ab0f880e61368268'
        print(url)

        x = requests.get(url2, headers=headers)
        r = requests.get(url, headers=headers)

        # x.cookies.clear()

        print(f"{r.status_code} \n {r.request.headers}")
        print(f"{x.status_code} \n {x.request.headers}")



        sys.exit()


def main():
    request(10)


main()