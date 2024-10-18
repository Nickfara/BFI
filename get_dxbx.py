link_auth = 'https://dxbx.ru/api/rest/v1/auth/login'



account_password = {"login": "nickfara@bk.ru", "password": "Paranormal1"}

def auth():

    import requests
    s = requests.Session()  # Создание сессии
    s.headers.update(
        {'User-Agent': 'okhttp/5.3.1'})  # Заголовок с данными

    response = s.post(link_auth, data = account_password)
    return response


response = auth()

print(response)

try:
    print(response.json())
except:
    print(response.reason)