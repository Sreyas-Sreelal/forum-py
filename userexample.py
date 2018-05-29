from forum.user import User
from forum.account import Account

name = input("Input forum username : ")
password = input("Input forum password : ")
a = Account(name,password)

id = input("Input user id ")
u = User(id)
info = u.info()

for i,j in info.items():
    print(i," : ",j)
print("User ",u.name," has reputation ",u.getreputation())
print("Last online : ",u.getlastactive(a))


