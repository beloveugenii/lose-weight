#!/usr/bin/env python3

import os
import libfc as fc
from time import sleep

def screen(header_text, menu_array, act):
    #while True:
   # fc.clear()
    fc.header(header_text)
    fc.menu(menu_array)
        #act = input('>> ')
        
    if act in [w[0] for w in menu_array]:
        return True
    else:
        return False
#
 #           if act == 'q':
  #              return old_act
   #         else:
    #            return act
    #    else:
    #        print('Неизвестная команда')
    #        sleep(1)
#act = ''
while True:
    if screen('main', ['add', 'edit', 'quit'], 'q'):
        act = input('>> ')
        print(act)
    #if act == 'a':
    #    while True:
    #        screen('add screen', ['sub add','quit'], act)
    #        act = input('>> ')
    #        if act == 's':
    #            act = screen('sub add screen', ['quit'], act)
    #        elif act == 'q':
    #            break
    elif act == 'q':
        break


    #if act == 'a':
    #    if act == 's':
#
#    elif act == 'q':
#        break
        



    
 



#try:
#    f = open(".config")
#except FileNotFoundError:

#ud = fc.get_data('user_data', 0)

#    для мужчин: (10 * ud['weight'] + 6.25 * ud['height'] – 5 * ud['age'] + 5) * ud['activity'];

# для женщин: (10 * ud['weight'] + 6.25 * ud['height'] – 5 * ud['age'] - 161) * ud['activity'];


