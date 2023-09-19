
### Name

Simple-sport - minimalistic console sport assistant with calorie diary.

### Synopsis

Usage: ./simple-sport.pl [OPTIONS] [FILE]
Usage: ./diary.py

### Description

This program will help you to do sport everytime and everythere: the program reads the files transferred to it and makes a list of exercises from them. The duration of pauses between exercises and repetitions, as well as the number of repetitions is indicated in the file with workout plan.

### Options of simple-sport

    -s enables a sound alarm when executing
    -t [exercise] make timer on
    -v show version of app
    -h show embedded help

### File format

In the new version, the exercise file contains all the necessary data to build a workout plan: the number of repeats, time intervals and the set of exercises itself.

The grid symbol ( # ) is used to create comments, empty lines will skip.

The execution time must be specified with a time modifier (s or m), the separator for the exercises is either a colon symbol ( : ) or a small arrow ( -> ).

The same principle is used to set parameters, but the separator is the equality symbol ( = ). If the parameter is set by a simple number, like the number of approaches, then the time modifier cannot be set.

    name='Warm-up'
    pause=5s
    relax=0s
    repiats=1
    on\_end=10s

    ex1:30s
    ex2->0.5m
    ex3->40s
    ex5:1m

### About diary.py

Diary.py is a small interactive script that allows you to keep a calorie diary. It uses SQLite to store a diary and product data that requires the installation of this utility.
