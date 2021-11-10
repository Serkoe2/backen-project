import requests

class GoogleAuth:
    def __init__(self, test = False):
        self.client_id = "914784116149-1n6schebrign35pv5ik0jhukrikot1k9.apps.googleusercontent.com"
        self.client_secret = "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"
        self.redirect_uri = "http://localhost:5000/test"
        self.test = test

    #Формируем ссылку для пользователя
    def get_auth_url(self):
        url = "https://accounts.google.com/o/oauth2/v2/auth"
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"
        }
        if (self.test):
            print("{}?client_id={}&redirect_uri={}&response_type={}&scope={}".format(url, *params.values()))
        return "{}?client_id={}&redirect_uri={}&response_type={}&scope={}".format(url, *params.values())
        

    #Формируем ссылку для получения токена POST
    def get_token_url(self, code):
        url = 'https://accounts.google.com/o/oauth2/token'
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code",
            "code": code
        }
        if (self.test):
            print("{}?client_id={}&client_secret={}&redirect_uri={}&grant_type={}&code={}".format(url, *params.values()))
        r = requests.post(url, params=params)
        if (r.status_code == 200):
            return r.json()

    #Получаем info Get
    def get_info_url(self, access_token, id_token):
        url = "https://www.googleapis.com/oauth2/v1/userinfo"
        params = {
            "access_token": access_token,
            "id_token": id_token,
            "token_type": "Bearer",
            "expires_in": 3599
        }
        if (self.test):
            print("{}?access_token={}&id_token={}&token_type={}&expires_in={}".format(url, *params.values()))
        r = requests.get(url, params=params)
        if (r.status_code == 200):
            return r.json()

    def menu(self):
        while True:
            print("1. Get url for Auth\n2. Get url for Token\n3. Get Info url\n0. Exit")
            ch = input()
            if (ch == '1'):
                self.get_auth_url()
            elif (ch == '2'):
                self.get_token_url(input("type your code\n"))
            elif (ch == '3'):
                self.get_info_url(input("type your access token:\n"),
                    input("type your id token:\n") )
            elif (ch == '0'):
                exit(0)

if __name__ == '__main__':
    test = GoogleAuth()
    test.menu(True)