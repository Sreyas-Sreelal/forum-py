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
import forum.ext.errors
from selenium.common.exceptions import WebDriverException

class User:
    """Represents a SA-MP forum user.
        Example to create object: 
            ``u = User(samp_forum_user_id)``
            returns a User object with attributes id and name initialised
    """
    def __init__(self,id):
        self.id = id
        self.name = self.__getusername()
    
    # internals   
     
    def __getusername(self):
        """Retrives current user's name """
        try:
            request = requests.get('http://forum.sa-mp.com/member.php?u=' + self.id)
            soup = BeautifulSoup(request.content,'html.parser')
            name = str(soup.find('h1').text.strip())
            return name
        
        except:
            raise forum.ext.errors.InvalidUserId 

    def getlastactive(self,account):
        """
        Retrives last active information of current user

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
            A dictionary {'Date':'date of last active','Time':'time of last active'}
        """
        if not account.loggined:
            raise forum.ext.errors.MustLogin
        last_online_dict = {}
        try:
            account.client.get('http://forum.sa-mp.com/member.php?u=' + self.id)
            soup = BeautifulSoup(account.client.page_source,'html.parser')
            last_online =  soup.find('div',id='last_online').text.strip()
            last_online = last_online[last_online.find(': ')+2:].strip()
           
            last_online_dict['Date'] = last_online[:last_online.find(' ')]
            last_online_dict['Time'] = last_online[last_online.find(' ')+2:]
        except AttributeError:
            last_online_dict['Date'] = "Hidden" 
            last_online_dict['Time'] = "Hidden"
        return last_online_dict

    def getforumlevel(self):
        """
        Retrives current user's forum level

        Returns
        --------
        string
            Forum level in string
        """
        request = requests.get('http://forum.sa-mp.com/member.php?u=' + self.id)
        soup = BeautifulSoup(request.content,'html.parser')
        return soup.find('h2').text

    def getthreads(self):
        """
        Retrives list of threads created by current user

        Returns
        --------
        list
            A list of :class:`Thread`
        """
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
        """
        Retrives current user's reputation points

        Returns
        --------
        int
            Reputation point of current user
        """
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
        """
        Retrives current user's information in profile field

        Returns
        --------
        dictionary
            dictionary with informations as key value pair
        """
        request = requests.get('http://forum.sa-mp.com/member.php?u=' + self.id)
        soup = BeautifulSoup(request.content,'html.parser')
        data = soup.find('dl',{'class':'smallfont list_no_decoration profilefield_list'}).text.split('\n')
        data = list(filter(('').__ne__, data))
        length = len(data)
        info = {}
        for i in range(0,length,2):
            info[data[i]] = data[i+1]
        return info
    
    def getcurrentactivity(self,account):
        """
        Retrives current activity of user.This function requires authorised :class:`Account`

        Raises
        -------
        MustLogin
            Passed :class:`Account` object is not authorised

        Returns
        --------
        string
            Current activity in string.If the user is offline the function returns "Offline"
        """
        if not account.loggined:
            raise forum.ext.errors.MustLogin
        try:
            account.client.get('http://forum.sa-mp.com/member.php?u=' + self.id)
            soup = BeautifulSoup(account.client.page_source,'html.parser')
            current_activity = soup.find('div',{'id':'activity_info'}).text
            idx = current_activity.find('Current Activity:')
            
            if idx ==-1:
                current_activity = "Offline"
            else:
                current_activity = current_activity[idx+18:].strip()
        except AttributeError:
            current_activity = "Offline"    
            
        return current_activity

    def getsignaturetext(self):
        """
        Retrives singature text of user specified.

        Returns
        --------
        string
            Signature text in string.If no signature returns None
        """
        try:
            request = requests.get("https://forum.sa-mp.com/member.php?u=" + self.id)
            soup = BeautifulSoup(request.content,"html.parser")
            signature = soup.find("dd",{'id':'signature'}).text
            return signature
        except:
            return None


