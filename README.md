# forum-py
[![GitHub issues](https://img.shields.io/github/issues/Sreyas-Sreelal/forum-py.svg)]() [![GitHub pull requests](https://img.shields.io/github/issues-pr-raw/sreyas-sreelal/forum-py.svg)]() [![GitHub pull license](https://img.shields.io/github/license/sreyas-sreelal/forum-py.svg)]()
>forumpy is an unofficial SA-MP forum api.This python library ,integerated with selenium and phantomJS,helps you to automate SA-MP forum acitivities like send and get pms,threads,userinfo,contacts etc.Please view the example files for information about using these features in your python application.forumpy is still under development and has not yet been released.

## Quick examples
* ###  Basic 
  ```Python
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
  ```
* ### Send and Get private messages
  ```Python
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
  ```

`Please view examples files for more examples`

## Requirements
* Python 3.5+
* `Selenium` library
* `PhantomJS` headless web driver
* `BeautifulSoup` library