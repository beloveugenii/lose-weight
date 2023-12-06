SQL_CREATE_STMT = {
    'create_food_stmt': "CREATE TABLE IF NOT EXISTS food(title TEXT, kcal REAL, p REAL, f REAL, c REAL)",
    'create_diary_stmt': "CREATE TABLE IF NOT EXISTS diary(user INT, date TEXT, title TEXT, value REAL)",
    'create_users_stmt': "CREATE TABLE IF NOT EXISTS users(name TEXT, sex TEXT, age INT, height REAL, weight REAL, activity REAL)",
    'create_dishes_stmt': "CREATE TABLE IF NOT EXISTS dishes(title TEXT, ingredients TEXT, kcal REAL, p REAL, f REAL, c REAL)",
    'training_params': "CREATE TABLE IF NOT EXISTS training_params(name TEXT, repeats INT, pause TEXT, relax TEXT, on_end TEXT)",
    'exercises_lists': "CREATE TABLE IF NOT EXISTS exercises_lists(title TEXT, duration TEXT, training_id)",
            }

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
    'user_ch': 'Выбор пользователя',
    'diary': 'Дневник питания',
    'food_db': 'Внесение данных о новом продукте',
    'interactive': 'Выберите тренировку',
    'timer': 'Таймер',
    'statistic': 'Статистика тренировки',
}
MENU_HELPS = {
    'main': "Enter the name of the food to be entered in the diary\n'n' go to the next day\n'p' go to the previous day\n'l' show food in database\n't' go to sport assistant\n'h' show this help\n'q' quit",
    'food': "Enter the name of the food to be entered in database\n'a' analyze the complex dish\n'r' remove from database\n'h' show this help\n'q' go back",
    'users': "Type user ID for choosing\n'n' create new user\n'h' show this help\n'q' quit",
    
    }
