from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
import time


#!/usr/bin/env python # -* - coding: utf-8-* -
print ("Кодировка uft-8 включена")

mnozitel_ozhidaniya = 1 # Множитель паузы ожидания на сайте

def auth():
    browser = Chrome()  # Загрузка браузера

    url = "https://idam.metro-cc.ru/web/Signin?state=a22fc20c7a8f4cc29527582a9b69f480&scope=openid+clnt%3DBTEX&locale_id=ru-RU&redirect_uri=https%3A%2F%2Fmshop.metro-cc.ru%2Fshop%2Fportal%2Fmy-orders%2Fall%3FidamRedirect%3D1&client_id=BTEX&country_code=RU&realm_id=SSO_CUST_RU&user_type=CUST&DR-Trace-ID=idam-trace-id&code_challenge=X24I_T1kLXCRhV-o24wLBVRODgj9AULUni3HeJ_21G4&code_challenge_method=S256&response_type=code"


    browser.get(url)

    browser.find_element(By.ID, 'user_id').send_keys("bokova_shura@mail.ru")  # Ввод логина
    browser.find_element(By.ID, 'password').send_keys("Dlink1980!!!")  # Ввод пароля
    browser.find_element(By.ID, 'submit').click()  # Нажатие кнопки "Войти"
    time.sleep(8*mnozitel_ozhidaniya)

    browser.find_element(By.XPATH,
                         '/html/body/div[1]/div/div/div[2]/div[2]/div[3]/div[3]/div/div/div/div/div/div/div[1]/div/div').click()
    time.sleep(3*mnozitel_ozhidaniya)
    return browser


def get_check(num_check=1):
    check_number = 1 + num_check  # Последний в списке начинается с: 2
    url2 = 'https://mshop.metro-cc.ru/shop/portal/my-orders/all?itm_pm=cookie_consent_accept_button'
    browser = auth()

    browser.get(url2)
    time.sleep(3*mnozitel_ozhidaniya)
    browser.find_element(By.XPATH, f'/html/body/div[1]/div/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div[2]/div[2]/div[1]/div/div/div[{check_number}]/div/div[2]/a').click()
    time.sleep(3*mnozitel_ozhidaniya)
    browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div[2]/div/div/div[2]/div[3]')



    soup = BeautifulSoup(browser.page_source, "html.parser") # Парсинг готового html кода

    items = soup.findAll('div', class_='mfcss_card-article-2--container-grid')
    date_doc = soup.findAll('div', class_='ca-suborder-lc')

    date = ''
    items_date = BeautifulSoup(str(date_doc), "html.parser")
    date = str(items_date).split('Дата доставки:</span>')[1].split('</span></div><div class="ca-suborder-lc__component">')[0]

    import re
    date = re.sub("[^0-9-:T]", "", date)
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
                item_end['cost'] = re.sub("[^0-9,.]", "", item_data_dict[3])
                item_end['count'] = re.sub("[^0-9,.]", "", item_data_dict[4])
                item_end['sum'] = re.sub("[^0-9,.]", "", item_data_dict[5].split('₽')[1])

            if item_data_dict != '':
                items_dict.append(item_end)
            id_item += 1

    doc = {'dateTime': '-'.join(date.split('/')) + 'T09:00',
           'requestNumber': 'Неизвестно (Временно)',
           'items': items_dict
           }
    return doc

get_check(num_check=1)