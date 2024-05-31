import pyautogui as ac
import time
import pyperclip

data = []


def copy():
    ac.hotkey('ctrl', 'a')
    ac.hotkey('ctrl', 'c')
    key = pyperclip.paste()
    print('Текст скопирован:')
    print(key)
    return key


def start():
    ac.scroll(-500)
    time.sleep(1)
    ac.doubleClick()
    time.sleep(10)
    name = copy()
    name_normal = name.capitalize()
    pyperclip.copy(name_normal)
    time.sleep(1)
    if name not in data:
        ac.hotkey('ctrl', 'v')
        time.sleep(1)
        ac.hotkey('ctrl', 's')
        time.sleep(5)
    return name


time.sleep(5)
for i in range(0, 8):
    name = start()
    if name in data:
        print(name)
        print(data)

        print('Произошла ошибка и товар определённо использовался уже скопированный')
        break
    data.append(name)









