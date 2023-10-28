import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import random

teams = {'Boston' : 'BOS','Buffalo' : 'BUF','Detroit' : 'DET','Florida' : 'FLA','Montreal' : 'MON','Ottawa' : 'OTT','Tampa Bay' :  'TB','Toronto' : 'TOR','Arizona' : 'ARI','Chicago' : 'CHI','Colorado' : 'COL','Dallas' : 'DAL','Minnesota' : 'MIN','Nashville' : 'NSH','St. Louis' : 'STL','Winnipeg' : 'WPG','Carolina' : 'CAR','Columbus' : 'CLB','N.Y. Islanders' : 'NYI','N.Y. Rangers' : 'NYR','New Jersey' :  'NJ','Philadelphia' : 'PHI','Pittsburgh' : 'PIT','Washington' : 'WAS','Anaheim' : 'ANA','Calgary' : 'CGY','Edmonton' : 'EDM','Los Angeles' :  'LA','San Jose' :  'SJ','Seattle' : 'SEA','Vancouver' : 'VAN','Vegas' : 'VGK'}

def randomHeader():
    user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
    ]
    return random.choice(user_agents)

#function that returns an array of gamers that have taken place between a given date range
def getGames(startDate : int, endDate: int):
    tempDate = startDate # variable that can be ittereated 
    gamesList = [] # array where the games can be stored
    while tempDate <= endDate: # checks if we are still in the date range
        url = f'https://www.cbssports.com/nhl/schedule/{tempDate}' #base url
        headers = {'User-Agent': randomHeader()} # url header
        page = requests.get(url, headers=headers)
        soup = bs(page.content, 'html.parser') # converts the page to a beautifulsoup item
        games = soup.findAll('span', class_ = 'TeamName') # findas all the spans on the page with the class TeamName
        numberOfGames = len(games)/2 #calculate the number of gamers playied
        count = 1
        home,away = [],[]
        for game in games:
            if count % 2 == 0: home.append(game.text) #even count teams are saved to the home array
            else: away.append(game.text) #odd count teams are saved to the away array
            count+=1 #increments the count
        i=0
        while i < numberOfGames: #loops through the games
            gameID = f'{tempDate}{teams[away[i]]}@{teams[home[i]]}' #the ID is the date, away team code, @, home team code
            gamesList.append([teams[away[i]],teams[home[i]],gameID,tempDate]) # adds the game data to the game list array
            i+=1
        tempDate+=1 # moves date to be serched to the next date
    return gamesList # returns the list of games

def getWinners(startDate: int, endDate: int):
    tempDate = startDate # variable that can be ittereated 
    winners = []
    while tempDate <= endDate: # checks if we are still in the date range
        url = f'https://www.cbssports.com/nhl/schedule/{tempDate}' #base url
        headers = {'User-Agent': randomHeader()} # url header
        page = requests.get(url, headers=headers)
        soup = bs(page.content, 'html.parser') # converts the page to a beautifulsoup item
        scores = soup.findAll('div', class_ = 'CellGame') # findas all the spans on the page with the class TeamNam
        for score in scores:
            winners.append(score.text[:3].strip())
        tempDate +=1
    return winners

startDate = 20231010
endDate = 20231027
df = pd.DataFrame(getGames(startDate,endDate))
df = df.rename(columns={0:'visitors', 1:'home', 2:'gameID', 3:'gameDate'})
dfw = pd.DataFrame(getWinners(startDate, endDate))
dfw = dfw.rename(columns={0:'winner'})
df = pd.concat([df,dfw], axis=1, join='inner')
df = df.set_index('gameID')
df['gameDate'] = pd.to_datetime(df['gameDate'], format='%Y%m%d')

df.to_csv(f'{startDate}-{endDate}_games.csv')

print('Done: File Saved')