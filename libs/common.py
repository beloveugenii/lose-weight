def isfloat(what):
    if what.startswith('-'):
        what = what[1:]
    parts = what.split('.')
    return len(parts) == 2 and parts[0].isnumeric() and parts[1].isnumeric()

def is_valid(value, type_str, char_list = None):

    v_types = ( 'is_number', 'is_num', 'is_float', 'is_fl',
        'is_negative', 'is_neg', 'in_lst', 'in_ls', 'len_g', )

    if type_str not in v_types:
        raise ValueError(f'"{type_str}" is not implemented yet')

    value = str(value).strip()

    return (
        type_str.startswith('is_num') and value.isnumeric() or
        type_str.startswith('is_neg') and value.startswith('-') or
        type_str.startswith('is_fl') and isfloat(value) or
        type_str.startswith('in_ls') and value in char_list# or
        #  type_str.startswith('len_g') and len(value) >
    )

def create_tables(cur, db_path):
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
