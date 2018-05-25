class Thread:
    def __init__(self,client,id):
        self.id = id
        self.client = client
        self.client.get("http://forum.sa-mp.com/showthread.php?t=" + self.id)
        self.author = self.__getauthor()
        self.title = self.__gettitle()
        
    def __getauthor(self):
        from forum.user import User
        self.client.get("http://forum.sa-mp.com/showthread.php?t=" + self.id)
        return User(self.client,self.client.find_element_by_xpath("//*[contains(@class, 'bigusername')]").get_attribute('href')[36:])
    
    def __gettitle(self):
        self.client.get("http://forum.sa-mp.com/showthread.php?t=" + self.id)
        return self.client.find_element_by_tag_name('strong').text


    def getrating(self):
        try:
            self.client.get("http://forum.sa-mp.com/showthread.php?t=" + self.id)
            rating_info = self.client.find_element_by_xpath("//*[starts-with(@src, 'images/rating/rating_')]").get_attribute('title')
            rating = {}
            rating['NoOfVotes'] = rating_info[rating_info.find(':')+2:rating_info.find('v')-1]
            rating['Average'] = rating_info[rating_info.find(',')+2:rating_info.find('aver')-1]
            return rating
        except:
            return {'NoOfVotes':'0','Average':'0'}

    def getsubforum(self):
        sub_forums_elements = self.client.find_elements_by_xpath("//*[starts-with(@href, 'forumdisplay.php?f=')]")
        sub_forums = []
        for e in sub_forums_elements:
            sub_forums.append(e.text)
        return sub_forums
