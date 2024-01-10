from time import sleep

messages = {
    'not_impl': 'Not implemented yet',
    'ua': 'Unsupported action',
    'small_str': 'Too small string',
    'need_gender': 'A gender designation is required: [mM or fF]',
    'need_number': 'A number is required',
    'interactive':
        "Enter the numbers of the required workout programs separated by spaces\n'c' for creating new training\n'r' to remove existed training\n'e' for editing the training\n'h' show this help\n'q' quit",
    'users':
        "Type user ID for choosing\n'n' create new user\n'h' show this help\n'q' quit",
    'diary':
        "Enter the name of the food to be entered in the diary\n'n' go to the next day\n'p' go to the previous day\n'l' show food in database\n't' go to sport assistant\n'h' show this help\n'q' quit",
    'food_db':
        "Enter the name of the food to be entered in database\n'a' analyze the complex dish\n'r' remove from database\n'h' show this help\n'q' go back",
    'analyzer':
        "Enter the name of the food to be entered in the diary\n'c' create a new dish\n'r' remove an existing dish\n'h' show this help\n'q' quit",
}

def help(*args):

    print(messages[args[0]])

    if len(args) > 1:
        sleep(args[1])
    else:
        empty_input = input()
