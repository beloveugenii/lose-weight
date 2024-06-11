import common
from ui import *
from liblw import *

screen_name = 'users'

## USERS
# Функция проверяет выбран ли какой-то пользователь на данный момент
# Если да - возвращает его id
# Если нет - перходит на экран выбора пользователя
def get_user_id(cur):
    was_changed = False
    user_id = check_data_in_table(cur, 'current_user')
    if user_id:
        user_id = user_id[0]

    while user_id is None:
        user_id, was_changed = set_user(cur)

    return user_id, was_changed

def set_user(cur):
    wc = False

    while True:
        # Get information about users from DB if it exists
        users = cur.execute('SELECT rowid, name FROM users').fetchall()

        # Prints screen with user information
        screen(headers[screen_name],
               lambda: print_as_table(users, ' ') if users else helps(messages['nu'], 0),
               menu_str[screen_name], 3
        )

        action = input('>> ').lower().strip()

        if action.isdigit():
            user_id = int(action)

            # Validating inputed number
            if user_id < 1 or user_id > len(users):
                helps('not_in_list')
                continue
        
            insert_user_id_in_db(cur, user_id)
            wc = True
            
            return user_id, wc

        elif action == 'a': 
            cur.execute("INSERT INTO users VALUES(:name, :sex, :age, :height, :weight, :activity)", get_new_user_data())
            wc = True
        elif action.startswith('r'): 
            cur.execute("DELETE FROM users WHERE rowid = ?", (action[1:],))
            wc = True
        elif action == 'q': 
            break
            #  return insert_user_id_in_db(cur, 1), was_changed
        elif action == 'h':
            helps(help_str[screen_name])
        else: 
            helps(messages['ua'], 1)


def insert_user_id_in_db(cur, user_id):
    stmt = 'UPDATE current_user SET user_id = ? where rowid = 1'
    # узнаем есть ли в таблице записи
    if cur.execute('SELECT COUNT(*) FROM current_user').fetchone()[0] == 0:
        stmt = 'INSERT INTO current_user VALUES(?)'
    cur.execute(stmt, (user_id,))

def get_user_data_by_id(cur, user_id):
    t = cur.execute('SELECT rowid, * FROM users WHERE rowid = ?', (user_id,)).fetchone()
    return dict(map(lambda *args: args, ('rowid', 'name', 'sex', 'age', 'height', 'weight', 'activity'), t) )



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
                helps('activity', 0)

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



