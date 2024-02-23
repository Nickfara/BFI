import json


def check(doc): # Сканер json чека
    check = None
    with open(doc, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        items = data['items']
        print(items)
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
    print(check)
    return check


def doc(shop, doc):
    import xlrd
    items = []
    # Open the Workbook
    if shop == 'Чек':
        return check(doc)
    else:
        try:
            workbook = xlrd.open_workbook(doc)
            # Open the worksheet
            worksheet = workbook.sheet_by_index(0)
            # Iterate the rows and columns
            print(shop)
            if shop == 'КОФ (Полный список)':
                index = [0, 1, 2, 3]
            elif shop == 'КОФ (Передний лист)':
                index = [0, 7, 5, 9]
            elif shop == 'METRO':
                index = [0, 3, 2, 4]
            elif shop == 'Матушка':
                index = [0, 8, 2, 13]
            elif shop == 'Хозы':
                index = [0, 8, 2, 9]
            else:
                return False
            id = 1
            for i in range(0, 900):
                item = {}
                item['id'] = id
                try:
                    if len(worksheet.cell_value(i, index[0])) > 2:
                        id += 1
                        item['name'] = worksheet.cell_value(i, index[0])
                        item['count'] = worksheet.cell_value(i, index[1])
                        item['type'] = worksheet.cell_value(i, index[2])
                        item['cost'] = worksheet.cell_value(i, index[3])
                        items.append(item)
                except:
                    pass
            print(items)
            return items
        except:
            print('Чтение файла не удалось!')