VERSION = '0.0.0.2'

import ui, re
from random import randint
from liblw import *

# Функция получает значение и пробует конвертировать его в число с точкой
def str_to_float(s=0):
    try: s = float(s)
    except: s = 0.0
    return s

# Функция проверяет, является ли переданное числом с точкой
# и возвращает логическое значение
def isfloat(what):
    if what.startswith('-'):
        what = what[1:]
    parts = what.split('.')
    return len(parts) == 2 and parts[0].isnumeric() and parts[1].isnumeric()

# Функция для проверки, является ли значение требуемым типом
def is_valid(value, type_str, char_list = None):

    v_types = ( 'is_number', 'is_num', 'is_float', 'is_fl',
        'is_negative', 'is_neg', 'in_lst', 'in_ls', 'len_g', )

    if type_str not in v_types:
        raise ValueError(f'"{type_str}" is not implemented yet')

    value = str(value).strip()

    return (
        type_str.startswith('is_num') and value.isnumeric() or
        type_str.startswith('is_neg') and value.startswith('-') or
        type_str.startswith('is_fl') and isfloat(value) or
        type_str.startswith('in_ls') and value in char_list# or
        #  type_str.startswith('len_g') and len(value) >
    )


def get_data_for_diary(cur, formated_date, user_id):
    return cur.execute(
        '''
        SELECT d.title, value, ROUND(f.kcal * (d.value / 100), 1) AS calories
        FROM diary AS d
        INNER JOIN food AS f
        WHERE d.title = f.title AND date = ? AND user = ?
        ''', (formated_date, user_id)).fetchall()



def get_food_list(cur):
    return cur.execute('SELECT title FROM food').fetchall()# + cur.execute('SELECT title FROM dishes').fetchall()

def get_dishes_list(cur):
    return cur.execute('SELECT title, kcal FROM dishes').fetchall()

def is_in_db(cur, title):
    return cur.execute("SELECT title, kcal FROM food WHERE title = ?", (title,)).fetchone()

def add_in_diary(cur, data):
    cur.execute("INSERT INTO diary VALUES(:user, :date, :title, :value)", data)

def add_new_food(cur, data):
    cur.execute('INSERT INTO food VALUES(:title, :kcal, :p, :f, :c)', data)

def get_data(params, delay):
    data = dict()
    for key in params:
        if key in ('title', 'name', 'sex'):
            while True:
                it = input(params[key][0].upper() + params[key][1:] + ': ').strip()
                if len(it) < 2 and not key == 'sex':
                    helps('small_str', delay)
                else:
                    if key == 'sex' and it not in 'мМжЖmMfF':
                        helps('need_gender', delay)
                    else:
                        data[key] = it
                        break
        elif key in ('kcal', 'age', 'height', 'weight', 'value', 'activity', 'p', 'c', 'f'):
            while True:
                if key == 'activity': helps(help_str['activity'], 0)

                try:
                    it = input(params[key] + ': ')

                    if it == '':
                        it = 1 if key == 'activity' else 0

                    data[key] = float(it)
                    break
                except ValueError:
                    helps('need_number', delay)

    return data


