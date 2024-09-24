from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
import time


def get_check(num_check=1):
    browser = Chrome() # Загрузка браузера
    last_checkssss = '/html/body/div[1]/div/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div[2]/div[2]/div[1]/div/div/div[3]/div/div[2]/a'
    pre_last_check = '/html/body/div[1]/div/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div[2]/div[2]/div[1]/div/div/div[2]/div/div[2]/a'
    check_number = 1 + num_check  # Последний в списке начинается с: 2

    url = "https://idam.metro-cc.ru/web/Signin?state=a22fc20c7a8f4cc29527582a9b69f480&scope=openid+clnt%3DBTEX&locale_id=ru-RU&redirect_uri=https%3A%2F%2Fmshop.metro-cc.ru%2Fshop%2Fportal%2Fmy-orders%2Fall%3FidamRedirect%3D1&client_id=BTEX&country_code=RU&realm_id=SSO_CUST_RU&user_type=CUST&DR-Trace-ID=idam-trace-id&code_challenge=X24I_T1kLXCRhV-o24wLBVRODgj9AULUni3HeJ_21G4&code_challenge_method=S256&response_type=code"
    url2 = 'https://mshop.metro-cc.ru/shop/portal/my-orders/all?itm_pm=cookie_consent_accept_button'

    browser.get(url)

    browser.find_element(By.ID, 'user_id').send_keys("bokova_shura@mail.ru") # Ввод логина
    browser.find_element(By.ID, 'password').send_keys("Dlink1980!!!") # Ввод пароля
    browser.find_element(By.ID ,'submit').click() # Нажатие кнопки "Войти"
    time.sleep(25)

    browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[2]/div[3]/div[3]/div/div/div/div/div/div/div[1]/div/div').click()
    time.sleep(16)

    browser.get(url2)
    time.sleep(16)
    browser.find_element(By.XPATH, f'/html/body/div[1]/div/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div[2]/div[2]/div[1]/div/div/div[{check_number}]/div/div[2]/a').click()
    time.sleep(16)
    browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[2]/div[3]/div[3]/div/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div[2]/div/div/div[2]/div[3]')

    soup = BeautifulSoup(browser.page_source, "html.parser") # Парсинг готового html кода
    items = soup.findAll('div', class_='mfcss_card-article-2--container-grid')
    items_dict = []

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

            if len(item_data_dict) > 5:
                item_end['name'] = item_data_dict[1]
                item_end['cost'] = item_data_dict[3]
                item_end['count'] = item_data_dict[4]
                item_end['price'] = item_data_dict[5]

            if item_data_dict != '':
                items_dict.append(item_end)

    return items_dict