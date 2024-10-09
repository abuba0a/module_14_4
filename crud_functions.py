import sqlite3

connection = sqlite3.connect('Products.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Products(
Id INTEGER PRIMARY KEY,
title TEXT NOT NULL,
description TEXT,
price INTEGER NOT NULL
)
''')

# >|Заполнение таблицы|<
# for i in range(1, 5):
#     cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
#                    (f'Продукт{i}', f'Описание{i}', f'{i * 100}'))
#     connection.commit()


def get_all_product():
    connection = sqlite3.connect('Products.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    connection.commit()
    return products


connection.commit()
connection.close()
