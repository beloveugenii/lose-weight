
### Name

Simple-diet - is a small console utility that contains a food diary for calorie tracking and a sports assistant simple-sport.

### Synopsis

Usage: ./simple-diet.py

Usage: ./simple-sport.py -f [files]

### Description

A food diary allows you to track the amount you eat during the day. It calculates your daily calorie intake and the caloric value of all foods eaten. Food diary uses SQLite to store its data.

The sports assistant allows you to create training programs and carry them out according to a timer. For creating new training file you can use every text editor you like. See *File format* section below.

### Options of simple-sport

    -f to work with training files
    -s enables a sound alarm when executing
    -t [exercise] make timer on
    -v show version of app
    -h show embedded help
    -i interactive file choosing

### File format

In the new version, the exercise file contains all the necessary data to build a workout plan: the number of repeats, time intervals and the set of exercises itself. The files have the extension '.tss'.

The grid symbol ( # ) is used to create comments, empty lines will skip.

The execution time must be specified with a time modifier (s or m), the separator for the exercises is either a colon symbol ( : ) or a small arrow ( -> ).

The same principle is used to set parameters, but the separator is the equality symbol ( = ). If the parameter is set by a simple number, like the number of approaches, then the time modifier cannot be set.

The vertical line symbol '|' makes it possible to randomly select an exercise.

    name='Warm-up'
    pause=5s
    relax=0s
    repiats=1
    on\_end=10s

    ex1|ex2|ex3:30s
    ex2|ex5->0.5m
    ex3->40s
    ex5:1m

