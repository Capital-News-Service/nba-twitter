# Jake Gluck - Capital News Service

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
import json

#Set up headless browser
chrome_options = Options()
chrome_options.add_argument("--headless")

#Fill in path to chromedrive.exe here
chromedriver = '/usr/bin/chromedriver/chromedriver'
driver = webdriver.Chrome(chromedriver, chrome_options=chrome_options)

#This is ther list of accounts you would like to gather, put in their twitter usernames
nba = ['cavs','okcthunder','celtics','NYKnicks','BrooklynNets','PelicansNBA', 'Pacers', 'OrlandoMagic','Timberwolves','MiamiHEAT',
'Hornets', 'DetroitPistons', 'DallasMavs', 'LAClippers', 'Lakers', 'UtahJazz', 'nuggets', 'WashWizards', 'chicagobulls',
'spurs', 'Suns', 'HoustonRockets', 'warriors', 'ATLHawks', 'MemGrizz', 'Bucks', 'Raptors', 'SacramentoKings', 'Sixers', 'trailblazers'];

NBACAPS = ['CAVS','OKCTHUNDER','CELTICS','NYKNICKS','BROOKLYNNETS','PELICANSNBA', 'PACERS', 'ORLANDOMAGIC','TIMBERWOLVES','MIAMIHEAT',
'HORNETS', 'DETROITPISTONS', 'DALLASMAVS', 'LACLIPPERS', 'LAKERS', 'UTAHJAZZ', 'NUGGETS', 'WASHWIZARDS', 'CHICAGOBULLS',
'SPURS', 'SUNS', 'HOUSTONROCKETS', 'WARRIORS', 'ATLHAWKS', 'MEMGRIZZ', 'BUCKS', 'RAPTORS', 'SACRAMENTOKINGS', 'SIXERS', 'TRAILBLAZERS'];

nbaSmall=['okcthunder','celtics','NYKnicks','BrooklynNets','PelicansNBA', 'Pacers', 'OrlandoMagic']

pages_visited = 0
empty_relations = 0

def countPage():
    global pages_visited
    pages_visited = pages_visited + 1

def countEmptyRelation():
    global empty_relations
    empty_relations = empty_relations + 1

def scroll_down():
     #scroll to bottom of page
    lastHeight = driver.execute_script("return document.body.scrollHeight")
        
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        newHeight = driver.execute_script("return document.body.scrollHeight")
        if newHeight == lastHeight:
            break
        lastHeight = newHeight
    
        driver.maximize_window()

        time.sleep(.5)

def scroll_down_overlay():  

    notRead = False
    while (notRead): 

        if check_exists_by_id('permalink-overlay-dialog'):

            per_over = driver.find_element_by_id('permalink-overlay-dialog')


            lastHeight = per_over.size['height']

            while True:
                driver.execute_script("document.getElementById('permalink-overlay').scrollTo(0, -250);")
                time.sleep(1)
                newHeight = per_over.size['height']
                if newHeight == lastHeight:
                    break
                lastHeight = newHeight
            
                driver.maximize_window()

                time.sleep(.5)

                notRead = True

        else:
            print("No dialog overlay")

def scroll_up_overlay():

    notRead = False
    while (notRead):
        

        if check_exists_by_id('permalink-overlay-dialog'):

            per_over = driver.find_element_by_id('permalink-overlay-dialog')

            lastHeight = per_over.size['height']

            while True:
                driver.execute_script("document.getElementById('permalink-overlay').scrollTo(0, " + str(lastHeight) + ");")
                time.sleep(1)
                newHeight = per_over.size['height']
                if newHeight == lastHeight:
                    break
                lastHeight = newHeight
            
                driver.maximize_window()

                time.sleep(.5)

            notRead = True
        else:
            print("No dialog overlay")

def load_page(url):
    countPage()
    driver.get(url) 
    time.sleep(1)

    scroll_down()

def load_page_tweet(url):
    countPage()
    driver.get(url) 
    time.sleep(1)


    scroll_up_overlay()

    scroll_down_overlay()
        

def check_exists_by_id(id):
    try:
        driver.find_element_by_id(id)
    except NoSuchElementException:
        return False
    return True

#get all conversations from on sender to one reciever
def getTweets(sender, to):
    
    print("From: " + sender + " To: " + to)
    #load page
    load_page("https://twitter.com/search?q=from%3A" + sender + "%20%40" + to + "&src=typd") 
    
    #load html
    soup = BeautifulSoup(driver.page_source, "lxml")
    stream = soup.find("ol", {"class": "stream-items"})
    
    row = []
       
    #if no tweets between return empty
    if (stream is None):
        countEmptyRelation()
        print("No tweets for this relation")
    else:
        
        items = stream.find_all("li", {"class": "stream-item"})
        
        
        headtweets = {}
        convs = {}        
        
        #loop through every tweet in mentions
        count = 1
        for i in items:
            #print(count)
            count = count + 1
            textcontent = i.find("p", {"class": "tweet-text"})
            
            #make sure it is a reply
            isthisareply = i.find_all("div", {"class": "ReplyingToContextBelowAuthor"})

            if (len(isthisareply) > 0):
                

                #if tweet is replying to an nba team
                test = json.loads(i.find("div", {"class": "tweet"})['data-reply-to-users-json'])

                replyusers = []

                for b in test:
                    replyusers.append(b['screen_name'].upper())

                valid = set(NBACAPS) - set([sender.upper()])

                isNba = False
                for username in replyusers:
                    if username in valid:
                        isNba = True

                if isNba:

                    #print("\nTweet: " + textcontent.get_text())

                    tweet_div = i.find_all("div", {"class": "tweet"})
                    data_permalink_path = str(tweet_div[0]['data-permalink-path'])

                    convo_url = "https://twitter.com" + data_permalink_path

                    finished = False

                    while(not finished):
                        load_page_tweet(convo_url)

                        soup = BeautifulSoup(driver.page_source, "lxml")
                        overlay = soup.find("div", {"class": "permalink-container"})

                        if(overlay):
                                                         
                            conv = []
                            
                            tweets = []
                            times = []
                            names = []
                            user_names = []
                            
                            #Get ancestor In overlay
                            ancestors = overlay.find_all("div", {"class": "permalink-in-reply-tos"})

                            if (len(ancestors) > 0):
                                topstream = ancestors[0].find_all("div", {"class": "tweet"})
                                
                                if (len(topstream) > 0):
                                    #print("in tweets")
                                    
                                    headtweet = topstream[0].find("p", {"class": "tweet-text"}).get_text()
                                    
                                    #print("HEAD: " + headtweet)
                                    #print("add tweet")
                                    conv.append(headtweet)
                                    conv.append(sender)
                                    conv.append(to) 
                                    
                                    #get all tweets in ancestor
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
                                        usernamecontent = i2.find("span", {"class": "username"})
                                        user_names.append(usernamecontent.get_text())
                                            
                                    #GET REPLIES
                                    topstream = overlay.find_all("div", {"class": "permalink-tweet"})
                                    
                                    #get all tweets in replies
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
                                        usernamecontent = i2.find("span", {"class": "username"})
                                        user_names.append(usernamecontent.get_text())
                                        
                                    
                                    if ((headtweet not in headtweets) or (headtweets[headtweet] < len(tweets))): 



                                        #Count how many unique nba teams are in convo 
                                        cc = 0 
                                        seen = []
                                        for n in user_names:
                                            name = n[1:].upper()
                                            if name in NBACAPS:
                                                if name not in seen:
                                                    seen.append(name)
                                                    cc = cc + 1



                                        if (cc > 1):
                                            conv.append(tweets)
                                            conv.append(len(tweets))
                                            conv.append(times)
                                            conv.append(names)
                                            conv.append(user_names)
                                            convs[headtweet] = conv
                                            headtweets[headtweet] = len(tweets)
                                            finished = True
                                        else:
                                            # print("Tweet: " + textcontent.get_text())
                                            # print("Not a convo \n")
                                            finished = True
                                    else:
                                        # print("Tweet: " + textcontent.get_text())
                                        # print("We saw this already \n")
                                        finished = True
                                else:
                                    print("Tweet: " + textcontent.get_text())
                                    print("this is a problem \n")             
                            else:
                                # print("Tweet: " + textcontent.get_text())
                                # print("--- No ancestors, must have been deleted --- \n") 
                                finished = True          
                        else:
                            print("----- no overlay ------") 
                        
                else:
                    1 + 1
                    print("----- not a nba team ------")
            else:
                1 + 1
                #print("----- not a reply ------")
                
        for key, value in convs.items():
            row.append(value)
     
    return row

def findData(teams):
    table = []
    c = 0
    for f in teams:
        for t in teams:
            if t != f:
                temp = getTweets(f,t)
                if (temp):
                    table = table + temp
                    print("relation finished " + str(c) + " size is " + str(len(table)) + "\n")
                else:
                    print("relation finished " + str(c) + " size is " + str(len(table)) + "\n")
                c = c + 1
    return table

result = findData(nba)
print("Finished\nPages Visited: " + str(pages_visited) + "\nEmpty Relations: " + str(empty_relations))
df = pd.DataFrame(result, columns=['head', 'from', 'to', 'tweets', 'size', 'dates', 'names', 'usernames'])
df = df.sort_values('size', ascending=False).drop_duplicates('head')
print(df)
df.to_csv("nba-conv-test.csv", sep=',')
driver.close()


