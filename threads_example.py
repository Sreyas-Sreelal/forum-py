from forum.threads import Thread

t = Thread(input("Input thread id : "))
print("*****Content*****\n",t.getcontent())
print("Author: ",t.author.name)
print("******Posts******\n")
for posts in t.getposts():
    print(posts)
