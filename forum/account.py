import forum.ext.errors
from bs4 import BeautifulSoup
import re
from selenium.common.exceptions import WebDriverException

class Account:
    def __init__(self,name,password):
        from forum.ext.driver import client
        self.client = client
        if not self.__login(name,password):
            self.loggined = False
            raise forum.ext.errors.InvalidCreditinals("Couldn't login")

        else:
            from forum.user import User
            self.User = User(self.id)
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
            soup = BeautifulSoup(self.client.page_source,'html.parser')
            islimit = soup.find('b',text=re.compile('You have used up your failed login quota!'))

            if islimit is not None:
                raise forum.ext.errors.MaxLoginLimit
            
            try:    
                self.client.get("http://forum.sa-mp.com")
                check = self.client.find_element_by_id("navbar_username")
            except:
                check = None

            if check is not None:
                return False

            soup = BeautifulSoup(self.client.page_source,'html.parser')
            self.id = soup.find('a',href=re.compile('member\.php\?u='))['href'][13:]
            return True
        
        except WebDriverException:
            return False

    def getcontacts(self):
        from forum.user import User
        contacts = []
        self.client.get('http://forum.sa-mp.com/profile.php?do=buddylist')
        soup = BeautifulSoup(self.client.page_source,'html.parser')
        elements = soup.find_all('a',{"title":"View Profile"})
        #elements = self.client.find_elements_by_xpath("//*[starts-with(@href, 'member.php?u=') and contains(@title,'View Profile')]")
        for element in elements:
            contacts.append(User(element['href'][13:]))
        return contacts

    def getIdFromUserName(self,username):
        #http://forum.sa-mp.com/memberlist.php?ltr=S&pp=10000&sort=username&order=asc&ausername=SyS
        self.client.get("http://forum.sa-mp.com/memberlist.php?ltr="+username[0]+"&pp=10000&sort=username&order=asc&ausername="+username)
        soup = BeautifulSoup(self.client.page_source,'html.parser')
        
        try:
            ausername_element = soup.find('td',{'class':'alt1Active'}).find('a')
            ausername = ausername_element.text.strip()
            
            if ausername.lower() != username.lower():
                while True:
                    try:
                        ausername_element = ausername_element.find_next('td',{'class':'alt1Active'}).find('a')
                        ausername = ausername_element.text.strip()
                        if ausername.lower() != username.lower():
                            continue
                        else:
                            break
                    except Exception as e:
                        print(str(e))
                        raise forum.ext.errors.InvalidUserId
        
        except:
            raise forum.ext.errors.InvalidUserId
        
        user_link = ausername_element['href']
        userid = user_link[user_link.find("=")+1:].strip()
        
        return userid


