from bs4 import BeautifulSoup
import re

class Thread:
    def __init__(self,client,id):
        self.id = id
        self.client = client
        self.author = self.__getauthor()
        self.title = self.__gettitle()
        
    def __getauthor(self):
        from forum.user import User
        self.client.get("http://forum.sa-mp.com/showthread.php?t=" + self.id)
        soup = BeautifulSoup(self.client.page_source,'html.parser')
        #self.client.find_element_by_xpath("//*[contains(@class, 'bigusername')]").get_attribute('href')[36:]
        return User(self.client,soup.find('a',{'class':'bigusername'})['href'][13:])
    
    def __gettitle(self):
        self.client.get("http://forum.sa-mp.com/showthread.php?t=" + self.id)
        soup = BeautifulSoup(self.client.page_source,'html.parser')
        return soup.find('strong').text

    def getrating(self):
        try:
            self.client.get("http://forum.sa-mp.com/showthread.php?t=" + self.id)
            soup = BeautifulSoup(self.client.page_source,'html.parser')
            rating_info = soup.find('img',src=re.compile('images/rating/'))['title']
            #rating_info = self.client.find_element_by_xpath("//*[starts-with(@src, 'images/rating/rating_')]").get_attribute('title')
            rating = {}
            rating['NoOfVotes'] = rating_info[rating_info.find(':')+2:rating_info.find('v')-1]
            rating['Average'] = rating_info[rating_info.find(',')+2:rating_info.find('aver')-1]
            return rating
        except:
            return {'NoOfVotes':'0','Average':'0'}

    def getsubforum(self):
        self.client.get("http://forum.sa-mp.com/showthread.php?t=" + self.id)
        soup = BeautifulSoup(self.client.page_source,'html.parser')
        sub_forums_elements = soup.find_all('a',href=re.compile('forumdisplay\.php\?f='))
        #sub_forums_elements = self.client.find_elements_by_xpath("//*[starts-with(@href, 'forumdisplay.php?f=')]")
        sub_forums = []
        for e in sub_forums_elements:
            sub_forums.append(e.text)
        return sub_forums
