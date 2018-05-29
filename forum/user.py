from bs4 import BeautifulSoup
import re
import requests
import forum.ext.errors

class User:
    def __init__(self,id):
        self.id = id
        self.name = self.__getusername()
        
    def __getusername(self):
        request = requests.get('http://forum.sa-mp.com/member.php?u=' + self.id)
        soup = BeautifulSoup(request.content,'html.parser')
        return str(soup.find('h1').text.strip())

    def getlastactive(self,account):
        if not account.loggined:
            raise forum.ext.errors.MustLogin

        account.client.get('http://forum.sa-mp.com/member.php?u=' + self.id)
        soup = BeautifulSoup(account.client.page_source,'html.parser')
        last_online =  soup.find('div',id='last_online').text.strip()
        last_online = last_online[last_online.find(': ')+2:].strip()
        last_online_dict = {}
        last_online_dict['Date'] = last_online[:last_online.find(' ')]
        last_online_dict['Time'] = last_online[last_online.find(' ')+2:]

        return last_online_dict

    def getforumlevel(self):
        request = requests.get('http://forum.sa-mp.com/member.php?u=' + self.id)
        soup = BeautifulSoup(request.content,'html.parser')
        return soup.find('h2').text

    def getthreads(self):
        from forum.threads import Thread
        request = requests.get('http://forum.sa-mp.com/search.php?do=finduser&u=' + self.id + '&starteronly=1')
        soup = BeautifulSoup(request.content,'html.parser')
        thread_elements = soup.find_all("a", id=re.compile("^thread_title_"))

        threads = []
        for te in thread_elements:
            try:
                threads.append(Thread(te['id'][13:]))
            except:
                continue        
        return threads

    def getreputation(self):
        try:
            request = requests.get("http://forum.sa-mp.com/search.php?do=finduser&u=" + self.id )
            soup = BeautifulSoup(request.content,'html.parser')
            post = soup.find('a',href=re.compile('^showthread\.php\?p='))['href']
            request = requests.get("http://forum.sa-mp.com/"+post)
            soup = BeautifulSoup(request.content,'html.parser')
            scrap_soup = soup.find('a',href=re.compile('u='+self.id)).find_next('div',{'class':'smallfont'}).find_next('div',{'class':'smallfont'}).find_next('div',{'class':'smallfont'}) 
            scrap_info = scrap_soup.text
            reputation = int(scrap_info[scrap_info.rfind('Reputation:')+12:].strip())
        except:
            try:
                scrap_info = scrap_soup.find_next('div',{'class':'smallfont'}).text
                reputation = int(scrap_info[scrap_info.rfind('Reputation:')+12:].strip())
            except:
                reputation = 0
        return reputation
        
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
        
    
