
### Name

Simple-sport - very minimalistic sport assistant   

### Synopsis  

Usage: simple-sport [OPTIONS] [FILE]  

### Description 

This program will help you to do sport everytime and everythere: the program reads the files transferred to it and makes a list of exercises from them. The duration of pauses between exercises and repetitions, as well as the number of repetitions can be passed to the program as options (see below).  

If no exercise files are transferred to the program, then warm-up and hitch files will be automatically started.  

### Options  

- 'help' show this help  
- 'version' show version of app  
- 'sound' enables sound in Termux  
- 'repeats NUM' set repeats NUM  
- 'pause VALUE' set pause between exerises at VALUE  
- 'relax VALUE' set relax duration at VALUE  

You can set VALUE like 15s for 15 secons, or 15m for 15 minutes  

### File format

The exercise file must be formatted in a certain way. It should contain lines like "exercise"->"duration".  
The colon symbol ":" can also act as a separator. The margins don't matter.  
The duration of each exercise can be specified as a number or a number with a suffix. For example: "15m" and "40s".  
