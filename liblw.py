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
    return cur.execute('SELECT * FROM ' + table_name).fetchone()

# Функция для начального создания таблиц в БД
def create_tables(cur):
    ct = 'CREATE TABLE IF NOT EXISTS'

    for t, p in tables.items():
        cur.execute(' '. join((ct, t , p)))
    
    #  for table in ['default_params']:
        #  if check_data_in_table(cur, table) is None:
            #  cur.execute('INSERT INTO default_params VALUES(49504, 0.15, 0.04, 0.13)')


