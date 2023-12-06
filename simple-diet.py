#!/usr/bin/env python3

import sqlite3, datetime, readline, signal
from os import system
from lib import *

PROG_NAME = 'simple-diet'
VERSION = '0.1.6a'
CONFIG_FILE_PATH = sys.path[0] + '/config'
DB_NAME = sys.path[0] + '/fc.db'
SS_PATH = sys.path[0] + '/simple-sport.py'
ANALYST_PATH = sys.path[0] + '/analyst.py'

current_date = datetime.date.today()
db_was_changed = False
user_was_changed = False

# Обработчик нажатия Ctrl-C
def sigint_handler(signum, frame):
    signame = signal.Signals(signum).name
    clear()
    print(f'Catched {signame}')
    exit(1)


# Creating connection to database and creating needed tables
con = sqlite3.connect(DB_NAME)
cur = con.cursor()

for stmt in SQL_CREATE_STMT.values():
    cur.execute(stmt)

# Enable SIG handlers and configure readline
signal.signal(signal.SIGINT, sigint_handler)
readline.set_completer_delims('\n')



########################
def set_user():
    while True:
        # Get user information from DB
        users = (cur.execute('SELECT rowid, name FROM users')).fetchall()
    
        # Prints screen with user information
        screen(HEADERS['user_ch'],
               lambda: print_as_table(users, ' ') if users else print('No users found in database'),
               ['new user creating', 'help', 'quit'], 3
        )

        uch = input('>> ').lower().strip()
    
        if uch.isdigit():
            # if user input is digit write it into file
            user_id = int(uch)
            set_user_id(CONFIG_FILE_PATH, user_id)
            break

        elif uch == 'n':
            # if uses input is 'n' asks data for creating new user

            user_data = get_data( { 
                               'name': 'ваше имя', 
                               'sex': 'ваш пол', 
                               'age': 'ваш возраст', 
                               'height': 'ваш рост', 
                               'weight': 'ваш вес', 
                               'activity': 'ваша активность'}, 1)

            cur.execute("INSERT INTO users VALUES(:name, :sex, :age, :height, :weight, :activity)", user_data)
            con.commit()

        elif uch == 'q':
            # if user input is 'q' quit from program
            exit(0)
    
        elif uch == 'h':
            print(MENU_HELPS['users'])

            a = input()
    
        else:
            print('Unsupported action')
            sleep(1)
        
    return user_id
#######################

# Try to get id of current user from config file
user_id = get_user_id(CONFIG_FILE_PATH)

if user_id is None:
    user_id = set_user()


user_data = dict( 
                map(lambda *args: args, 
                    ('rowid', 'name', 'sex', 'age', 'height', 'weight', 'activity'), 
                    (cur.execute("SELECT rowid, * from users WHERE rowid = ?", (user_id,)).fetchone())
                )
            )




food_list = cur.execute("SELECT title FROM food").fetchall() + cur.execute("SELECT title FROM dishes").fetchall()

while True:
    clear()
    if db_was_changed:
        food_list = cur.execute("SELECT title FROM food").fetchall() + cur.execute("SELECT title FROM dishes").fetchall()
        db_was_changed = False

    if user_was_changed:
        user_data = dict(
                map(lambda *args: args, 
                    ('rowid', 'name', 'sex', 'age', 'height', 'weight', 'activity'), 
                    (cur.execute("SELECT rowid, * from users WHERE rowid = ?", (user_id,)).fetchone())
                )
            )
        user_was_changed = False


    diary = cur.execute("SELECT d.title, value, ROUND(f.kcal * (d.value / 100), 1) AS calories FROM diary AS d INNER JOIN food AS f WHERE d.title = f.title and date = ? and user = ?", (current_date.strftime('%Y-%m-%d'), user_id)).fetchall()
    
    kcal_norm = get_calories_norm(user_data)
    kcal_per_day = '%.1f' % sum([line[2] for line in diary])
    
    screen(HEADERS['diary'] + ' ' + current_date.strftime('%Y-%m-%d'),
                    lambda: print_as_table( [('норма калорий'.upper(), '', kcal_norm)] + diary + [('всего'.upper(), '', kcal_per_day)],  ' ' ) if diary else print(f'No entries at {current_date}'),
           ['list of food', 'users', 'previous entry', 'next entry', 'simple-sport', 'help', 'quit'], 2)
    
    # Enable tab-completion
    readline.parse_and_bind('tab: complete')
    readline.set_completer(completer([food[0] for food in food_list]).complete)

    action = input('>> ').lower().strip()
    
    if action == 'q':
        break
    
    elif action == 'u':
        user_id = set_user()
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
        while True:
            clear()
            res = sorted((cur.execute('select title, cast(kcal as int), cast(p as int), cast(f as int), cast(c as int) from food')).fetchall())

            # Disable tab-completion
            readline.parse_and_bind('tab: \t')

            screen(HEADERS['food_db'],
                   lambda: print_as_table( [('title','kcal','p', 'f', 'c',)] + res,  ' ') if res else print("No data in database yet"),
                    ['analyst', 'remove', 'help', 'quit'], 2)

            action = input('>> ').lower().strip()

            if action == 'q':
                break
            
            elif action == 'a':
                print('Not implemented yet')
                sleep(1)
                #os.system('python ' + ANALYST_PATH)

            elif action == 'h':
                print(MENU_HELPS['food'])
                a = input()

            elif action == 'r':
                print('Not implemented yet')
                sleep(1)
            
            elif action not in 'arqh' and len(action) > 3:

                d = get_data({ 'kcal': 'калорийность', 
                              'p': 'содержание белков', 
                              'f': 'содержание жиров',
                              'c': 'содержание углеводов'}, 1)
                d['title'] = action

                cur.execute('INSERT INTO food VALUES(:title, :kcal, :p, :f, :c)', d)
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
        
        res = (cur.execute("SELECT title, kcal FROM food WHERE title = :title", new_entry)).fetchone()
        
        if res is None:
            print('Похоже, что такого блюда нет в базе\nТребуется ввод дополнительной инофрмации')
            
            # Добавляем новый продукт в БД
            d = get_data({'kcal': 'калорийность', 
                          'p': 'содержание белков', 
                          'f': 'содержание жиров',
                          'c': 'содержание углеводов'}, 1)
            
            d['title'] = new_entry['title']

            cur.execute('INSERT INTO food VALUES(:title, :kcal, :p, :f, :c)', d)
            con.commit()
            db_was_changed = True
        
        # Добавляем запись в дневник
        cur.execute("INSERT INTO diary VALUES(:user, :date, :title, :value)", new_entry)
        con.commit()
    else:
        print("Unsupported action")
        sleep(1)

