#!/usr/bin/env python
import sys
import re

def hms_to_sec(time):
    match = re.search(r'^([\d\.]+)(.*)$', time).groups()
    
    if match[1] in 'hч':
        print(time, float(match[0]) * 3600)
    elif match[1] in 'мm':
        print(time, float(match[0]) * 60)
    else:
        print(time, float(match[0]))
        


def prepare_training(data):
    pass

def parse_file(file_name):
    '''takes a training file name and parses it'''
    file = open(file_name, 'rt')

    data = dict.fromkeys(('name', 'repeats', 'pause', 'relax', 'on_end', ), None)
    
    data['training_list'] = list()

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
    # return data dict 
    return data


hms_to_sec('10')
hms_to_sec('2.5')
hms_to_sec('10')
hms_to_sec('10s')
hms_to_sec('10с')
hms_to_sec('2м')
hms_to_sec('2.5m')
hms_to_sec('1h')
hms_to_sec('1ч')
