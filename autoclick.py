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
    if key.find(',0') != -1:
        x = False
    else:
        x = True
    os.system('echo ' + 'текст'.strip() + '| clip')
    return x

def start(items, shop, checkboxs):
    print('Автокликер запущен!')
    time.sleep(5)
    if type(items[0]) is dict and len(items) > 0:
        for i in items:
            print(f'Заводится: {i["name"]}')
            time.sleep(1)
            if checkboxs['name']:
                paste(i['name'])
            pyautogui.press('enter')
            pyautogui.press('enter')
            if keyboard():
                print('Курсор не на количестве, нажимается ентер.')
                pyautogui.press('enter')
            if keyboard():
                print('Курсор не на количестве, нажимается вправо.')
                pyautogui.press('right')

            print('ТИП РАБОТАЕТ')
            if checkboxs['type']:
                if i['type'].lower() == "шт":
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
                                pyautogui.press('left')
                            pyautogui.press('1')
                            paste('0')
                            if keyboard():
                                pyautogui.press('enter')
                            paste('0')
                            if keyboard():
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
            if checkboxs['count']:
                paste(i['count'])
            pyautogui.press('enter')
            if checkboxs['cost']:
                paste(i['cost'])
            pyautogui.press('enter')

            pyautogui.press('left', presses=6)
            time.sleep(0.2)
            pyautogui.press('down')
            time.sleep(1)
    print('Автокликер закончил свою работу!')
