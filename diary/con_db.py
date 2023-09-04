#!/usr/bin/env python3

import sqlite3

# Подключаемся к файлу БД и создаем объекты для работы с подключением и запросами
con = sqlite3.connect('fc.db')
cur = con.cursor()

# Создаем, если нет, таблицы
# Данные о продуктах
#cur.execute("CREATE TABLE IF NOT EXISTS food(title TEXT, cal REAL, p REAL, f REAL, c REAL)")

# Дневник питания
#cur.execute("CREATE TABLE IF NOT EXISTS diary(date TEXT, title TEXT, value REAL)")


# В конце работы закрываем БД     
con.close()
