#!/usr/bin/env python3

import sqlite3, datetime, readline, os, signal, sys
from time import sleep
from libsui import *

VERSION = '0.1.6'
NAME = 'fcrasher.py'
CONFIG_FILE_PATH = sys.path[0] + '/config'
DB_NAME = sys.path[0] + '/fc.db'

def get_user_id(file):
    try:
        # Пытаемся получить номера активного пользователя из файла
        f = open(file, 'r')
        for line in f:
            user_id = line.split('=')[1].strip()
        f.close()
    except FileNotFoundError:
        user_id = None
    return user_id

def set_user_id(file, user_id):
    f = open(file, 'a')
    f.write('uid='+str(user_id)+'\n')
    f.close()

def get_calories_norm(user_data):

    basic = 10 * user_data['weight'] + 6.25 * user_data['height'] - 5 * user_data['age']
    # Для мужчин
    if user_data['sex'] in 'мМmM':
        return str((basic + 5)  * user_data['activity'])[:-1]
    # Для женщин
    elif user_data['sex'] in 'жЖfF':
        return str((basic - 161) * user_data['activity'])[:-1]

   
def get_data(params, delay):
    data = dict()
    for key in params:
        if key in ('title', 'name', 'sex'):
            while True:
                it = promt(params[key])
                if len(it) < 2 and not key == 'sex':
                    print('Слишком короткая строка')
                    sleep(delay)
                else:
                    if key == 'sex' and it not in 'мМжЖmMfF':
                        print('Требуется обозначение пола: [мМ или жЖ]')
                        sleep(delay)
                    else:
                        data[key] = it
                        break
        elif key in ('kcal', 'age', 'height', 'weight', 'value', 'activity', 'p', 'c', 'f'):
            while True:
                if key == 'activity':
                    print("1.2 – минимальная активность, сидячая работа, не требующая значительных физических нагрузок", "1.375 – слабый уровень активности: интенсивные упражнения не менее 20 минут один-три раза в неделю", "1.55 – умеренный уровень активности: интенсивная тренировка не менее 30-60 мин три-четыре раза в неделю", "1.7 – тяжелая или трудоемкая активность: интенсивные упражнения и занятия спортом 5-7 дней в неделю или трудоемкие занятия", "1.9 – экстремальный уровень: включает чрезвычайно активные и/или очень энергозатратные виды деятельности", sep='\n')

                try:
                    it = promt(params[key])

                    if it == '':
                        it = 1 if key == 'activity' else 0

                    data[key] = float(it)
                    break
                except ValueError:
                    print('Здесь требуется число')
                    sleep(delay)

    return data

# Обработчик нажатия Ctrl-C
def sigint_handler(signum, frame):
    signame = signal.Signals(signum).name
    clear()
    print(f'Catched {signame}')
    exit(1)

def validate(what, need_type):
    ''''''
    what = str(what)

    def isfloat(what):
        if what.startswith('-'):
            what = what[1:]
        parts = what.split('.')
        return len(parts) == 2 and parts[0].isnumeric() and parts[1].isnumeric()

    if need_type == 'int':
        return what.isdigit()
    elif need_type == 'float':
        return isfloat(what)
    else:
        return 'Unsupported type'

# Enable SIG handlers and configure readline
signal.signal(signal.SIGINT, sigint_handler)

readline.set_completer_delims('\n')

# Создаем подключение к БД и объект для работы с sql-запросами
con = sqlite3.connect(DB_NAME)
cur = con.cursor()

# Создаем таблицы с данными о продуктах, дневник питания и о пользователе
cur.execute("CREATE TABLE IF NOT EXISTS food(title TEXT, kcal REAL, p REAL, f REAL, c REAL)")
cur.execute("CREATE TABLE IF NOT EXISTS diary(user INT, date TEXT, title TEXT, value REAL)")
cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, sex TEXT, age INT, height REAL, weight REAL, activity REAL)")

user_id = get_user_id(CONFIG_FILE_PATH)

while user_id is None:
    users = (cur.execute('SELECT rowid, name FROM users')).fetchall()
    screen('Выбор пользователя', 
           lambda: print_as_table(users, ' ') if users else print('No users found in database'),
           ['new', 'quit'], 0)

    # Enable tab-completion
    readline.parse_and_bind('tab: complete')

    readline.set_completer(completer([str(n[0]) for n in cur.execute('select rowid from users').fetchall()]).complete)

    choice = input('>> ').lower().strip()
    
    if choice.isdigit():
        user_id = int(choice)
        set_user_id(CONFIG_FILE_PATH, user_id)
    
    elif choice == ':n':
        user_data = get_data( {'name': 'ваше имя', 
                      'sex': 'ваш пол', 
                      'age': 'ваш возраст', 
                      'height': 'ваш рост', 
                      'weight': 'ваш вес', 
                      'activity': 'ваша активность'}, 1)

        cur.execute("INSERT INTO users VALUES(:name, :sex, :age, :height, :weight, :activity)", user_data)
        con.commit()

    elif choice == ':q':
        exit(0)
    
    elif choice == ':h':
        print("Type user ID for choosing", 
              "':n' create new user",
              "':h' show this help",
              "':q' quit", sep='\n')

        a = input()
    
    else:
        print('Unsupported action')
        sleep(1)
         
user_data = dict(
                map(lambda *args: args, 
                    ('rowid', 'name', 'sex', 'age', 'height', 'weight', 'activity'), 
                    (cur.execute("SELECT rowid, * from users WHERE rowid = ?", (user_id,)).fetchone())
                )
            )

current_date = datetime.date.today()

while True:
    clear()
    food_list = cur.execute("SELECT title FROM food").fetchall()
    
    diary = cur.execute("SELECT d.title, value, ROUND(f.kcal * (d.value / 100), 1) AS calories FROM diary AS d INNER JOIN food AS f WHERE d.title = f.title and date = ? and user = ?", (current_date.strftime('%Y-%m-%d'), user_id)).fetchall()
    
    kcal_norm = get_calories_norm(user_data)
    kcal_per_day = '%.1f' % sum([line[2] for line in diary])
    
    screen('Дневник питания ' + current_date.strftime('%Y-%m-%d'),
                    lambda: print_as_table( [('норма калорий'.upper(), '', kcal_norm)] + diary + [('всего'.upper(), '', kcal_per_day)],  ' ' ) if diary else print(f'No entries at {current_date}'),
           ['list of food', 'previous entry', 'next entry', 'trainings', 'quit'], 0)
    
    # Enable tab-completion
    readline.parse_and_bind('tab: complete')
    readline.set_completer(completer([food[0] for food in food_list]).complete)

    action = input('>> ').lower().strip()
    
    if action == ':q':
        break
    
    elif action == ':p':
        current_date -= datetime.timedelta(days = 1)

    elif action == ':n':
        current_date += datetime.timedelta(days = 1)
    
    elif action == ':t':
        os.system('perl ' + os.path.dirname(__file__) + '/s_assist.pl -i')

    elif action == ':h':
        print("Enter the name of the food to be entered in the diary", 
              "':n' go to the next day",
              "':p' go to the previous day",
              "':l' show food in database",
              "':t' go to sport assistant",
              "':h' show this help",
              "':q' quit", sep='\n')
        a = input()

    elif action == ':l':
        while True:
            clear()
            res = sorted((cur.execute('select title, cast(kcal as int), cast(p as int), cast(f as int), cast(c as int) from food')).fetchall())

            # Disable tab-completion
            readline.parse_and_bind('tab: \t')

            screen('Внесение данных о новом продукте',
                   lambda: print_as_table( [('title','kcal','p', 'f', 'c',)] + res,  ' ') if res else print("No data in database yet"),
                    ['remove', 'quit'], 0)

            action = input('>> ').lower().strip()

            if action == ':q':
                break
           
            elif action == ':h':
                print("Enter the name of the food to be entered in database", 
                    "':r' remove from database",
                    "':h' show this help",
                    "':q' go back", sep='\n')
                a = input()

            elif action == ':r':
                print('Not implemented yet')
                sleep(1)
            
            elif action not in [':' + c for c in 'rqh'] and len(action) > 3:
            #elif action not in (':r', ':q', ':h') and len(action) > 3:

                d = get_data({ 'kcal': 'калорийность', 
                       'p': 'содержание белков', 
                       'f': 'содержание жиров', 'c': 
                       'содержание углеводов'}, 1)
                d['title'] = action

                cur.execute('INSERT INTO food VALUES(:title, :kcal, :p, :f, :c)', d)
                con.commit()

            else:
                print('Unsupported action')
                sleep(1)
                
    elif action not in [':' + c for c in 'lpnqht'] and len(action) > 3:
 #   elif action not in [':' + cfor c in 'lpnqht'](':l', ':p', ':n', ':q', ':h', ':t') and len(action) > 3:

        new_entry = {'title': action,
                     'value': promt('количество'),
                     'date': current_date,
                     'user': user_id}

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
        
        # Добавляем запись в дневник
        cur.execute("INSERT INTO diary VALUES(:user, :date, :title, :value)", new_entry)
        con.commit()
    else:
        print("Unsupported action")
        sleep(1)
