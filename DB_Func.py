import json
import DB_Code as db

try:
    with open('iIko_items.db', 'r') as f:
        pass
except:
    db.create_base()
    print('База данных отсутствовала, поэтому была создана. Приложение закрылось.')
    exit()


def take_items(item=None):
    print('\033[32mФУНК: take_items\033[0m')
    items = db.get_item(item)
    if items == None:
        return('Ошибка')
    return items


def add_item(item=None):
    print('\033[32mФУНК: add_items\033[0m')
    print(item)
    if type(item) is str:
        db.add_item(item)

def clear_item(item=None):
    print('\033[32mФУНК: clear_item\033[0m')
    print(item)
    if type(item) is str:
        db.clear_item(item=item)

def delete_item(item=None):
    print('\033[32mФУНК: delete_item\033[0m')
    print(item)
    if type(item) is str:
        db.delete_item(item)


def update_items(item=None, name=None):
    print('\033[32mФУНК: update_items\033[0m')
    names = db.get_item(item)
    print(f'names = {names}\nПотому что item={item}, \nname={name}')
    if names != False:
        names = names['names']
        if names is not None:
            if name is not None and item is not None:
                print('ЗАПУСК АПДЕЙТ БАЗЫ')
                names_list = names.split('///')
                if name['name'] not in names_list:
                    names += '///' + name['name']
                db.update_item(item, names)
        else:
            if type(name) == list:
                name = ''
                for i in name:
                    name += '///' + i
                db.update_item(item, name)
            else:
                db.update_item(item, name['name'])
    else:
        print('Объекта "' + item + '" нет в базе!')
        return False


def get_item(name = None):
    if name is not None:
        name = name['name']
        item = db.get_item_names(name)
        if item != False:
            return item
        else:
            return False
