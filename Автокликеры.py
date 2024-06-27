import pyautogui
import time
import pyperclip

def site():
    def start():
        for i in range(0, 3):
            pyautogui.hotkey('ctrl', 'c')

            time.sleep(1.5)
            pyautogui.press('right')
            time.sleep(1)

            pyautogui.hotkey('alt', 'tab')
            time.sleep(2.5)

            pyautogui.hotkey('ctrl', 'v')
            time.sleep(2.5)
            pyautogui.hotkey('ctrl', 'z')
            time.sleep(1)
            pyautogui.press('right')
            time.sleep(1)

            pyautogui.hotkey('alt', 'tab')
            time.sleep(2.5)

        pyautogui.press('left', presses=3)
        pyautogui.press('down')
        time.sleep(1)

        pyautogui.hotkey('alt', 'tab')
        time.sleep(2)

        pyautogui.press('left', presses=3)
        pyautogui.press('down')
        time.sleep(1)

        pyautogui.hotkey('alt', 'tab')
        time.sleep(2)


    time.sleep(10)
    for i in range(0, 16):
        start()

def test():
    from openpyxl import load_workbook
    worksheet = load_workbook('documents/qnnrwfzw6809.xlsx')
    stroka = worksheet.active[f'A2'].value
    print(stroka)

test()






