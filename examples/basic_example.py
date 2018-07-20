# -*- coding: utf-8 -*-
"""
Copyright (C) 2018  Sreyas Sreelal

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

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



