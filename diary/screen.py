#!/usr/bin/env python3

from time import sleep
from datetime import date
# После отладки перенести в файл модуля screen.py
from os import get_terminal_size                       

screen_width = get_terminal_size()[0]

def header(text):
    header_length = len(text)
    header_length = header_length + 1 if header_length % 2 == 1 else header_length
    header_field = ' ' * ((screen_width - header_length) // 2)

    print('-' * screen_width, header_field + text + header_field, '-' * screen_width, sep='\n')

def clear():
    print('\033[2J\033[H')

def colored(color, text):
    if color == 'red':
        return "\033[31m" + text + "\033[97m"

def menu(items):
    for item in items:
        print('[' + item[0] + ']' + item[1:])


