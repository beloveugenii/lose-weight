#!/usr/bin/env python3

import sqlite3, datetime, readline
from time import sleep
import libui as ui
import libsui as sui

# Регистрация клавиши `tab` для автодополнения
readline.parse_and_bind('tab: complete')

def is_float(it):
    # Функция аргумент - число или числововая строка
    # Возвращает Истинну, если параметр - число с точкой
    it = str(it)
    if it.startswith('-'):
        it = it[1:]
    parts = it.split('.')
    return len(parts) == 2 and parts[0].isnumeric() and parts[1].isnumeric()

def get_data(params, delay):
    data = dict()
    # Функция последовательно запрашивает данные, переданные в первом параметрe
    # Второй параметр - задержка в секундах между появлением сообщения о неверном вводе и новым приглашением на ввод
    # Название любая не пустая строка, остальные параметры - натуральные или вещественные числа
    # Возвращает словарь с данными
    for key in params:
        if key in ('title', 'name', 'sex'):
            while True:
                it = ui.promt(params[key])
                if len(it) < 1:
                    print('Требуется строка')
                    sleep(delay)
                else:
                    if key == 'sex' and it not in 'мМжЖmMfF':
                        print('Требуется обозначение пола: [мМ или жЖ]')
                        sleep(delay)
                    else:
                        data[key] = it
                        break
        elif key in ('kcal', 'age', 'height', 'weight', 'value'):
            while True:
                try:
                    it = ui.promt(params[key])
                    data[key] = float(it)
                    break
                except ValueError:
                    print('Здесь требуется число')
                    sleep(delay)
        else:
            while True:
                if key == 'activity':
                    print("1.2 – минимальная активность, сидячая работа, не требующая значительных физических нагрузок", "1.375 – слабый уровень активности: интенсивные упражнения не менее 20 минут один-три раза в неделю", "1.55 – умеренный уровень активности: интенсивная тренировка не менее 30-60 мин три-четыре раза в неделю", "1.7 – тяжелая или трудоемкая активность: интенсивные упражнения и занятия спортом 5-7 дней в неделю или трудоемкие занятия", "1.9 – экстремальный уровень: включает чрезвычайно активные и/или очень энергозатратные виды деятельности", sep='\n')
                try:
                    it = ui.promt(params[key])
                    if it == '':
                        it = 1 if key == 'activity' else 0
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
        act = sui.screen(
                'Выбор пользователя', 
                lambda: sui.print_as_table(cur.execute('SELECT rowid, name FROM users').fetchall(), ' '),
                ['new user', 'chooce', 'quit'], 3)
            
        if act.startswith('new'):
            ud = get_data( {'name': 'ваше имя', 
                      'sex': 'ваш пол', 
                      'age': 'ваш возраст', 
                      'height': 'ваш рост', 
                      'weight': 'ваш вес', 
                      'activity': 'ваша активность'}, 0)

            cur.execute("INSERT INTO users VALUES(:name, :sex, :age, :height, :weight, :activity)", ud)
            con.commit()
        
        elif act.startswith('q'):
            exit(0)

        elif act.startswith('ch'):
            user_rowid = sui.screen(
                'Выбор пользователя', 
                lambda: sui.print_as_table(cur.execute('SELECT rowid, name FROM users').fetchall(), ' '),
                [str(n[0]) for n in cur.execute('select rowid from users').fetchall()] + ['quit'], 2)
         
            if user_rowid.startswith('q'):
                exit(0)
        # Можно выбрать существующего, если ввести его номер
            f = open('config', 'a')
            f.write('uid='+str(user_rowid)+'\n')
            f.close()
            break 
        else:
            print('Выберите пользователя или создайте нового')
            sleep(1)
        

current_date = datetime.date.today().strftime('%Y-%m-%d')

def print_diary(ud, arr):
    # Показывает содержимое дневника за ень

    try:
        t_kcal = sum([line[2] for line in arr])
        basic = 10 * ud['weight'] + 6.25 * ud['height'] - 5 * ud['age']

        #l, f = ui.get_fields_len(arr )
        # Для мужчин
        if ud['sex'] in 'мМmM':
            basic = (basic + 5)  * ud['activity']
        # Для женщин
        elif ud['sex'] in 'жЖfF':
            basic = (basic - 161) * ud['activity']

    #print('%s%-*s%s%-*s%s%*s%s' % (' ' * f, l[0], 'норма калорий:'.upper(),  ' ' * f, l[1], ' ',  ' ' * f, l[2], basic, ' ' * f))
        sui.print_as_table(arr,  ' ')
        print() 
    #print('%s%-*s%s%-*s%s%*s%s' % (' ' * f, l[0], 'Всего:'.upper(),  ' ' * f, l[1], ' ', ' ' * f, l[2], t_kcal, ' ' * f))
    except IndexError:
        print(f'No records at {current_date}')
 
# Получаем данные пользователя из БД по его rowid

ud = (cur.execute("SELECT rowid, * from users WHERE rowid = ?", (user_rowid,)).fetchone())
if len(ud) == 0:
    print('В базе данных нет пользователей\nУдалите файл настроек и перезапустите программу')
    exit(-1)

ud = tup_to_dict(('rowid', 'name', 'sex', 'age', 'height', 'weight', 'activity'), ud)

food_list = cur.execute("select title from food").fetchall()


while True:
    # Основной экран дневника питания
    ui.clear()
    ui.header('Дневник питания ' + current_date)

    # Получаем данные из дневника для нужного пользователя за текущее числоа
    diary = cur.execute("SELECT d.title, value, f.kcal * (d.value / 100) AS calories FROM diary AS d INNER JOIN food AS f WHERE d.title = f.title and date = ? and user = ?", (current_date, user_rowid)).fetchall()

    #try:
    print_diary(ud, diary)
    #except IndexError:
    #    print(f'No records at {current_date}')

    # Выводим дневник и меню
    ui.menu(['add in diary', 'new in database','quit'], 2)
    
    readline.set_completer(ui.cmpl(['a', 'n', 'q']).complete)
    action = ui.promt('>>').strip()[0]
    
    if action in 'aA':
        readline.set_completer(ui.cmpl([f[0] for f in food_list]).complete)
        # Добавляем новое блюдо
        n = get_data({'title': 'блюдо', 
                      'value': 'количество'},1)
        n['date'] = current_date
        n['user'] = user_rowid
        
        # Пытаемся получить данные о введенном продукте из БД
        res = (cur.execute("SELECT title, kcal FROM food WHERE title = :title", n)).fetchone()
        
        # Если данных нет, то запрашиваем их у пользователя
        if res is None:
            print('Похоже, что такого блюда нет в базе\nТребуется ввод дополнительной инофрмации')
            
            # Добавляем новый продукт в БД
            d = get_data({'kcal': 'калорийность', 
                          'p': 'содержание белков', 
                          'f': 'содержание жиров',
                          'c': 'содержание углеводов'}, 1)
            
            d['title'] = n['title']

            cur.execute('INSERT INTO food VALUES(:title, :kcal, :p, :f, :c)', d)
            con.commit()
            # Получаем данные о новом продукте
            res = cur.execute("SELECT title, kcal FROM food WHERE title = :title", n)
        
        # Добавляем запись в дневник
        cur.execute("INSERT INTO diary VALUES(:user, :date, :title, :value)",  n)
        con.commit()
    elif action in 'nN':
        # Добавляем новый продукт в БД
        d = get_data({'title': 'название',
                      'kcal': 'калорийность', 
                        'p': 'содержание белков', 
                        'f': 'содержание жиров', 'c': 
                        'содержание углеводов'}, 1)

        cur.execute('INSERT INTO food VALUES(:title, :kcal, :p, :f, :c)', d)
        con.commit()

    elif action in 'pP':
        pass
        current_date = datetime.date.today().strftime('%Y-%m-%d')
    

    elif action in 'qQ':
        con.close()
        exit(0)
    else:
        print('Неизвестная команда')
        sleep(1)


    



