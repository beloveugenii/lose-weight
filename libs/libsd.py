from re import search

def parse_line(line):
    '''parses line of user input'''
    '''return tuple with title and value'''
    pat = r'^(.+?)\s*(\d+(?:\.\d+)?)?$'
    matched = search(pat, str(line))
    return (matched[1], matched[2],)

def get_calories_norm(user):
    '''calculate caloriris norm per day'''
    basic = 10 * user['weight'] + 6.25 * user['height'] - 5 * user['age']

    if user['sex'] in 'мМmM':
        return str((basic + 5)  * user['activity'])[:-1]
    elif user['sex'] in 'жЖfF':
        return str((basic - 161) * user['activity'])[:-1]

HEADERS = {
    'diary': 'Дневник питания',
    'food_db': 'Внесение данных о новом продукте',
    'analyzer': 'Анализатор калорийности рецепта',
}

EMPTY_BODY = {
    'diary': 'No entries',
    'food_db': 'No data in database yet',
    'analyzer': 'No entries',
}

MENUS_ENTRIES = {
    'diary': ('list of food', 'users', 'previous entry', 'next entry', 'simple-sport', 'help', 'quit'),
    'food_db': ('analyst', 'remove', 'help', 'quit'),
    'analyzer': ('create a new dish',  'remove an existing dish', 'quit'),
}


