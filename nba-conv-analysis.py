# Jake Gluck - Capital News Service - jagluck.github.io

#import libraries
import pandas as pd
import numpy as np

#load twitter conv data gathered by the scraper
df = pd.read_csv('/Users/jagluck/Documents/GitHub/nba-twitter/nba-conv.csv')

NBACAPS = {'CAVS','OKCTHUNDER','CELTICS','NYKNICKS','BROOKLYNNETS','PELICANSNBA', 'PACERS', 'ORLANDOMAGIC','TIMBERWOLVES','MIAMIHEAT',
'HORNETS', 'DETROITPISTONS', 'DALLASMAVS', 'LACLIPPERS', 'LAKERS', 'UTAHJAZZ', 'NUGGETS', 'WASHWIZARDS', 'CHICAGOBULLS',
'SPURS', 'SUNS', 'HOUSTONROCKETS', 'WARRIORS', 'ATLHAWKS', 'MEMGRIZZ', 'BUCKS', 'RAPTORS', 'SACRAMENTOKINGS', 'SIXERS', 'TRAILBLAZERS'}

#coverts to list of strings
def convertType(toConv, makeUpper):

    toConv = toConv.str.replace("'", "")
    toConv = toConv.str.replace("@", " ")
    
    if makeUpper:
        toConv = toConv.str.upper()
          
    toConv = toConv.str.strip("[]")
    toConv = toConv.str.split(',')
    
    count1 = 0
    for x in toConv:
        count2 = 0
        for y in x:
            toConv[count1][count2] = y.strip()
            count2 = count2 + 1
        count1 = count1 + 1
        
    return toConv

# Helper: counts time value is in list of lists
def countContains(toCount, data):
    count = 0
    for x in data:
        if toCount in x:
            count = count + 1
    return count

# Helper: stores value when value in list of list is found
def countLengths(toCount, data1, data2):
    count = []
    for x, y in zip(data1, data2):
        if toCount in x:
            count.append(y)
    return np.mean(count)
    
# convert types  
df = df.drop(['Unnamed: 0'], axis=1)
df = df.drop(['to'], axis=1)
df = df.drop(['from'], axis=1)
df['names'] = convertType(df['names'], False)
df['usernames'] = convertType(df['usernames'], True)
                
## What is the typical converation size? ##########
df['size'].describe()

### What teams Tweet the most #######
names = []
participations = []
lengths = []
for name in NBACAPS:
    names.append(name)
    participations.append(countContains(name,df['usernames']))
    lengths.append(countLengths(name,df['usernames'],df['size']))

teams = pd.DataFrame(
        {'name': names,
         'participation': participations,
         'avg_lengths': lengths
        })
    
teams = teams.sort_values(by='participation', ascending=False)
print(teams)

#What teams have the longest and shortest conversations
teams = teams.sort_values(by='avg_lengths', ascending=False)
print(teams)

#What teams talk to other teams the most/least? 

def countDuoConvos(name, name2):
    count = 0
    for x in df['usernames']:
        if name in x:
            if name2 in x:
                count = count + 1
    return count
 
tos = []
froms = []
convo_counts = []

for name in NBACAPS:
    for name2 in NBACAPS:
        if name != name2:
            tos.append(name)
            froms.append(name2)
            convo_counts.append(countDuoConvos(name, name2))
                
convos = pd.DataFrame(
        {'to': tos,
         'from': froms,
         'convo_count': convo_counts
        })
 
convos = convos.sort_values(by='convo_count', ascending=False)       
print(convos)

