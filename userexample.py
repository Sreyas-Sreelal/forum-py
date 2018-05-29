from forum.user import User
from forum.account import Account

name = input("Input forum username : ")
password = input("Input forum password : ")
a = Account(name,password)

id = input("Input user id : ")
u = User(id)
info = u.info()

print("Name : ",u.name)
print("Forum level : ",u.getforumlevel())
for i,j in info.items():
    print(i," : ",j)
print("Reputation : ",u.getreputation())
print("Last online : ",u.getlastactive(a))


