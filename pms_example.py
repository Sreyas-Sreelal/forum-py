from forum.user import User
from forum.account import Account

name = input("Input forum username : ")
password = input("Input forum password : ")
a = Account(name,password)
print(a.getpms())

rec_names = input("Input name of recipents (seperated by space) : ").split(" ")

users = []
for rec_name in rec_names:
    users.append(User(a.getIdFromUserName(rec_name)))
title = input("Input title : ")
content = input("Input content : ")
a.send_pm(users,title,content)


