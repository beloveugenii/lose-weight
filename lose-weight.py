#!/usr/bin/env python3

import sqlite3, datetime, readline, sys, os
from signal import signal, SIGINT
from users import *
from ui import *
from common import *
from liblw import *

PROG_NAME = 'lose-weight'
VERSION = '0.1.7.1'
DB_NAME = sys.path[0] + '/data.db'

con = sqlite3.connect(DB_NAME)
cur = con.cursor()
create_tables(cur)


# Enable SIG handlers and configure readline
signal(SIGINT, sigint_handler)
readline.set_completer_delims('\n,')
#  readline.parse_and_bind('tab: complete')

wc = False
user_id = check_data_in_table(cur, 'current_user')
current_date = datetime.date.today()


while True:
    while user_id == 0:
        user_id, wc = set_user(cur)
        if wc:
            con.commit()
            wc = not wc
        
        user_id = check_data_in_table(cur, 'current_user')
        
    # Get user data and diary from db
    user_data = get_user_data_by_id(cur, user_id)
    food_list = get_food_list(cur)

    screen_name = 'diary'
    clear()
    if wc:
        food_list = get_food_list(cur)
        wc = not wc



    diary = get_data_for_diary(cur, current_date.strftime('%Y-%m-%d'), user_id)
    kcal_norm = float(get_calories_norm(user_data))
    kcal_per_day = '%.1f' % sum([line[2] for line in diary])

    screen(
        user_data['name'] + ': ' + headers[screen_name] + ' ' + current_date.strftime('%Y-%m-%d'),
        lambda:
        print_as_table( [('норма калорий'.upper(), '', kcal_norm)] + diary + [('всего'.upper(), '', kcal_per_day)],  ' ' ) if diary else helps(messages['ndip'], 0),
        menu_str[screen_name], 2)

    # Enable tab-completion
    readline.parse_and_bind('tab: complete')
    readline.set_completer(Completer([food[0] for food in food_list]).complete)

    action = input('>> ').lower().strip()

    if action == 'q': break
    elif action == 'p': current_date -= datetime.timedelta(days = 1)
    elif action == 'n': current_date += datetime.timedelta(days = 1)
    elif action == 'h': helps(help_str[screen_name])

    elif action == 'u':
        user_id, wc = set_user(cur)
        if wc:
            con.commit()
            wc = not wc
            #  \cuser_id = check_data_in_table(cur, 'current_user')

    elif action == 'l':
        screen_name = 'food_db'
        while True:
            clear()
            res = get_food_data(cur)

            # Disable tab-completion
            readline.parse_and_bind('tab: \t')

            screen(
                headers[screen_name],
                lambda: print_as_table( [('title','kcal','p', 'f', 'c',)] + res,  ' ') if res else helps(messages['nd'], 0),
                menu_str[screen_name], 2)

            action = input('>> ').lower().strip()

            if action == 'q': break
            elif action == 'h': helps(help_str[screen_name])
            elif action in 'ar': helps(messages['not_impl'], 1)

            elif action not in 'arqh' and len(action) > 3:

                new_food_params = {'kcal': 'калорийность', 'p': 'содержание белков',
                   'f': 'содержание жиров','c': 'содержание углеводов'}
                d = get_data(new_food_params, 1)
                d['title'] = action
                add_new_food(cur, d)
                con.commit()
                wc = True

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
    


           
            else: helps(messages['ua'], 1)

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


