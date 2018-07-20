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

from bs4 import BeautifulSoup
import re
import requests
from selenium.common.exceptions import WebDriverException
import forum.ext.errors

class Thread:
    """Represents a SA-MP forum thread.
        Example to create object: 
            ``t = Thread(samp_forum_thread_id)``
            returns a Thread object with attributes id,author and title initialised
    """
    def __init__(self,id):
        self.id = id
        self.author = self.__getauthor()
        self.title = self.__gettitle()
    
    #internals    
    
    def __getauthor(self):
        """Retrives current thread's author """
        try:
            request = requests.get("http://forum.sa-mp.com/showthread.php?t=" + self.id)
            soup = BeautifulSoup(request.content,'html.parser')
            from forum.user import User
            #self.client.find_element_by_xpath("//*[contains(@class, 'bigusername')]").get_attribute('href')[36:]
            return User(soup.find('a',{'class':'bigusername'})['href'][13:])
        
        except:
            raise forum.ext.errors.InvalidThreadId
        
    def __gettitle(self):
        """Retrives current thread's title"""
        request = requests.get("http://forum.sa-mp.com/showthread.php?t=" + self.id)
        soup = BeautifulSoup(request.content,'html.parser')
        return soup.find('strong').text.strip()

    def getrating(self,account):
        """
        Retrives rating information of current thread

        Parameters
        -----------
        account : :class:`Account`
            Authorised forum account
        
        Raises
        -------
        MustLogin
            Passed :class:`Account` object is not authorised

        Returns
        --------
        dictionary
            A dictionary {'NoOfVotes':'total number of votes','Average':'Average rating point'}
        """
        if not account.loggined:
            raise forum.ext.errors.MustLogin            
        try:
            account.client.get("http://forum.sa-mp.com/showthread.php?t=" + self.id)
            soup = BeautifulSoup(account.client.page_source,'html.parser')
            rating_info = soup.find('img',src=re.compile('^images/rating/'))['title']
            #rating_info = self.client.find_element_by_xpath("//*[starts-with(@src, 'images/rating/rating_')]").get_attribute('title')
            rating = {}
            rating['NoOfVotes'] = rating_info[rating_info.find(':')+2:rating_info.find('v')-1]
            rating['Average'] = rating_info[rating_info.find(',')+2:rating_info.find('aver')-1]
            return rating
        except:
            return {'NoOfVotes':'0','Average':'0'}

    def getsubforum(self):
        """
        Retrives sub forums of current thread as a list

        Returns
        --------
        list
            A list of sub forum names
        """
        request = requests.get("http://forum.sa-mp.com/showthread.php?t=" + self.id)
        soup = BeautifulSoup(request.content,'html.parser')
        sub_forums_elements = soup.find_all('a',href=re.compile('forumdisplay\.php\?f='))
        #sub_forums_elements = self.client.find_elements_by_xpath("//*[starts-with(@href, 'forumdisplay.php?f=')]")
        sub_forums = []
        for e in sub_forums_elements:
            sub_forums.append(e.text)
        return sub_forums

    def getcontent(self):
        """
        Retrives sub forums of current thread as a list

        Returns
        --------
        list
            A list of sub forum names
        """
        request = requests.get("http://forum.sa-mp.com/showthread.php?t=" + self.id)
        soup = BeautifulSoup(request.content,'html.parser')
        content = soup.find('div',id=re.compile('^post_message_')).text
        return content

    def getposts(self):
        """
        Retrives posts in current :class:`Thread` as a list

        Returns
        --------
        list
            A list of posts in :class:`Thread`
        """
        request = requests.get("http://forum.sa-mp.com/printthread.php?t=" + self.id)
        soup = BeautifulSoup(request.content,'html.parser')
        all_post_html = soup.find_all('td',{'class':'page'})[1:]
        
        try:
            pages_data = soup.find('td',{'class':'vbmenu_control'}).text
            total_pages = int(pages_data[pages_data.find('of')+3:])
        except:
            total_pages = 1

        for i in range(2,total_pages+1):
            request = requests.get("http://forum.sa-mp.com/printthread.php?t=" + self.id + "&pp=40&page=" + str(i) )
            soup = BeautifulSoup(request.content,'html.parser')
            all_post_html = all_post_html + soup.find_all('td',{'class':'page'})
        
        posts_raw = [p.text.strip() for p in all_post_html]
        
        posts = []
        temp_dict = {}

        for pr in posts_raw:
            temp_dict = dict(temp_dict)
            authend_idx = pr.find('\n')
            temp_dict['author'] = pr[:authend_idx].strip()
            pr = pr[authend_idx:]
            dateend_idx = pr.find(' ') + 1
            temp_dict['date'] = pr[:dateend_idx].strip()
            pr = pr[dateend_idx:]
            timeend_idx = pr.find('\n')
            temp_dict['time'] = pr[:timeend_idx]
            pr = pr[timeend_idx:].strip()
            temp_dict['content'] = pr[pr.find('\n')+1:]
            posts.append(temp_dict)

        return posts






