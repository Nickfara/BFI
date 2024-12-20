import logging
import os
import re
import time

import pyautogui
import pyperclip

import Database_connections as dc

log = True
check_text = 'Пика узелок'


def paste(text):
    pyperclip.copy(text)
    if type(str(text)) in (str, int, float):
        text = re.sub('[^а-яА-Я0-9.,]', '', str(text))
        if len(str(text)) > 0:
            pyautogui.hotkey('ctrl', 'v')

def copy_text():  # Проверка
    logging.info('АВТОКЛИКЕР: keyboard\033[0m')
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    key = pyperclip.paste()
    os.system('echo ' + 'текст'.strip() + '| clip')
    return key

def keyboard():  # Проверка
    logging.info('АВТОКЛИКЕР: keyboard\033[0m')
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')
    key = pyperclip.paste()
    if log: print('Key=', str(key))
    if key.find(',') != -1 and len(key) < 8:
        x = False
    elif key == check_text:
        x = check_text
    else:
        x = key
    os.system('echo ' + 'текст'.strip() + '| clip')
    return x


def header(shop, check_data):
    logging.info('АВТОКЛИКЕР: header\033[0m')
    print(check_data)
    shop_name = check_data['header']['shop']

    shops = {'Чек': 'Рынок/Магазин', 'Коф': 'ИП Петухов В.В.', 'КофП': 'ИП Петухов В.В.',
             'Метро': 'ООО "МЕТРО КЭШ ЭНД КЕРРИ"', 'Матушка': 'ООО ТД "Матушка"', 'ООО ТД Матушка': 'ООО ТД "Матушка"', 'Хозы': 'ИП Касумов М.А.',
             'Юнит': 'ООО "Юнит"', 'Выпечка': 'ИП Насретдинов Д.Н.', 'Айсберри': 'ООО ТД "Айсберри"',
             'Десан': 'ООО "ДЕСАН"', 'Виста': 'ООО "ВИСТ"', 'Кофе': 'ООО "СТС"', 'Арома': 'ИП Щербакова И. В.'}

    numbers = {'Чек': 'чек ', 'Коф': '', 'КофП': '',
               'Метро': '61 /030', 'Матушка': 'MKER-', 'Хозы': '',
               'Юнит': '', 'Выпечка': '', 'Айсберри': '',
               'Десан': '', 'Виста': 'USKA-00', 'Кофе': '', 'Арома': ''}

    shops_name = ('Рынок/Магазин', 'ИП Петухов В.В.', 'ООО "МЕТРО КЭШ ЭНД КЕРРИ"', 'ООО ТД "Матушка"',
                  'ИП Касумов М.А.', 'ООО "Юнит"', 'ИП Насретдинов Д.Н.', 'ООО ТД "Айсберри"', 'ООО "ДЕСАН"',
                  'ООО "ВИСТ"', 'ООО "СТС"', 'ИП Щербакова И. В.')

    repeater = True

    while repeater and dc.get_item('АВТОКЛИКЕР')['names'] == '1':
        paste(shops[shop.text])
        time.sleep(4    )
        pyautogui.press('enter')
        if keyboard() in shops_name:
            repeater = False

    repeater = True

    while repeater and dc.get_item('АВТОКЛИКЕР')['names'] == '1':
        result = copy_text()

        print(result)
        if '9:00' in str(result) and len(result) == 15:
            repeater = False
        else:
            if result in ('Основной склад', 'Склад Бар', 'Склад Кухня'):
                pyautogui.hotkey('shift', 'tab')
            elif result in ('Рынок/Магазин', 'ИП Петухов В.В.', 'ООО "МЕТРО КЭШ ЭНД КЕРРИ"', 'ООО ТД "Матушка"',
                            'ИП Касумов М.А.', 'ООО "Юнит"', 'ИП Насретдинов Д.Н.', 'ООО ТД "Айсберри"', 'ООО "ДЕСАН"',
                            'ООО "ВИСТ"', 'ООО "СТС"', 'ИП Щербакова И. В.'):
                pyautogui.press('tab')
            else:
                for i in range(1, 13):
                    pyautogui.hotkey('shift', 'tab')
                pyautogui.press('tab', presses=4)

    pyautogui.press('left')
    time.sleep(1.5)

    if len(check_data['header']['date']) == 1:
        check_data['header']['date'] = check_data['header']['date'][0]
    if check_data != None:
        time.sleep(0.5)
        if shop.text == 'Чек':
            check_data['header']['date'] = check_data['header']['date'].split('.')
        else:
            check_data['header']['date'] = check_data['header']['date'].split('.')
            if len(check_data['header']['date']) > 2:
                check_data['header']['date'] = (check_data['header']['date'][2], check_data['header']['date'][1], check_data['header']['date'][0])
            else:
                check_data['header']['date'] = ('01', '01', '2024')


        check_data['header']['date']
        paste(check_data['header']['date'][2])
        time.sleep(5)
        paste(check_data['header']['date'][1])
        paste(check_data['header']['date'][0])
        time.sleep(5)
        pyautogui.press('tab', presses=2)
    else:
        pyautogui.press('tab', presses=3)

    time.sleep(0.5)
    repeater = True

    while repeater and dc.get_item('АВТОКЛИКЕР')['names'] == '1':
        if shop.text in ('Виста', 'Кофе', 'Айсберри'):
            paste('Склад Бар')
        elif shop.text in ('ДЕСАН', 'Хозы'):
            paste('Основной склад')
        else:
            paste('Склад Кухня')

        time.sleep(0.5)
        result = copy_text()
        if result in ('Основной склад', 'Склад Бар', 'Склад Кухня'):
            repeater = False
        else:
            for i in range(1, 13):
                pyautogui.hotkey('shift', 'tab')
            pyautogui.press('tab', presses=6)

    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('tab', presses=3)
    time.sleep(0.5)
    if check_data != None:
        paste(check_data['header']['number'])
        time.sleep(0.5)
        pyautogui.press('tab')
        if shop.text != 'Чек':
            paste(check_data['header']['number'])
            time.sleep(0.5)
        pyautogui.press('tab', presses=2)
        time.sleep(0.5)
        paste(check_data['header']['date'][2])
        paste(check_data['header']['date'][1])
        paste(check_data['header']['date'][0])
        time.sleep(0.5)
        pyautogui.press('tab', presses=2)
        time.sleep(0.2)
        if shop.text != 'Чек':
            paste(check_data['header']['number'])
            time.sleep(0.5)
        pyautogui.press('tab', presses=4)
    else:
        paste(numbers[shop.text])
        time.sleep(0.5)
        pyautogui.press('tab', presses=9)
        time.sleep(0.5)


def type_input(shop, name):
    time.sleep(1)
    if shop.text in ('Метро', 'Чек'):
        tc = name.split(' ')[0]
        print('tc = ' + str(tc))
        if tc.lower() in ('1кг', "1л", "1000г", '1'):
            pyautogui.press('right')
        else:
            pyautogui.press('1')
            pyautogui.press('right', presses=3)
            pyautogui.press(tc[0])
            pyautogui.press('0')
            pyautogui.press('0')
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.hotkey('ctrl', 'c')
            key = pyperclip.paste()
            if key == '0,000':
                pass
            else:
                pyautogui.press('enter')


def start(items, shop, checkboxs, format, type, check_data=None):
    logging.info('АВТОКЛИКЕР: start\033[0m')
    if log: print('\033[46m')
    if log: print('Автокликер запущен!')
    dc.update_item('АВТОКЛИКЕР', '1')
    time.sleep(5)
    item_n = 1
    item_warning = []

    print('ПРОВЕРКА')
    print(items)
    if len(items) > 0:
        if isinstance(items, list):
            if isinstance(items[0], dict) and len(items) > 0:
                if checkboxs['header']:
                    header(shop, check_data)
                for i in items:
                    if dc.get_item('АВТОКЛИКЕР')['names'] == '1':
                        if log: print(f'Заводится: {i["name"]}')
                        if log: print('ПРОВЕРКА ЧЕКБОКСОВ')
                        if log: print(checkboxs)
                        if checkboxs['name'] or checkboxs['type']:
                            check_position('name')

                            time.sleep(0.5)
                            if checkboxs['name']:
                                print('Заводится название: ' + str(i['name']))
                                paste(i['name'])

                            pyautogui.press('enter')

                            if keyboard():
                                pyautogui.press('enter')

                            if keyboard():
                                if log: print('Курсор не на количестве, нажимается вправо.')
                                pyautogui.press('right')

                            if checkboxs['type']:
                                type_click(shop, i)

                        if checkboxs['count'] or checkboxs['cost']:
                            check_position('count')

                            if checkboxs['count']:
                                print('Заводится количество: ' + str(i['count']))
                                pyautogui.press('0')
                                paste(i['count'])

                                pyautogui.press('enter')

                            if shop.text in ['Айсбери', 'Десан',
                                             'Алма']:  # Если одна из этих накладных, то заводися сумма - шаги вправо
                                pyautogui.press('right', presses=4)

                            if checkboxs['cost']:
                                print('Заводится цена: ' + str(i['cost']))
                                pyautogui.hotkey('ctrl', 'a')
                                pyautogui.hotkey('ctrl', 'c')
                                key = re.sub('[^0-9.,]', '', pyperclip.paste())

                                try:  # Проверка на дорогую стоимость
                                    check_sum = float(i['cost']) / float('.'.join(key.split(',')))
                                    if check_sum > 1.7:
                                        print('ПРЕДУПРЕЖДЕНИЕ! В ДАННОЙ ПОЗИЦИИ СУММА СИЛЬНО ОТЛИЧАЕТСЯ!')
                                        item_warning.append(item_n)
                                except:
                                    pass

                                paste(i['cost'])

                                pyautogui.press('enter')

                            if shop.text in ['Айсбери',
                                             'Десан']:  # Если одна из этих накладных, то заводися сумма - шаги влево
                                pyautogui.press('left', presses=3)

                            if checkboxs['name'] or checkboxs['type']:
                                print('Выполняется 6 шагов влево')
                                pyautogui.press('left', presses=6)
                            else:
                                print('Выполняется 4 шага влево')
                                pyautogui.press('left', presses=4)

                            time.sleep(0.2)
                            pyautogui.press('down')
                            time.sleep(0.5)
                        else:
                            pyautogui.press('left', presses=2)
                            time.sleep(0.2)
                            pyautogui.press('down')
                            time.sleep(1)
    if log: print('Автокликер закончил свою работу!')
    if log: print('\033[0m')
    dc.update_item('АВТОКЛИКЕР', '0')
    return item_warning


def check_position(type):
    repeater = True
    while repeater and dc.get_item('АВТОКЛИКЕР')['names'] == '1':
        if type == 'count':
            print('Проводится проверка на позицию в количестве')
            pyautogui.press('0')
        elif type == 'name':
            print('Проводится поверка на позицию в названии')
            paste(check_text)
            pyautogui.press('enter')

        result = keyboard()

	
        if result != (False if type == 'count' else check_text if type == 'name' else True):
            pyautogui.press('tab', presses=3)
            pyautogui.press('left', presses=10)
            pyautogui.press('tab', presses=3 if type == 'count' else 1 if type == 'name' else 0)
            print(f'Нажат 3 раза таб, 10 шагов влево и {3 if type == "count" else 1 if type == "name" else 0} раза таб')

        if result == (False if type == 'count' else check_text if type == 'name' else True):
            repeater = False
            print('Выключается цикл проверки позиции')


def type_click(shop, i):
    if log: print('Заводится ТИП: ' + str(i['type']))
    if i['type'].lower() in ("шт", 'уп', 'рул', 'упак', 'мст'):
        if shop.text == 'Чек':
            count_check = True
            float_ = float(i['count'])
            float_ = float_ % 1
            if float_ > 0.0:
                count_check = False
            if count_check:
                pyautogui.press('tab')
                pyautogui.press('left', presses=6)
                pyautogui.press('right', presses=2)
                pyautogui.press('1')
        else:
            pyautogui.press('tab')
            pyautogui.press('left', presses=6)
            pyautogui.press('right', presses=2)

            if i['original'].split(' ')[0].lower() in ('1кг', "1л", "1000г", '1'):
                pyautogui.press('right')
            else:
                print('Объём тары:')
                print(i['original'].split(' ')[0].lower())
                pyautogui.press('1')

            if type:
                type_input(shop, i['original'])

    if log: print('ТИП ДОРАБОТАЛ')
