import json
import re
import logging

import xlrd
from openpyxl import load_workbook

log = True
h = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P",
     "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z","AA", "AB", "AC", "AD", "AE",
     "AF", "AG", "AH", "AI", "AJ", "AK", "AL", "AM", "AN", "AO", "AP", "AQ", "AR",
     "AS", "AT", "AU", "AV", "AW", "AX", "AY", "AZ"]


def hat(worksheet, i):
    logging.info('СКАН: hat')
    if log: print('\033[43m')
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
    if log: print('Работа с заголовком завершена')
    if log: print('\033[0m')


def fix(item, worksheet, i, ii, index, shop):
    logging.info('СКАН: fix')
    if log: print('\033[41m')
    if item['count'].find(' ') != -1:
        item['count'] = ','.join(item['count'].split(' '))

    x = 0
    item['type'] = re.sub('[^а-яА-Я,."]', '', item['type'])
    item['count'] = re.sub('[^0-9.,]', '', item['count'])
    item['cost'] = re.sub('[^0-9.,]', '', item['cost'])
    print('ПРОВЕРКА Данных после очистки символов:')
    print(item['type'])
    print(item['count'])
    print(item['cost'])
    while True and shop != 'Коф':
        if item['count'].find(',') != -1 or item['count'].find('.') != -1:
            try:
                l = len(re.sub('[^0-9.,]', '', str(item['count'].split(',')[1])))
            except:
                try:
                    l = len(re.sub('[^0-9.,]', '', str(item['count'].split('.')[1])))
                except:
                    l = 0
            print('Проверка L:' + str(l))
            if l == 3:
                s = str(worksheet.cell_value(i, index[1] + ii + (1 if x == 0 else 2)))
                if s.find(',') != -1 or s.find('.') != -1:

                    temp_count1 = str(worksheet.cell_value(i, index[1] + ii + (1 if x == 0 else 2 if x == 1 else 3)))
                    try:
                        print(temp_count1.split(',')[1])
                    except:
                        print(temp_count1.split('.')[1])
                    try:
                        l2 = len(
                            re.sub('[^0-9.,]', '', str(worksheet.cell_value(i, index[1] + ii + (1 if x == 0 else 2 if x == 1 else 3))).split(
                                ',')[1]))
                    except:
                        l2 = len(str(worksheet.cell_value(i, index[1] + ii + (
                            1 if x == 0 else 2 if x == 1 else 3))).split('.')[1])
                    print('Проверка L2:' + str(l2))
                    if l2 == 2:
                        if log: print('1 ИСПРАВЛЕН ID')
                        break
                    else:
                        if log: print('1 ИСПРАВЛЕНО КОЛИЧЕСТВО!')
                        if log: print('COUNT до: ' + str(item['count']))
                        item['count'] = str(worksheet.cell_value(i, index[1] + ii + (
                            1 if x == 0 else 2 if x == 1 else 3)))
                        item['count'] = re.sub('[^0-9.,]', '', item['count'])
                        if log: print('COUNT после: ' + str(item['count']))
                        if item['count'].find(' ') != -1:
                            item['count'] = ','.join(item['count'].split(' '))
                        if x == 2: break
                        x = 1 if x == 0 else 2
                else:
                    if log: print('2 ИСПРАВЛЕН ID')
                    break
            else:
                if log: print('2 ИСПРАВЛЕНО КОЛИЧЕСТВО!')
                if log: print('COUNT до: ' + str(item['count']))
                new_id = index[1] + ii + (1 if x == 0 else 2)
                if log: print('new_id: ' + str(new_id))
                item['count'] = str(worksheet.cell_value(i, new_id))
                item['count'] = re.sub('[^0-9.,]', '', item['count'])
                if log: print('COUNT после: ' + str(item['count']))
                if item['count'].find(' ') != -1:
                    item['count'] = ','.join(item['count'].split(' '))
                if x == 2: break
                x = 1 if x == 0 else 2
        else:
            if log: print('3 ИСПРАВЛЕНО КОЛИЧЕСТВО!')
            if log: print('COUNT до: ' + str(item['count']))
            if shop != 'Хозы':
                item['count'] = str(worksheet.cell_value(i, index[1] + ii + (1 if x == 0 else 2)))
                item['count'] = re.sub('[^0-9.,]', '', item['count'])
            else:
                try:
                    int(item['count'])
                    break
                except:
                    pass
            if log: print('COUNT: после ' + str(item['count']))
            if item['count'].find(' ') != -1:
                item['count'] = ','.join(item['count'].split(' '))
            if x == 2: break
            x = 1 if x == 0 else 2

    if str(item['count']).find(',') != -1:
        item['count'] = ','.join(item['count'].split(','))

    if log: print('COST: ' + str(item['cost']))


    if item['cost'].find(' ') != -1:
        item['cost'] = '.'.join(item['cost'].split(' '))
    if item['cost'].find(',') != -1:
        item['cost'] = '.'.join(item['cost'].split(','))
    if len(item['cost'].split('.')) > 2:
        temp = item['cost'].split('.')
        temp2 = str(temp[0]) + '' +str(temp[1]) + '.' + str(temp[2])
        item['cost'] = temp2

    if log: print('COST2: ' + str(item['cost']))

    if shop == 'Матушка':
        if str(item['cost']) in ('10', '20'):
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
        if False:
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
    else:
        print('Поиск ячейки цены')
        print('COST = ' + str(item['cost']))
        print('COST = ' + str(len(item['cost'])))
        for li in range(0, 4):
            if item['cost'].find('.') != -1:
                if len(item['cost'].split('.')[1]) == 3:
                    print('ячейка это цена')
                    item['cost'] = str(worksheet.cell_value(i, index[3] + ii + li))
                    if item['cost'].find(' ') != -1:
                        item['cost'] = '.'.join(item['cost'].split(' '))
                    if item['cost'].find(',') != -1:
                        item['cost'] = '.'.join(item['cost'].split(','))
                    if len(item['cost'].split('.')[1]) == 2:
                        print('Ячейка с ценой найдена!')
                        break
            if len(item['cost']) < 2:
                print('Строка пустая')
                item['cost'] = str(worksheet.cell_value(i, index[3] + ii + li + 2))
                if item['cost'].find(' ') != -1:
                    item['cost'] = '.'.join(item['cost'].split(' '))
                if item['cost'].find(',') != -1:
                    item['cost'] = '.'.join(item['cost'].split(','))
                if item['cost'].find('.') != -1:
                    if len(item['cost'].split('.')[1]) == 2:
                        break

    if log: print('COST3: ' + str(item['cost']))
    if str(item['cost']).find(',') != -1:
        item['cost'] = item['cost'].split(',')
        item['cost'] = '.'.join(item['cost'])

    if item['cost'] == '':
        item['cost'] = '0'

    if len(item['name']) < 4:
        item['name'] = str(worksheet.cell_value(i, index[0] + ii - 1))
        if len(item['name']) < 4:
            item['name'] = str(worksheet.cell_value(i, index[0] + ii - 2))
    if log: print('Фикс завершен')
    if log: print('\033[0m')
    return item


def check_(doc_): # Сканер json чека
    logging.info('СКАН: check')
    if log: print('\033[43m')
    check = None
    with open(doc_, 'r', encoding='utf-8') as json_file:
        if doc_.split('.')[1].lower() in ('json', 'wb', 'ms'):
            data = json.load(json_file)
            print('ВНУТРЕННОСТИ JSONa')
            print(data)
            items = data['items']
            if log: print(items)
            filter_items = []
            id = 1
            for i in items: # Фильтрация обьектов
                temp = 0
                e = 0
                if doc_.split('.')[1].lower() not in ('wb', 'ms'):
                    while e < len(filter_items):
                        if i['name'] == filter_items[e]['name']:
                            filter_items[e]['count'] += i['quantity']
                            filter_items[e]['sum'] += i['sum']/100
                            filter_items[e]['cost'] = filter_items[e]['sum'] / filter_items[e]['count']
                            temp = 1
                        e += 1

                    if temp == 0:
                        filter_items.append({'id': id, 'name': i['name'], 'cost': float(i['price'])/100,
                                         'count': i['quantity'], 'sum': i['sum']/100, 'type': 'шт'})
                        id += 1
                else:
                    filter_items = items

            if doc_.split('.')[1].lower() not in ('wb', 'ms'):
                check = {'date': data['dateTime'], 'check': data['requestNumber'], 'items': filter_items, }
            else:
                check = {'date': data['dateTime'], 'check': data['requestNumber'], 'items': filter_items, }
            return check
        else:
            return False
    if log: print('Сканирование чека завершено')
    if log: print('\033[0m')


def doc(shop, doc_):
    logging.info('СКАН: doc')
    if log: print('\033[46m')
    items = []
    # Open the Workbook
    if shop == 'Чек':
        return check_(doc_)
    else:
        if shop == 'КофП':
            index = [3, 5, 4, 6]
        elif shop == 'Коф':
            index = [2, 23, 8, 25]
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
            index = [0, 8, 2, 10]
        elif shop == 'Десан':
            index = [0, 4, 3, 10]
        elif shop == 'Арома':
            index = [0, 4, 3, 5]
        else:
            return False
        try:
            if doc_.split('.')[1] == 'xls':
                if log: print('Чтение XLS')
                workbook = xlrd.open_workbook(doc_)
                worksheet = workbook.sheet_by_index(0)
                if log: print(shop)
                id = 1
                types = ("шт", 'уп', 'рул', 'упак', 'мст', 'кг', 'кор', 'шг', 'кт', 'уг')
                header_find = True
                type_find = True
                for i in range(0, 80):
                    if log: print('Цикл сканирования')
                    if header_find and type_find:
                        header = hat(worksheet, i)
                        if header != False:
                            header_find = False
                    item = {}
                    item['id'] = id
                    try:
                        ii = 0
                        while ii < 6:
                            temp_Type = re.sub('[^а-яА-Я,."]', '', str(worksheet.cell_value(i, index[2] + ii)).lower())
                            if str(temp_Type).lower() in types:
                                break
                            else:
                                ii += 1

                        temp_Name = str(worksheet.cell_value(i, index[0] + ii))
                        if len(temp_Name) < 4:
                            temp_Name = str(worksheet.cell_value(i, index[0] + ii - 1))
                            if len(temp_Name) < 4:
                                temp_Name = str(worksheet.cell_value(i, index[0] + ii - 2))

                        if log: print('\n\nКоррекция сдвига на: ' + str(ii))
                        if log: print('Тип упаковки: ' + str(worksheet.cell_value(i, index[2] + ii)).lower())
                        if log: print('Наименование: ' + str(worksheet.cell_value(i, index[0] + ii)))

                        temp_Type = re.sub('[^а-яА-Я,."]', '', temp_Type)
                        print('tempType:')
                        print(temp_Type)
                        if len(temp_Name) > 2 and temp_Type in types:
                            if log: print('Имя больше 2-х и тип есть в types')
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
                if log: print('items: ' + str(items))
                if log: print('header: ' + str(header))
                if header != False and len(header) >= 2:
                    check = {'date': str(header[1]), 'check': str(header[0]), 'items': items}
                else:
                    check = items
                return check
            elif doc_.split('.')[1] == 'xlsx':
                if log: print('Чтение XLSX')
                worksheet = load_workbook(doc_)
                if log: print(shop)

                id = 1
                types = ("шт", 'уп', 'рул', 'упак', 'мст', 'кг', 'кор', 'шг', 'кт', 'уг')
                header_find = True
                type_find = True

                date = str(worksheet.active['M19'].value).lower()
                number = str(worksheet.active['P19'].value).lower()
                header = (number, date)

                for i in range(25, 80):
                    item = {}
                    item['id'] = id
                    if log: print('\n\nЧтение строки:' + str(i))

                    item['name'] = str(worksheet.active[f'{h[index[0]]}{i}'].value)
                    item['count'] = str(worksheet.active[f'{h[index[1]]}{i}'].value)
                    item['type'] = str(worksheet.active[f'{h[index[2]]}{i}'].value).lower()
                    item['cost'] = str(worksheet.active[f'{h[index[3]]}{i}'].value)

                    if str(item['type']).lower() in types:
                        if log: print(items)
                        items.append(item)
                        id += 1
                    if log: print('item: ' + str(item))

                check = {'date': str(header[0]), 'check': str(header[1]), 'items': items}


                if log: print('Результат сканирования:')
                if log: print('items: ' + str(items))
                if log: print('header: ' + str(header))
                return check
        except Exception as e:
            if e == 'list index out of range':
                if log: print('Строки закончились')
            else:
                if log: print('ОШИБКА: ' + str(e))
        else:
            if log: print('Формат файла не поддерживается!')
            return False
    if log: print('Сканирование документа завершено')
    if log: print('\033[0m')
