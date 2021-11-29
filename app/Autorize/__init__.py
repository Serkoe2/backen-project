from .GoogleAuth import GoogleAuth
from .VkAuth import VkAuth
from .YandexAuth import YandexAuth

class Autorize:
    def __init__(self):
        self.Google = GoogleAuth()
        self.Vk = VkAuth()
        self.Yandex = YandexAuth()

authorizer = Autorize()
