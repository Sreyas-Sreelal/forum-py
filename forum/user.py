from bs4 import BeautifulSoup
import re
import requests

class User:
    def __init__(self,id):
        self.id = id
        self.name = self.__getusername()
        
    def __getusername(self):
        request = requests.get('http://forum.sa-mp.com/member.php?u=' + self.id)
        soup = BeautifulSoup(request.content,'html.parser')
        return str(soup.find('h1').text)
        #return self.client.find_element_by_tag_name('h1').text

    def getlastactive(self):
        request = requests.get('http://forum.sa-mp.com/member.php?u=' + self.id)
        soup = BeautifulSoup(request.content,'html.parser')
        return soup.find('div',id='last_online').text
        #self.client.find_element_by_id('last_online').text 

    def getforumlevel(self):
        request = requests.get('http://forum.sa-mp.com/member.php?u=' + self.id)
        soup = BeautifulSoup(request.content,'html.parser')
        return soup.find('h2').text
        #return self.client.find_element_by_tag_name('h2').text

    def getthreads(self):
        from forum.threads import Thread
        request = requests.get('http://forum.sa-mp.com/search.php?do=finduser&u=' + self.id + '&starteronly=1')
        soup = BeautifulSoup(request.content,'html.parser')
        thread_elements = soup.find_all("a", id=re.compile("^thread_title_"))

        threads = []
        for te in thread_elements:
            try:
                #print("Debug : thread id : ",te.get_attribute('id')[13:])
                threads.append(Thread(te['id'][13:]))
            except:
                continue        
        return threads

    """def getreputation(self):
        request = requests.get("http://forum.sa-mp.com/search.php?do=finduser&u=" + self.id )
        #post_element = self.client.
        pass
    """
    
    def info(self):
        request = requests.get('http://forum.sa-mp.com/member.php?u=' + self.id)
        soup = BeautifulSoup(request.content,'html.parser')
        data = soup.find('dl',{'class':'smallfont list_no_decoration profilefield_list'}).text.split('\n')
        data = list(filter(('').__ne__, data))
        length = len(data)
        info = {}
        for i in range(0,length,2):
            info[data[i]] = data[i+1]
        return info
        
    
