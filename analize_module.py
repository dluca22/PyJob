from fileinput import filename
import re
import sys
import time
# from dictionary import languages
import matplotlib.pyplot as plt
from flask import url_for


# gets data from main program and analize the text
# outputs data to a file

# this is an helper function, so it works independently from the source of the data (in this case indeed, but later should manage the same text from other websites/listing)

# second dictionary with only non zero values
result_dict = {}
counter = 0

# ===========================================================

def analisis(text, default_dict):
    global result_dict, counter

    # CHANGE "languages", should not be imported from a py file but from the later defined dict

    # matches = list that gets populated by every occurence of the key of the dictionary
    matches = []

    # looping over keys in the dict, it assigns the number of times the str gets appended to matches[]
    for key in default_dict:
        #  \bWORD\b matches unique expression that is not part of another word
        matches = re.findall(rf'\b{key}\b', text)
        # if it matches default creates a list with all occurences
        if len(matches) >= 1:
            # just counts EVERY matches found for dev_mode
            counter = counter + len(matches)
            # just add 1 to the dict
            default_dict[key] += 1

        # new dict with only the keys that are not 0
        for k, v in default_dict.items():
            if v != 0:
                # if key is already present, adds the value
                if  k in result_dict:
                    result_dict[k] += v
                # else creates a new k:v pair
                result_dict.update({k : v})

            # fine analize()
# ===========================================================

def elaborate():
    # calls the 2 functions that order and transform the dict to a more readable format
    global result_dict
    global counter

    elaborated = percent_calc(sort_dictionary(result_dict))
    # sys.exit(list(elaborated.values()))
    finish_time = time.time()
    # pretty format header of the output file
    # output.write(f'Skill = Nr. of matches (% of relevance) \n')
    # output.write(f'Total keywords matching: {counter} in {len(ids)} unique offers \n \n')

    # # in dev_mode print matches and time taken (add num of pages and maybe links to every job offer)
    # # writes the counter of ALL matches, the total of unique offers searched (set of ids)
    # if dev_mode ==True:
    #     output.write(f'<Time: {round(timing, 2)}s > \n')
    #     output.write('(other useless things for dev_mode) \n \n')

    # # for every key and value of the dict > write a line to the output file

    # REMOVE
    # for k, v in elaborated.items():
    #         output.write(f"{k.capitalize()} =   {result_dict[k]} ({v} %)\n")
    pie_chart(elaborated)

    return elaborated, finish_time, counter


# print to file every checked job title and job link (but it's kinda useless for what i need)


# ===========================================================

    # from int values intrasforms to percent float w/ 2 decimal place
def percent_calc(dictionary):
    total = sum(dictionary.values())
    for k, v in dictionary.items():
        # updates dict with same Key but a Value x 100 divided by total of sum of dict values
        dictionary.update({k : float("{:.2f}".format(v *100 / total ))})
        # only add percent sign to the file writing so it is still a computable number for later use
    return dictionary

# ===========================================================

# makes a list from dict values and sorts it
def sort_dictionary(unsorted_dict):
    sorted_values = sorted(unsorted_dict.values(), reverse=True)
    # new dict because can't change the original one
    sorted_dict = {}

    # if the sorted value matches the value of the original dict > copy the value to the sorted_dict
    for i in sorted_values:
        for k in unsorted_dict.keys():
            if unsorted_dict[k] == i:
                sorted_dict[k] = unsorted_dict[k]

    return sorted_dict

# ===========================================================

def pie_chart(dictionary):

    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = list(dictionary.keys())
    sizes = list(dictionary.values())

    # starting list for exploded view
    # should contain a value for each value to plot, else ValueError
    explode = [0.1]
    # dinamically append other values to match the len of values to display
    for _ in range(1, len(sizes)):
        explode.append(0)


    fig1, ax1 = plt.subplots()

    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=0)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.savefig('./static/graph.png')