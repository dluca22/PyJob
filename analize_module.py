import re
import app
import time
import matplotlib.pyplot as plt


# second dictionary with only non zero values
result_dict = {}
counter = 0

# ===========================================================

def analisis(text, default_dict):
    global result_dict
    global counter


    # matches = list that gets populated by every occurence of the key of the dictionary
    matches = []

    # looping over keys in the dict, it assigns the number of times the str gets appended to matches[]
    for key in default_dict:
        #  \bWORD\b matches unique expression that is not part of another word
        # error on c++
        matches = re.findall(rf'\b{key}\b', text)
        # matches = re.findall(rf'\b{key}\b', text)
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

# ===========================================================

def elaborate():
    # calls the 2 functions that order and transform the dict to a more readable format
    global result_dict
    global counter

    elaborated = add_percent(sort_dictionary(result_dict))

    finish_time = time.time()

    pie_chart(result_dict)

    return elaborated, finish_time, counter


# ===========================================================

    # from int values intrasforms to percent float w/ 2 decimal place
def add_percent(dictionary):
    total = sum(dictionary.values())
    for k, v in dictionary.items():
        # updates dict with same Key but a Value x 100 divided by total of sum of dict values
        # dictionary.setdefault(k, []).append(float("{:.2f}".format(v *100 / total )))
        dictionary.update({k : [v, float("{:.2f}".format(v *100 / total ))]})
        # only add percent sign to the file writing so it is still a computable number for later use
    return dictionary
# # ===========================================================

#     # from int values intrasforms to percent float w/ 2 decimal place
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

    result = percent_calc(sort_dictionary(dictionary))

    if not dictionary:
        app.error("what the fuck")
    else:
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        labels = list(result.keys())
        sizes = list(result.values())

        # starting list for exploded view
        # should contain a value for each value to plot, else ValueError
        explode = [0.2]
        # dinamically append other values to match the len of values to display
        for _ in range(1, len(sizes)):
            explode.append(0)


        fig1, ax1 = plt.subplots()

        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                    shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # save image w/ transparent background in case of darkmode
        plt.savefig('./static/img/graph.png', transparent=True)