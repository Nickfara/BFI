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
        if doc.split('.')[1] in ['xls', 'xlsx']:
            if log: print('Чтение XLS')
            workbook = xlrd.open_workbook(doc)
            worksheet = workbook.sheet_by_index(0)
            if log: print(shop)
            id = 1
            try:
                for i in range(0, 40):
                    item = {}
                    item['id'] = id
                    try:
                        ii = 0
                        while ii < 4:
                            if str(worksheet.cell_value(i, index[2] + ii)).lower() in (
                            "шт", 'уп', 'рул', 'упак', 'мст', 'кг', 'кор'):
                                break
                            else:
                                ii += 1
                        if log: print('\n\nКоррекция сдвига на: ' + str(ii))
                        if log: print('Тип упаковки: ' + str(worksheet.cell_value(i, index[2] + ii)).lower())
                        if log: print('Наименование: ' + str(worksheet.cell_value(i, index[0] + ii)))
                        if len(str(worksheet.cell_value(i, index[0] + ii))) > 2 and str(worksheet.cell_value(i, index[2] + ii)).lower() in (
                            "шт", 'уп', 'рул', 'упак', 'мст', 'кг', 'кор'):
                            id += 1
                            item['name'] = str(worksheet.cell_value(i, index[0] + ii))
                            item['count'] = str(worksheet.cell_value(i, index[1] + ii))
                            if item['count'].find(' ') != -1:
                                item['count'] = ','.join(item['count'].split(' '))

                            x = 0

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
                                                l2 = len(str(worksheet.cell_value(i, index[1] + ii + (1 if x == 0 else 2 if x == 1 else 3))).split(',')[1])
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
                                                    item['count'] = ','.join(item['count'].strip(' '))
                                                if x == 2: break
                                                x = 1 if x == 0 else 2
                                        else:
                                            if log: print('2 ИСПРАВЛЕН ID')
                                            break
                                    else:
                                        if log: print('2 ИСПРАВЛЕНО КОЛИЧЕСТВО!')
                                        item['count'] = str(worksheet.cell_value(i, index[1] + ii + 1 if x == 0 else 2))
                                        if item['count'].find(' ') != -1:
                                            item['count'] = ','.join(item['count'].strip(' '))
                                        if x == 2: break
                                        x = 1 if x == 0 else 2
                                else:
                                    if log: print('3 ИСПРАВЛЕНО КОЛИЧЕСТВО!')
                                    if log: print('COUNT: ' + str(item['count']))
                                    item['count'] = str(worksheet.cell_value(i, index[1] + ii + (1 if x == 0 else 2)))
                                    if log: print('COUNT: ' + str(item['count']))
                                    if item['count'].find(' ') != -1:
                                        item['count'] = ','.join(item['count'].strip(' '))
                                    if x == 2: break
                                    x = 1 if x == 0 else 2

                            if str(item['count']).find(',') != -1:
                                item['count'] = ','.join(item['count'].split(','))

                            item['type'] = str(worksheet.cell_value(i, index[2] + ii)).lower()
                            item['cost'] = str(worksheet.cell_value(i, index[3] + ii))
                            if log: print('COST: ' + str(item['cost']))

                            if item['cost'].find(' ') != -1:
                                item['cost'] = '.'.join(item['cost'].split(' '))
                            if log: print('COST2: ' + str(item['cost']))
                            if shop == 'Матушка':
                                if str(item['cost']).find('%') != -1:
                                    item['cost'] = '.'.join(str(worksheet.cell_value(i, index[3] + ii + 2)).strip(' '))
                                    if log: print('COST: ' + str(item['cost']))
                                elif str(worksheet.cell_value(i, index[3] + ii - 1)).find('%') != -1:
                                    item['cost'] = '.'.join(str(worksheet.cell_value(i, index[3] + ii + 1)).strip(' '))
                                elif str(worksheet.cell_value(i, index[3] + ii + 1)).find('%') != -1:
                                    item['cost'] = '.'.join(str(worksheet.cell_value(i, index[3] + ii + 3)).strip(' '))
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

                            if log: print('TYPE: ' + item['type'])
                            if str(item['type']).lower()  in ("шт", 'уп', 'рул', 'упак', 'мст', 'кг', 'кор'):
                                if log: print(items)
                                items.append(item)
                        else:
                            if log: print('Длина наименования менее двух символов и не найден вид упаковки')
                    except Exception as e:
                        if log: print('ОШИБКА: ' + str(e))
                        if log: print('ID: ' + str(i))
                if log: print(items)
                return items
            except Exception as e:
                if e == 'list index out of range':
                    if log: print('Строки закончились')
                else:
                    if log: print(e)
        else:
            if log: print('Формат файла не поддерживается!')
            return False