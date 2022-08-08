import re
from dictionary import languages



# gets data from main program and analize the text
# outputs data to a file

# this is an helper function, so it works independently from the source of the data (in this case indeed, but later should manage the same text from other websites/listing)

# second dictionary with only non zero values
res_dict = {}
counter = 0

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

def print_to_file(dev_mode=False, timing=0, ids=None, jobList=None):
    # calls the 2 functions that order and transform the dict to a more readable format
    with open('results.txt', 'w') as output:
        elaborated = percent_calc(sort_dictionary(res_dict))

        # pretty format header of the output file
        output.write(f'Skill = Nr. of matches (% of relevance) \n \n')

        # in dev_mode print matches and time taken (add num of pages and maybe links to every job offer)
        # writes the counter of ALL matches, the total of unique offers searched (set of ids)
        if dev_mode ==True:
            output.write(f'< Total matches: {counter} in {len(ids)} unique offers, Time: {round(timing, 2)}s > \n')
            output.write('Total matches does not limit to the count to just 1 per offer, but EVERY match) \n \n')

        # for every key and value of the dict > write a line to the output file
        for k, v in elaborated.items():
                output.write(f"{k.capitalize()} =   {res_dict[k]} ({v} %)\n")

        # if dev_mode == True:
        #     for items in jobList:
        #         # print('eee', items)
        #         if items['id'] in ids:
        #             print('ooo', items['id'])
# ===========================================================

def analisis(text):
    global res_dict, counter

    # matches = list that gets populated by every occurence of the key of the dictionary
    matches = []

    # looping over keys in the dict, it assigns the number of times the str gets appended to matches[]
    for key in languages:
        matches = re.findall(rf'\b{key}\b', text)
        # if it matches creates a list with all occurences
        if len(matches) >= 1:
            # just counts EVERY matches found for dev_mode
            counter = counter + len(matches)
            # just add 1 to the dict
            languages[key] += 1


    # OPTIONAL logs for every description as argV
    # with open('block_of_text.txt', 'a') as alltext:
        # alltext.write(f'{text} \n ========================================================== \n' )

        # new dict with only the keys that are not 0
        for k, v in languages.items():
            if v != 0:
                # if key is already present, adds the value
                if  k in res_dict:
                    res_dict[k] += v
                # else creates a new k:v pair
                res_dict.update({k : v})

            # fine analize()