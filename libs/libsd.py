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

def get_data_for_diary(cur, formated_date, user_id):
    return cur.execute(
        '''
        SELECT d.title, value, ROUND(f.kcal * (d.value / 100), 1) AS calories
        FROM diary AS d
        INNER JOIN food AS f
        WHERE d.title = f.title AND date = ? AND user = ?
        ''', (formated_date, user_id)).fetchall()





def get_food_data(cur):
    return sorted(cur.execute('SELECT title, CAST(kcal AS INT), CAST(p AS INT), CAST(f AS INT), CAST(c AS INT) FROM food').fetchall())

def get_food_list(cur):
    return cur.execute('SELECT title FROM food').fetchall()# + cur.execute('SELECT title FROM dishes').fetchall()

def get_dishes_list(cur):
    return cur.execute('SELECT title, kcal FROM dishes').fetchall()

def is_in_db(cur, title):
    return cur.execute("SELECT title, kcal FROM food WHERE title = ?", (title,)).fetchone()


def add_in_diary(cur, data):
    cur.execute("INSERT INTO diary VALUES(:user, :date, :title, :value)", data)

def add_new_food(cur, data):
    cur.execute('INSERT INTO food VALUES(:title, :kcal, :p, :f, :c)', data)
