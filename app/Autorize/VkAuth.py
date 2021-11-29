import requests

#Документация https://vk.com/dev/authcode_flow_user

class VkAuth:
    def __init__(self):
        self.client_id = "6183039"
        self.client_secret = "H9OuqkX31nsVuxqpTZAl"
        #self.client_secret = "6dfdc90a6dfdc90a6dfdc90add6da3917566dfd6dfdc90a33cef895a61e67cb30ed008a"
        self.redirect_uri = "http://127.0.0.1:5000/auth_handler/vk"
    
    #Формируем ссылку для браузера
    def get_auth_url(self):
        url = "https://oauth.vk.com/authorize"
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "display": "page",
            "state": "vk_auth_test",
            "scope": "email",
            "v":"5.131"
        }
        return "{}?client_id={}&redirect_uri={}&response_type={}&display={}&state={}&scope={}&v={}".format(url, *params.values())
    
    #Отправляем запрос для полчения инфо
    def get_info(self, code):
        url = "https://oauth.vk.com/access_token"
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "code": code
        }
        r = requests.get(url, params=params)
        if (r.status_code == 200):
            return r.json()
        else:
            return {"status": "False", "Message": "Auth Failed", "Vk_say": r.text}

