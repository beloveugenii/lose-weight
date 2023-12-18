#!/usr/bin/env python3

import sqlite3, datetime, readline, signal
from os import system
from lib import *

PROG_NAME = 'simple-diet'
VERSION = '0.1.6a'
CONFIG_FILE_PATH = sys.path[0] + '/config'
DB_NAME = sys.path[0] + '/fc.db'
SS_PATH = sys.path[0] + '/simple-sport.py'

current_date = datetime.date.today()
db_was_changed = False
user_was_changed = False

# Обработчик нажатия Ctrl-C
def sigint_handler(signum, frame):
    signame = signal.Signals(signum).name
    clear()
    print(f'Catched {signame}')
    exit(1)


# Creating connection to database 
con = sqlite3.connect(DB_NAME)
cur = con.cursor()

# Creating tables if needed
create_tables(cur)

# Enable SIG handlers and configure readline
signal.signal(signal.SIGINT, sigint_handler)
readline.set_completer_delims('\n')


# Try to get id of current user from config file
user_id = get_user_id_from_file(CONFIG_FILE_PATH)

if user_id is None:
    user_id = set_user(cur, CONFIG_FILE_PATH)
    con.commit()

user_data = convert_user_data(get_user_data_by_id(cur, user_id))

food_list = get_food_list(cur)

screen_name = 'diary'

while True:
    clear()
    if db_was_changed:
        food_list = get_food_list(cur)
        db_was_changed = False

    if user_was_changed:
        user_data = convert_user_data(get_user_data_by_id(cur, user_id))
        user_was_changed = False


    diary = get_data_for_diary(cur, current_date.strftime('%Y-%m-%d'), user_id)
    
    kcal_norm = get_calories_norm(user_data)
    kcal_per_day = '%.1f' % sum([line[2] for line in diary])
    
    screen(
        HEADERS[screen_name] + ' ' + current_date.strftime('%Y-%m-%d'),
        lambda: 
        print_as_table( [('норма калорий'.upper(), '', kcal_norm)] + diary + [('всего'.upper(), '', kcal_per_day)],  ' ' ) if diary else print(EMPTY_BODY[screen_name] + f' {current_date}'),
        MENUS_ENTRIES[screen_name],2)
    
    # Enable tab-completion
    readline.parse_and_bind('tab: complete')
    readline.set_completer(completer([food[0] for food in food_list]).complete)

    action = input('>> ').lower().strip()
    
    if action == 'q':
        break
    
    elif action == 'u':
        user_id = set_user(cur, CONFIG_FILE_PATH)
        user_was_changed = True

    elif action == 'p':
        current_date -= datetime.timedelta(days = 1)

    elif action == 'n':
        current_date += datetime.timedelta(days = 1)
    
    elif action == 's':
        system('python3 ' + SS_PATH + ' -i')

    elif action == 'h':
        print(MENU_HELPS['main'])
        a = input()

    elif action == 'l':
        screen_name = 'food_db'
        while True:
            clear()
            res = get_food_data(cur)

            # Disable tab-completion
            readline.parse_and_bind('tab: \t')

            screen(
                HEADERS[screen_name],
                lambda: print_as_table( [('title','kcal','p', 'f', 'c',)] + res,  ' ') if res else print(EMPTY_BODY[screen_name]),
                MENUS_ENTRIES[screen_name], 2)

            action = input('>> ').lower().strip()

            if action == 'q':
                break
            
            elif action == 'a':
                screen_name = 'analyzer'
                while True:
                    dishes_list = get_dishes_list(cur)
                    # АНАЛИЗАТОР РЕЦЕПТА
                    screen(
                        HEADERS[screen_name],
                        lambda: print(*dishes_list) if dishes_list else print(EMPTY_BODY[screen_name]),
                        MENUS_ENTRIES[screen_name], 3)

                    action = input('>> ').lower().strip()

                    if action == 'q':
                        break
                    elif action == 'c':
        #  введите список продуктов с указанием количества, помогает табуляция
        #  проверка, все ли продукты известны
        #  подсчет данныэ
        #  введите название блюда
        #  сохранение в бд dishes
                        print('Not implemented yet')
                        sleep(1)
    
                    elif action == 'r':
                        print('Not implemented yet')
                        sleep(1)

                    elif action == 'h':
                        print(MENU_HELPS['analyzer'])
                        a = input()
    
                    else:
                        print('Unsupported action')
                        sleep(1)


            elif action == 'h':
                print(MENU_HELPS['food'])
                a = input()

            elif action == 'r':
                print('Not implemented yet')
                sleep(1)
            
            elif action not in 'arqh' and len(action) > 3:

                d = get_data(new_food_params, 1)
                d['title'] = action
                add_new_food(cur, d)
                con.commit()
                db_was_changed = True

            else:
                print('Unsupported action')
                sleep(1)
                
    elif action not in 'lpnqht' and len(action) > 3:

        new_entry = { 'date': current_date, 'user': user_id, }
        data = parse_line(action)
        
        if data is None:
            new_entry['title'] = action
            new_entry['value'] = promt('количество') 
        else:
            new_entry['title'] = data[0]
            new_entry['value'] = data[1] 
        
        if is_in_db(cur, new_entry['title']) is None:
            print('Похоже, что такого блюда нет в базе\nТребуется ввод дополнительной инофрмации')
            
            # Добавляем новый продукт в БД
            d = get_data({'kcal': 'калорийность', 
                          'p': 'содержание белков', 
                          'f': 'содержание жиров',
                          'c': 'содержание углеводов'}, 1)
            
            d['title'] = new_entry['title']
            add_new_food(cur, d)
            con.commit()
            db_was_changed = True
        
        # Добавляем запись в дневник
        add_in_diary(cur, new_entry)
        con.commit()
    else:
        print("Unsupported action")
        sleep(1)

