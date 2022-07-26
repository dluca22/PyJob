import json
import csv
import re

dict = {}
# saved raw input from github because no internet connection, so saved to a .txt file and continued offline
def clean_text(str):
    # conditions to be substituted from the text
    replace_conditions = {"'": "", "[":"", "]":""}
    # remove_quotes = str.replace("'", "").replace("\[")
    for i, j in replace_conditions.items():
        str = str.replace(i, j)
    return str
    # cleaned = re.sub(!, str)

    # return cleaned



with open('raw_list_from_github.txt', 'r') as raw:
    #reads as a string, removing quotes from each str
    reader = raw.read()
    cleaned = clean_text(reader).lower()
    # # transforms the str obj to a list separated at the ","
    list = list(cleaned.split(","))

    # # loop the list and gives def value of 0
    for i in list:
        dict[i] = 0
    with open('values_dict.txt', 'w'):

        print(dict)