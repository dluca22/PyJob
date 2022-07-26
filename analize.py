import re
from dictionary import languages


# gets data from main program and analize the text
# outputs data to a file

# this should be an helper function, as it sould work independently from the source of the data (in this case indeed, but later should manage the same text from other websites/listing)

dict = {
    'css' : 0,
    'javascript' : 0,
    'android' : 0
}
# TO BE REMOVED - just testing read from an example file with a random listing text
# file I/O is built-in in python
with open("random_listing.txt", 'r') as descr:
    # returns body of text as a 'str'
    text = descr.read()
    # list that gets populated by every occurence of the key of the dictionary
    matches = []

    # looping over keys in the dict, it assigns the number of times the str gets appended to the matches[] list
    for key in dict:
        matches = re.findall(rf'\b{key}\b', text)

        dict[key] = len(matches)

        # print(dict)
    print(dict)