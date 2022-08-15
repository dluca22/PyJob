from dictionary import languages


# temporarily used to retrieve dict keys

with open("list_of_keys.txt", "w") as test:
    list = list(languages.keys())
    for items in sorted(list):
            test.write(f'{items} \n')