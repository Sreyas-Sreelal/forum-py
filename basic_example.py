from forum.account import Account

name = input("Input your forum user name : ")
password = input("Input your forum password : ")
a = Account(name,password)
print("Logined with user id : ",a.id)
print("\t**Account info**\n",a.User.info())

print("\n\t***Contacts***\n")
print("\tId\tUsername")

for i in a.getcontacts():
    print("\t",i.id,"\t",i.name)

print("\n\t***Threads***\n")
print("\tTitle\tRatings\tAuthor")

for i in a.User.getthreads():
    print(i.title,"\t",i.getrating(),"\t",i.author.name)



