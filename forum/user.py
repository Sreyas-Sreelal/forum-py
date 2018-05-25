from bs4 import BeautifulSoup
import re

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

    def getforumlevel(self):
        self.client.get('http://forum.sa-mp.com/member.php?u=' + self.id)
        return self.client.find_element_by_tag_name('h2').text

    def getthreads(self):
        from forum.threads import Thread
        self.client.get('http://forum.sa-mp.com/search.php?do=finduser&u=' + self.id + '&starteronly=1')
        soup = BeautifulSoup(self.client.page_source,'html.parser')
        thread_elements = soup.find_all("a", id=re.compile("^thread_title_"))

        threads = []
        for te in thread_elements:
            try:
                #print("Debug : thread id : ",te.get_attribute('id')[13:])
                threads.append(Thread(self.client,te['id'][13:]))
            except:
                continue        
        return threads

    """def getreputation(self):
        self.client.get("http://forum.sa-mp.com/search.php?do=finduser&u=" + self.id )
        #post_element = self.client.
        pass
    """
    
    def info(self):
        self.client.get('http://forum.sa-mp.com/member.php?u=' + self.id)
        return self.client.find_element_by_xpath("//*[contains(@class, 'smallfont list_no_decoration profilefield_list')]").text
        
    
