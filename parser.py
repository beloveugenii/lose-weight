#!/usr/bin/env python
import sys
import re

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
    
       

# передавать список и текущий подход, на основе чего строить список
def prepare_training(data):


    result_list = [('Приготовьтесь', hms_to_sec(data['pause']))]

    # for each repeat
    for repeat in range(int(data['repeats'])):

        # for every exercise in list
        for i in range(len(data['training_list'])):

            k, v = data['training_list'][i]

            result_list.append((k, hms_to_sec(v)))

            if i != len(data['training_list']) - 1:
                result_list.append(('Пауза', hms_to_sec(data['pause'])))

        if repeat < int(data['repeats']):
            result_list.append (('Время отдохнуть', hms_to_sec(data['relax'])))
        else:
            result_list.append (('Конец тренировки', hms_to_sec(data['on_end'])))

    

    return result_list




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

l = prepare_training(parse_file(sys.argv[1]))

for i in l:
    print(l)
