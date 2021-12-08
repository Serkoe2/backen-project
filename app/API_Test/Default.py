import requests
import json

class Deafult:
    url = "http://127.0.0.1:5000/"
    headers = {'Content-type': 'application/json'}
    
    @classmethod
    def default_test(cls, method, data) -> list:
        payload = json.dumps(data["request"])
        r = requests.post("{}/{}".format(cls.url, method), data = payload,  headers = cls.headers)
        try:
            response = json.loads(r.text)
        except:
            response = r.text
        if (data["response"] == response):
            return [True, "Response OK"]
        else:
            return [False, "Response not OK, Response must {}, but {} given".format(data["response"], response)]

