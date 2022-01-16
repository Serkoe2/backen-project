from .GoogleAuth import GoogleAuth
from .VkAuth import VkAuth
from .YandexAuth import YandexAuth

class Autorize:
    def __init__(self):
        """
        Модуль объектов авторизации

        Google

        Yandex

        *Github*
        """
        self.Google = GoogleAuth()
        self.Yandex = YandexAuth()