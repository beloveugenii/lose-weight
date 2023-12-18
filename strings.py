
BNUMS = { 0: ( "#########", "#########", "###   ###", "###   ###", "###   ###", "###   ###", "#########", "#########", ),
        1: ( "    ###  ", "    ###  ", "    ###  ", "    ###  ", "    ###  ", "    ###  ", "    ###  ", "    ###  " ),
        2: ( "#########", "#########", "      ###", "#########", "#########", "###      ", "#########", "#########", ),
        3: ( "#########", "#########", "      ###", "  #######", "  #######", "      ###", "#########", "#########", ),
        4: ( "###   ###", "###   ###", "###   ###", "#########", "#########", "      ###", "      ###", "      ###", ),
        5: ( "#########", "#########", "###      ", "#########", "#########", "      ###", "#########", "#########", ),
        6: ( "#########", "#########", "###      ", "#########", "#########", "###   ###", "#########", "#########", ),
        7: ( "#########", "#########", "      ###", "      ###", "      ###", "      ###", "      ###", "      ###", ),
        8: ( "#########", "#########", "###   ###", "#########", "#########", "###   ###", "#########", "#########", ),
        9: ( "#########", "#########", "###   ###", "#########", "#########", "      ###", "#########", "#########", ),
        -1: ( "         ", "         ", "         ", "         ", "         ", "         ", "         ", "         ", ), }
strings = {'pause': 'Пауза', 'prepare': 'Приготовьтесь', 'relax': 'Время отдохнуть', 'on_end': 'Конец тренировки'}

SPEEDS = ('Средне', 'Быстро')

HEADERS = {
    'users': 'Выбор пользователя',
    'diary': 'Дневник питания',
    'food_db': 'Внесение данных о новом продукте',
    'interactive': 'Выберите тренировку',
    'timer': 'Таймер',
    'statistic': 'Статистика тренировки',
    'analyzer': 'Анализатор калорийности рецепта',
}

EMPTY_BODY = {
    'users': 'No users found in database',
    'diary': 'No entries',
    'food_db': 'No data in database yet',
    'analyzer': 'No entries',
}

MENUS_ENTRIES = {
    'users': ('new user creating', 'help', 'quit'),
    'diary': ('list of food', 'users', 'previous entry', 'next entry', 'simple-sport', 'help', 'quit'),
    'food_db': ('analyst', 'remove', 'help', 'quit'),
    'analyzer': ('create a new dish',  'remove an existing dish', 'quit'),
}

new_user_params = {'name': 'ваше имя', 'sex': 'ваш пол',
               'age': 'ваш возраст', 'height': 'ваш рост',
               'weight': 'ваш вес', 'activity': 'ваша активность'}

new_food_params = {'kcal': 'калорийность', 'p': 'содержание белков', 
                   'f': 'содержание жиров','c': 'содержание углеводов'}

MENU_HELPS = {
    'main': "Enter the name of the food to be entered in the diary\n'n' go to the next day\n'p' go to the previous day\n'l' show food in database\n't' go to sport assistant\n'h' show this help\n'q' quit",
    'food': "Enter the name of the food to be entered in database\n'a' analyze the complex dish\n'r' remove from database\n'h' show this help\n'q' go back",
    'users': "Type user ID for choosing\n'n' create new user\n'h' show this help\n'q' quit",
    'analyzer': "Enter the name of the food to be entered in the diary\n'c' create a new dish\n'r' remove an existing dish\n'h' show this help\n'q' quit",
    }
