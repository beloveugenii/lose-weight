from ui import *
from sys import path
from signal import Signals
import re
from common import *

STRINGS = path[0] + '/strings.json'
TABLES = path[0] + '/tables.json'

headers, messages, menu_str, help_str, params, user_params, BNUMS, food_params = get_from_json(STRINGS, 'dicts', 'headers', 'messages', 'menu_str', 'help_str', 'params', 'user_params', 'BNUMS', 'food_params')
tables = get_from_json(TABLES, 'dicts', 'tables')[0]
speeds = get_from_json(STRINGS, 'lists',  'speeds')[0]


# Обработчик нажатия Ctrl-C
def sigint_handler(signum, frame):
    signame = Signals(signum).name
    clear()
    print(f'Catched {signame}')
    exit(1)

# Функция получает ссылку на словарь и ключ какого-то элемента
# Пытается прибавить единицу в этот ключ если он существует или создает его, если такого ключа не было
def incr_or_av(some_dict, key):
    try:
        some_dict[key] += 1
    except KeyError:
        some_dict[key] = 0


SQLS = {
    'training_params':
        'SELECT rowid, * FROM trainings WHERE rowid = ?',
    'training_list':
        'WITH tmp AS (SELECT exer_id, duration FROM exercises_lists WHERE training_id = ?) SELECT e.title, tmp.duration FROM tmp INNER JOIN exercises AS e WHERE tmp.exer_id = e.rowid',

}


    
def sec_to_hms(sec):
    # Функция получает время в секундах и преобразует его в часы и минуты
    h, m = 0, 0
    res = ''
    h = sec // 3600
    sec -= 3600 * h
    m = sec // 60
    sec -= 60 * m

    if h > 0: res += '{}ч '.format(h)
    if m > 0: res += '{}м '.format(m)
    res += '{}с'.format(sec)
    return res

def hms_to_sec(time):
    # Функция получает время в часах и минутах и преобразует его в секунды
    try:
        match = re.search(r'^([\d\.]+)(.*)$', time).groups()
        mult = 1

        # without if expreasion it returns multiplied on 60
        if match[1] == '':
            mult = 1
        elif match[1] in 'мm':
            mult = 60
        elif match[1] in 'hч':
            mult = 3600

        return int(float(match[0]) * mult)

    except AttributeError:
        return None

def prepare_training(data, current_repeat):
    '''takes data dict and current repeat number'''
    '''repeats list of exercises for current repeat in right order'''
    r_list = []
    for k, v in data['training_list']:
        k =  k.split('|')
        v = hms_to_sec(v)

        r_list.append((params['pause'], hms_to_sec(data['pause'])))
        r_list.append((k[randint(0, len(k) - 1)], v))

    if current_repeat == 0:
        r_list[0] = (params['prepare'], hms_to_sec(data['pause']))
    else:
        r_list[0] = (params['relax'], hms_to_sec(data['relax']))

    if current_repeat == int(data['repeats']) - 1:
        r_list.append((params['on_end'], hms_to_sec(data['on_end'])))

    return r_list

def print_big_nums(num):
    '''takes a num and prints big digits of it'''
    l, c  = -1, -1
    if num > 99:
        l = num // 100
        num %= 100
    c = num // 10
    num %= 10
    if c == 0 and l == -1:
        c = -1

    for i in range(8):
        print_as_table([(BNUMS[l][i], BNUMS[c][i],BNUMS[num][i],)])


















# Функция для начального создания таблиц в БД
def create_tables(cur):
    ct = 'CREATE TABLE IF NOT EXISTS'

    for t, p in tables.items():
        cur.execute(' '. join((ct, t , p)))
    
def empty_start(PROG_NAME):
    '''Fileless startup handler'''
    print("No file set.\nUsage: " + PROG_NAME + ".py [OPTIONS] [FILE]")
    exit(-1)


def show_statistic(stat_dict):
    if len(stat_dict) < 1:
        exit(0)
    total_counter = 0

    clear()
    header(headers['statistic'])
    for title, duration in stat_dict.items():
        if title in params.values():
            continue
        total_counter += duration
        print(title + ': ' + sec_to_hms(duration))

    if total_counter > 0:
        print(f'\nОбщее время тренировки: {sec_to_hms(total_counter)}')
    restore_cursor()
    a = input()
    clear()

def get_calories_norm(user):
    '''calculate caloriris norm per day'''
    basic = 10 * user['weight'] + 6.25 * user['height'] - 5 * user['age']

    if user['sex'] in 'мМmM':
        return str((basic + 5)  * user['activity'])[:-1]
    elif user['sex'] in 'жЖfF':
        return str((basic - 161) * user['activity'])[:-1]

def parse_line(line):
    '''parses line of user input'''
    '''return tuple with title and value'''
    pat = r'^(.+?)\s*(\d+(?:\.\d+)?)?$'
    matched = re.search(pat, str(line))
    return (matched[1], matched[2],)

def parse_file(file_name):
    '''takes a training file name and parses it'''
    '''return dict with data from .fct file'''

    data = dict.fromkeys(('name', 'repeats', 'pause', 'relax', 'on_end', ), None)
    data['training_list'] = list()

    try:
        file = open(file_name, 'rt')
        for line in file:
            # chomp line
            line = line.strip()

            if line.startswith('#') or len(line) == 0:
                # skip comments
                continue
            try:
                match = re.search(r'^(.+)([:=]|(?:->))(.+)$', line).groups()
            except AttributeError:
                continue

            if match[1] == '=':
                # line with param splits and set in dict
                data[match[0]] = match[2]

            else:
                # line with exercise splits on tuple of title and duration
                # and appends to list in dict
                data['training_list'].append((match[0], match[2]))

        file.close()
    except:
        pass

    return data


