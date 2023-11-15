#!/usr/bin/env python
from libsui import *
from lib import *
from time import sleep
import sys, os
import argparse
import signal

VERSION = '0.1.5'
EXERCISES_DIR = sys.path[0] + '/basics'


parser = argparse.ArgumentParser(description='Minimalistic console sport assistant. It is part of fcracher',)
parser.add_argument('-s', '--sound', action='store_true', help='enables sound in Termux')
parser.add_argument('-t', '--timer', action='store', help='start timer with given exercise name')
parser.add_argument('-v', '--version', action='store_true', help='show program version')
parser.add_argument('-i', '--interactive', action='store_true', help='start an interactive mode')

args = parser.parse_args()
statistic = dict()


for i in os.scandir(EXERCISES_DIR):
    print(i.name)

def s_to_hms(sec):
    h, m = 0, 0
    res = ''
 #   while sec >= 3600:
 #       h += 1
 #       sec -= 3600
    h = sec // 3600
    sec -= 3600 * h
 #   while sec >= 60:
 #       m += 1
 #       sec -= 60
    m = sec // 60
    sec -= 60 * m

    if h > 0:
        res += '{}ч '.format(h)
    if m > 0:
        res += '{}м '.format(m)
    res += '{}с'.format(sec)
    return res

def show_statistic():
    for item in statistic.items():
        print(item[0] + ': ' + s_to_hms(item[1]))
 #   print(statistic)

def sigint_handler(signum, frame):
    signame = signal.Signals(signum).name
    clear()
    header('Статистика')
   # print(f'Catched {signame}')
    show_statistic()
    restore_cursor()
    exit(1)

signal.signal(signal.SIGINT, sigint_handler)
def print_big_nums(num):
    '''This subroutine get number and prints big digits of it'''
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
        print ("Текущее упражнение: " + ex + "\n" * 5)
        save_cursor_pos()
        print("\n" * 12)
        restore_cursor_pos()
        print_big_nums(timer)
        restore_cursor_pos()
        sleep(1)
        statistic[ex] += 1
        timer += 1


# Start timer-mode
if args.timer:
    timer(args.timer)

