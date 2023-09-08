#!/usr/bin/env python3

import os
import libfc as fc
 



#try:
#    f = open(".config")
#except FileNotFoundError:

ud = fc.get_data('user_data', 0)


def get_calories_norm(ud):
    # Функция получает данные о пользователе и возвращает дневнуютнорму калорий
    
    basic = 10 * ud['weight'] + 6.25 * ud['height'] - 5 * ud['age']

    # Для мужчин
    if ud['sex'] in 'мМmM':
       return (basic + 5)  * ud['activity']
    # Для женщин
    elif ud['sex'] in 'жЖfF':
        return (basic - 161) * ud['activity']

print(get_calories_norm(ud))

