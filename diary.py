#!/usr/bin/env python3

import sqlite3, datetime
from time import sleep
import libui as ui

   
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
    data = {'title': 'блюдо', 'value': 'количество'}
    
    if for_place == 'db':
        
        data = {'title': 'название', 'kcal': 'калорийность', 'p': 'содержание белков', 'f': 'содержание жиров', 'c': 'содержание углеводов'}
    
    elif for_place == 'user_data':
        
        data = {'name': 'ваше имя', 'sex': 'ваш пол', 'age': 'ваш возраст', 'height': 'ваш рост', 'weight': 'ваш вес', 'activity': 'ваша активность'}

    for key in data:
        if key in ('title', 'name', 'sex'):
            while True:
                it = ui.promt(data[key])
                if len(it) < 1:
                    print('Требуется строка')
                    sleep(delay)
                else:
                    data[key] = it
                    break
        else:
            while True:
                if key == 'activity':
                    print("1.2 – минимальная активность, сидячая работа, не требующая значительных физических нагрузок", "1.375 – слабый уровень активности: интенсивные упражнения не менее 20 минут один-три раза в неделю", "1.55 – умеренный уровень активности: интенсивная тренировка не менее 30-60 мин три-четыре раза в неделю", "1.7 – тяжелая или трудоемкая активность: интенсивные упражнения и занятия спортом 5-7 дней в неделю или трудоемкие занятия", "1.9 – экстремальный уровень: включает чрезвычайно активные и/или очень энергозатратные виды деятельности", sep='\n')
                try:
                    it = ui.promt(data[key])
                    if for_place != 'user_data' and it == '':
                        it = 0
                    data[key] = float(it)
                    break
                except ValueError:
                    print('Здесь требуется число')
                    sleep(delay)

    return data

def tup_to_dict(keys, values):
    # Принимает два списка и строит из них словарь
    d = {}
    for i in range(len(keys)):
        d[keys[i]] = values[i]
    return d


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
        ui.clear()
        ui.header('Выбор пользователя')
        for line in (cur.execute('SELECT rowid, name FROM users').fetchall()):
            print("\t%d\t%s" % line)
        ui.menu(['new user', 'user id', 'quit'], 2)

        act = ''
        while len(act) == 0:
            act = ui.promt('>>').strip()[0]
            
        if act == 'n':
        # Можно создать нового пользователя
            ud = get_data('user_data', 0)
            cur.execute("INSERT INTO users VALUES(:name, :sex, :age, :height, :weight, :activity)", ud)
            con.commit()
        
        elif act == 'q':
            exit(0)

        elif act.isdigit():
        # Можно выбрать существующего, если ввести его номер
            if int(act) in [ line[0] for line in cur.execute('SELECT rowid FROM users').fetchall()]:
                user_rowid = act
                f = open('config', 'a')
                f.write('uid='+str(user_rowid)+'\n')
                f.close()
                break 
            else:
                print("Нет пользователя с таким номером")
        else:
            print('Выберите пользователя или создайте нового')
            sleep(1)
        

current_date = datetime.date.today().strftime('%Y-%m-%d')

def print_diary(ud, arr):
    # Показывает содержимое дневника за ень
    t_kcal = sum([line[2] for line in arr])
    basic = 10 * ud['weight'] + 6.25 * ud['height'] - 5 * ud['age']

    l, f = ui.get_fields_len(arr + [('суточная норма калорий:',)])
    # Для мужчин
    if ud['sex'] in 'мМmM':
        basic = (basic + 5)  * ud['activity']
    # Для женщин
    elif ud['sex'] in 'жЖfF':
        basic = (basic - 161) * ud['activity']

    print('%s%-*s%s%-*s%s%-*s%s' % (' ' * f, l[0], 'Суточная норма калорий:'.upper(),  ' ' * f, l[1], ' ',  ' ' * f, l[2], basic, ' ' * f))
    print() 
    ui.print_as_table(arr,  ' ')
    print() 
    print('%s%-*s%s%-*s%s%-*s%s' % (' ' * f, l[0], 'Всего:'.upper(),  ' ' * f, l[1], ' ', ' ' * f, l[2], t_kcal, ' ' * f))
    
 


# Получаем данные пользователя из БД по его rowid
ud = cur.execute("SELECT rowid, * from users WHERE rowid = ?", (user_rowid,))

ud = tup_to_dict(('rowid', 'name', 'sex', 'age', 'height', 'weight', 'activity'), ud.fetchone())

while True:
    # Основной экран дневника питания
    ui.clear()
    ui.header('Дневник питания ' + current_date)

    # Получаем данные из дневника для нужного пользователя за текущее числоа
    diary = cur.execute("SELECT d.title, value, f.kcal * (d.value / 100) AS calories FROM diary AS d INNER JOIN food AS f WHERE d.title = f.title and date = ? and user = ?", (current_date, user_rowid)).fetchall()

    try:
        print_diary(ud, diary)
    except IndexError:
        print()
    # Выводим дневник и меню
    ui.menu(['add in diary', 'new in database','quit'], 2)
    
    action = ui.promt('>>').strip()[0]
    
    if action in 'aA':
        # Добавляем новое блюдо
        n = get_data('diary', 1)
        n['date'] = current_date
        n['user'] = user_rowid
        
        # Пытаемся получить данные о введенном продукте из БД
        res = (cur.execute("SELECT title, kcal FROM food WHERE title = :title", n)).fetchone()
        
        # Если данных нет, то запрашиваем их у пользователя
        if res is None:
            print('\nПохоже, что такого блюда нет в базе\nТребуется ввод дополнительной инофрмации\n')
            
            # Добавляем новый продукт в БД
            d = get_data('db', 0)
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


    


