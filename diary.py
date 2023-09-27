#!/usr/bin/env python3

import sqlite3, datetime, readline
from time import sleep
from libsui import *

config_file_path = './config'

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
        return (basic + 5)  * user_data['activity']
    # Для женщин
    elif user_data['sex'] in 'жЖfF':
        return(basic - 161) * user_data['activity']

   
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

def tuple_to_dict(keys, values):
    # Принимает два списка и строит из них словарь
    d = {}
    for i in range(len(keys)):
            d[keys[i]] = values[i]
    return d
 
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

# Создаем подключение к БД и объект для работы с sql-запросами
con = sqlite3.connect('fc.db')
cur = con.cursor()

# Создаем таблицы с данными о продуктах, дневник питания и о пользователе
cur.execute("CREATE TABLE IF NOT EXISTS food(title TEXT, kcal REAL, p REAL, f REAL, c REAL)")
cur.execute("CREATE TABLE IF NOT EXISTS diary(user INT, date TEXT, title TEXT, value REAL)")
cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, sex TEXT, age INT, height REAL, weight REAL, activity REAL)")

user_id = get_user_id(config_file_path)

readline.parse_and_bind('tab: complete')

while user_id is None:
    users = (cur.execute('SELECT rowid, name FROM users')).fetchall()
    screen('Выбор пользователя', 
           lambda: print_as_table(users, ' ') if users else print('No users found in database'),
           ['new', 'quit'], 2)

    readline.set_completer(completer([str(n[0]) for n in cur.execute('select rowid from users').fetchall()] + ['n', 'q']).complete)
    choice = promt('>>').lower()
    
    if choice.isdigit():
        user_id = int(choice)
        set_user_id(config_file_path, user_id)
    
    elif choice.startswith('n'):
        user_data = get_data( {'name': 'ваше имя', 
                      'sex': 'ваш пол', 
                      'age': 'ваш возраст', 
                      'height': 'ваш рост', 
                      'weight': 'ваш вес', 
                      'activity': 'ваша активность'}, 0)

        cur.execute("INSERT INTO users VALUES(:name, :sex, :age, :height, :weight, :activity)", user_data)
        con.commit()
     
    elif choice.startswith('q'):
        exit(0)
    
    else:
        print('Unsupported action')
        sleep(1)
         

user_data = tuple_to_dict( ('rowid', 'name', 'sex', 'age', 'height', 'weight', 'activity'), 
                         (cur.execute("SELECT rowid, * from users WHERE rowid = ?", (user_id,)).fetchone()))

current_date = datetime.date.today().strftime('%Y-%m-%d')



while True:

    food_list = cur.execute("SELECT title FROM food").fetchall()
    
    diary = cur.execute("SELECT d.title, value, f.kcal * (d.value / 100) AS calories FROM diary AS d INNER JOIN food AS f WHERE d.title = f.title and date = ? and user = ?", (current_date, user_id)).fetchall()
    
    kcal_norm = get_calories_norm(user_data)
    kcal_per_day = sum([line[2] for line in diary])
    
    screen('Дневник питания ' + current_date,
                    lambda: print_as_table( [('норма калорий'.upper(), '', kcal_norm)] + diary + [('всего'.upper(), '', kcal_per_day)],  ' ' ) if diary else print(f'No entries at {current_date}'),
                    ['new food type', 'previous entry', 'quit'], 2)
    
    readline.set_completer(completer([food[0] for food in food_list] + ['n', 'p', 'q']).complete)
    
    action = promt('>>').lower()
    
    if action.startswith('q'):
        break
    
    elif action.startswith('p'):
        print('Not implemented yet')
        sleep(1)
    
    elif action.startswith('n'):
        while True:

            res = (cur.execute('select * from food')).fetchall()

            screen('Внесение данных о новом продукте',
                   lambda: print_as_table( [('title','kcal','p', 'f', 'c',)] + res,  ' ') if res else print("No data in database yet"),
                    ['add', 'remove', 'quit'], 3)

            action = promt('>>').lower()

            if action.startswith('a'):
                d = get_data({'title': 'название',
                       'kcal': 'калорийность', 
                       'p': 'содержание белков', 
                       'f': 'содержание жиров', 'c': 
                       'содержание углеводов'}, 1)
                cur.execute('INSERT INTO food VALUES(:title, :kcal, :p, :f, :c)', d)
                con.commit()

            elif action.startswith('r'):
                print('Not implemented yet')
                sleep(1)
            elif action.startswith('q'):
                break
            else:
                print('Unsupported action')
                sleep(1)
                
        
    
    elif not (action.startswith('n') or action.startswith('q')) and len(action) > 3:

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
