import pip


pip.main(['install','birdy'])
pip.main(['install','bs4'])

from bs4 import BeautifulSoup
from birdy.twitter import UserClient
import requests

CONSUMER_KEY = 	'HYPw5GfsyGWkRu5e4wDV5dxXT'
CONSUMER_SECRET = 'fq7OQnRpU7ZiIw4x64gr046qV4gyc8axqG4SkVUjTAOoqXxIop'
ACCESS_TOKEN = '214745075-xq2gmGnOy0B4mglHoUDKdu3VZi06MTtVsiTjKwV0'
ACCESS_TOKEN_SECRET = 'bXvLzi1onSijRcmNwtdOtARNwJz2dsJp8cGZds1NK03K9'
client = UserClient(CONSUMER_KEY,
                    CONSUMER_SECRET,
                    ACCESS_TOKEN,
                    ACCESS_TOKEN_SECRET)

#response = client.api.users.show.get(screen_name='capitals')
#response.data

nba = ['okcthunder','celtics','NYKnicks','BrooklynNets','PelicansNBA', 'Pacers', 'OrlandoMagic','Timberwolves','MiamiHEAT',
'Hornets', 'DetroitPistons', 'DallasMavs', 'LAClippers', 'Lakers', 'UtahJazz', 'nuggets', 'WashWizards', 'ChicagoBulls',
'spurs', 'Suns', 'HoustonRockets', 'Warriors', 'ATLHawks', 'MemGrizz', 'Bucks', 'Raptors', 'SacramentoKings', 'Sixers', 'trailblazers'];



page = requests.get("https://twitter.com/search?q=from%3Apacers%20%40trailblazers&src=typd")

soup = BeautifulSoup(page.content, 'html.parser')
#table = soup.find_all('div', class_="stream-items")

print(table.prettify())