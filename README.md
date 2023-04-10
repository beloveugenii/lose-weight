
## About project

At this moment the development of this program is stopped

### Name

Simple-sport - minimalistic console sport assistant   

### Synopsis  

Usage: simple-sport [OPTIONS] [FILE]  

### Description 

This program will help you to do sport everytime and everythere: the program reads the files transferred to it and makes a list of exercises from them. The duration of pauses between exercises and repetitions, as well as the number of repetitions can be passed to the program as options (see below).  

If no exercise files are transferred to the program, then warm-up and hitch files will be automatically started.  

### Options  

TODO

### File format

In the new version, the exercise file contains all the necessary information to build a workout plan: the number of repetitions, time intervals and the set of exercises itself. 

The execution time must be specified with a time modifier (s or m), the separator for the exercise is either a colon symbol or a small arrow ( -> ).

The same principle is used to set parameters, but the separator is the equality symbol ( = ). If the parameter is set by a simple number, like the number of approaches, then the time modifier cannot be set. Parameters used: name, pause, relax, repiats, on\_end.

The grid symbol ( # ) is used to create comments.
