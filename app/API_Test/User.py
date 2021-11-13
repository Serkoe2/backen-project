from app.API_Test.Default import Deafult
from app.Controller import controller
from app.Models import *
from app.API_Test.datasets import *

class UserAPI(Deafult):
    method = "/api/v1/user/"
    @classmethod
    def test(cls):
        msg = ""
        for i in range(0, len(test_new)):
            msg += "Test {}\n".format(i)
            msg += cls.test_new(test_new [i])
        return msg

    @classmethod
    def test_new(cls, data):
        if  "SaveTestUser" in data:
            SaveTestUser = data["SaveTestUser"]
        else:
            SaveTestUser = False
        result = cls.default_test("{}new".format(cls.method), data)
        request_msg = result[1]
        # Проверить есть ли такой пользователь в БД
        u = controller.User.find(data["request"])
        if (u):
            db_msg = "User was created"
            if not SaveTestUser:
                controller.User.delete_user(u)
                db_msg += "\nUser was delete"
        else:
            db_msg = "User wasn't created"
        msg = "{}\n{}\n".format(request_msg, db_msg)
        print(msg)
        return msg

