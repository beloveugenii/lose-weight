# This file defines subroutins, which working with SQLite.Cursor objects and returns some data from DB

def get_food_list(sql_cursor):
    return sql_cursor.execute('SELECT title FROM food').fetchall()# + sql_cursor.execute('SELECT title FROM dishes').fetchall()

def get_dishes_list(sql_cursor):
    return sql_cursor.execute('SELECT title, kcal FROM dishes').fetchall()

def get_user_names(sql_cursor):
    return sql_cursor.execute('SELECT rowid, name FROM users').fetchall()

def get_user_data_by_id(sql_cursor, user_id):
    return sql_cursor.execute('SELECT rowid, * FROM users WHERE rowid = ?', (user_id,)).fetchone()

def get_data_for_diary(sql_cursor, formated_date, user_id):
    return sql_cursor.execute(
        '''
        SELECT d.title, value, ROUND(f.kcal * (d.value / 100), 1) AS calories
        FROM diary AS d
        INNER JOIN food AS f
        WHERE d.title = f.title AND date = ? AND user = ?
        ''', (formated_date, user_id)).fetchall()

def get_food_data(sql_cursor):
    return sorted(sql_cursor.execute('SELECT title, CAST(kcal AS INT), CAST(p AS INT), CAST(f AS INT), CAST(c AS INT) FROM food').fetchall())

def add_new_user(sql_cursor, user_data):
    sql_cursor.execute("INSERT INTO users VALUES(:name, :sex, :age, :height, :weight, :activity)", user_data)

def add_new_food(sql_cursor, data):
    sql_cursor.execute('INSERT INTO food VALUES(:title, :kcal, :p, :f, :c)', data)

def add_in_diary(sql_cursor, data):
    sql_cursor.execute("INSERT INTO diary VALUES(:user, :date, :title, :value)", data)

def is_in_db(sql_cursor, title):
    return sql_cursor.execute("SELECT title, kcal FROM food WHERE title = ?", (title,)).fetchone()
