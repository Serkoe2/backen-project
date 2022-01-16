import requests

#Документация https://yandex.ru/dev/oauth/doc/dg/concepts/about.html

class YandexAuth:
    def __init__(self):
        self.client_id = "3906c9adf6484f3fbbb3b3e302ec6e00"
        self.client_secret = "f0caf4830287423684a80e5cf40467bc"
        self.redirect_uri = "http://127.0.0.1:5000/auth_handler/yandex"
    
    #Формируем ссылку для браузера
    def get_auth_url(self):
        url = "https://oauth.yandex.ru/authorize?"
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "token",
            "display": "popup",
            "scope": "login:email",
        }
        return "{}client_id={}&redirect_uri={}&response_type={}&display={}&scope={}".format(url, *params.values())
    
    #Отправляем запрос для полчения инфо
    def get_info(self, code):
        url = "https://login.yandex.ru/info?"
        params = {
            "format": "json",
            "oauth_token": code
        }
        r = requests.get(url, params=params)
        if (r.status_code == 200):
            return r.json()
        else:
            return {"status": "False", "Message": "Auth Failed", "Yandex_say": r.text}

