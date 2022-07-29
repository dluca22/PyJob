import re
from dictionary import languages


# gets data from main program and analize the text
# outputs data to a file

# this should be an helper function, as it sould work independently from the source of the data (in this case indeed, but later should manage the same text from other websites/listing)

dict = {
    'css': 0,
    'javascript': 0,
    'android': 0
}
# second dictionary with only the non zero values
results = {}

# "c++" throws an error, had to change to c+
# languages is a dict imported from another python file


# TO BE REMOVED - just testing read from an example file with a random listing text
# file I/O is built-in in python
with open("random_listing2.txt", 'r') as descr:
    # returns body of text as a 'str' lowercased
    text = descr.read().lower()
    # list that gets populated by every occurence of the key of the dictionary
    matches = []

    # looping over keys in the dict, it assigns the number of times the str gets appended to the matches[] list
    for key in languages:
        matches = re.findall(rf'\b{key}\b', text)
        # if matches creates a list with
        if len(matches) >= 1:
            # just add 1 to the dict
            languages[key] = +1
    with open('results.txt', 'a'):

        # print only the keys that are not 0
        for k, v in languages.items():
            if v != 0:
                # print(k, ":", v)
                results.keys() = languages[k]
                results.values() = languages[v]

        print(results)
        
