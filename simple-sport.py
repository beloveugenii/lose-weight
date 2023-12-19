#!/usr/bin/env python3
from lib import *
from random import choice
from time import sleep
from os import scandir
import argparse
import signal

PROG_NAME = 'simple-sport'
VERSION = '0.1.6a'
EXERCISES_DIR = sys.path[0] + '/basics'

parser = argparse.ArgumentParser(description='Minimalistic console sport assistant',)

parser.add_argument('-f', action='append', nargs='+', help='start training from files')
parser.add_argument('-t', action='store', help='start timer with given exercise name')
parser.add_argument('-v','--version', action='version', version=f'{PROG_NAME} {VERSION}')
#  parser.add_argument('-s', '--sound', action='store_true', help='enables sound in Termux')
parser.add_argument('-i', action='store_true', help='start an interactive mode')

# Dict for statistic
STATISTIC = dict()

#  ВКЛЮЧЕНИЕ ЗВУКА В ТЕРМУКСЕ
#  ВЫКЛЮЧЕНИЕ ЗВУКА ПРИ ПРЕРЫВАНИИ  ИЛИ ЗАВЕРШЕНИИ РАБОТЫ
#  ПОКАЗЫВАТЬ ПРОГРАММУ ТРЕНИРОВКИ

args = parser.parse_args()

def sigint_handler(signum, frame):
    restore_cursor()
    show_statistic(STATISTIC)
    exit(-1)

signal.signal(signal.SIGINT, sigint_handler)


def interactive():
    '''Interactive mode'''
    r_files = list()
    files = [EXERCISES_DIR + '/' + file.name for file in scandir(EXERCISES_DIR)]
    clear()
    header(HEADERS['interactive'])
    for i in range(len(files)):
        print(i + 1, parse_file(files[i])['name'])
    line()
    a = input('>> ')
    for i in a.split():
        try:
            i = int(i)
        except ValueError:
            continue
        
        r_files.append(files[i - 1])
    
    return r_files

def timer(title):
    timer = 0
    hide_cursor()
    
    clear()
    header(HEADERS['timer'])
    print(f'Текущее упражнение: {title}' + "\n" * 4)
    save_cursor_pos()

    while True:
        print_big_nums(timer)
        incr_or_av(STATISTIC, title)
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
        current_list = prepare_training(data, repeat)
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
            
            if title not in strings.values():
                print(f'Скорость выполнения: {choice(("Средне", "Быстро"))}' + '\n' * 3)
            else:
                print('\n' * 3)

            save_cursor_pos()
            print('\n' * 12)

            if i != current_list_len - 1:
                print(f'Следующее упражнение: {next_title} {next_duration}',end='')
            else:
                if repeat != int(data['repeats']) - 1:
                    print(strings['relax'], end='')
                else:
                    print(end='')

            for t in range(duration, -1, -1):
                restore_cursor_pos()
                print_big_nums(t)
                incr_or_av(STATISTIC, title)
                sleep(1)

# Start timer-mode
if args.t:
    timer(args.t)

# Start interactive mode
if args.i:
    choosed_files = interactive()
    if len(choosed_files) > 0:
        for file in choosed_files:
            do_training(file)
    else:
        empty_start(PROG_NAME)

# Command-line mode
if args.f:
    for file in args.f[0]:
        do_training(file)

# after whole training
show_statistic(STATISTIC)

