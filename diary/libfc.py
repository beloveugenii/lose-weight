from os import get_terminal_size                       
from time import sleep
# Библиотека с функциями для дневника питания

screen_width = get_terminal_size()[0]

def clear():
    # Очистка экрана
    print('\033[2J\033[H', end='')

def promt(what):
    what = str(what)
    # Функция полчает значение 'строка' и возвращает его в виде: 'Строка: '
    return what[0].upper() + what[1:] + ': '

def get_fields(screen_width, fields, elem_array):
    # функция получает ширину экрана,
    # количество полей с текстом и
    # список элементов в виде массива
    # возвращает ширину поля под текст и
    # ширину просвета между колонками
    l = max( [len(elem) for elem in elem_array] )
    f = ' ' * ((screen_width - l * fields) // ( fields + 1))
    return l, f

def header(text):
    # Функция печатает заголовок экрана   
    ht, hf = get_fields(screen_width, 1, [text])

    print('-' * screen_width)
    print('%s%-*s%s' % (hf, ht, text, hf))
    print('-' * screen_width)

def menu(items):
    # Функция получает список и выводит его в виде меню, ограниченного рамкой
    if len(items) % 2 == 1:
        items.append(' ')
    
    tf, ef = get_fields(screen_width, 2,items)

    print('-' * screen_width)
    for i in range(0, len(items) - 1, 2):
        f, s = items[i], items[i+1]
        print('%-s%-*s%-s%-*s%-s' % 
              (ef, tf, f, ef, 
               tf, s, ef))
    print('-' * screen_width)

def print_diary(arr):
    # Показывает содержимое дневника за текущий день
    format = '%s%-*s%s%*s%s%*s%s'
    diary = []
    t_kcal = 0

    l, df = get_fields(
            screen_width,
            3,
            ['продукт', 'количество', 'ккал'] + 
            [i[0] for i in arr])

#    print(format % 
#          (df, l, 'Продукт'.upper(), 
#           df, l, 'количество'.upper(), 
#           df, l, 'ккал'.upper(), df))
    
    for line in arr:
        t_kcal += line[2]
        print(format % 
              (df, l,  line[0], 
               df, l, line[1], 
               df, l, line[2], df))
    print('-' * screen_width) 
    print(format % 
          (df, l, 'Всего'.upper(), 
           df, l, '', 
           df, l, t_kcal, df))
    

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
                it = input(promt(data[key]))
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
                    it = input(promt(data[key]))
                    if for_place != 'user_data' and it == '':
                        it = 0
                    data[key] = float(it)
                    break
                except ValueError:
                    print('Здесь требуется число')
                    sleep(delay)

    return data








