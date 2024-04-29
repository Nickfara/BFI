import json
import re
import logging

log = True

def check(doc): # Сканер json чека
    logging.info('СКАН: check')
    check = None
    with open(doc, 'r', encoding='utf-8') as json_file:
        if doc.split('.')[1] == 'json':
            data = json.load(json_file)
            items = data['items']
            if log: print(items)
            filter_items = []
            id = 1
            for i in items: # Фильтрация обьектов
                temp = 0
                e = 0
                while e < len(filter_items):
                    if i['name'] == filter_items[e]['name']:
                        filter_items[e]['count'] += i['quantity']
                        filter_items[e]['sum'] += i['sum']/100
                        filter_items[e]['cost'] = filter_items[e]['sum'] / filter_items[e]['count']
                        temp = 1
                    e += 1

                if temp == 0:
                    filter_items.append({'id': id, 'name': i['name'], 'cost': i['price']/100,
                                     'count': i['quantity'], 'sum': i['sum']/100, 'type': 'шт'})
                    id += 1

            check = {'date': data['dateTime'], 'check': data['requestNumber'], 'items': filter_items, }
            return check
        else:
            return False


def hat(worksheet, i):
    i2 = 0
    find1 = False
    find2 = False
    number = None
    date = None
    while i2 < 15:
        try:
            print(str(worksheet.cell_value(i, i2)).lower())
            if 'документ' in str(worksheet.cell_value(i, i2)).lower():
                find1 = True
                number = str(worksheet.cell_value(i+1, i2))
            if 'дата' in str(worksheet.cell_value(i, i2)).lower():
                find2 = True
                date = str(worksheet.cell_value(i+1, i2)).lower()
        except:
            pass

        i2 += 1
    if find1 and find2:
        date = re.sub('[^0-9.]', '', date)
        number = re.sub('[^0-9-.MKERSUmkersu]', '', number)
        return (number, date)
    else:
        return False


def fix(item, worksheet, i, ii, index, shop):
    logging.info('СКАН: fix')
    if item['count'].find(' ') != -1:
        item['count'] = ','.join(item['count'].split(' '))

    x = 0
    item['type'] = re.sub('[^а-яА-Я]', '', item['type'])
    while True:
        if item['count'].find(',') != -1 or item['count'].find('.'):
            try:
                l = len(item['count'].split(',')[1])
            except:
                try:
                    l = len(item['count'].split('.')[1])
                except:
                    l = 0
            if l == 3:
                s = str(worksheet.cell_value(i, index[1] + ii + (1 if x == 0 else 2)))
                if s.find(',') != -1 or s.find('.') != -1:
                    try:
                        l2 = len(
                            str(worksheet.cell_value(i, index[1] + ii + (1 if x == 0 else 2 if x == 1 else 3))).split(
                                ',')[1])
                    except:
                        l2 = len(str(worksheet.cell_value(i, index[1] + ii + (
                            1 if x == 0 else 2 if x == 1 else 3))).split('.')[1])
                    if l2 == 2:
                        if log: print('1 ИСПРАВЛЕН ID')
                        break
                    else:
                        if log: print('1 ИСПРАВЛЕНО КОЛИЧЕСТВО!')
                        item['count'] = str(worksheet.cell_value(i, index[1] + ii + (
                            1 if x == 0 else 2 if x == 1 else 3)))
                        if item['count'].find(' ') != -1:
                            item['count'] = ','.join(item['count'].split(' '))
                        if x == 2: break
                        x = 1 if x == 0 else 2
                else:
                    if log: print('2 ИСПРАВЛЕН ID')
                    break
            else:
                if log: print('2 ИСПРАВЛЕНО КОЛИЧЕСТВО!')
                item['count'] = str(worksheet.cell_value(i, index[1] + ii + 1 if x == 0 else 2))
                if item['count'].find(' ') != -1:
                    item['count'] = ','.join(item['count'].split(' '))
                if x == 2: break
                x = 1 if x == 0 else 2
        else:
            if log: print('3 ИСПРАВЛЕНО КОЛИЧЕСТВО!')
            if log: print('COUNT: ' + str(item['count']))
            item['count'] = str(worksheet.cell_value(i, index[1] + ii + (1 if x == 0 else 2)))
            if log: print('COUNT: ' + str(item['count']))
            if item['count'].find(' ') != -1:
                item['count'] = ','.join(item['count'].split(' '))
            if x == 2: break
            x = 1 if x == 0 else 2

    if str(item['count']).find(',') != -1:
        item['count'] = ','.join(item['count'].split(','))

    if log: print('COST: ' + str(item['cost']))

    if item['cost'].find(' ') != -1:
        item['cost'] = '.'.join(item['cost'].split(' '))

    if log: print('COST2: ' + str(item['cost']))

    if shop == 'Матушка':
        if str(item['cost']).find('%') != -1:
            item['cost'] = str(worksheet.cell_value(i, index[3] + ii + 2))
            if log: print('COST: ' + str(item['cost']))
        elif str(worksheet.cell_value(i, index[3] + ii - 1)).find('%') != -1:
            item['cost'] = str(worksheet.cell_value(i, index[3] + ii + 1))
        elif str(worksheet.cell_value(i, index[3] + ii + 1)).find('%') != -1:
            item['cost'] = str(worksheet.cell_value(i, index[3] + ii + 3))
        if ' ' in item['cost']:
            print(item['cost'])
            print(item['cost'].split(' '))
            item['cost'] = item['cost'].split(' ')
            item['cost'] = '.'.join(item['cost'])
            print('ЕБАНАЯ ПРОВЕРКА')
            print(item['cost'])
    elif shop == 'Коф':
        if len(item['count']) > 8:
            item['count'] = str(worksheet.cell_value(i, index[1] + ii + 1))
        if item['cost'].find(',') != -1 or item['cost'].find('.') != -1:
            try:
                len_cost = len(item['cost'].split(',')[1])
            except:
                len_cost = len(item['cost'].split('.')[1])
            if len_cost == 3:
                item['cost'] = str(worksheet.cell_value(i, index[3] + ii + 1))
                item['cost'] = '.'.join(item['cost'].split(' '))
                try:
                    len_cost = len(item['cost'].split(',')[1])
                except:
                    len_cost = len(item['cost'].split('.')[1])
                if len_cost == 3:
                    item['cost'] = str(worksheet.cell_value(i, index[3] + ii + 2))
                    item['cost'] = '.'.join(item['cost'].split(' '))


    if str(item['cost']).find(',') != -1:
        item['cost'] = item['cost'].split(',')
        item['cost'] = '.'.join(item['cost'])

    if item['cost'] == '':
        item['cost'] = '0'

    if len(item['name']) < 4:
        item['name'] = str(worksheet.cell_value(i, index[0] + ii - 1))
        if len(item['name']) < 4:
            item['name'] = str(worksheet.cell_value(i, index[0] + ii - 2))
    return item


def doc(shop, doc):
    logging.info('СКАН: doc')
    import xlrd
    items = []
    # Open the Workbook
    if shop == 'Чек':
        return check(doc)
    else:
        if shop == 'КофП':
            index = [0, 1, 2, 3]
        elif shop == 'Коф':
            index = [0, 8, 4, 9]
        elif shop == 'Метро':
            index = [0, 3, 2, 4]
        elif shop == 'Матушка':
            index = [0, 8, 2, 13]
        elif shop == 'Хозы':
            index = [0, 1, 2, 3]
        elif shop == 'Айсбери':
            index = [0, 4, 3, 13]
        elif shop == 'Юнит':
            index = [0, 8, 2, 9]
        elif shop == 'Выпечка':
            index = [0, 6, 2, 10]
        elif shop == 'Десан':
            index = [0, 4, 3, 10]
        elif shop == 'Арома':
            index = [0, 4, 3, 5]
        else:
            return False
        try:
            if doc.split('.')[1] in ['xls', 'xlsx']:
                if log: print('Чтение XLS')
                workbook = xlrd.open_workbook(doc)
                worksheet = workbook.sheet_by_index(0)
                if log: print(shop)
                id = 1
                types = ("шт", 'уп', 'рул', 'упак', 'мст', 'кг', 'кор', 'шг', 'кт', 'уг')
                header_find = True
                type_find = True
                for i in range(0, 40):
                    if header_find and type_find:
                        header = hat(worksheet, i)
                        if header != False:
                            header_find = False
                    item = {}
                    item['id'] = id
                    try:
                        ii = 0
                        while ii < 4:
                            temp_Type = re.sub('[^а-яА-Я]', '', str(worksheet.cell_value(i, index[2] + ii)).lower())
                            if str(temp_Type).lower() in types:
                                break
                            else:
                                ii += 1

                        temp_Name = str(worksheet.cell_value(i, index[0] + ii))
                        print(temp_Type)

                        if len(temp_Name) < 4:
                            temp_Name = str(worksheet.cell_value(i, index[0] + ii - 1))
                            if len(temp_Name) < 4:
                                temp_Name = str(worksheet.cell_value(i, index[0] + ii - 2))

                        if log: print('\n\nКоррекция сдвига на: ' + str(ii))
                        if log: print('Тип упаковки: ' + str(worksheet.cell_value(i, index[2] + ii)).lower())
                        if log: print('Наименование: ' + str(worksheet.cell_value(i, index[0] + ii)))

                        if len(temp_Name) > 2 and temp_Type in types:
                            type_find = False
                            id += 1
                            item['name'] = str(worksheet.cell_value(i, index[0] + ii))
                            item['count'] = str(worksheet.cell_value(i, index[1] + ii))
                            item['type'] = str(worksheet.cell_value(i, index[2] + ii)).lower()
                            item['cost'] = str(worksheet.cell_value(i, index[3] + ii))

                            item = fix(item, worksheet, i, ii, index, shop) # Коррекция таблицы

                            if log: print('TYPE: ' + item['type'])

                            if str(item['type']).lower() in types:
                                if log: print(items)
                                items.append(item)
                        else:
                            if log: print('Длина наименования менее двух символов и не найден вид упаковки')
                    except Exception as e:
                        if log: print('ОШИБКА: ' + str(e))
                        if log: print('ID: ' + str(i))
                if log: print('Результат сканирования:')
                if log: print(items)
                if log: print(header)
                if header != False and len(header) >= 2:
                    check = {'date': str(header[1]), 'check': str(header[0]), 'items': items}
                else:
                    check = items
                return check
        except Exception as e:
            if e == 'list index out of range':
                if log: print('Строки закончились')
            else:
                if log: print('ОШИБКА: ' + str(e))
        else:
            if log: print('Формат файла не поддерживается!')
            return False