from os import get_terminal_size                       
# Библиотека с функциями для дневника питания

screen_width = get_terminal_size()[0]

def get_diary(arr):
    # Показывает содержимое дневника за текущий день
    l = 0
    diary = []
    t_kcal = 0

    for line in arr:
        if len(line[0]) > l:
            l = len(line[0])

    df = ' ' * ((screen_width - l * 3) // 5)
    format = '%s%-*s%s%-*s%s%-*s%s'

    print(format % (df, l, 'Продукт'.upper(), df, l, 'количество'.upper(), df, l, 'ккал'.upper(), df))
    for line in arr:
        t_kcal += line[2]
        print(format % (df, l,  line[0], df, l, line[1], df, l, line[2], df))
    
    print(format % (df, l, 'Всего'.upper(), df, l, '', df, l, t_kcal, df))
    

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
                it = input(promt(data[key]))
                if len(it) < 1:
                    print('Требуется название')
                    sleep(delay)
                else:
                    data[key] = it
                    break
        else:
            while True:
                try:
                    it = input(promt(data[key]))
                    if it == '':
                        it = 0
                    data[key] = float(it)
                    break
                except ValueError:
                    print('Здесь требуется число')
                    sleep(delay)

    return data




def header(text):
    header_length = len(text)
    header_length = header_length + 1 if header_length % 2 == 1 else header_length
    header_field = ' ' * ((screen_width - header_length) // 2)

    print('-' * screen_width, header_field + text + header_field, '-' * screen_width, sep='\n')

def clear():
    # Очистка экрана
    print('\033[2J\033[H', end='')

def colored(color, text):
    if color == 'red':
        return "\033[31m" + text + "\033[97m"

def menu(items):
    # Функция получает список и выводит его в виде меню, ограниченного рамкой
    if len(items) % 2 == 1:
        items.append('')
    
    longest = 0
    for item in items:
        if len(item) > longest:
            longest = len(item)
   
    #longest += 4
    #if longest % 2 == 1:
    #    longest -= 1

    mf = ' ' * ((screen_width - longest * 2) // 4)

    print('-' * screen_width)
    i = 0
    while i < len(items)- 1:
        f, s = items[i], items[i+1]
        print('%-s%-*s%-s%-*s%-s' % (mf, longest ,f , mf * 2 , longest , s , mf))
        i += 2
    print('-' * screen_width)



def promt(what):
    # Функция полчает значение 'строка' и возвращает его в виде: 'Строка: '
    return what[0].upper() + what[1:] + ': '



