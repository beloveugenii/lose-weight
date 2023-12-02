#!/usr/bin/env python3

import sqlite3, datetime, readline, os, signal, sys
from time import sleep
from libsui import *
from lib import *
import re

VERSION = '0.1.0'
NAME = 'analyst.py'
DB_NAME = sys.path[0] + '/fc.db'

def get_ingrs():
    ingr = None
    lst = []
    while ingr != '' :
        ingr = input('ingr: ').lower().strip()
        if ingr == '':
            break
        lst.append(ingr)
    return tuple(lst)
 
# Обработчик нажатия Ctrl-C
def sigint_handler(signum, frame):
    '''Simple sigint handler'''
    signame = signal.Signals(signum).name
    clear()
    print(f'Catched {signame}')
    exit(1)

#def validate(what, need_type):
#    ''''''
#    what = str(what)

#    def isfloat(what):
#        if what.startswith('-'):
#            what = what[1:]
#        parts = what.split('.')
#        return len(parts) == 2 and parts[0].isnumeric() and parts[1].isnumeric()

#    if need_type == 'int':
#        return what.isdigit()
#    elif need_type == 'float':
#        return isfloat(what)
#    else:
#        return 'Unsupported type'


# Создаем подключение к БД и объект для работы с sql-запросами
con = sqlite3.connect(DB_NAME)
cur = con.cursor()

# Enable SIG handlers and configure readline
signal.signal(signal.SIGINT, sigint_handler)
readline.set_completer_delims('\n')

  # Enable tab-completion
#readline.parse_and_bind('tab: complete')

   
 
while True:
    clear()
    # данные из таблицы с блюдами
    dishes_list = cur.execute("SELECT title FROM dishes").fetchall()
    food_list = cur.execute("SELECT title FROM food").fetchall()
# вче для анализатора   
    screen('Анализатор калорийности рецепта',
            lambda: print(*dishes_list) if dishes_list else print('No entries') ,
           ['create a new dish',  'remove an existing dish', 'quit'], 3)
    

    # Enable tab-completion
    readline.parse_and_bind('tab: complete')
    readline.set_completer(completer([food[0] for food in food_list]).complete)

#    action = input('>> ').lower().strip()

#    if action == ':q':
#        break
    
#    elif action == ':c':
        # введите список продуктов с указанием количества, помогает табуляция
        # проверка, все ли продукты известны
        # подсчет данныэ
        # введите название блюда
        # сохранение в бд dishes
#        print('Not implemented yet')
#        sleep(1)
    
#    elif action == ':r':
#        print('Not implemented yet')
#        sleep(1)

#    elif action == ':h':
#        print("Enter the name of the food to be entered in the diary", 
#              "':c' create a new dish",
#              "':r' remove an existing dish",
#              "':h' show this help",
#              "':q' quit", sep='\n')
#        a = input()
    
#    else:
#        print('Unsupported action')
#        sleep(1)


 # Disable tab-completion
#            readline.parse_and_bind('tab: \t')

#            screen('Внесение данных о новом продукте',
#                   lambda: print_as_table( [('title','kcal','p', 'f', 'c',)] + res,  ' ') if res else print("No data in database yet"),
#                    ['remove', 'quit'], 0)


#                cur.execute('INSERT INTO food VALUES(:title, :kcal, :p, :f, :c)', d)
#        if res is None:
#            print('Похоже, что такого блюда нет в базе\nТребуется ввод дополнительной инофрмации')
            
            # Добавляем новый продукт в БД
#            d = get_data({'kcal': 'калорийность', 
#                          'p': 'содержание белков', 
#                          'f': 'содержание жиров',
#                          'c': 'содержание углеводов'}, 1)
            
#            d['title'] = new_entry['title']

#            cur.execute('INSERT INTO food VALUES(:title, :kcal, :p, :f, :c)', d)
#            con.commit()
        
        # Добавляем запись в дневник
#        cur.execute("INSERT INTO diary VALUES(:user, :date, :title, :value)", new_entry)
#        con.commit()
 
