import common
from ui import *
from liblw import *

screen_name = 'users'

def users_main(cur, old_user_id):
    user_id = None
    wc = False

    while user_id is None:
        u_list = get_users_info(cur)
        action = screen(
                headers[screen_name],
                lambda: print_as_table(
                    [('',) + tuple([k for k in user_params.values()])] + u_list
                    ) if u_list else print(messages['nu']),
                menu_str[screen_name], 3
        )
        
        if action.isdigit(): 
            digit = int(action)
            if digit < 1 or digit > len(u_list): helps(messages['not_in_list'], 1)
            else:
                user_id = digit
                wc = set_user(cur, user_id)
        elif action == 'qq': 
            clear()
            exit(-1)
        else:
            do, args = command_parser(action, [k[0] for k in menu_str[screen_name]])

            if do == 'a': return add_user(cur, get_new_user_data()) 
            elif do == 'r': return remove_user(cur, args[0])
            elif do == 'e': helps(messages['not_impl'], 0.5)
            elif do == 'h': helps(help_str[screen_name])
            elif do == 'q':
                if old_user_id is None: helps(messages['no_user'], 0.5)
                else: user_id = old_user_id
            else: helps(messages['ua'], 1)

    return user_id, wc

# Функция проверяет, есть ли в таблице записи и возвращает количество строк
def check_data_in_table(cur, table_name):
    return cur.execute('SELECT COUNT(*) FROM ' + table_name).fetchone()[0]

def get_user_id(cur):
    try: user_id = cur.execute('SELECT user_id FROM current_user'). fetchone()[0]
    except: user_id = None
    return user_id

# Функция получает id
# Возврашает словрь с параметрами пользователя
def get_user_data_by_id(cur, user_id):
    t = cur.execute('SELECT rowid, * FROM users WHERE rowid = ?', (user_id,)).fetchone()
    return dict(map(lambda *args: args, ('rowid', 'name', 'sex', 'age', 'height', 'weight', 'activity'), t) )

def get_users_info(cur):
    return cur.execute('SELECT rowid, * FROM users').fetchall()

def add_user(cur, params):
    cur.execute("INSERT INTO users VALUES(:name, :sex, :age, :height, :weight, :activity)", params).fetchone()
    return None, True

def remove_user(cur, user_id):
    cur.execute("DELETE FROM users WHERE rowid = ?", (user_id,)).fetchone()
    return None, True

def set_user(cur, user_id):
    stmt = 'UPDATE current_user SET user_id = ? where rowid = 1'
    if check_data_in_table(cur, 'current_user') == 0: stmt = 'INSERT INTO current_user VALUES(?)'
    cur.execute(stmt, (user_id,))
    return True

def convert_sex(sex): 
    if sex in 'mMмМ':
        return 'm'
    elif sex in 'fFжЖ':
        return 'f'

def get_new_user_data():
    rd = dict()
    for k in user_params:
        while True:
            clear()
            header(headers['new_user'])
            print_as_table([('', user_params[i], rd.get(i, ''), '') for i in user_params]), 
            line()
            if k == 'activity': helps(help_str['activity'], 0.5)

            it = input(f'{user_params[k][0].upper() + user_params[k][1:]}: ').strip()
            
            if it == 'q': break
            if k == 'name':
                if len(it) > 1: 
                    it = it[0].upper() + it[1:]
                    break
                else: helps(messages['small_str'], 1)
            elif k == 'sex':
                if it in 'mMfFмМжЖ' and len(it) > 0:
                    it = convert_sex(it)
                    break
                else: helps(messages['need_gender'], 1)

            elif k in ('age', 'height', 'weight', 'activity'):
                if (it.isnumeric() or common.isfloat(it)): break
                else: helps(messages['need_number'], 1)
        rd[k] = it

    return rd
