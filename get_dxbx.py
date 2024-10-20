import time

from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

log = True

# !/usr/bin/env python # -* - coding: utf-8-* -
print("Кодировка uft-8 включена")

account_password = {"login": "nickfara@bk.ru", "password": "Paranormal1"}


def cirkle(numb, lengue=0):
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

    if log: print('[parse_dxbx    ][auth]: ', str('Начало авторизации!'))
    url = "https://dxbx.ru/fe/login"

    browser.get(url)

    while True:
        try:
            browser.find_element(By.ID, 'loginForm_login').send_keys(account_password['login'])  # Ввод логина
            browser.find_element(By.ID, 'loginForm_password').send_keys(account_password['password'])  # Ввод пароля
            break
        except:
            time.sleep(1)

    while True:
        try:
            browser.find_element(By.XPATH, '/html/body/div[1]/section/section/main/div/div[1]/form/button').click()  # Нажатие кнопки "Войти
            break
        except:
            time.sleep(1)

    if log: print('[parse_dxbx    ][auth]: ', str('Успешная авторизация!'))
    return browser


def get_check(num_check=2):
    check_number = 1 + num_check  # Последний в списке начинается с: 2
    url2 = 'https://dxbx.ru/index#app/list/invoice'

    header = ''

    browser = auth()

    while True:
        try:
            browser.find_element(By.XPATH,
                                 f'/html/body/div[4]/div[2]/div/div/div[1]/div/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/table/tbody/tr[{num_check}]').click()
            break
        except:
            time.sleep(1)

    while True:
        try:
            header = browser.find_element(By.XPATH,
                                 '/html/body/div[4]/div[2]/div/div/div[1]/div[1]/h1').text

            header = {
                'date': header.split(' ')[4],
                'number': header.split(' ')[2],
                'shop': header.split('поставщик: ')[1].split(' (')[0]
            }
            break
        except:
            time.sleep(1)

    while True:
        try:
            browser.find_element(By.XPATH,
                                 '/html/body/div[4]/div[2]/div/div/div[1]/div[2]/div/div[1]/ul/li[2]').click()
            break
        except:
            time.sleep(1)


    soup = BeautifulSoup(browser.page_source, "html.parser")  # Парсинг готового html кода

    items = soup.findAll('tr', class_='nomenclature-row box')

    items_dict = []
    number = 0
    for item in items:
        number += 1
        elements = item.find_all()
        element_dict = {}
        element_dict['id'] = number
        for element in elements:
            if '">\n<div class="nomenclature-block">\n</div>' in str(element):
                element = str(element).split('<div class="nomenclature-block">\n</div>\n                        ')
                element = str(element[1]).split('\n                    </td>')[0]
                print(header['shop'])
                if header['shop'] == 'ООО ТД Матушка':
                    element = element.split(' (ER-')[0]
                elif header['shop'] == 'ИП Касумов М.А.':
                    element = element.split(' (100.')[0]
                element_dict['name'] = element
            elif '<td class="price number">' in str(element):
                element = str(element).split('<td class="price number">\n                        ')[1]
                element = element.split('\n                    <div class="priceControl-block accept" in')[0]
                element_dict['cost'] = float(element)
            elif '<td class="number beforeReceivedCount" style="display: none;">' in str(element):
                element = str(element).split('<td class="number beforeReceivedCount" style="display: none;">\n                    ')[1]
                element = element.split('\n                    </td>')[0]
                element_dict['count'] = float(element)
            elif '<td>' in str(element):
                element = str(element).split('<td>')[1]
                element = element.split('</td>')[0]
                element_dict['type'] = element

        items_dict.append(element_dict)

    items_dict_filtered = []
    items_dict_names = {}
    items_dict_ids = []
    for i in items_dict:
        if i['name'] not in items_dict_names:
            items_dict_filtered.append(i)
            items_dict_names[i['name']] = i['id']
        else:
            items_dict_ids.append((items_dict_names[i['name']], i['id']))

    for i in items_dict_ids:
        print(i)
        items_dict_filtered[i[0]-1]['count'] += items_dict[i[1]-1]['count']
    print(items_dict_ids)

    doc = {'header': header, 'items': items_dict_filtered}
    return doc

items = get_check()
for i in items:
    print(items[i])
    pass