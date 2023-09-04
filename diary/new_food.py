#!/usr/bin/env python3

import sqlite3
from time import sleep
import datetime
import screen as scr

con = sqlite3.connect('fc.db')
cur = con.cursor()

# Данные о продуктах
cur.execute("CREATE TABLE IF NOT EXISTS food(title TEXT, kcal REAL, p REAL, f REAL, c REAL)")

# Дневник питания
cur.execute("CREATE TABLE IF NOT EXISTS diary(date TEXT, title TEXT, value REAL)")

def is_float(it):
    # Функция аргумент - число или числововая строка
    # Возвращает Истинну, если параметр - число с точкой
    it = str(it)
    if it.startswith('-'):
        it = it[1:]
    parts = it.split('.')
    return len(parts) == 2 and parts[0].isnumeric() and parts[1].isnumeric()








def get_data(for_place, delay):
    # Функция последовательно запрашивает данные, зависящие от первого параметра - места, куда они будут сохраняться
    # Второй параметр - задержка в секундах между появлением сообщения о неверном вводе и новым приглашением на ввод
    # Название любая не пустая строка, остальные параметры - натуральные или вещественные числа
    # Возвращает словарь с данными
    data = {}
    if for_place == 'db':
        data = {'title': 'название', 'kcal': 'калорийность', 'p': 'содержание белков', 'f': 'содержание жиров', 'c': 'содержание углеводов'}
    elif for_place == 'diary':
        data = {'title': 'блюдо', 'value': 'количество'}

    for key in data:
        if key == 'title':
            while True:
                it = input(scr.promt(data[key]))
                if len(it) < 1:
                    print('Требуется название')
                    sleep(delay)
                else:
                    data[key] = it
                    break
        else:
            while True:
                try:
                    it = input(scr.promt(data[key]))
                    if it == '':
                        it = 0
                    data[key] = float(it)
                    break
                except ValueError:
                    print('Здесь требуется число')
                    sleep(delay)

    return data



current_date = datetime.date.today().strftime('%Y-%m-%d')
scr.clear()

scr.header('Дневник питания ' + current_date)

#diary = cur.execute("SELECT title, value FROM diary WHERE date = ?", (datetime.date.today(),))

diary = cur.execute("SELECT d.title, value, f.kcal * (d.value / 100) AS calories FROM diary AS d INNER JOIN food AS f WHERE d.title = f.title and date = ?", (current_date,))

for line in diary.fetchall():
    print(line)

scr.menu(['add'])

if input() == 'a':
    n = get_data('diary', 0)
    n['date'] = current_date 
    
    res = (cur.execute("SELECT title, kcal FROM food WHERE title = :title", n)).fetchone()


    if res is None:
        print('\nПозоже, что такого блюда нет в базе\nТребуется ввод дополнительной инофрмации\n')
    
        d = get_data('db', 0)
    
        cur.execute('INSERT INTO food VALUES(:title, :kcal, :p, :f, :c)', d)
        con.commit()
    
        res = cur.execute("SELECT title, kcal FROM food WHERE title = :title", n)

    cur.execute("INSERT INTO diary VALUES(:date, :title, :value)", n)
    con.commit()


    

# запрашиваем бд, есть ли такое блюдо уже в ней
# Если есть - дергаем данные, подсчитываем клорийность порции

