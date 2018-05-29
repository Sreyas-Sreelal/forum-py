from forum.account import Account
from forum.ext.errors import InvalidUserId
from forum.user import User

name = input("Input your forum user name : ")
password = input("Input your forum password : ")
a = Account(name,password)

while True:
    try:    
        name2search = input("Input name of user : ")
        id = a.getIdFromUserName(name2search)
        print("\n\nUser id is : ",id)
        u = User(id)
        info = u.info()

        print("Name : ",u.name)
        print("Forum level : ",u.getforumlevel())
        for i,j in info.items():
            print(i," : ",j)
        print("Reputation : ",u.getreputation())
        print("Last online : ",u.getlastactive(a))

    except InvalidUserId:
        print("Invalid user name")

    if input("Search more? (y/n)").lower() == "n":
        break