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

import forum.ext.errors
from bs4 import BeautifulSoup
import re
from selenium.common.exceptions import WebDriverException
import requests
import csv
from io import StringIO
import os

class Account:
    """Represents a SA-MP forum account.
        Example to create object: 
            ``a = Account(samp_forum_user_name,account_password)``
            returns a Account object with attributes client,loggined,User and name initialised
    """
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
    
    # Internals    
    
    def __login(self,name,password):
        """Logs into user account"""
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
        """
        Retrives contact list in user account

        Returns
        --------
        list
            A list of :class:`User` representing contacts in account 
        """
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
        """
        Retrives user id from forum forum user name

        Parameters
        -----------
        username : string
            forum user name
        
        Raises
        -------
        InvalidUserId
            A user with that name doesn't exists in forum

        Returns
        --------
        string
            A string representing forum user id
        """
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
                        raise forum.ext.errors.InvalidUserId
        
        except:
            raise forum.ext.errors.InvalidUserId
        
        user_link = ausername_element['href']
        userid = user_link[user_link.find("=")+1:].strip()
        
        return userid

    def getnew(self,max_number_threads=1000):
        """
        Retrives lastest active threads

        Parameters
        -----------
        max_number_threads(optional) : int
            max number of threads to retrive (default 1000)
        
        Returns
        --------
        list
            A list of :class:`Threads` representing latest active threads
        """
        from forum.threads import Thread
        self.client.get("http://forum.sa-mp.com/search.php?do=getnew")
        self.client.get(self.client.current_url+"&pp="+str(max_number_threads))
        soup = BeautifulSoup(self.client.page_source,'html.parser')
                
        thread_elements = soup.find_all('a',id=re.compile('^thread_title_'))
        
        threads = []
        for te in thread_elements:
            try:
                threads.append(Thread(te['id'][13:]))
            except:
                continue

        return threads

    def getpms(self):
        """
        Retrives inbox messages
        
        Returns
        --------
        list
            A list of dictionary with pm details as key value pairs 
        """
        self.client.get("http://forum.sa-mp.com/private.php?do=downloadpm&dowhat=csv")
        session = requests.Session()
        cookies = self.client.get_cookies()

        for cookie in cookies: 
            session.cookies.set(cookie['name'], cookie['value'])

        local_filename = self.name+"_temp.csv"
        
        r = session.get("http://forum.sa-mp.com/private.php?do=downloadpm&dowhat=csv",stream=True)
        
        if str(r) != "<Response [200]>":
            raise forum.ext.errors.MustLogin

        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk: 
                    f.write(chunk)
        f.close()
        
        f = open(local_filename,'r')
        reader = csv.DictReader(f)
        pms = list(reader)
        f.close()
        os.remove(local_filename)
        
        return pms

    def send_pm(self,users,title,content):
        """
        Sends a private message to specified user(s)

        Parameters
        -----------
        users : list
            list of :class:`User` representing recipents (max number of users at a time is 5)
        title : string
            title of the private message
        content:
            content or body of the private message

        Raises
        -------
        RecipentLimitReached
            More than 5 recipents are specified

        Returns
        --------
        True
            Message send successfully
        False
            Message couldn't send

        Note
        --------
            The forum has a limit of sending one pm in 15 minutes.Therefore once used this function has to wait
            15 minutes before sending another private message otherwise it will return false
        """
        if len(users) > 5 :
            raise forum.ext.errors.RecipentLimitReached
            
        if users is None or title is None or content is None:
            return False
        recipents = ""

        try:
            for user in users:
                recipents += user.name + ";"

            self.client.get("http://forum.sa-mp.com/private.php?do=newpm")
            recipents_element = self.client.find_element_by_id("pmrecips_txt")
            title_element = self.client.find_element_by_xpath( "//input[@name='title']")
            contents_element = self.client.find_element_by_id("vB_Editor_001_textarea")
            send_button = self.client.find_element_by_id("vB_Editor_001_save")

            recipents_element.send_keys(recipents)
            title_element.send_keys(title)
            contents_element.send_keys(content)
            send_button.click()

            soup = BeautifulSoup(self.client.page_source,'html.parser')
            islimit = soup.find(text=re.compile('This forum requires that you wait'))
            if islimit is not None:
                raise forum.ext.errors.MaxPMLimit 
            return True

        except WebDriverException:
            return False


