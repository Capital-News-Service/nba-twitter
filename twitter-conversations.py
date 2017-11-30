import sys  

#pip.main(['install','selenium'])
#pip.main(['install','bs4'])
#pip.main(['install','lxml'])

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from random import *

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'

driver = webdriver.Chrome(executable_path="C:\\Users\\jagluck\\Documents\\GitHub\\nba-twitter\\chromedriver.exe", chrome_options=chrome_options)

nba = ['cavs','okcthunder','celtics','NYKnicks','BrooklynNets','PelicansNBA', 'Pacers', 'OrlandoMagic','Timberwolves','MiamiHEAT',
'Hornets', 'DetroitPistons', 'DallasMavs', 'LAClippers', 'Lakers', 'UtahJazz', 'nuggets', 'WashWizards', 'ChicagoBulls',
'spurs', 'Suns', 'HoustonRockets', 'Warriors', 'ATLHawks', 'MemGrizz', 'Bucks', 'Raptors', 'SacramentoKings', 'Sixers', 'trailblazers'];

nbaSmall=['trailblazers','celtics']

def check_exists_by_id(id):
    try:
        driver.find_element_by_id(id)
    except NoSuchElementException:
        return False
    return True

def getTweets(sender, to):
    
    driver.get("https://twitter.com/search?q=from%3A" + sender + "%20%40" + to + "&src=typd") 
    time.sleep(2)
    
    lastHeight = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        newHeight = driver.execute_script("return document.body.scrollHeight")
        if newHeight == lastHeight:
     	    break
        lastHeight = newHeight
    
    soup = BeautifulSoup(driver.page_source, "lxml")
    stream = soup.find("ol", {"class": "stream-items"})
    if (stream is None):
        return [sender,to]
    items = stream.find_all("li", {"class": "stream-item"})
    
    row = []
    
    headtweets = {}
    convs = {}
    
    
    #loop through every tweet in mentions
    for i in items:
        #make sure it is a reply
        isthisareply = i.find_all("div", {"class": "ReplyingToContextBelowAuthor"})
        if (len(isthisareply) > 0):
            
             
            textcontent = i.find("p", {"class": "tweet-text"})
            #print("----- " + textcontent.get_text())
                
            #if tweet is replying to an nba team
            replyusers = isthisareply[0].findAll("span", {"class": "username"})
            isNba = False
            for username in replyusers:
                if username.get_text()[1:] in nba:
                    isNba = True
            
            if isNba:
                #print("isNba")
                
                driver.get("https://twitter.com/search?q=from%3A" + sender + "%20%40" + to + "&src=typd") 
                time.sleep(2)
                
                lastHeight = driver.execute_script("return document.body.scrollHeight")
                
                while True:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(.5)
                    newHeight = driver.execute_script("return document.body.scrollHeight")
                    if newHeight == lastHeight:
                 	    break
                    lastHeight = newHeight
    
                driver.maximize_window()
                id = i.get('id')
                if (check_exists_by_id(id)):
                    ele = driver.find_element_by_id(id)
                    time.sleep(.5)
                    ele.click()
                    time.sleep(.5)
                    
                    soup = BeautifulSoup(driver.page_source, "lxml")
                    overlay = soup.find("div", {"class": "permalink-container"})
                    
                    time.sleep(1)
                    
                    if (check_exists_by_id(id)):
                        ele = driver.find_element_by_id(id)
                        elesize = ele.size
                        elewidth = elesize['width']
                        eleheight = elesize['height']
                        isfound = True
                        while (not overlay):
                            xloc = randint(0, eleheight)
                            yloc = randint(0, elewidth)
                            if (check_exists_by_id(id)):
                                ele = driver.find_element_by_id(id)
                                action = webdriver.common.action_chains.ActionChains(driver)
                                action.move_to_element_with_offset(ele, xloc, yloc)
                                action.click()
                                action.perform()
                                #print("in here")
                                time.sleep(.5)
                                soup = BeautifulSoup(driver.page_source, "lxml")
                                overlay = soup.find("div", {"class": "permalink-container"})
                            else:
                                isfound = False
                                print("----- not found 1 ------")
                                print("----- " + textcontent.get_text())
                                break
                            
                        if (isfound):
                            
                            lastHeight = driver.execute_script("return document.body.scrollHeight")
                        
                            while True:
                                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                                time.sleep(.5)
                                newHeight = driver.execute_script("return document.body.scrollHeight")
                                if newHeight == lastHeight:
                             	    break
                                lastHeight = newHeight
                            
            
                            conv = []
                            
                            tweets = []
                            times = []
                            names = []
                            
                            #Get First Tweet In Overlay
                            topstream = overlay.find_all("div", {"class": "permalink-ancestor-tweet"})
                            
                            if (len(topstream) > 0):
                                headtweet = topstream[0].find("p", {"class": "tweet-text"}).get_text()
                                
                                #print("added")
                                conv.append(headtweet)
                                conv.append(sender)
                                conv.append(to) 
                                for i2 in topstream:
                                    textcontent = i2.find("p", {"class": "tweet-text"})
                                    timecontent = i2.find('span', {"class":"_timestamp"})
                                    tweets.append(textcontent.get_text())
                                    date = timecontent.get_text()
                                    if (date[-4:-2] == '20'):
                                        times.append(date)
                                    else:
                                        times.append(date + " 2017")
                                    namecontent = i2.find("strong", {"class": "fullname"})
                                    names.append(namecontent.get_text())
                                        
                                #GET REPLIES
                                topstream = overlay.find_all("div", {"class": "permalink-tweet"})
                                
                                for i2 in topstream:
                                    textcontent = i2.find("p", {"class": "tweet-text"})
                                    timecontent = i2.find('span', {"class":"_timestamp"})
                                    tweets.append(textcontent.get_text())
                                    date = timecontent.get_text()
                                    if (date[-4:-2] == '20'):
                                        times.append(date)
                                    else:
                                        times.append(date + " 2017")
                                    namecontent = i2.find("strong", {"class": "fullname"})
                                    names.append(namecontent.get_text())
                                    
                                
                                if (headtweet not in headtweets or headtweets[headtweet] < len(tweets)):    
                                    conv.append(tweets)
                                    conv.append(len(tweets))
                                    conv.append(times)
                                    conv.append(names)
                                    conv.append(len(names))
                                    convs[headtweet] = conv
                                    headtweets[headtweet] = len(tweets)
                                    
                    else:
                        print("----- not found 2 ------")
                        print("----- " + textcontent.get_text())
                else:
                    print("----- not found 3 ------")
                    print("----- " + textcontent.get_text())
    
        
    for key, value in convs.items():
        row.append(value)
     
    return row

def findData(teams):
    table = []
    c = 0
    teamcount = -1
    for f in teams:
        teamcount = teamcount + 1
        
        if (teamcount > 13 and teamcount < 15):
            for t in teams:
                if t != f:
                    temp = getTweets(f,t)
                    if (temp):
                        table = table + getTweets(f,t)
                        print("relation finished " + str(c) + " size is " + str(len(table)))
                    else:
                        print("relation finished " + str(c) + " size is " + str(len(table)))
                    c = c + 1
    return table

   
result = findData(nba)
print("done")
df = pd.DataFrame(result)
print(df)
df.to_csv("nba-conversations14.csv", sep=',')

driver.close()

