import common
from ui import *
from liblw import *

screen_name = 'users'


def set_user(cur):
    screen_name = 'users'
    #  wc = False
    user_id = 0
    while user_id == 0:
        users = cur.execute('SELECT rowid, name FROM users').fetchall()
        screen(headers[screen_name],
               lambda: print_as_table(users, ' ') if users else helps(messages['nu'], 0),
               menu_str[screen_name], 3
        )
        action = input('>> ').lower().strip()


        if action.isdigit():
            user_id = int(action)

            # Validating inputed number
            if user_id < 1 or user_id > len(users):
                helps(messages['not_in_list'], 0)
                continue
            else:
                insert_user_id_in_db(cur, user_id)
                return user_id, True

        elif action == 'a': 
            cur.execute("INSERT INTO users VALUES(:name, :sex, :age, :height, :weight, :activity)", get_new_user_data())
            return 0, True
        elif action.startswith('r'): 
            cur.execute("DELETE FROM users WHERE rowid = ?", (action[1:],))
            return 0, True
        elif action == 'q': 
            return 0, False
        elif action == 'h':
            helps(help_str[screen_name])
        else: 
            helps(messages['ua'], 1)


def insert_user_id_in_db(cur, user_id):
    stmt = 'UPDATE current_user SET user_id = ? where rowid = 1'
    if check_data_in_table(cur, 'current_user') == 0:
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



