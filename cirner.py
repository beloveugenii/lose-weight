#!/usr/bin/env python3
#  from lib import *
import common 
from ui import *
import argparse, signal, sys, os, sqlite3
from random import choice
from time import sleep
from liblw import *

#from init_db import *

PROG_NAME = 'simple-sport'
VERSION = '0.1.7.1'
EXERCISES_DIR = sys.path[0] + '/basics'
DB_NAME = sys.path[0] + '/data.db'
DELAY = 0

con = sqlite3.connect(DB_NAME)
cur = con.cursor()
#create_tables(cur)


parser = argparse.ArgumentParser(description='Minimalistic console sport assistant',)

parser.add_argument('-f', action='append', nargs='+', help='start training from files')
parser.add_argument('-t', action='store', help='start timer with given exercise name')
parser.add_argument('-v','--version', action='version', version=f'{PROG_NAME} {VERSION}')
#  parser.add_argument('-s', '--sound', action='store_true', help='enables sound in Termux')
parser.add_argument('-i', action='store_true', help='start an interactive mode')


#  ВКЛЮЧЕНИЕ ЗВУКА В ТЕРМУКСЕ
#  ВЫКЛЮЧЕНИЕ ЗВУКА ПРИ ПРЕРЫВАНИИ  ИЛИ ЗАВЕРШЕНИИ РАБОТЫ
#  ПОКАЗЫВАТЬ ПРОГРАММУ ТРЕНИРОВКИ

def sigint_handler(signum, frame):
    restore_cursor()
    show_statistic(STATISTIC)
    exit(-1)


#def get_training_from_db(training_id):
#    training_params = cur.execute(common.SQLS['training_params'], (training_id,)).fetchone()
#    exercises_list = list()

#    if training_params is None:
#        return training_params
#    else:
#        training = dict(map(lambda *args: args, params, training_params[1:]))

#    training['list'] = cur.execute(common.SQLS['training_list'], (training_id,)).fetchall()

#    if training['list'] is None:
#        return None
#    else:
#      return training



def interactive():
    screen_name = 'interactive'
    '''Interactive mode'''
    r_files = list()
    r_ids = list()

    files = [EXERCISES_DIR + '/' + file.name for file in os.scandir(EXERCISES_DIR)]

#    from_db = cur.execute("SELECT name FROM trainings").fetchall()

    while len(r_files) < 1:
        clear()
        header(headers[screen_name])

        for i in range(len(files)):
            print(i + 1, parse_file(files[i])['name'])
  #      print()
 #       for i in range(len(from_db)):
#            print(i + 1, get_training_from_db(i + 1)['name'])
            #  print(i + 1, str(*files[i]).title())

        menu(menu_str[screen_name], 4)

        a = input('>> ')

        if a == 'q': exit(0)
        elif a in ('cer'): helps(messages['not_impl'], 1)
        elif a == 'h': helps(help_str[screen_name])
        else:
            for i in [int(l) for l in a.split() if l.isnumeric()]:
                if i > 0 and i <= len(files):
                    r_files.append(files[i - 1])
                else:
                    helps(messages['no_file'], 1)

    return r_files

def timer(title):
    timer = 0
    hide_cursor()

    clear()
    header(headers['timer'])
    print(f'Текущее упражнение: {title}' + "\n" * 4)
    save_cursor_pos()

    while True:
        common.print_big_nums(timer)
        common.incr_or_av(STATISTIC, title)
        sleep(1)
        timer += 1
        restore_cursor_pos()

    show_statistic(STATISTIC)
    exit(0)

def do_training(file):
    hide_cursor()

    # Parse every file
    data = parse_file(file)

    for repeat in range(int(data['repeats'])):
        # For every repeat generate exercises list
        current_list = common.prepare_training(data, repeat)
        # And take its length
        current_list_len = len(current_list)

        for i in range(current_list_len):
            # For every exercise takes its title and duration
            title, duration = current_list[i]

            # And title and duration for next exercise
            next_title, next_duration = None, None
            try:
                next_title, next_duration = current_list[i + 1]
            except IndexError:
                pass

            # main screen with exercise and timer
            clear()
            header(f'{data["name"]} {repeat + 1} / {data["repeats"]}')

            print(f'Текущее упражнение: {title} {duration}')

            if title not in params.values():
                print(f'Скорость выполнения: {choice(speeds)}' + '\n' * 3)
            else:
                print('\n' * 3)

            save_cursor_pos()
            print('\n' * 12)

            if i != current_list_len - 1:
                print(f'Следующее упражнение: {next_title} {next_duration}',end='')
            else:
                if repeat != int(data['repeats']) - 1:
                    print(params['relax'], end='')
                else:
                    print(end='')

            for t in range(duration, -1, -1):
                restore_cursor_pos()
                common.print_big_nums(t)
                common.incr_or_av(STATISTIC, title)
                sleep(DELAY)


signal.signal(signal.SIGINT, sigint_handler)
args = parser.parse_args()

# Dict for statistic
STATISTIC = dict()
FILES = list()

# Start timer-mode
if args.t:
    timer(args.t)

# Start interactive mode
if args.i:
    FILES = interactive()
elif args.f:
     FILES = args.f[0]

if len(FILES) > 0:
    for f in FILES:
        do_training(f)
    show_statistic(STATISTIC)
else:
    common.empty_start(PROG_NAME)


