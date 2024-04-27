import pyautogui
import time
import pyperclip
import os
import logging
import Database_connections as dc
log = True
def paste(text):
    pyperclip.copy(text)
    pyautogui.keyDown('ctrl')
    pyautogui.press('v')
    pyautogui.keyUp('ctrl')


def keyboard():  # Проверка расскладки и изменение на английскую!
    logging.info('АВТОКЛИКЕР: keyboard\033[0m')
    pyautogui.keyDown('ctrl')
    pyautogui.press('a')
    pyautogui.press('c')
    pyautogui.keyUp('ctrl')
    key = pyperclip.paste()
    if log: print(key)
    if key.find(',') != -1 and len(key) < 8:
        x = False
    else:
        x = True
    os.system('echo ' + 'текст'.strip() + '| clip')
    return x


def header(shop, check_data):
    logging.info('АВТОКЛИКЕР: header\033[0m')
    shops = {'Чек':'Рынок/Магазин', 'Коф':'ИП Петухов В.В.', 'КофП':'ИП Петухов В.В.',
                'Метро':'ООО "МЕТРО КЭШ ЭНД КЕРРИ"', 'Матушка':'ООО ТД "Матушка"','Хозы':'ИП Касумов М.А.',
                'Юнит':'ООО "Юнит"', 'Выпечка':'ИП Насретдинов Д.Н.', 'Айсберри':'ООО ТД "Айсберри"',
                'Десан':'ООО "ДЕСАН"', 'Виста':'ООО "ВИСТ"', 'Кофе':'ООО "СТС"', 'Арома':'ИП Щербакова И. В.'}
    numbers = {'Чек': 'чек ', 'Коф': '', 'КофП': '',
             'Метро': '61 /030', 'Матушка': 'MKER-', 'Хозы': '',
             'Юнит': '', 'Выпечка': '', 'Айсберри': '',
             'Десан': '', 'Виста': 'USKA-00', 'Кофе': '', 'Арома': ''}
    paste(shops[shop.text])
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(1.5)
    if check_data != None:
        pyautogui.press('tab')
        time.sleep(0.5)
        check_data['date'] = check_data['date'].split('T')[0].split('-')
        paste(check_data['date'][2])
        time.sleep(5)
        paste(check_data['date'][1])
        paste(check_data['date'][0])
        time.sleep(5)
        pyautogui.press('tab', presses=2)
    else:
        pyautogui.press('tab', presses=3)
    time.sleep(0.5)
    if shop.text in ('Виста', 'Кофе', 'Айсберри'):
        paste('Склад Бар')
    elif shop.text in ('ДЕСАН', 'Хозы'):
        paste('Основной склад')
    else:
        paste('Склад Кухня')

    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('tab', presses=3)
    time.sleep(0.5)
    if check_data != None:
        paste(check_data['number'])
        time.sleep(0.5)
        pyautogui.press('tab', presses=3)
        time.sleep(0.5)
        paste(check_data['date'][2])
        paste(check_data['date'][1])
        paste(check_data['date'][0])
        time.sleep(0.5)
        pyautogui.press('tab', presses=6)
    else:
        paste(numbers[shop.text])
        time.sleep(0.5)
        pyautogui.press('tab', presses=9)
        time.sleep(0.5)


def start(items, shop, checkboxs, check_data=None):
    logging.info('АВТОКЛИКЕР: start\033[0m')
    if log: print('Автокликер запущен!')
    dc.update_item('АВТОКЛИКЕР', '1')
    time.sleep(5)
    if shop.text in ['Виста', 'Кофе', 'Айсберри']:
        if log: print('Заводится накладная c 1 товаром')
        header(shop, check_data)
        paste('вода виста' if shop.text == 'Виста' else 'Мороженое в ас-те' if shop.text == 'Айсберри' else 'кофе')
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(0.5)
        if shop.text == 'Айсберри':
            pyautogui.press('left')
            time.sleep(0.5)
            pyautogui.press('1')
        else:
            paste('240' if shop.text == 'Виста' else '8')
            pyautogui.press('enter')
    else:
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
                            if checkboxs['name']:
                                paste(i['name'])
                            pyautogui.press('enter')
                            if keyboard():
                                pyautogui.press('enter')
                            if keyboard():
                                if log: print('Курсор не на количестве, нажимается вправо.')
                                pyautogui.press('right')

                            if checkboxs['type']:
                                if log: print('ТИП РАБОТАЕТ')
                                if i['type'].lower() in ("шт", 'уп', 'рул', 'упак', 'мст'):
                                    if shop.text == 'Чек':
                                        count_check = True
                                        float_ = float(i['count'])
                                        float_ = float_ % 1
                                        if float_ > 0.0:
                                            count_check = False
                                        if count_check:
                                            paste('0')
                                            if keyboard():
                                                pass
                                            else:
                                                if log: print('Нажимается влево так как курсор на цифре')
                                                pyautogui.press('left')
                                            pyautogui.press('1')
                                            paste('0')
                                            if keyboard():
                                                if log: print('Курсор не на количестве, нажимается ентер.')
                                                pyautogui.press('enter')
                                            paste('0')
                                            if keyboard():
                                                if log: print('Курсор не на количестве, нажимается вправо.')
                                                pyautogui.press('right')
                                    else:
                                        if log: print('У товара указано штука, начало изменения позиции.')
                                        paste('0')
                                        if keyboard():
                                            pass
                                        else:
                                            if log: print('Курсор на количестве, нажимается влево, для изменения на шт.')
                                            pyautogui.press('left')
                                        pyautogui.press('1')
                                        paste('0')
                                        if keyboard():
                                            if log: print('Курсор не на количестве, нажимается ентер.')
                                            pyautogui.press('enter')
                                        paste('0')
                                        if keyboard():
                                            if log: print('Курсор не на количестве, нажимается вправо.')
                                            pyautogui.press('right')
                            if log: print('ТИП ДОРАБОТАЛ')
                        if checkboxs['count'] or checkboxs['cost']:
                            if checkboxs['count']:
                                paste('0')
                                paste(i['count'])
                            pyautogui.press('enter')
                            if shop.text in ['Айсбери', 'ДЕСАН']: # Если одна из этих накладных, то заводися сумма - шаги вправо
                                pyautogui.press('right', presses=4)
                            if checkboxs['cost']:
                                paste(i['cost'])
                            pyautogui.press('enter')
                            if shop.text in ['Айсбери', 'ДЕСАН']: # Если одна из этих накладных, то заводися сумма - шаги влево
                                pyautogui.press('left', presses=3)
                            if checkboxs['name'] or checkboxs['type']:
                                pyautogui.press('left', presses=6)
                            else:
                                pyautogui.press('left', presses=4)
                            time.sleep(0.2)
                            pyautogui.press('down')
                            time.sleep(1)
                        else:
                            pyautogui.press('left', presses=2)
                            time.sleep(0.2)
                            pyautogui.press('down')
                            time.sleep(1)
    if log: print('Автокликер закончил свою работу!')
    dc.update_item('АВТОКЛИКЕР', '0')
