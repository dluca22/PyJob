import sys

dev_mode = False
page = 0
usage_message = "Usage: $ python3 lookfor.py [pages 1-5, default=1] [dev_mode, default=OFF]"

# for i in (sys.argv):
#     print(i)
# print(len(sys.argv))


# if 1 argum is help print help message
if len(sys.argv) == 2 and sys.argv[1].lower() == 'help':
    sys.exit(f"!!! ERROR !!! \n{usage_message}")

# if 1 or 2 arguments passed
elif len(sys.argv) >= 2:
    # if argv[1] is a number convert as page int
    try:
        page = int(sys.argv[1])
        # only accept 1-5
        if page in range(1, 6):
            page = (page - 1) * 10
        else:
            sys.exit("Error: can only accept numbers 1 to 5")
    # if argv[1] not a number
    except ValueError:
        sys.exit(f"!!! ERROR !!! \n{usage_message}")

    # but if arguments are 2 and the second is 'dev_mode'
    if len(sys.argv) == 3 and sys.argv[2] == 'dev_mode':
                    # set developer mode as True
                dev_mode = True
    else:
        sys.exit(f"!!! ERROR !!! \n{usage_message}")
# if more than 2 arguments
if len(sys.argv) > 3:
    sys.exit(f"Invalid number of arguments!!!! \n{usage_message}")


print(page)
print(dev_mode)