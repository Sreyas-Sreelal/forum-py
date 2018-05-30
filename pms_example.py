from forum.user import User
from forum.account import Account

name = input("Input forum username : ")
password = input("Input forum password : ")
a = Account(name,password)
print(a.getpms())

