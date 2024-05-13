# Создание таблиц в БД
# Вносить в словарь название таблицы в качестве ключа и параметры в качетсве значения

TABLES = {
        'food': "(title TEXT, kcal REAL, p REAL, f REAL, c REAL)",
        'diary': "(user INT, date TEXT, title TEXT, value REAL)",
        'users': "(name TEXT, sex TEXT, age INT, height REAL, weight REAL, activity REAL)",
        'current_user': "(user_id INT)",
        'dishes':"(title TEXT, ingredients TEXT, kcal REAL, p REAL, f REAL, c REAL)", 

        'trainings': '(name TEXT, repeats INT, pause TEXT, relax TEXT, on_end TEXT)',
        'exercises': '(title TEXT, body_part TEXT)',
        'exercises_lists': '(exer_id INT, duration TEXT, training_id INT)',
            }

def create_tables(cur):
    # Функция получает объект указателя на БД, создает таблицы и заполняет их при необходимости
    ct = 'CREATE TABLE IF NOT EXISTS'

    for t, p in TABLES.items():
        cur.execute(' '. join((ct, t , p)))

    #  rv = cur.execute('SELECT * FROM default_params').fetchone()
    #  if rv is None:
    #  cur.execute('INSERT INTO default_params VALUES(49504, 0.15, 0.04, 0.13)')


