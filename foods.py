import common
from ui import *
from liblw import *

screen_name = 'food_db'

def foods_main(cur):
    wc = False

    while True:
        res = get_food_data(cur)
        
        action = screen(
                headers[screen_name],
                lambda: print_as_table( [tuple(food_params.values())] + res,  ' ') if res else print(messages['nd']),
                menu_str[screen_name], 2
        )

        if action in [food[0] for food in res]:
            clear()
            line()
            print_as_table([tuple(food_params.values())] + get_one_food_data(cur, action))
            line()
            input()
            continue
        
        if action in [k[0] for k in menu_str[screen_name]]:
        
            if action == 'q': 
                return True, False
            elif action == 'h': 
                helps(help_str[screen_name])
            elif action == 'a':
                helps(messages['not_impl'], 1)
            elif action == 'e':
                helps(messages['not_impl'], 1)
            elif action == 'r': 
                helps(messages['not_impl'], 1)
        else: helps(messages['ua'], 1)

            #  elif action not in 'arqh' and len(action) > 3:

                #  new_food_params = {'kcal': 'калорийность', 'p': 'содержание белков',
                   #  'f': 'содержание жиров','c': 'содержание углеводов'}
                #  d = get_data(new_food_params, 1)
                #  d['title'] = action
                #  add_new_food(cur, d)


    return wc

def get_food_data(cur):
    return sorted(cur.execute('SELECT title, CAST(kcal AS INT), CAST(p AS INT), CAST(f AS INT), CAST(c AS INT) FROM food').fetchall())


def get_one_food_data(cur, title):
    return cur.execute('SELECT title, CAST(kcal AS INT), CAST(p AS INT), CAST(f AS INT), CAST(c AS INT) FROM food where title == ?', (title,)).fetchall()

