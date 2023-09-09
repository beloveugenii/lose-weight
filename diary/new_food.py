#!/usr/bin/env python3

import sqlite3
from time import sleep
import datetime
import libfc as fc

# Создаем подключение к БД и объект для работы с sql-запросами
con = sqlite3.connect('fc.db')
cur = con.cursor()

# Создаем таблицы с данными о продуктах, дневник питания и о пользователе
cur.execute("CREATE TABLE IF NOT EXISTS food(title TEXT, kcal REAL, p REAL, f REAL, c REAL)")
cur.execute("CREATE TABLE IF NOT EXISTS diary(user INT, date TEXT, title TEXT, value REAL)")
cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT, sex TEXT, age INT, height REAL, weight REAL, activity REAL)")

try:
    # Пытаемся получить номера активного пользователя
    f = open("config", 'r')
    for line in f:
        user_rowid = line.split('=')[1].strip()
    f.close()
except FileNotFoundError:
    while True:
        # Экран выбора пользователя
        fc.clear()
        fc.header('Выбор пользователя')
        for line in (cur.execute('SELECT rowid, name FROM users').fetchall()):
            print("\t%d\t%s" % line)
        fc.menu(['new user', 'user id', 'quit'])

        act = input('>> ').strip()

        if act == 'n':
        # Можно создать нового пользователя
            ud = fc.get_data('user_data', 0)
            cur.execute("INSERT INTO users VALUES(:name, :sex, :age, :height, :weight, :activity)", ud)
            con.commit()
        elif act == 'q':
            exit(0)
        else:
        # Можно выбрать существующего, если ввести его номер
            if int(act) in [ line[0] for line in cur.execute('SELECT rowid FROM users').fetchall()]:
                user_rowid = act
                f = open('config', 'a')
                f.write('uid='+str(user_rowid)+'\n')
                f.close()
                break 
            else:
                print("Нет пользователя с таким номером")
                sleep(1)

        

current_date = datetime.date.today().strftime('%Y-%m-%d')
# Получаем данные пользователя из БД по его rowid
ud = cur.execute("SELECT rowid, * from users WHERE rowid = ?", (user_rowid,))
ud = fc.tup_to_dict(('rowid', 'name', 'sex', 'age', 'height', 'weight', 'activity'), ud.fetchone())

while True:
    # Основной экран дневника питания
    fc.clear()
    fc.header('Дневник питания ' + current_date)

    # Получаем данные из дневника для нужного пользователя за текущее числоа
    diary = cur.execute("SELECT d.title, value, f.kcal * (d.value / 100) AS calories FROM diary AS d INNER JOIN food AS f WHERE d.title = f.title and date = ? and user = ?", (current_date, user_rowid))
    # Выводим дневник и меню
    fc.print_diary(ud, diary.fetchall())
    fc.menu(['add in diary', 'new in database','quit'])
    
    action = input('>> ')
    if action in 'aA':
        # Добавляем новое блюдо
        n = fc.get_data('diary', 1)
        n['date'] = current_date
        n['user'] = user_rowid
        
        # Пытаемся получить данные о введенном продукте из БД
        res = (cur.execute("SELECT title, kcal FROM food WHERE title = :title", n)).fetchone()
        
        # Если данных нет, то запрашиваем их у пользователя
        if res is None:
            print('\nПохоже, что такого блюда нет в базе\nТребуется ввод дополнительной инофрмации\n')
            
            # Добавляем новый продукт в БД
            d = fc.get_data('db', 0)
            cur.execute('INSERT INTO food VALUES(:title, :kcal, :p, :f, :c)', d)
            con.commit()
            # Получаем данные о новом продукте
            res = cur.execute("SELECT title, kcal FROM food WHERE title = :title", n)
        
        # Добавляем запись в дневник
        cur.execute("INSERT INTO diary VALUES(:user, :date, :title, :value)",  n)
        con.commit()
    elif action in 'nN':
        # Добавляем новый продукт в БД
        d = fc.get_data('db', 0)
        cur.execute('INSERT INTO food VALUES(:title, :kcal, :p, :f, :c)', d)
        con.commit()
    

    elif action in 'qQ':
        con.close()
        exit(0)
    else:
        print('Неизвестная команда')
        sleep(1)


    


