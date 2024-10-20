import time
import json

from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from os import listdir
from os.path import isfile, join

# !/usr/bin/env python # -* - coding: utf-8-* -
print("Кодировка uft-8 включена")

log = True

# !/usr/bin/env python # -* - coding: utf-8-* -
print("Кодировка uft-8 включена")

mnozitel_ozhidaniya = 6  # Множитель паузы ожидания на сайте


def cirkle(numb, lengue = 0):
    try:
        float(numb)
    except:
        print('Число не является дробным')
        return None

    numb = str(numb)
    right_numb = numb.split('.')[1]
    left_numb = numb.split('.')[0]

    while len(right_numb) > lengue:
        
        if int(right_numb[-1]) >= 5:
            add = 1
        else:
            add = 0

        if len(right_numb) > 2:
            right_numb = right_numb[:-1]
            new_last_numb = str(int(right_numb[-1]) + add)
            right_numb = right_numb[:-1]
            right_numb = right_numb + new_last_numb
        else:
            right_numb = ''
            new = int(left_numb) + add
            return new

    new = str(left_numb) + '.' + str(right_numb)
    return float(new)


def auth():
    browser = Chrome()  # Загрузка браузера

    if log: print('[parse_metro    ][auth]: ', str('Начало авторизации!'))
    url = "https://idam.metro-cc.ru/web/Signin?state=a22fc20c7a8f4cc29527582a9b69f480&scope=openid+clnt%3DBTEX&locale_id=ru-RU&redirect_uri=https%3A%2F%2Fmshop.metro-cc.ru%2Fshop%2Fportal%2Fmy-orders%2Fall%3FidamRedirect%3D1&client_id=BTEX&country_code=RU&realm_id=SSO_CUST_RU&user_type=CUST&DR-Trace-ID=idam-trace-id&code_challenge=X24I_T1kLXCRhV-o24wLBVRODgj9AULUni3HeJ_21G4&code_challenge_method=S256&response_type=code"

    browser.get(url)
    browser.execute_script("document.body.style.zoom='15%'")

    browser.find_element(By.ID, 'user_id').send_keys("bokova_shura@mail.ru")  # Ввод логина
    browser.find_element(By.ID, 'password').send_keys("Dlink1980!!!")  # Ввод пароля

    while True:
        try:
            browser.find_element(By.ID, 'submit').click()  # Нажатие кнопки "Войти
            break
        except:
            time.sleep(1)

    if log: print('[parse_metro    ][auth]: ', str('Успешная авторизация!'))

    while True:
        try:
            browser.find_element(By.XPATH,
                                 '/html/body/div[1]/div/div/div[2]/div[2]/div[3]/div[3]/div/div/div/div/div/div/div[1]/div/div').click()
            break
        except:
            time.sleep(1)
            browser.execute_script("document.body.style.zoom='15%'")

    if log: print('[parse_metro    ][auth]: ', str('Выбор адреса доставки выполнен!'))
    return browser


def get_check(num_check=1):
    check_number = 1 + num_check  # Последний в списке начинается с: 2
    url2 = 'https://mshop.metro-cc.ru/shop/portal/my-orders/all?itm_pm=cookie_consent_accept_button'

    browser = auth()

    while True:
        try:
            browser.get(url2)
            if log: print('[parse_metro    ][get_check]: ', str('Корзина открыта!'))
            break
        except:
            time.sleep(1)
            browser.execute_script("document.body.style.zoom='15%'")

    while True:
        try:
            browser.find_element(By.XPATH,
                                 f'/html/body/div[1]/div/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div[2]/div[2]/div[1]/div/div/div[{check_number}]/div/div[2]/a').click()
            break
        except:
            time.sleep(1)
            browser.execute_script("document.body.style.zoom='15%'")

    while True:
        try:
            browser.find_element(By.XPATH,
                                 '/html/body/div[1]/div/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div[2]/div/div/div[2]/div[3]')
            break
        except:
            time.sleep(1)
            browser.execute_script("document.body.style.zoom='15%'")

    soup = BeautifulSoup(browser.page_source, "html.parser")  # Парсинг готового html кода

    items = soup.findAll('div', class_='mfcss_card-article-2--container-grid')
    date_doc = soup.findAll('div', class_='ca-suborder-lc')

    date = ''
    items_date = BeautifulSoup(str(date_doc), "html.parser")
    date = \
    str(items_date).split('Дата доставки:</span>')[1].split('</span></div><div class="ca-suborder-lc__component">')[0]

    import re

    date = re.sub("[^0-9-:T/]", "", date)

    date = '.'.join(date.split('/'))
    items_dict = []

    id_item = 1
    for item in items:
        if item.find('div', class_='mfcss_card-article-2--title') is not None:
            item_data = BeautifulSoup(str(item), "html.parser")
            item_data_dict = []
            for data in item_data:
                for data2 in data:
                    for data3 in data2:
                        if data3 != '':
                            text = str(data3.text)
                            item_data_dict.append(text)
            item_end = {}

            import re
            if len(item_data_dict) > 5:
                item_end['id'] = id_item
                item_end['name'] = item_data_dict[1]
                if '/' in item_data_dict[4]:
                    item_end['count'] = re.sub("[^0-9,.]", "", item_data_dict[4].split(' / ')[0])
                    print('Разделение по черте')
                else:
                    item_end['count'] = re.sub("[^0-9,.]", "", item_data_dict[4].split(' ')[0])
                    print('Разделение по пробелу')

                try:
                    item_end['count'] = float(item_end['count'])
                    item_end['sum'] = float(re.sub("[^0-9,.]", "", item_data_dict[5].split('₽')[1]).replace(',', '.'))
                    item_end['cost'] = cirkle((item_end['sum'] / item_end['count']), 2) # Получение стоимости за шт, делением суммы на количество и Округление до двух знаков
                except:
                    item_end['sum'] = -1.00
                    item_end['cost'] = -1.00
                    item_end['count'] = -1.000

                item_end['type'] = re.sub("[^аА-яЯ]", "", item_data_dict[4])


            if item_data_dict != '' and item_end['count'] != 0:
                items_dict.append(item_end)
            id_item += 1

    header = {'date': date,
           'number': '',
           'shop': 'Метро'}
    doc = {'header': header, 'items': items_dict}
    return doc


def save_doc(check):
    if log: print('[save_doc    ][get_metro]: ' + str(check))

    numb = 1
    print(numb)
    while numb < 10:
        print(numb)
        temp_date = '-'.join(check['header']["date"].split("."))
        print(temp_date)
        name = f'{temp_date} - Метро({numb}).dc'
        print(name)

        onlyfiles = [f for f in listdir('documents') if isfile(join('documents', f))]
        print(onlyfiles)
        print(name)
        if name not in onlyfiles:
            print('Имени нет в папке')
            print(onlyfiles)
            with open(f'documents/{name}', 'w', encoding='utf-8') as fp:
                json.dump(check, fp)
            numb = 10
        numb += 1

def launch_parser(number_doc):
    try:
        numb_doc = number_doc
        print('numb_doc:')
        print(numb_doc)
        if "-" in numb_doc:
            numb_doc = numb_doc.split("-")
            int(numb_doc[0])
            int(numb_doc[1])
            more = True
            more_type = 0
        elif "," in numb_doc:
            numb_doc = numb_doc.split(",")
            for i in numb_doc:
                int(i)
            more_type = 1
        else:
            numb_doc = int(number_doc)
            more = False
    except:
        numb_doc = 1
        more = False
    try:
        if more:
            if more_type == '1':
                doc_ind = numb_doc
            else:
                doc_ind = range(int(numb_doc[0]), int(numb_doc[1]))

            for i in doc_ind:
                check = get_check(i)
                save_doc(check)
        else:
            check = get_check(int(numb_doc))
            save_doc(check)
    except:
        return True
    return True