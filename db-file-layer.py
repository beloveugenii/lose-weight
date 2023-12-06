import sqlite3
import sys

DB_NAME = sys.path[0] + '/fc.db'
con = sqlite3.connect(DB_NAME)
cur = con.cursor()

def get_training_data_from_db(training_id):
    training_params = dict( 
                map(lambda *args: args, 
                    ('name', 'repeats', 'pause', 'relax', 'on_end'), 
                    (cur.execute("SELECT * from training_params WHERE rowid = ?", (training_id,)).fetchone())
                )
            )
    return training_params

def get_exercises_list_from_db(training_id):
    exercises_list = cur.execute("SELECT title, duration from exercises_lists where training_id = ?", (training_id,)).fetchall()
    return exercises_list


for key, value in get_training_data_from_db(1).items():
    print(key + '=', value)

for title, duration in get_exercises_list_from_db(1):
    print(title + ':' + duration)
# получаем данные из бд по номеру тренировки
# получаем список упражнений по номеру тренировки
# создаем текстовый файл куда записыввем все данные так, ятобы получился файл tss
