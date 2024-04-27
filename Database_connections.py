import sqlite3
import logging
log = False

# Соединение с row
def get_db_connection():
    conn = sqlite3.connect('Database_iIko_items.db')
    conn.row_factory = sqlite3.Row
    return conn


# Соединение без row
def get_db_connection2():
    conn = sqlite3.connect('Database_iIko_items.db')
    return conn


# Получения товара по названию
def get_item(item=None):
    if log: logging.info('БД: get_item')
    conn = get_db_connection()
    if type(item) is str:
        user_row = conn.execute('SELECT * FROM Items WHERE item = ?', (item.lower(),)).fetchone()
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
    logging.info('БД: get_item_names')
    if log: print(name)
    conn = get_db_connection()
    if type(name) is str:
        name = name.lower()
        user_row = conn.execute("SELECT * FROM Items WHERE names LIKE ? OR names LIKE ? OR names LIKE ? OR names LIKE ?", (f'{name}', f'{name}///%', f'%///{name}', f'%///{name}///%')).fetchone()
        if log: print(user_row)
        conn.close()
        if user_row:
            # Преобразуем sqlite3.Row в словарь
            user_dict = dict(user_row)
            if log: print(user_dict)
            if log: logging.info('БД: get_item_names - закончила работу!')
            return user_dict
        else:
            if log: logging.info('БД: get_item_names - закончила работу!')
            return False
    else:
        if log: logging.info('БД: get_item_names - закончила работу!')
        return False


# Добавление товара
def add_item(item=None):
    logging.info('БД: add_item')
    if log: print(f'Товар: {item}, добавляется!')
    items = get_item()
    if item not in items:
        if item != None:
            if log: logging.info('Сработала БД: create_item')
            conn = get_db_connection()
            conn.execute('INSERT INTO Items (item) VALUES (?)', (item.lower(),))
            conn.commit()
            conn.close()
            return True
        else:
            return False
    else:
        return False


# Обновления данных
def update_item(item=None, names=None, items=None):
    logging.info('БД: update_item')
    if type(item) is str and names is not None:
        if log: print(f'item={item}')
        if log: print(f'names={names}')
        if log: print(f'items={items}')
        conn = get_db_connection()
        conn.execute('UPDATE Items SET item = ?, names = ? WHERE item = ?', (item.lower(), names.lower(), item.lower()))
        conn.commit()
        conn.close()
        if log: logging.info('БД: update_item - закончила работу!')
        return True
    else:
        return False


# Удаление товара
def delete_item(item=None):
    logging.info('БД: delete_items')
    if item != None:
        conn = get_db_connection()
        conn.execute('DELETE FROM Items WHERE item = ?', (item.lower(),))
        conn.commit()
        conn.close()
        return True
    else:
        return False


# Удаление названий из товара
def clear_item(item=None, names=None):
    logging.info('БД: delete_items')
    if item != None:
        conn = get_db_connection()
        conn.execute('UPDATE Items SET item = ?, names = ? WHERE item = ?', (str(item).lower(), str(names).lower(), str(item).lower()))
        conn.commit()
        conn.close()
        return True
    else:
        return False


# Создание таблицы
def create_base():
    logging.info('БД: create_base')
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


def lowered_base():
    logging.info('БД: lowered_base')
    if log: print(get_item())
    connection = get_db_connection()
    item_row = connection.execute('SELECT * FROM Items')
    item_get = item_row.fetchall()
    item_return = {}
    for x in item_get:
        item_return[dict(x)['item']] = dict(x)['names']
        item = dict(x)['item']
        names = dict(x)['names']
        if names != None:
            connection.execute('UPDATE Items SET names = ? WHERE item = ?', (names.lower(), item))
        if item != None:
            connection.execute('UPDATE Items SET item = ? WHERE item = ?', (item.lower(), item))
    connection.commit()
    connection.close()
    if log: print(get_item())

lowered_base()

