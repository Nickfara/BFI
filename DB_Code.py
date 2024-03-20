import sqlite3


# Соединение с row
def get_db_connection():
    conn = sqlite3.connect('iIko_items.db')
    conn.row_factory = sqlite3.Row
    return conn


# Соединение без row
def get_db_connection2():
    conn = sqlite3.connect('iIko_items.db')
    return conn


# Получения товара по названию
def get_item(item=None):
    print('\033[32mБД: get_item\033[0m')
    conn = get_db_connection()
    if type(item) is str:
        user_row = conn.execute('SELECT * FROM Items WHERE item = ?', (item,)).fetchone()
        conn.close()
        if user_row:
            # Преобразуем sqlite3.Row в словарь
            user_dict = dict(user_row)
            return user_dict
        else:
            return False
    else:
        item_row = conn.execute('SELECT * FROM Items')
        item_get = item_row.fetchall()
        item_return = {}
        for x in item_get:
            item_return[dict(x)['item']] = dict(x)['names']
        conn.close()
        return item_return


# Получения товара по наименованию
def get_item_names(name=None):
    conn = get_db_connection()
    if type(name) is str:
        user_row = conn.execute('SELECT * FROM Items WHERE names LIKE ?', (f'%{name}%',)).fetchone()
        conn.close()
        if user_row:
            # Преобразуем sqlite3.Row в словарь
            user_dict = dict(user_row)
            return user_dict
        else:
            return False
    else:
        return False


# Добавление товара
def add_item(item=None):
    print('\033[32mБД: add_item\033[0m')
    print(f'Товар: {item}, добавляется!')
    items = get_item()
    if item not in items:
        if item != None:
            print('\033[32mСработала БД: create_item\033[0m')
            conn = get_db_connection()
            conn.execute('INSERT INTO Items (item) VALUES (?)', (item,))
            conn.commit()
            conn.close()
            return True
        else:
            return False
    else:
        return False


# Обновления данных
def update_item(item=None, names=None, items=None):
    if type(item) is str and names is not None:
        print('\033[32mБД: update_item\033[0m')
        print(f'item={item}')
        print(f'names={names}')
        print(f'items={items}')
        item_ = items[item]
        conn = get_db_connection()
        conn.execute('UPDATE Items SET item = ?, names = ? WHERE item = ?', (item, names, item))
        conn.commit()
        conn.close()
        print('\033[32mБД: update_item - закончила работу!\033[0m')
        return True
    else:
        return False


# Удаление товара
def delete_item(item=None):
    if item != None:
        print('\033[32mБД: delete_items\033[0m')
        conn = get_db_connection()
        conn.execute('DELETE FROM Items WHERE item = ?', (item,))
        conn.commit()
        conn.close()
        return True
    else:
        return False


# Удаление названий из товара
def clear_item(item=None, names=None):
    if item != None:
        print('\033[32mБД: delete_items\033[0m')
        conn = get_db_connection()
        conn.execute('UPDATE Items SET item = ?, names = ? WHERE item = ?', (item, names, item))
        conn.commit()
        conn.close()
        return True
    else:
        return False


# Создание таблицы
def create_base():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Создаем таблицу Items
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Items (
    item TEXT,
    names TEXT
    )
    ''')

    # Сохраняем изменения и закрываем соединение
    connection.commit()
    connection.close()


#delete_name(item='сливки 33%', names=None)