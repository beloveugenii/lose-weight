from libs import libsd, ui
from sqls import *
from time import sleep

HEADERS = { 'users': 'Выбор пользователя', }

EMPTY_BODY = { 'users': 'No users found in database', }

MENUS_ENTRIES = { 'users': ('new user creating', 'help', 'quit'), }

MENU_HELPS = { 'users': "Type user ID for choosing\n'n' create new user\n'h' show this help\n'q' quit", }

new_user_params = {
    'name': 'ваше имя', 'sex': 'ваш пол',
    'age': 'ваш возраст', 'height': 'ваш рост',
    'weight': 'ваш вес', 'activity': 'ваша активность'
}

new_food_params = {'kcal': 'калорийность', 'p': 'содержание белков', 
                   'f': 'содержание жиров','c': 'содержание углеводов'}

def set_user(sql_cursor, config_file):
    screen_name = 'users'

    while True:
        # Get user information from DB
        users = get_user_names(sql_cursor)
    
        # Prints screen with user information
        ui.screen(HEADERS[screen_name],
               lambda: ui.print_as_table(users, ' ') if users else print(EMPTY_BODY[screen_name]),
               MENUS_ENTRIES[screen_name], 3
        )

        uch = input('>> ').lower().strip()

        if uch.isdigit():
          user_id = int(uch)
          f = open(config_file, 'a')
          f.write('uid='+str(user_id)+'\n')
          f.close()
          return user_id

        elif uch == 'n':
            add_new_user(sql_cursor, get_data(new_user_params, 1))

        elif uch == 'q': exit(0)
    
        elif uch == 'h':
            print(MENU_HELPS[screen_name])
            a = input()

        else:
            print('Unsupported action')
            sleep(1)




def convert_user_data(t):
    return dict(map(lambda *args: args, ('rowid', 'name', 'sex', 'age', 'height', 'weight', 'activity'), t) )


def isfloat(what):
    if what.startswith('-'):
        what = what[1:]
    parts = what.split('.')
    return len(parts) == 2 and parts[0].isnumeric() and parts[1].isnumeric()

def get_data(params, delay):
    data = dict()
    for key in params:
        if key in ('title', 'name', 'sex'):
            while True:
                it = input(params[key] + ': ')
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
                    it = input(params[key] + ': ')

                    if it == '':
                        it = 1 if key == 'activity' else 0

                    data[key] = float(it)
                    break
                except ValueError:
                    print('Здесь требуется число')
                    sleep(delay)

    return data



