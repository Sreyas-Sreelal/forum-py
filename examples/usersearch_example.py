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