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

driver = webdriver.Chrome(executable_path="C:\\Users\\jagluck\\Documents\\GitHub\\nba-twitter\\chromedriver.exe", chrome_options=chrome_options)

nba = ['cavs','okcthunder','celtics','NYKnicks','BrooklynNets','PelicansNBA', 'Pacers', 'OrlandoMagic','Timberwolves','MiamiHEAT',
'Hornets', 'DetroitPistons', 'DallasMavs', 'LAClippers', 'Lakers', 'UtahJazz', 'nuggets', 'WashWizards', 'ChicagoBulls',
'spurs', 'Suns', 'HoustonRockets', 'Warriors', 'ATLHawks', 'MemGrizz', 'Bucks', 'Raptors', 'SacramentoKings', 'Sixers', 'trailblazers'];

nbaSmall=['UtahJazz','trailblazers','okcthunder']

def getTweets(sender, to):
    driver.get("https://twitter.com/search?q=from%3A" + sender + "%20%40" + to + "&src=typd") 
    time.sleep(2)
    
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
    items = stream.find_all("div", {"class": "content"})
    
    row = []
    row.append(sender)
    row.append(to)
    
    tweets = []
    times = []
    isreply = []
    for i in items:
        isthisareply = i.find_all("div", {"class": "ReplyingToContextBelowAuthor"})
        if (len(isthisareply) > 0):
            print(isthisareply[0].get_text())
            textcontent = i.find("p", {"class": "tweet-text"})
            timecontent = i.find('span', {"class":"_timestamp"})
            tweets.append(textcontent.get_text())
            date = timecontent.get_text()
            if (date[-4:-2] == '20'):
                times.append(date)
            else:
                times.append(date + " 2017")
                
   
    row.append(len(tweets))
    row.append(tweets)
    #row.append(len(times))
    row.append(times)
    
    #row.append(len(isreply))
    #row.append(isreply)
    return row

def findData(teams):
    table = []
    c = 0
    for f in teams:
        for t in teams:
            if t != f:
                table.append(getTweets(f,t))
                print(c)
                c = c + 1
    return table
    
result = findData(nbaSmall)
print("done")
df = pd.DataFrame(result)
print(df)
df.to_csv("nba-test.csv", sep=',')

driver.close()

