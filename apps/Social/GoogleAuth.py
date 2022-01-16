from dataclasses import dataclass
import re
from marshmallow.fields import Bool, Boolean, Dict
import requests
from apps.Schemas import RedirectUrl

class GoogleAuth:
    def __init__(self):
        self.client_id = "914784116149-1n6schebrign35pv5ik0jhukrikot1k9.apps.googleusercontent.com"
        self.client_secret = "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"
        self.redirect_uri = "http://localhost:5000/api/v1/social/handler/google"
        self.user_redirect_uri:RedirectUrl = self.set_auth_url()

    #Формируем ссылку для пользователя
    def set_auth_url(self)->RedirectUrl:
        """
        Возвращает ссылку на форму Google для авторизации
        """
        url = "https://accounts.google.com/o/oauth2/v2/auth"
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"
        }
        return "{}?client_id={}&redirect_uri={}&response_type={}&scope={}".format(url, *params.values())

    #Формируем ссылку для получения токена POST
    def get_token_url(self, code)-> Dict:
        url = 'https://accounts.google.com/o/oauth2/token'
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code",
            "code": code
        }
        r = requests.post(url, params=params)
        if (r.status_code == 200):
            return  r.json()
        else:
            return None

    #Получаем info Get
    def get_info(self, access_token, id_token):
        url = "https://www.googleapis.com/oauth2/v1/userinfo"
        params = {
            "access_token": access_token,
            "id_token": id_token,
            "token_type": "Bearer",
            "expires_in": 3599
        }
        r = requests.get(url, params=params)
        if (r.status_code == 200):
            return r.json()
