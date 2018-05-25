import forum.ext.errors
from forum.user import User

class Account:
    def __init__(self,client,name,password):
        self.client = client
        if not self.__login(name,password):
            self.loggined = False
            raise forum.ext.errors.InvalidCreditinals("Couldn't login")

        else:
            self.User = User(self.client,self.id)
            self.name = name
            self.loggined = True
        
    def __login(self,name,password):
        try:
            input_username = self.client.find_element_by_id("navbar_username")
            input_password = self.client.find_element_by_id("navbar_password")
            check_remember = self.client.find_element_by_id("cb_cookieuser_navbar")
            input_username.send_keys(name)
            input_password.send_keys(password)
            check_remember.click()
            self.client.find_element_by_class_name("button").click()
            self.client.get("http://forum.sa-mp.com")
            self.id = self.client.find_element_by_xpath("//*[starts-with(@href, 'member.php?u=')]").get_attribute('href')[36:]
            return True
        except:
            return False
    