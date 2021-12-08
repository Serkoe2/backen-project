from app.Controller.Command import *
from app.Controller.Task import *
from app.Controller.User import *

class Controller:
    def __init__(self):
        self.Command = CommandController
        self.Task = TaskController
        self.User = UserController

controller = Controller()