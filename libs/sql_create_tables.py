
def create(db_path):
    import sqlite3
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    for stmt in [
            "CREATE TABLE IF NOT EXISTS food(title TEXT, kcal REAL, p REAL, f REAL, c REAL)",
            "CREATE TABLE IF NOT EXISTS diary(user INT, date TEXT, title TEXT, value REAL)",
            "CREATE TABLE IF NOT EXISTS users(name TEXT, sex TEXT, age INT, height REAL, weight REAL, activity REAL)",
            "CREATE TABLE IF NOT EXISTS current_user(user_id INT)",
            "CREATE TABLE IF NOT EXISTS dishes(title TEXT, ingredients TEXT, kcal REAL, p REAL, f REAL, c REAL)",
            'CREATE TABLE IF NOT EXISTS trainings (name TEXT, repeats INT, pause TEXT, relax TEXT, on_end TEXT)',
            'CREATE TABLE IF NOT EXISTS exercises (title TEXT, body_part TEXT)',
            'CREATE TABLE IF NOT EXISTS exercises_lists (exer_id INT, duration TEXT, training_id INT)',

    ]:

        cur.execute(stmt)
        con.commit()
    con.close()
