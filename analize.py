import re
from dictionary import languages


# gets data from main program and analize the text
# outputs data to a file

# this should be an helper function, as it sould work independently from the source of the data (in this case indeed, but later should manage the same text from other websites/listing)

# second dictionary with only non zero values
res_dict = {}
counter = 0

# ===========================================================

    # from int values intrasforms to percent float 2 decimal place
def percent_calc(dictionary):
    #/ total = sum(dictionary.values())
    #/ for k, v in dictionary.items():
        # updates dict with same Key but a Value x 100 divided by total of sum of dict values
       #/ dictionary.update({k : float("{:.2f}".format(v *100 / total ))})
        # only add percent sign to the file writing so it is still a computable number for later use

    return dictionary

# ===========================================================

def sort_dictionary(unsorted_dict):
    # makes a list from dict values and sorts it
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

def print_to_file(dictionary):
    # calls the 2 functions that order and transform the dict to a more readable format
    with open('results.txt', 'w') as output:
        elaborated = percent_calc(sort_dictionary(dictionary))

        # for every k, v of the dict > write a line to the output file
        for k, v in elaborated.items():
                output.write(f"{k} = {v} % \n")
        print(counter)

# ===========================================================

def analisis(text):
    global counter
    # "c++" throws an error, had to change to c+
    # languages is a dict imported from another python file


    # matches = list that gets populated by every occurence of the key of the dictionary
    matches = []

        # looping over keys in the dict, it assigns the number of times the str gets appended to the matches[] list
    for key in languages:
        matches = re.findall(rf'\b{key}\b', text)
        # if it matches creates a list with all occurences
        if len(matches) >= 1:
            counter = counter + len(matches)
            # just add 1 to the dict
            languages[key] += 1
            # languages[key] = len(matches) #temp
    with open('block_of_text.txt', 'a') as alltext:
        alltext.write(f'{text} \n ========================================================== \n' )

        # print only the keys that are not 0
        for k, v in languages.items():
            if v != 0:
                # adds to result dict only the non zero valule
                res_dict.update({k : v})
            elif  k in res_dict:
                res_dict[k] += v

            # fine analize()

# ===========================================================

def pass_dict():
    return res_dict



