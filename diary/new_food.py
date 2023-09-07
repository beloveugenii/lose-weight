#!/usr/bin/env python3

import sqlite3
from time import sleep
import datetime
import libfc as fc

# Создаем подключение к БД и объект для работы с sql-запросами
con = sqlite3.connect('fc.db')
cur = con.cursor()

# Создаем таблицы с данными о продуктах и дневник питания
cur.execute("CREATE TABLE IF NOT EXISTS food(title TEXT, kcal REAL, p REAL, f REAL, c REAL)")
cur.execute("CREATE TABLE IF NOT EXISTS diary(date TEXT, title TEXT, value REAL)")

current_date = datetime.date.today().strftime('%Y-%m-%d')

while True:
    fc.clear()
    fc.header('Дневник питания ' + current_date)

    diary = cur.execute("SELECT d.title, value, f.kcal * (d.value / 100) AS calories FROM diary AS d INNER JOIN food AS f WHERE d.title = f.title and date = ?", (current_date,))

    # информация о пользовтеле
    fc.print_diary(diary.fetchall())
    
    fc.menu(['add', 'quit', 'testts', 'strings', 'a', 'text'])
    
    action = input()
    if action == 'a':
        n = fc.get_data('diary', 0)
        n['date'] = current_date 
        
        # Пытаемся получить данные из БД
        res = (cur.execute("SELECT title, kcal FROM food WHERE title = :title", n)).fetchone()

        if res is None:
            print('\nПохоже, что такого блюда нет в базе\nТребуется ввод дополнительной инофрмации\n')
    
            d = fc.get_data('db', 0)
    
            cur.execute('INSERT INTO food VALUES(:title, :kcal, :p, :f, :c)', d)
            con.commit()
    
            res = cur.execute("SELECT title, kcal FROM food WHERE title = :title", n)

        cur.execute("INSERT INTO diary VALUES(:date, :title, :value)", n)
        con.commit()
    elif action == 'q':
        con.close()
        exit(0)
    else:
        print('Неизвестная команда')
        sleep(1)


    


