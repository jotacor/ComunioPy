#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from bs4 import BeautifulSoup
from datetime import date as dt
import os
from pyvirtualdisplay import Display
import re
import requests
from selenium import webdriver
import sys
import time

Leagues = {'BBVA':'www.comunio.es',
           'Adelante':'www.comuniodesegunda.es',
           'Bundesliga':'www.comunio.de',
           'Bundesliga2':'www.comdue.de',
           'Serie A':'www.comunio.it',
           'Premier League':'www.comunio.co.uk',
           'Liga Sagres':'www.comunio.pt'}

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0'

class Comunio:

    def __init__(self,username,password,league):
        self.username = username
        self.password = password
        self.domain = Leagues[league]
        self.session = requests.session()

    def login(self):
        payload = { 'login':self.username,
                    'pass':self.password,
                    'action':'login'}
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain","User-Agent": user_agent}
        req = self.session.post('http://'+self.domain+'/login.phtml',headers=headers,data=payload).content
        #soup = BeautifulSoup(req)
        if 'puntos en proceso' in req:
            print 'Comunio webpage not available.'
            sys.exit(1)
        self.load_info() #Function to load the account information
  
    def load_info(self):
        ''' Get info from account logged '''
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain",'Referer': 'http://'+self.domain+'/login.phtml',"User-Agent": user_agent}
        req = self.session.get('http://'+self.domain+'/team_news.phtml',headers=headers).content
        soup = BeautifulSoup(req)
        self.title = soup.title.string
        
        estado = soup.find('div',{'id':'content'}).find('div',{'id':'manager'}).string
        if estado:
            print estado.strip()
            sys.exit(1)
            
        [s.extract() for s in soup('strong')]
        if (soup.find('div',{'id':'userid'}) != None):
            self.id = soup.find('div',{'id':'userid'}).p.text.strip()[2:]
            self.money = int(soup.find('div',{'id':'manager_money'}).p.text.strip().replace(".","")[:-2])
            self.teamvalue = int(soup.find('div',{'id':'teamvalue'}).p.text.strip().replace(".","")[:-2])

    def get_money(self):
        '''Get my money'''
        return self.money
    
    def get_team_value(self):
        '''Get my team value'''
        return self.teamvalue
    
    def get_myid(self):
        '''Get my id'''
        return self.id
    
    def get_title(self):
        '''Title of the webpage'''
        return self.title

    def get_news(self):
        '''Get all the news from first page'''
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain",'Referer': 'http://'+self.domain+'/login.phtml',"User-Agent": user_agent}
        req = self.session.get('http://'+self.domain+'/team_news.phtml',headers=headers).content
        soup = BeautifulSoup(req)
        news = []
        for i in soup.find_all('div',{'class','article_content_text'}):
            news.append(i.text)
        return news
      

    def logout(self):
        '''Logout from Comunio'''
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain","User-Agent": user_agent}
        self.session.get('http://'+self.domain+'/logout.phtml',headers=headers)

  
    def standings(self):
        '''Get standings from the community's account'''
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain","User-Agent": user_agent}
        req = self.session.get('http://'+self.domain+'/standings.phtml',headers=headers).content
        soup = BeautifulSoup(req)
        table = soup.find('table',{'id':'tablestandings'}).find_all('tr')
        clasificacion = []
        [clasificacion.append(('%s\t%s\t%s\t%s\t%s')%(tablas.find('td').text,tablas.find('div')['id'],tablas.a.text,tablas.find_all('td')[3].text,tablas.find_all('td')[4].text)) for tablas in table[1:]]
        return clasificacion


    def info_user(self,userid):
        '''Get user info using a ID'''
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain",'Referer': 'http://'+self.domain+'/standings.phtml',"User-Agent": user_agent}
        req = self.session.get('http://'+self.domain+'/playerInfo.phtml?pid='+userid,headers=headers).content
        soup = BeautifulSoup(req)
        title = soup.title.string
        community = soup.find_all('table',border=0)[1].a.text
        info = []
        info.append(title)
        info.append(community)
        for i in soup.find_all('table',border=0)[1].find_all('td')[1:]:
            info.append(i.text)
        for i in soup.find('table',cellpadding=2).find_all('tr')[1:]:
            cad = i.find_all('td')
            numero=cad[0].text
            nombre=cad[2].text.strip()
            team=cad[3].find('img')['alt']
            precio=cad[4].text.replace(".","")
            puntos=cad[5].text
            posicion=cad[6].text
            info.append([numero,nombre,team,precio,puntos,posicion])
        return info


    def lineup_user(self,userid):
        '''Get user lineup using a ID'''
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain",'Referer': 'http://'+self.domain+'/standings.phtml',"User-Agent": user_agent}
        req = self.session.get('http://'+self.domain+'/playerInfo.phtml?pid='+userid,headers=headers).content
        soup = BeautifulSoup(req)
        info = []
        for i in soup.find_all('td',{'class':'name_cont'}):
            info.append(i.text.strip())
        return info


    def info_community(self,teamid):
        '''Get comunity info using a ID'''
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain",'Referer': 'http://'+self.domain+'/standings.phtml',"User-Agent": user_agent}
        req = self.session.get('http://'+self.domain+'/teamInfo.phtml?tid='+teamid,headers=headers).content
        soup = BeautifulSoup(req)
        info = []
        for i in soup.find('table',cellpadding=2).find_all('tr')[1:]:
            info.append('%s\t%s\t%s\t%s\t%s'%(i.find('td').text,i.find('a')['href'].split('pid=')[1],i.a.text,i.find_all('td')[2].text,i.find_all('td')[3].text))
        return info


    def info_player(self,pid):
        ''''
        Get info football player using a ID
        @return: [name,position,team,points,price]
        '''
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain",'Referer': 'http://'+self.domain+'/team_news.phtml',"User-Agent": user_agent}
        req = self.session.get('http://'+self.domain+'/tradableInfo.phtml?tid='+pid,headers=headers).content
        soup = BeautifulSoup(req)
        info = []
        info.append(soup.title.text.strip())
        for i in soup.find('table',cellspacing=1).find_all('tr'):
            info.append(i.find_all('td')[1].text.replace(".",""))
        return info


    def info_player_id(self,name):
        '''Get id using name football player'''
        name=name.title().replace(" ", "+")
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain",'Referer': 'http://'+self.domain+'/team_news.phtml',"User-Agent": user_agent}
        req = self.session.get('http://stats.comunio.es/search.php?name='+name,headers=headers).content
        soup = BeautifulSoup(req)
        for i in soup.find_all('a',{'class','nowrap'}):
            number = re.search("([0-9]+)-", str(i)).group(1)
            break # Solo devuelve la primera coincidencia
        return number


    def club(self,cid):
        '''
        Get info by real team using a ID
        @return: name,[player list]
        '''
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain",'Referer': 'http://'+self.domain+'/',"User-Agent": user_agent}
        req = self.session.get('http://'+self.domain+'/clubInfo.phtml?cid='+cid,headers=headers).content
        soup = BeautifulSoup(req)
        plist = []
        for i in soup.find('table',cellpadding=2).find_all('tr')[1:]:
            plist.append('%s\t%s\t%s\t%s\t%s'%(i.find_all('td')[0].text,i.find_all('td')[1].text,i.find_all('td')[2].text,i.find_all('td')[3].text,i.find_all('td')[4].text))
        return soup.title.text,plist


    def team_id(self,team):
        '''
        Get team ID using a real team name
        @return: id
        '''
        #UTF-8 comparison
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain",'Referer': 'http://'+self.domain+'/',"User-Agent": user_agent}
        req = self.session.get('http://'+self.domain,headers=headers).content
        soup = BeautifulSoup(req)
        for i in soup.find('table',cellpadding=2).find_all('tr'):
            #Get teamid from the bets
            team1 = i.find('a')['title']
            team2 = i.find_all('a')[1]['title']
            if (team == team1):
                return i.find('a')['href'].split('cid=')[1]
            elif (team == team2):
                return i.find_all('a')[1]['href'].split('cid=')[1]
        return None


    def user_id(self, user):
        ''' 
        Get userid from a name
        @return: id
        '''
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain",'Referer': 'http://'+self.domain+'/team_news.phtml',"User-Agent": user_agent}
        req = self.session.get('http://'+self.domain+'/standings.phtml',headers=headers).content
        soup = BeautifulSoup(req)
        for i in soup.find('table',cellpadding=2).find_all('tr'):
            try:
                if (user == i.find_all('td')[2].text.encode('utf8')):
                    return  i.find('a')['href'].split('pid=')[1]
            except:
                continue
        return None


    def players_onsale(self, only_computer=False):
        '''
        Returns the football players currently on sale
        @return: [[name, team, min_price, market_price, points, date, owner, position]]
        '''
        reintentos=0
        current_year = dt.today().year
        current_month = dt.today().month
        display = Display(visible=0, size=(800, 600))
        display.start()
        xpaths = { 'usernameTxtBox':   ".//*[@id='login-ubox']/input",
                   'passwordTxtBox':   ".//*[@id='login-pwbox']/input",
                   'loginButton'   :   ".//*[@id='login-box-wrapper']/a",
                   'exchange_table':   ".//*[@id='searchTextResults']"
                   }
        browser = webdriver.Firefox()
        browser.get("http://www.comunio.es/login.phtml")
        browser.find_element_by_xpath(xpaths['usernameTxtBox']).clear()
        browser.find_element_by_xpath(xpaths['usernameTxtBox']).send_keys(self.username)
        browser.find_element_by_xpath(xpaths['passwordTxtBox']).clear()
        browser.find_element_by_xpath(xpaths['passwordTxtBox']).send_keys(self.password)
        browser.find_element_by_xpath(xpaths['loginButton']).click()
        time.sleep(3)
        # Esperaremos en el while hasta que termine de cargar el JS de la página
        browser.get('http://www.comunio.es/exchangemarket.phtml')
        time.sleep(3)
        while True and reintentos < 20:
            req = browser.page_source
            soup = BeautifulSoup(req)
            on_sale = []
            year_flag = 0
            try:
                for i in soup.find('table',{'class','tablecontent03'}).find_all('tr')[2:]:
                    name = i.find_all('td')[0].text.strip()
                    team = i.find('span')['title']
                    min_price = i.find_all('td')[2].text.replace(",","").strip()
                    market_price = i.find_all('td')[3].text.replace(",","").strip()
                    points = i.find_all('td')[4].text.strip().strip()
                    # Controlamos el cambio de año, ya que comunio no lo dá
                    if current_month <= 7 and int(i.find_all('td')[5].text[3:5]) > 7:
                        year_flag = 1
                    date = str(current_year-year_flag)+i.find_all('td')[5].text[3:5]+i.find_all('td')[5].text[:2]
                    owner = i.find_all('td')[6].text.strip()
                    position = i.find_all('td')[7].text.strip()
                    # Comprobamos si solamente queremos los de la computadora o no
                    if (only_computer and owner == 'Computer') or not only_computer:
                        on_sale.append([name, team, min_price, market_price, points, date, owner, position])
                # Llegaremos al break cuando se haya cargado el JS y cargado la lista
                if on_sale != []:
                    break
            except Exception as e:
                reintentos+=1
                print 'Error looking for players on sale "players_onsale": ', e
                print 'Trying again (%s).' % reintentos
                if reintentos == 10:
                    browser.get('http://www.comunio.es/exchangemarket.phtml')
                time.sleep(3)
        
        browser.quit()
        display.stop()
        return on_sale


    def bids_to_you(self):
        '''
        Get bids made to you
        @return: [[player,owner,team,money,date,datechange,status],]
        '''
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain",'Referer': 'http://'+self.domain+'/team_news.phtml',"User-Agent": user_agent}
        req = self.session.get('http://'+self.domain+'/exchangemarket.phtml?viewoffers_x=',headers=headers).content
        soup = BeautifulSoup(req)
        table = []
        for i in soup.find('table',{'class','tablecontent03'}).find_all('tr')[1:]:
            player,owner,team,price,bid_date,trans_date,status = self._parse_bid_table(i)
            table.append([player,owner,team,price,bid_date,trans_date,status])
        return table


    def bids_from_you(self):
        '''
        Get your bids made for
        @return: [[player,owner,team,money,date,datechange,status],]
        '''
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain",'Referer': 'http://'+self.domain+'/team_news.phtml',"User-Agent": user_agent}
        req = self.session.get('http://'+self.domain+'/exchangemarket.phtml?viewoffers_x=',headers=headers).content
        #secondpage = 'http://www.comunio.es/exchangemarket.phtml?viewoffers_x=34&sort=&sortAsc=&tbl=&1277428601_total=14&1277428601_listmin=10'
        soup = BeautifulSoup(req)
        table = []
        for i in soup.find_all('table',{'class','tablecontent03'})[1].find_all('tr')[1:]:
            player,owner,team,price,bid_date,trans_date,status = self._parse_bid_table(i)
            table.append([player,owner,team,price,bid_date,trans_date,status])
        return table

    
    def _parse_bid_table(self, table):
        '''
        Convert table row values into strings
        @return: player, owner, team, price, bid_date, trans_date, status
        '''
        player = table.find_all('td')[0].text
        owner = table.find_all('td')[1].text
        team = table.find('img')['alt']
        price = int(table.find_all('td')[3].text.replace(".",""))
        bid_date = table.find_all('td')[4].text
        trans_date = table.find_all('td')[5].text
        status = table.find_all('td')[6].text
        return player,owner,team,price,bid_date,trans_date,status
    