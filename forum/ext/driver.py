from selenium import webdriver
from selenium import common
from forum.ext.errors import DriverLoadError

try:
    client = webdriver.PhantomJS()
    client.get("http://forum.sa-mp.com")

except common.exceptions.WebDriverException:
    raise DriverLoadError("Selenium driver is not found")

    
