import json
import csv

dict = {}

with open('raw_list_from_github.txt', 'r') as raw:
    reader = raw.read().replace("'", "")
    list = list(reader.split(","))
    # csv_reader = csv.reader(raw)
    # print(reader[8])
    # print(csv_reader)

    # for item in reader:
    #     dict[item] = 0
    # print(dict)
    for i in list