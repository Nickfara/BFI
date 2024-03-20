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


def update_items(item=None, name=None, items=None):
    print('\033[32mФУНК: update_items\033[0m')
    print(f'Потому что item={item}, \nname={name}')
    if type(item) == dict:
        for key in item:
            item_names = items[key]
            item_item = key
    print(f'item_names = {item_names}')
    print(f'item_item = {item_item}')
    if item != None:
        if None not in [item_names, item_item]:
            if name is not None:
                print('ЗАПУСК АПДЕЙТ БАЗЫ')
                names_list = item_names.split('///')
                if name['name'] not in names_list:
                    item_names += '///' + name['name']
                db.update_item(item_item, item_names, items)
        else:
            print('Товар не имеет наименований!')
            if type(name) == list:
                name = ''
                for i in name:
                    name += '///' + i
                db.update_item(item_item, name, items)
            else:
                db.update_item(item_item, name['name'], items)
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
