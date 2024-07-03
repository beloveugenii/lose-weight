import common
from ui import *
from liblw import *
import completer as c
import readline

screen_name = 'food_db'
d_delims = readline.get_completer_delims()

def foods_main(cur):
    wc = False

    while True:
        res = get_food_data(cur)
        buttons = [e[0] for e in menu_str[screen_name]]
        readline.set_completer(c.Completer(dict().fromkeys(
            buttons + 
            [food[0] for food in res]
        )).complete)
        
        action = screen(
                headers[screen_name],
                lambda: print_as_table( [tuple(food_params.values())] + res[:20],  ' ') if res else print(messages['nd']),
                menu_str[screen_name], 2
        )

        if action in [food[0] for food in res]:
            clear()
            header(headers['about_dish'])
            print_as_table([tuple(food_params.values())] + get_one_food_data(cur, action))
            line()
            input()
            continue
        
        if action in buttons:
        
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

