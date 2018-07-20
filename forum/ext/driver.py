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

from selenium import webdriver
from selenium import common
from forum.ext.errors import DriverLoadError

try:
    client = webdriver.PhantomJS()
    client.get("http://forum.sa-mp.com")

except common.exceptions.WebDriverException:
    raise DriverLoadError("Selenium driver is not found [PhantomJs needs to be in PATH]")

    
