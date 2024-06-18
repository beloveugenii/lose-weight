#!/usr/bin/env python3

import sqlite3, datetime, readline, sys, os
from signal import signal, SIGINT
from users import *
from ui import *
from common import *
from liblw import *
from foods import *

PROG_NAME = 'lose-weight'
VERSION = '0.1.7.2'
DB_NAME = sys.path[0] + '/data.db'

con = sqlite3.connect(DB_NAME)
cur = con.cursor()
create_tables(cur)

wc = False
current_date = datetime.date.today()

# Enable SIG handlers and configure readline
signal(SIGINT, sigint_handler)
readline.set_completer_delims('\n,')

while True:
    user_id = get_user_id(cur)
    while user_id is None:
        user_id, wc = users_main(cur, user_id)
        if wc:
            con.commit()
            wc = not wc

    user_data = get_user_data_by_id(cur, user_id)
    food_list = get_food_list(cur)

    screen_name = 'diary'

    diary = get_data_for_diary(cur, current_date.strftime('%Y-%m-%d'), user_id)
    kcal_norm = float(get_calories_norm(user_data))
    kcal_per_day = '%.1f' % sum([line[2] for line in diary])

    # Enable tab-completion
    readline.parse_and_bind('tab: complete')
    readline.set_completer(Completer([food[0] for food in food_list]).complete)


    action = screen(
        user_data['name'] + ': ' + headers[screen_name] + ' ' + current_date.strftime('%Y-%m-%d'),
        lambda:
        print_as_table( [('норма калорий'.upper(), '', kcal_norm)] + diary + [('всего'.upper(), '', kcal_per_day)],  ' ' ) if diary else print(messages['ndip']),
        menu_str[screen_name], 2)

   

    if action == 'q': break
    elif action == 'p': current_date -= datetime.timedelta(days = 1)
    elif action == 'n': current_date += datetime.timedelta(days = 1)
    elif action == 'h': helps(help_str[screen_name])
    elif action == 's': 
        os.system('python3 ' + sys.path[0] + '/cirner.py -i')

    elif action == 'u':
        old_user_id = user_id
        user_id = None
        while user_id is None:
            user_id, wc = users_main(cur, old_user_id)
            if wc:
                con.commit()
                wc = not wc


    elif action == 'l':
        end_work = False
        while not end_work:
            end_work, wc = foods_main(cur)
            if wc:
                con.commit()
                wc = not wc




            #  elif action == 'a':
                #  screen_name = 'analyzer'
                #  while True:
                    #  dishes_list = get_dishes_list(cur)
                    #  # АНАЛИЗАТОР РЕЦЕПТА
                    #  screen(
                        #  headers[screen_name],
                        #  lambda: print(*dishes_list) if dishes_list else helps(messages['nd'], 0),
                        #  menu_str[screen_name], 3)

                    #  action = input('>> ').lower().strip()

                    #  if action == 'q': break
                    #  elif action == 'c':
        #  #  введите список продуктов с указанием количества, помогает табуляция
        #  #  проверка, все ли продукты известны
        #  #  подсчет данныэ
        #  #  введите название блюда
        #  #  сохранение в бд dishes
    


           
            #  else: helps(messages['ua'], 1)

    elif action not in 'lpnqht' and len(action) > 2:
        new_entry = { 'date': current_date, 'user': user_id, }

        for el in [ i.strip() for i in action.split(',') ]:

            data = parse_line(el)

            new_entry['title'] = data[0]
            new_entry['value'] = data[1] if data[1] is not None else input(f"количество для '{new_entry['title'][:1].upper() + new_entry['title'][1:]}': ")

            if is_in_db(cur, new_entry['title']) is None:
                print(f'Похоже, что такого блюда как \'{new_entry["title"]}\' нет в базе\nТребуется ввод дополнительной инофрмации')

                # Добавляем новый продукт в БД
                d = get_data({'kcal': 'калорийность',
                          'p': 'содержание белков',
                          'f': 'содержание жиров',
                          'c': 'содержание углеводов'}, 1)

                d['title'] = new_entry['title']
                add_new_food(cur, d)
                con.commit()
                wc = True

            # Добавляем запись в дневник
            add_in_diary(cur, new_entry)
            con.commit()

    else: helps(messages['ua'], 1)

con.close()
clear()





