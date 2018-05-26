from forum.user import User
id = input("Input user id ")
u = User(id)
print("User ",u.name," has reputation ",u.getreputation())