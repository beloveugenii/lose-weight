from ui import helps, get_const, clear
from sys import path
from signal import Signals

STRINGS = path[0] + '/strings.json'
TABLES = path[0] + '/tables.json'

headers = dict(get_const(STRINGS, 'headers'))
messages = dict(get_const(STRINGS, 'messages'))
menu_str = dict(get_const(STRINGS, 'menu_str'))
help_str = dict(get_const(STRINGS, 'help_str'))
tables = dict(get_const(TABLES, 'tables'))

# Обработчик нажатия Ctrl-C
def sigint_handler(signum, frame):
    signame = Signals(signum).name
    clear()
    print(f'Catched {signame}')
    exit(1)



# Функция проверяет, есть ли в таблице хоть одна запись
def check_data_in_table(cur, table_name):
    res = cur.execute('SELECT * FROM ' + table_name).fetchone()
    if res: return res[0]
    else: return 0

# Функция получает id
# Возврашает словрь с параметрами пользователя
def get_user_data_by_id(cur, user_id):
    t = cur.execute('SELECT rowid, * FROM users WHERE rowid = ?', (user_id,)).fetchone()
    return dict(map(lambda *args: args, ('rowid', 'name', 'sex', 'age', 'height', 'weight', 'activity'), t) )

# Получает указать на БД
# Возвращает данные о пользователях в виде списка коретежей или None
def get_user_info(cur):
    return cur.execute('SELECT rowid, name FROM users').fetchall()

# Получает указатель на БД и словарь с данными, и добавляет пользователя в БД
# Вовращает True
def add_user(cur, params):
    return not cur.execute("INSERT INTO users VALUES(:name, :sex, :age, :height, :weight, :activity)", params).fetchone()

# Получает указатель на БД и id пользователя, и удалеяет пользователя из БД
# Вовращает True
def remove_user(cur, user_id):
    return not cur.execute("DELETE FROM users WHERE rowid = ?", (user_id,)).fetchone()






# Функция для начального создания таблиц в БД
def create_tables(cur):
    ct = 'CREATE TABLE IF NOT EXISTS'

    for t, p in tables.items():
        cur.execute(' '. join((ct, t , p)))
    
    #  for table in ['default_params']:
        #  if check_data_in_table(cur, table) is None:
            #  cur.execute('INSERT INTO default_params VALUES(49504, 0.15, 0.04, 0.13)')




