from forum.user import User
from forum.account import Account

name = input("Input forum username : ")
password = input("Input forum password : ")
a = Account(name,password)
max = input("Input max number of threads : ")
print("\t\t###New threads###\n")
for t in a.getnew(max):
    print("\t",t.title,"\t",t.author.name)