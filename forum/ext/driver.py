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
from selenium.webdriver.support import expected_conditions  
from selenium.webdriver.support.ui import WebDriverWait
from forum.ext.errors import DriverLoadError

try:
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')
    client = webdriver.Chrome(chrome_options=options)
    wait = WebDriverWait(client,10)
    client.get("http://forum.sa-mp.com")
    wait.until(expected_conditions.title_is('SA-MP Forums - Powered by vBulletin'))

except common.exceptions.TimeoutException:
    raise TimeoutError('Connection to forum is timed out')
except common.exceptions.WebDriverException:
    raise DriverLoadError("[Driver is not found] Chrome driver needs to be in PATH")

    
