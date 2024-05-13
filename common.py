import ui, re
from random import randint
BNUMS = { 0: ( "#########", "#########", "###   ###", "###   ###", "###   ###", "###   ###", "#########", "#########", ),
        1: ( "    ###  ", "    ###  ", "    ###  ", "    ###  ", "    ###  ", "    ###  ", "    ###  ", "    ###  " ),
        2: ( "#########", "#########", "      ###", "#########", "#########", "###      ", "#########", "#########", ),
        3: ( "#########", "#########", "      ###", "  #######", "  #######", "      ###", "#########", "#########", ),
        4: ( "###   ###", "###   ###", "###   ###", "#########", "#########", "      ###", "      ###", "      ###", ),
        5: ( "#########", "#########", "###      ", "#########", "#########", "      ###", "#########", "#########", ),
        6: ( "#########", "#########", "###      ", "#########", "#########", "###   ###", "#########", "#########", ),
        7: ( "#########", "#########", "      ###", "      ###", "      ###", "      ###", "      ###", "      ###", ),
        8: ( "#########", "#########", "###   ###", "#########", "#########", "###   ###", "#########", "#########", ),
        9: ( "#########", "#########", "###   ###", "#########", "#########", "      ###", "#########", "#########", ),
        -1: ( "         ", "         ", "         ", "         ", "         ", "         ", "         ", "         ", ), }


def parse_line(line):
    '''parses line of user input'''
    '''return tuple with title and value'''
    pat = r'^(.+?)\s*(\d+(?:\.\d+)?)?$'
    matched = re.search(pat, str(line))
    return (matched[1], matched[2],)

SQLS = {
    'training_params':
        'SELECT rowid, * FROM trainings WHERE rowid = ?',
    'training_list':
        'WITH tmp AS (SELECT exer_id, duration FROM exercises_lists WHERE training_id = ?) SELECT e.title, tmp.duration FROM tmp INNER JOIN exercises AS e WHERE tmp.exer_id = e.rowid',

}
def isfloat(what):
    if what.startswith('-'):
        what = what[1:]
    parts = what.split('.')
    return len(parts) == 2 and parts[0].isnumeric() and parts[1].isnumeric()
HEADERS = {
    'diary': 'Дневник питания',
    'food_db': 'Внесение данных о новом продукте',
    'analyzer': 'Анализатор калорийности рецепта',
    'interactive': 'Выберите тренировку',
    'timer': 'Таймер',
    'statistic': 'Статистика тренировки',
}

EMPTY_BODY = {
    'diary': 'No entries',
    'food_db': 'No data in database yet',
    'analyzer': 'No entries',
}

MENUS_ENTRIES = {
    'interactive': ('create', 'remove', 'edit', 'help', 'quit'),
    'diary': ('list of food', 'users', 'previous entry', 'next entry', 'help', 'quit'),
    'food_db': ('analyst', 'remove', 'help', 'quit'),
    'analyzer': ('create a new dish',  'remove an existing dish', 'quit'),
}

STRINGS = {
    'params':
    {'name': 'имя','pause': 'Пауза', 'prepare': 'Приготовьтесь', 'relax': 'Время отдохнуть', 'on_end': 'Конец тренировки'},
    'speeds':
        ('Средне', 'Быстро'),
}

def isfloat(what):
    if what.startswith('-'):
        what = what[1:]
    parts = what.split('.')
    return len(parts) == 2 and parts[0].isnumeric() and parts[1].isnumeric()


def get_calories_norm(user):
    '''calculate caloriris norm per day'''
    basic = 10 * user['weight'] + 6.25 * user['height'] - 5 * user['age']

    if user['sex'] in 'мМmM':
        return str((basic + 5)  * user['activity'])[:-1]
    elif user['sex'] in 'жЖfF':
        return str((basic - 161) * user['activity'])[:-1]

def empty_start(PROG_NAME):
    '''Fileless startup handler'''
    print("No file set.\nUsage: " + PROG_NAME + ".py [OPTIONS] [FILE]")
    exit(-1)


def incr_or_av(some_dict, key):
    '''try increment value of key in some_dict'''
    '''create pair with given key if no key in dict'''
    try:
        some_dict[key] += 1
    except KeyError:
        some_dict[key] = 0

def show_statistic(stat_dict):
    if len(stat_dict) < 1:
        exit(0)
    total_counter = 0

    ui.clear()
    ui.header(HEADERS['statistic'])
    for title, duration in stat_dict.items():
        if title in STRINGS['params'].values():
            continue
        total_counter += duration
        print(title + ': ' + sec_to_hms(duration))

    if total_counter > 0:
        print(f'\nОбщее время тренировки: {sec_to_hms(total_counter)}')
    ui.restore_cursor()
    a = input()
    ui.clear()

def hms_to_sec(time):
    '''takes time and return it in seconds'''
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

def sec_to_hms(sec):
    '''takes time in seconds'''
    '''returns formated string with time in hours, minutes and seconds'''
    h, m = 0, 0
    res = ''
    h = sec // 3600
    sec -= 3600 * h
    m = sec // 60
    sec -= 60 * m

    if h > 0:
        res += '{}ч '.format(h)
    if m > 0:
        res += '{}м '.format(m)
    res += '{}с'.format(sec)
    return res

def hms_to_sec(time):
    '''takes time and return it in seconds'''
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

def sec_to_hms(sec):
    '''takes time in seconds'''
    '''returns formated string with time in hours, minutes and seconds'''
    h, m = 0, 0
    res = ''
    h = sec // 3600
    sec -= 3600 * h
    m = sec // 60
    sec -= 60 * m

    if h > 0:
        res += '{}ч '.format(h)
    if m > 0:
        res += '{}м '.format(m)
    res += '{}с'.format(sec)
    return res

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

def prepare_training(data, current_repeat):
    '''takes data dict and current repeat number'''
    '''repeats list of exercises for current repeat in right order'''
    r_list = []
    for k, v in data['training_list']:
        k =  k.split('|')
        v = hms_to_sec(v)

        r_list.append((STRINGS['params']['pause'], hms_to_sec(data['pause'])))
        r_list.append((k[randint(0, len(k) - 1)], v))

    if current_repeat == 0:
        r_list[0] = (STRINGS['params']['prepare'], hms_to_sec(data['pause']))
    else:
        r_list[0] = (STRINGS['params']['relax'], hms_to_sec(data['relax']))

    if current_repeat == int(data['repeats']) - 1:
        r_list.append((STRINGS['params']['on_end'], hms_to_sec(data['on_end'])))

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
        ui.print_as_table([(BNUMS[l][i], BNUMS[c][i],BNUMS[num][i],)], ' ')







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

def get_food_data(cur):
    return sorted(cur.execute('SELECT title, CAST(kcal AS INT), CAST(p AS INT), CAST(f AS INT), CAST(c AS INT) FROM food').fetchall())

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


