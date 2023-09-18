# python implementation of libui.pm
# not finished yet =)
from os import get_terminal_size                       
from time import sleep
# Библиотека с функциями для дневника питания

screen_width = get_terminal_size()[0]
line = '-' * screen_width

def clear():
    # Очистка экрана
    print('\033[2J\033[H', end='')

def promt(what):
    what = str(what)
    # Функция полчает значение 'строка' и возвращает его в виде: 'Строка: '
    return input(what[0].upper() + what[1:] + ': ')


def get_fields_len(array):
    # функция получает список кортежей
    fields = []

    # определяем наибольшее количество строк и колонок
    rows = len(array)
    try:
        cols =  max([len(col) for col in array])
    except ValueError:
        cols = 0
    
    # если в какой то строке элементов недостаточно, то строки неявно дополняются
    for r in range(rows):
        while len(array[r]) < cols:
            array[r] = array[r] + ('',)
    
    # получаем список ширин полей
    for c in range(cols):
        fields.append(max(len(str(array[r][c])) for r in range(rows)))
    
    # получаем ширину разделителя
    sep_len = (screen_width - sum(fields)) // ( len(fields) + 1)
    
    while sum(fields) + (cols + 1) * sep_len > screen_width:
        sep_len -= 1

    # возвращает список ширин полей под каждый элемент и ширину разделителя между ними
    return fields, sep_len


def print_as_table(items, sep):
    # функция получает список кортежей
    # выводит на экран элементы кортежей разделяя их разделителем
    fields, sep_len = get_fields_len(items)
    for row in items:
        for c in range(len(row)):
            print('%s%-*s' % (sep * sep_len, fields[c], row[c]), end='')
        else:
            print('%s' % (sep * sep_len,))

def header(text):
    # получает строку текста
    # выводит ее по центру экрана в рамке
    print(line)
    print_as_table([(text,), ],' ')
    print(line)

def menu(array, cols):
    # получает список элементов и количество колонок
    menu_lst = []
    
    # строим список кортежей с нужным количеством колонок
    for i in range(0, len(array) + 1, cols):
        tmp = []
        for c in range(cols):
            try:
                tmp.append(array[i + c])
            except IndexError:
                tmp.append('')
        menu_lst.append(tuple(tmp))
    
    # выводит список в виде меню, ограниченного рамкой
    print(line)
    print_as_table(menu_lst,' ')
    print(line)

def screen(header_title, menu_lst, menu_cols):
    header(header_title)
    menu(menu_lst, menu_cols)
    if promt('>> ') not in [word[0] for word in menu_lst]:
        print('Неизвестная команда')
    else:
        print('Работаем дальше')




class cmpl():
    def __init__(self, options):
        self.options = sorted(options)
        return

    def complete(self, text, state):
        response = None
        if state == 0:
            # Создание списка соответствий.
            if text:
                self.matches = [s 
                    for s in self.options
                    if s and s.startswith(text)]
            else:
                self.matches = self.options[:]
        # Вернуть элемент состояния из списка совпадений, 
        # если их много. 
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        return response

