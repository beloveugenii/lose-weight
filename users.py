import common
from ui import *
from liblw import *
import sqlite3
import sys

DB_NAME = sys.path[0] + '/data.db'
screen_name = 'users'

con = sqlite3.connect(DB_NAME)
cur = con.cursor()
create_tables(cur)

def main(cur):
    screen_name = 'users'
    wc = False
    user_id = None

    while not user_id:
    
        u_list = get_users_info(cur)
        
        action = screen(headers[screen_name],
               lambda: print_as_table(u_list) if u_list else print(messages['nu']),
               menu_str[screen_name], 3
        )
        
        if action.isdigit(): 
            a = int(action)
            if a < 1 or a > len(u_list):
                helps(messages['not_in_list'], 1)
                #  continue
            else:
                user_id = set_user(cur, a)
                wc = True

        
        elif action == 'a': 
            wc = add_user(cur, get_new_user_data()) 
        
        elif action.startswith('r'): 
            wc = remove_user(cur, action[1])

        elif action == 'h': 
            helps(help_str[screen_name])
        elif action == 'q': 
            return -1
        else: 
            helps(messages['ua'])

        if wc:
            con.commit()
            wc = not wc 

    return user_id
 
# Получает указать на БД
# Возвращает данные о пользователях в виде списка коретежей или None
def get_users_info(cur):
    return cur.execute('SELECT rowid, name FROM users').fetchall()

# Получает указатель на БД и словарь с данными, и добавляет пользователя в БД
# Вовращает True
def add_user(cur, params):
    return not cur.execute("INSERT INTO users VALUES(:name, :sex, :age, :height, :weight, :activity)", params).fetchone()

# Получает указатель на БД и id пользователя, и удалеяет пользователя из БД
# Вовращает True
def remove_user(cur, user_id):
    return not cur.execute("DELETE FROM users WHERE rowid = ?", (user_id,)).fetchone()




def set_user(cur, user_id):
    stmt = 'UPDATE current_user SET user_id = ? where rowid = 1'
    if check_data_in_table(cur, 'current_user') == 0:
        stmt = 'INSERT INTO current_user VALUES(?)'
    cur.execute(stmt, (user_id,))
    return user_id




def get_new_user_data():
    new_user_params = {
        'name': 'ваше имя', 'sex': 'ваш пол',
        'age': 'ваш возраст', 'height': 'ваш рост',
        'weight': 'ваш вес', 'activity': 'ваша активность'
    }


    for k in new_user_params:
        promt = new_user_params[k][0].upper() + new_user_params[k][1:]
        it = ''

        while True:
            clear()
            for a, b in new_user_params.items():
                print(a, b)

            if k == 'activity':
                helps(help_str['activity'])

            it = input(f'\n{promt}: ').strip()

            if k == 'name':
                if len(it) > 2:
                    break
                else:
                    helps(messages['small_str'], 1)

            elif k == 'sex':
                if common.is_valid(it, 'in_lst', 'mMfFмМжЖ') and len(it) > 0:
                    break
                else:
                    helps(messages['need_gender'], 1)

            elif k in ('age', 'height', 'weight'):
                if common.is_valid(it, 'is_num') and len(it) > 1:
                    break
                else:
                    helps(messages['need_number'], 1)

            elif k == 'activity':
                if common.is_valid(it, 'is_fl') and not it.startswith('-') and len(it) > 1:
                    break
                else:
                    helps(messages['need_number'], 1)

        new_user_params[k] = it

    return new_user_params







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


rv = main(cur)
exit(-1)
