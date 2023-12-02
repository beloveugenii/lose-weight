from libsui import *
import re
from time import sleep
import sys
from random import randint, choice

# SIMPLE_SPORT BLOCK
nums = { 0: ( "#########", "#########", "###   ###", "###   ###", "###   ###", "###   ###", "#########", "#########", ),
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

strings = {'pause': 'Пауза', 'prepare': 'Приготовьтесь', 'relax': 'Время отдохнуть', 'on_end': 'Конец тренировки'}

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

def get_random_speed():
    '''return random string with speed'''
    return choice(('Медленно', 'Нормально', 'Быстро'))

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
    
def incr_or_av(some_dict, key):
    '''try increment value of key in some_dict'''
    '''create pair with given key if no key in dict'''
    try:
        some_dict[key] += 1
    except KeyError:
        some_dict[key] = 0

def parse_file(file_name):
    '''takes a training file name and parses it'''
    '''return dict with data from .fct file'''

    data = dict.fromkeys(('name', 'repeats', 'pause', 'relax', 'on_end', ), None)
    data['training_list'] = list()

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
    return data

def prepare_training(data, current_repeat):
    '''takes data dict and current repeat number'''
    '''repeats list of exercises for current repeat in right order'''
    r_list = []
    for k, v in data['training_list']:
        k =  k.split('|')
        v = hms_to_sec(v)

        r_list.append((strings['pause'], hms_to_sec(data['pause'])))
        r_list.append((k[randint(0, len(k) - 1)], v))

    if current_repeat == 0:
        r_list[0] = (strings['prepare'], hms_to_sec(data['pause']))
    else:
        r_list[0] = (strings['relax'], hms_to_sec(data['relax']))

    if current_repeat == int(data['repeats']) - 1:
        r_list.append((strings['on_end'], hms_to_sec(data['on_end'])))

    return r_list

def show_statistic(stat_dict):
    clear()
    if len(stat_dict) < 2:
        exit(0)
    total_counter = 0
    header('Статистика тренировки')
    for title, duration in stat_dict.items():
        if title in strings.values():
            continue
        total_counter += duration
        print(title + ': ' + sec_to_hms(duration))
    
    if total_counter > 0:
        print(f'\nОбщее время тренировки: {sec_to_hms(total_counter)}')
    restore_cursor()
    a = input()

# FCRASHER BLOCK
def parse_line(line):
    '''parse single element of ingredients list'''
    '''return tuple with title and value, or empty tuple'''
    pat = r'^(.+?)\s*(\d+(?:\.\d+)?)$'
    try:
        matched = re.search(pat, str(line))
        return (matched[1], matched[2],)
    
    except TypeError:
        return None
        
def get_user_id(file):
    '''try to get user id from file'''
    try:
        f = open(file, 'r')
        for line in f:
            user_id = line.split('=')[1].strip()
        f.close()
    
    except FileNotFoundError:
        user_id = None
    return user_id

def set_user_id(file, user_id):
    '''write userid into file'''
    f = open(file, 'a')
    f.write('uid='+str(user_id)+'\n')
    f.close()

def get_calories_norm(user):
    '''calculate caloriris norm per day'''
    basic = 10 * user['weight'] + 6.25 * user['height'] - 5 * user['age']

    if user['sex'] in 'мМmM':
        return str((basic + 5)  * user['activity'])[:-1]
    elif user['sex'] in 'жЖfF':
        return str((basic - 161) * user['activity'])[:-1]


def isfloat(what):
    if what.startswith('-'):
        what = what[1:]
    parts = what.split('.')
    return len(parts) == 2 and parts[0].isnumeric() and parts[1].isnumeric()

def get_data(params, delay):
    data = dict()
    for key in params:
        if key in ('title', 'name', 'sex'):
            while True:
                it = input(params[key] + ': ')
                if len(it) < 2 and not key == 'sex':
                    print('Слишком короткая строка')
                    sleep(delay)
                else:
                    if key == 'sex' and it not in 'мМжЖmMfF':
                        print('Требуется обозначение пола: [мМ или жЖ]')
                        sleep(delay)
                    else:
                        data[key] = it
                        break
        elif key in ('kcal', 'age', 'height', 'weight', 'value', 'activity', 'p', 'c', 'f'):
            while True:
                if key == 'activity':
                    print("1.2 – минимальная активность, сидячая работа, не требующая значительных физических нагрузок", "1.375 – слабый уровень активности: интенсивные упражнения не менее 20 минут один-три раза в неделю", "1.55 – умеренный уровень активности: интенсивная тренировка не менее 30-60 мин три-четыре раза в неделю", "1.7 – тяжелая или трудоемкая активность: интенсивные упражнения и занятия спортом 5-7 дней в неделю или трудоемкие занятия", "1.9 – экстремальный уровень: включает чрезвычайно активные и/или очень энергозатратные виды деятельности", sep='\n')

                try:
                    it = input(params[key] + ': ')

                    if it == '':
                        it = 1 if key == 'activity' else 0

                    data[key] = float(it)
                    break
                except ValueError:
                    print('Здесь требуется число')
                    sleep(delay)

    return data



