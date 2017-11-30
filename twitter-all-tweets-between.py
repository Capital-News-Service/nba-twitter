import sys  

#pip.main(['install','selenium'])

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.binary_location = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'

driver = webdriver.Chrome(executable_path="C:\\cygwin64\\home\\jagluck\\twitter-teams\\chromedriver.exe", chrome_options=chrome_options)

nba = ['okcthunder','celtics','NYKnicks','BrooklynNets','PelicansNBA', 'Pacers', 'OrlandoMagic','Timberwolves','MiamiHEAT',
'Hornets', 'DetroitPistons', 'DallasMavs', 'LAClippers', 'Lakers', 'UtahJazz', 'nuggets', 'WashWizards', 'ChicagoBulls',
'spurs', 'Suns', 'HoustonRockets', 'Warriors', 'ATLHawks', 'MemGrizz', 'Bucks', 'Raptors', 'SacramentoKings', 'Sixers', 'trailblazers'];

nbaSmall=['celtics','DetroitPistons']

def getTweets(sender, to):
    driver.get("https://twitter.com/search?q=from%3A" + sender + "%20%40" + to + "&src=typd") 
    time.sleep(3)
    
    lastHeight = driver.execute_script("return document.body.scrollHeight")
    print(lastHeight)
    
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        newHeight = driver.execute_script("return document.body.scrollHeight")
        print(newHeight)
        if newHeight == lastHeight:
     	    break
        lastHeight = newHeight
    
    soup = BeautifulSoup(driver.page_source, 'lxml')
    stream = soup.find("ol", {"class": "stream-items"})
    if (stream is None):
        return [sender,to]
    items = stream.find_all("p", {"class": "tweet-text"})
   # times = stream.find_all("span", {"class": "timestamp"})
    
    tweets = []
   # times = []
    tweets.append(sender)
    tweets.append(to)
   # times.append(sender)
    #times.append(to)
    for i in items:
        tweets.append(i.get_text())
   
   # for i in times:
       # times.append(i)
            
    print("Over")
    return tweets

def findData(teams):
    table = []
    c = 0
    for f in teams:
        for t in teams:
            if t != f:
                table.append(getTweets(f,t))
                print(c)
                c = c + 1
    print("finished")
    return table
    
result = findData(nbaSmall)
print("done")
df = pd.DataFrame(result)
print(df)
df.to_csv("testtweets.csv", sep=',')

driver.close()

