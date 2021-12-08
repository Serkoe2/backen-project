# Приложение создает команду GetOffer из 4х участников и наполняет ее 2 вакансиями
from random import choice
from app.Models import *

data = [ 
    ["Сергей Тимошенков", "s.timoshenkov@get-offer.com", "dmiq!e299"],
    ["Ринат Девитяров","r.devityrov@get-offer.com","d9ej1,2909"],
    ["Евгений Сажин","e.sazshin@get-offer.com"," d2ejs 19((dnq2"],
    ["Руслан Денисламов","r.denislamov@get-offer.com","9djaf7493**"]
]

users = []
# Создание аккаунтов
for i in data:
    u = User()
    u.name, u.surname = i[0].split(' ')
    u.email = i[1]
    users.append(u)
    db.session.add(u)
    print(u)
    print(u.name)
db.session.commit()

# Создание команды
command = Command()
command.name = "GetOffer"
command.description = "Rule"
command_slug = "getoffer"
command.owner = choice(users).id
db.session.add(command)
db.session.commit()

for i in users:
    cua = Command_User_Assigment()
    cua.command_id = command.id
    cua.user_id = i.id
    db.session.add(cua)

db.session.commit()