#!/usr/bin/env python3

import sqlite3

def check_and_return(text, that):
    # Эта функция получает строку и параметр, куда предполагается ее сохранить.
    # Возвращает приведенный в нужную форму параметр или зацикливает ввод до тех пор, пока не будет введено нужное значкние.
    if that == 'имя':
        while True:
            if text.isalpha() and len(text) > 1:
                return text[0].upper() + text[1:]
            else:
                text = input('Здесь требуется строка: ' )
    elif that == 'пол':
        while True:
            if text in 'мМжЖ':
                return text.lower()
            else:
                text = input('Введите \'м\' или \'ж\': ')
    else:
        while True:
            if text.isnumeric():
                return float(text)
            else:
                text = input('Здесь требуется число: ')


        
        

#cur.execute('CREATE TABLE users (name TEXT, age INT, sex TEXT, height INT, weight INT, activity REAL);')
#запуск, проверка есть ли пользователь.
    # проверка есть ли файл конфиг
f = ''
while not f:
    try:
        f = open('.config', 'r')
        ## читаем файл и получаем id, по которому нвходим в бд всю инфу
        for line in f:
            print(line)
        f.close()
    
    except FileNotFoundError:
        print("Похоже, что это первый запуск.\nНеобходимо ввести некоторые данные о себе.")

## !!!!!!? сд4лать здесььчловарь
        p = ('имя', 'возраст', 'пол', 'вес', 'рост', 'активность')

        v = []

        for i in range(len(p)):
            v.append(check_and_return(input('Введите ' + p[i] + ': ' ), p[i]))
        

        #cur.execute('INSERT INTO users VALUES(?, ?, ?, ?, ?)', v)
        #con.commit()

# надо записать rowid польщователя в файл 

        f = open('.config', 'w')
        for d in v:
            f.write(str(d) + '\n')
        f.close()
    



#записи в дневнике с id пользователя
