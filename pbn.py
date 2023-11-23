#!/usr/bin/env python3
from libsui import *
from lib import *
from time import sleep
import sys, os
import argparse
import signal

VERSION = '0.1.5'
EXERCISES_DIR = sys.path[0] + '/basics'


#  parser = argparse.ArgumentParser(description='Minimalistic console sport assistant. It is part of fcracher',)
#  parser.add_argument('-s', '--sound', action='store_true', help='enables sound in Termux')
#  parser.add_argument('-t', '--timer', action='store', help='start timer with given exercise name')
#  parser.add_argument('-v', '--version', action='store_true', help='show program version')
#  parser.add_argument('-i', '--interactive', action='store_true', help='start an interactive mode')

#  args = parser.parse_args()
statistic = dict()


# Start timer-mode
#  if args.timer:
    #  timer(args.timer)

def show_statistic():
    clear()
    header('Статистика')
    for item in statistic.items():
        print(item[0] + ': ' + sec_to_hms(item[1]))
    restore_cursor()
    a = input()
 #   print(statistic)

def sigint_handler(signum, frame):
    #  signame = signal.Signals(signum).name
    restore_cursor()
    show_statistic()
    exit(0)

signal.signal(signal.SIGINT, sigint_handler)

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
        print_as_table([(nums[l][i],nums[c][i], nums[num][i],)], ' ')

def empty_start():
    '''Fileless startup handler'''
    print("No file set.\nUsage: " + NAME + " [OPTIONS] [FILE]")
    sys.exit(-1)

def timer(ex):
    hide_cursor()
    timer = 0
    statistic[ex] = 0
    while True:
        clear()
        header('Таймер')
        print ("Текущее упражнение: " + ex + "\n" * 4)
        save_cursor_pos()
        print("\n" * 12)
        print_big_nums(timer)
        restore_cursor_pos()
        sleep(1)
        statistic[ex] += 1
        timer += 1

# ДЛЯ КАЖДОГО ВЫБРАННОГО ФАЙЛА ТРЕНИРОВКИ

hide_cursor()

for file in sys.argv[1:]:
    # Parse every file
    data = parse_file(file)




    for repeat in range(int(data['repeats'])):
        # For every repeat generate exercises list
        current_list = prepare_training(data, repeat)
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

            clear()
            header(f'{data["name"]} {repeat + 1} / {data["repeats"]}')

            print(f'Текущее упражнение: {title} {duration}' + "\n" * 4)
            save_cursor_pos()
            print('\n' * 12)

            if i != current_list_len - 1:
                print(f'Следующее упражнение: {next_title} {next_duration}')
            else:
                if repeat != int(data['repeats']) - 1:
                    print('Конец подхода')
                else:
                    print()

            for t in range(current_list[i][1], -1, -1):
                restore_cursor_pos()
                print_big_nums(t)
                sleep(1)
        
            sleep(0.25)

show_statistic()
