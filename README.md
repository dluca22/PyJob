# PyJob

The idea is a CLI with python to scrape job offers on the main search websites based on Postcode.

Since i've been looking around for job listing for IT/Dev-jobs i've noticed that many of the frameworks and coding languages required in the job offers vary quite noticeably based on the area of search.

Many of the trending languages or framework that are relevant in the US and talked about on media platforms and forums, sometimes are not that relevant where I live (Italy), and it is quite a task to keep up to date on the more relevant skills in my area.

Coding and learning is really fun, but it is also a lot of commitment in terms of time, so it would be ideal for an automation tool to return to the user a list of relevant skills and knowledge (ordered by descending percentage relevance) to have in a particular field, based on the user's search location.

**----- Structure -----**
`lookfor.py` gets user input and scrapes from indeed the job listing, retrieving the listed jobs.
After retrieving sends the job description to `analize.py` that computes the texts and outputs the matching relevant data, then logs the most requested languages/frameworks that are being looked for in the job market.

It will output to a text file with some value for most required skills that later will be processed in a more visual representation (like graphs or charts)

**----- The roadmap -----**

* First iteration would be to have the CLI web scraper working and returning data based on few parameters an user should input to the program.

* Second iteration would be adding a `.JSON` or `.config` file for a user to fill once and the program to execute routinely without re entering the same informations over again.
    *or evaluate if using a question input() to ask for a personalized search (instead of re configuring the config file)


* Third iteration would be implementing it to a Telegram Bot or a GUI, in order to be more generally scoped to non technical people.
