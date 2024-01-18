from libs import ui, helps, common
from sqls import *

HEADERS = { 'users': 'Выбор пользователя', }
EMPTY_BODY = { 'users': 'No users found in database', }
MENUS_ENTRIES = { 'users': ('new user creating','delete user', 'help', 'quit'), }

def set_user(sql_cursor):
    screen_name = 'users'

    while True:
        # Get information about users from DB if it exists
        users = sql_cursor.execute('SELECT rowid, name FROM users').fetchall()

        # Prints screen with user information
        ui.screen(HEADERS[screen_name],
               lambda: ui.print_as_table(users, ' ') if users else print(EMPTY_BODY[screen_name]),
               MENUS_ENTRIES[screen_name], 3
        )

        action = input('>> ').lower().strip()

        if action.isdigit():
            user_id = int(action)

            # Validating inputed number
            if user_id < 1 or user_id > len(users):
                helps.help('not_in_list')
                continue

            return insert_user_id_in_db(sql_cursor, user_id)

        elif action == 'n': sql_cursor.execute("INSERT INTO users VALUES(:name, :sex, :age, :height, :weight, :activity)", get_new_user_data())
        elif action.startswith('d'): sql_cursor.execute("DELETE FROM users WHERE rowid = ?", (action[1:],))
        elif action == 'q': exit(0)
        elif action == 'h': helps.help(screen_name)
        else: helps.help('ua', 1)


def insert_user_id_in_db(sql_cursor, user_id):
    stmt = 'UPDATE current_user SET user_id = ? where rowid = 1'
    # узнаем есть ли в таблице записи
    if sql_cursor.execute('SELECT COUNT(*) FROM current_user').fetchone()[0] == 0:
        stmt = 'INSERT INTO current_user VALUES(?)'
    sql_cursor.execute(stmt, (user_id,))
    return user_id

def get_user_data_by_id(sql_cursor, user_id):
    t = sql_cursor.execute('SELECT rowid, * FROM users WHERE rowid = ?', (user_id,)).fetchone()
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
            ui.clear()
            for a, b in new_user_params.items():
                print(a, b)

            if k == 'activity':
                helps.help('activity', 0)

            it = input(f'\n{promt}: ').strip()

            if k == 'name':
                if len(it) > 2:
                    break
                else:
                    helps.help('small_str', 1)

            elif k == 'sex':
                if common.is_valid(it, 'in_lst', 'mMfFмМжЖ') and len(it) > 0:
                    break
                else:
                    helps.help('need_gender', 1)

            elif k in ('age', 'height', 'weight'):
                if common.is_valid(it, 'is_num') and len(it) > 1:
                    break
                else:
                    helps.help('need_number', 1)

            elif k == 'activity':
                if common.is_valid(it, 'is_fl') and not it.startswith('-') and len(it) > 1:
                    break
                else:
                    helps.help('need_number', 1)

        new_user_params[k] = it

    return new_user_params







def get_data(params, delay):
    data = dict()
    for key in params:
        if key in ('title', 'name', 'sex'):
            while True:
                it = input(params[key][0].upper() + params[key][1:] + ': ').strip()
                if len(it) < 2 and not key == 'sex':
                    helps.help('small_str', delay)
                else:
                    if key == 'sex' and it not in 'мМжЖmMfF':
                        helps.help('need_gender', delay)
                    else:
                        data[key] = it
                        break
        elif key in ('kcal', 'age', 'height', 'weight', 'value', 'activity', 'p', 'c', 'f'):
            while True:
                if key == 'activity': helps.help('activity', 0)

                try:
                    it = input(params[key] + ': ')

                    if it == '':
                        it = 1 if key == 'activity' else 0

                    data[key] = float(it)
                    break
                except ValueError:
                    helps.help('need_number', delay)

    return data



