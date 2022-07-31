import sys

dev_mode = False
number_of_pages = ['1','2','3','4','5']
page = ''

if len(sys.argv) > 3:
    print("Invalid number of arguments")
    sys.exit("linea 9")

elif len(sys.argv) >= 2:
    try:
        page = int(sys.argv[1])
        if page in range(1, 6):
            page = (page - 1) * 10
        else:
            sys.exit("Error: can only accept numbers 1 to 5")
    except ValueError:
        sys.exit("!!! ERROR !!! \nUsage: python3 lookfor.py [pages 1-5, default=1][dev_mode, default=OFF]")

if len(sys.argv) == 3:
    if sys.argv[2] == 'dev_mode':
        dev_mode = True
        print(dev_mode)
    else:
        sys.exit("!!! ERROR !!! \nUsage: python3 lookfor.py [pages 1-5, default=1][dev_mode, default=OFF]")


print(page)