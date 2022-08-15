# populate dictionary from textfile list

# create empty dictionary as a start
dict = {}

# open file
with open("textfile.txt", "r") as file:
    # iterate over every line
    for line in file:
        # declare a dict[key] with name of iterator and = to_value_we_want
        # strip() to remove newline "\n" at the end of every line
        dict[line.strip()] = 0
    print(dict)
# {'.js': 0, '.net': 0, 'algol': 0, 'ams': 0, 'android': 0, 'android studio': 0, ....}