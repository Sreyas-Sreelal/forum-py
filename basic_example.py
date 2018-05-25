from forum.ext.driver import client

from forum.account import Account

name = input("Input your forum user name : ")
password = input("Input your forum password : ")

a = Account(client,name,password)
print("\t***Contacts***\n")
print("\tId\tUsername")

for i in a.User.getcontacts():
    print("\t"+i.id+"\t"+i.name)
