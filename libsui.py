# libsui.py

from os import get_terminal_size                       

version = '0.0.1b'
screen_width = get_terminal_size()[0]
line = '-' * screen_width

def clear():
    # clears the screen
    print('\033[2J\033[H', end='')

def promt(what):
    # takes a string
    what = str(what)
    # return gived string in looks 'String: '
    return input(what[0].upper() + what[1:] + ': ')

def get_fields_len(array):
    # takes a list of tuples
    fields = []

    # defines the number of rows and columns
    rows = len(array)
    try:
        cols =  max([len(col) for col in array])
    except ValueError:
        cols = 0
    
    # expands each row to the maximum number of columns
    for r in range(rows):
        while len(array[r]) < cols:
                array[r] = array[r] + ('',)
    
    # defines width of every columns
    for c in range(cols):
        fields.append(max(len(str(array[r][c])) for r in range(rows)))
    
    # defines wifth of empty fields 
    sep_len = (screen_width - sum(fields)) // ( len(fields) + 1)
    
    while sum(fields) + (cols + 1) * sep_len > screen_width:
        sep_len -= 1

    # returns list of every columns width and empty field width
    return fields, sep_len


def print_as_table(items, sep):
    # takes the list of tuples
    fields, sep_len = get_fields_len(items)

    # prints tuples elements in fieldd separating with empty spaces
    for row in items:
        for c in range(len(row)):
            print('%s%-*s' % (sep * sep_len, fields[c], row[c]), end='')
        else:
            print('%s' % (sep * sep_len,))

def header(text):
    # takes a string and transform it to list of tuples with single element
    # print a string in center of screen
    print(line)
    print_as_table([(text,), ],' ')
    print(line)

def menu(array, cols):
    # takes a list ol menu elements and columns number
    menu_lst = []
    array = list(map(lambda word: '[' + word[0]+ ']' + word[1:], array))

    if len(array) % 2 == 1 and cols % 2 == 0:
        array.append('')
    
    # convert list to list of tuples
    while len(array) > 0:
        tmp = []
        for t in range(cols):
            tmp.append(array.pop(0))
        menu_lst.append(tuple(tmp))

    # print list of tuples like menu
    print(line)
    print_as_table(menu_lst, ' ')
    print(line)

def screen(header_title, func, menu_lst, menu_cols):
    # takes a list with header text, some function, menu list and number of menu columns
    # clear the screen and prints header, output of body function and menu
    clear()
    header(header_title)
    func()
    menu(menu_lst, menu_cols)

class completer():
    def __init__(self, options):
        self.options = sorted(options)
        return

    def complete(self, text, state):
        response = None
        if state == 0:
            # Создание списка соответствий.
            if text:
                # если какой то текст есть, то вернуть список слов из списка, которые начинаются на текст
                self.matches = [s 
                    for s in self.options
                    if s and s.startswith(text)]
            else:
                # или вернуть весь список
                self.matches = self.options[:]
        # Вернуть элемент состояния из списка совпадений, 
        # если их много. 
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        return response
