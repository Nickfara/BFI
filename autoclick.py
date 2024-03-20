import pyautogui
import time
import pyperclip
import os

def paste(text):
    pyperclip.copy(text)
    pyautogui.keyDown('ctrl')
    pyautogui.press('v')
    pyautogui.keyUp('ctrl')


def keyboard():  # Проверка расскладки и изменение на английскую!
    pyautogui.keyDown('ctrl')
    pyautogui.press('a')
    pyautogui.press('c')
    pyautogui.keyUp('ctrl')
    key = pyperclip.paste()
    print(key)
    if key.find(',') != -1 and len(key) < 8:
        x = False
    else:
        x = True
    os.system('echo ' + 'текст'.strip() + '| clip')
    return x


def start(items, shop, checkboxs):
    print('Автокликер запущен!')
    time.sleep(5)
    if shop.text in ['Виста', 'Кофе']:
        print('Заводится накладная висты')
        paste('ООО "ВИСТ"' if shop.text == 'Виста' else 'ООО "СТС"')
        pyautogui.press('enter')
        time.sleep(1.5)
        pyautogui.press('tab', presses=3)
        paste('Склад Бар')
        pyautogui.press('enter')
        time.sleep(0.5)
        pyautogui.press('tab', presses=3)
        paste('USKA-00' if shop.text == 'Виста' else '')
        pyautogui.press('tab', presses=9)
        paste('вода виста' if shop.text == 'Виста' else 'кофе')
        pyautogui.press('enter')
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(0.5)
        paste('240' if shop.text == 'Виста' else '8')
        pyautogui.press('enter')
    else:
        if type(items) is list:
            if type(items[0]) is dict and len(items) > 0:
                for i in items:
                    print(f'Заводится: {i["name"]}')
                    if checkboxs['name'] or checkboxs['type']:
                        if checkboxs['name']:
                            paste(i['name'])
                        pyautogui.press('enter')
                        if keyboard():
                            pyautogui.press('enter')
                        if keyboard():
                            print('Курсор не на количестве, нажимается вправо.')
                            pyautogui.press('right')

                        if checkboxs['type']:
                            print('ТИП РАБОТАЕТ')
                            if i['type'].lower() in ["шт", 'уп', 'рул', 'упак', 'мст']:
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
                                            print('Нажимается влево так как курсор на цифре')
                                            pyautogui.press('left')
                                        pyautogui.press('1')
                                        paste('0')
                                        if keyboard():
                                            print('Курсор не на количестве, нажимается ентер.')
                                            pyautogui.press('enter')
                                        paste('0')
                                        if keyboard():
                                            print('Курсор не на количестве, нажимается вправо.')
                                            pyautogui.press('right')
                                else:
                                    print('У товара указано штука, начало изменения позиции.')
                                    paste('0')
                                    if keyboard():
                                        pass
                                    else:
                                        print('Курсор на количестве, нажимается влево, для изменения на шт.')
                                        pyautogui.press('left')
                                    pyautogui.press('1')
                                    paste('0')
                                    if keyboard():
                                        print('Курсор не на количестве, нажимается ентер.')
                                        pyautogui.press('enter')
                                    paste('0')
                                    if keyboard():
                                        print('Курсор не на количестве, нажимается вправо.')
                                        pyautogui.press('right')
                        print('ТИП ДОРАБОТАЛ')
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
    print('Автокликер закончил свою работу!')
