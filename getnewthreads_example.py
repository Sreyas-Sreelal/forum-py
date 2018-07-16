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

from forum.user import User
from forum.account import Account

name = input("Input forum username : ")
password = input("Input forum password : ")
a = Account(name,password)
max = input("Input max number of threads : ")
print("\t\t###New threads###\n")
for t in a.getnew(max):
    print("\t",t.title,"\t",t.author.name)


    