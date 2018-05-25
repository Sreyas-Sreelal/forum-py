from bs4 import BeautifulSoup

class User:
    
    def __init__(self,client,id):
        self.client = client
        self.id = id
        self.name = self.__getusername()
        
    def __getusername(self):
        self.client.get('http://forum.sa-mp.com/member.php?u=' + self.id)
        return self.client.find_element_by_tag_name('h1').text

    def getlastactive(self):
        self.client.get('http://forum.sa-mp.com/member.php?u=' + self.id)
        return self.client.find_element_by_id('last_online').text 

    def getcontacts(self):
        contacts = []
        self.client.get('http://forum.sa-mp.com/profile.php?do=buddylist')
        soup = BeautifulSoup(self.client.page_source,'html.parser')
        elements = soup.find_all('a',{"title":"View Profile"})
        #elements = self.client.find_elements_by_xpath("//*[starts-with(@href, 'member.php?u=') and contains(@title,'View Profile')]")
        for element in elements:
            contacts.append(User(self.client,element['href'][13:]))
        return contacts

    def getforumlevel(self):
        self.client.get('http://forum.sa-mp.com/member.php?u=' + self.id)
        return self.client.find_element_by_tag_name('h2').text

    def getthreads(self):
        #NOTE:need to work
        self.client.get('http://forum.sa-mp.com/search.php?do=finduser&u=' + self.id + '&starteronly=1')
        pass

    def getreputation(self):
        
        pass

    def postcounts(self):
        pass

    def joined(self):
        pass
    
