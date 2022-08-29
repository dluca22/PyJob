# DevSkills
#### Video Demo: https://youtu.be/kNj5dm7GiDs
#### Description:

The purpose of this web application is to offer the user an easier way to discover the most requested skills that different job position require.

Since I started looking for work in the tech industry, I have had a hard time keeping up with the skills required across different career paths.


While the Internet is full of resources and information, it can still be somewhat challenging to understand what skills and framework you need to learn to create a more attractive resume for a desired position.

I started this project as a simple CLI tool with python to browse Indeed.com and Indeed.it to get job descriptions using beautiful soup and count all matching keywords for the most popular coding languages, frameworks and platforms in use.
The first version of the app had a main.py function and "analize.py" helper function, where the first one manages the user input, the requests and the data collection via beautifulsoup, the helper function was called to analize the various parts of the data that got retrieved and kept the count and logic for the whole duration of the runtime, at the end of which, the helper function printed the result list into a text file and the pie chart as an image using the matplotlib library.

Upon confirming that the script was functional and stable I decided it would be a more useful tool and accessible to a wider audience as a web application, so i kept both of the python files as modules of the app.py that runs the Flask framework.
Flask manages the templating routes, and user requests and passes the data to the two modules.
I also implemented the feature to let the user add some custom keywords in case he wants to search for other keywords not yet implemented or that are outside the tech field.

The results of the matching keywords are stored and updated as dictionaries but in the future i plan on changing it to a database so that the application can store the results permanently and monitor the trends and patterns for different position in various geographical areas


My only source of data at the moment is Indeed US and Indeed ITA, however in the future I plan on supporting additional job search engines like LinkedIn, Monster Jobs etc, possibly integrating other useful information like the average seniority required or the availability of remote work.

My plan is to publish this web application on a hosting platform in the hope that it will be a useful resource for anyone looking for a new career

