import json
import csv

dict = {}
# saved raw input from github because no internet connection, so saved to a .txt file and continued offline
with open('raw_list_from_github.txt', 'r') as raw:
    #reads as a string, removing quotes from each str
    reader = raw.read().replace("'", "")
    # transforms the str obj to a list separated at the ","
    list = list(reader.split(","))

    # loop the list and gives def value of 0
    for i in list:
        dict[i] = 0

    print(dict)