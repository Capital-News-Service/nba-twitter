# Jake Gluck - Capital News Service

#import libraries
import pandas as pd

#load twitter conv data gathered by the scraper
df = pd.read_csv('/Users/jagluck/Documents/GitHub/nba-twitter/nba-conv.csv')

#coverts to list of strings
def convertType(toConv):

    toConv = toConv.str.replace("'", "")
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
  
# convert types  
df = df.drop(['Unnamed: 0'], axis=1)
    
df['names'] = convertType(df['names'])


#Stats about size of conversations
df['size'].describe()

def countContains(toCount, data):
    count = 0
    for x in data:
        if toCount in x:
            count = count + 1
    return count
    
print(countContains('Bucks', df['names']))
    


