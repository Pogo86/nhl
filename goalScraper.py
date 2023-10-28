import pandas as pd
import requests
import random
from bs4 import BeautifulSoup as bs

firstDate = 20231026
lastDate = 20231027

teams = {'Boston' : 'BOS','Buffalo' : 'BUF','Detroit' : 'DET','Florida' : 'FLA','Montreal' : 'MON','Ottawa' : 'OTT','Tampa Bay' :  'TB','Toronto' : 'TOR','Arizona' : 'ARI','Chicago' : 'CHI','Colorado' : 'COL','Dallas' : 'DAL','Minnesota' : 'MIN','Nashville' : 'NSH','St. Louis' : 'STL','Winnipeg' : 'WPG','Carolina' : 'CAR','Columbus' : 'CLB','N.Y. Islanders' : 'NYI','N.Y. Rangers' : 'NYR','New Jersey' :  'NJ','Philadelphia' : 'PHI','Pittsburgh' : 'PIT','Washington' : 'WAS','Anaheim' : 'ANA','Calgary' : 'CGY','Edmonton' : 'EDM','Los Angeles' :  'LA','San Jose' :  'SJ','Seattle' : 'SEA','Vancouver' : 'VAN','Vegas' : 'VGK'}

def rendomHeader():
    user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    ]
    return random.choice(user_agents)

#takes a start date and end dates and returns an array of urls for the play by play for each game in the time frame
def getGames(startDate, endDate):
    tempDate = startDate
    urls = []
    while tempDate <= endDate:
        url = f'https://www.cbssports.com/nhl/schedule/{tempDate}'
        headers = {'User-Agent': rendomHeader()}
        page = requests.get(url, headers=headers)
        playbyURL = f'https://www.cbssports.com/nhl/gametracker/playbyplay/NHL_{tempDate}_'

        soup = bs(page.content, 'html.parser')

        games = soup.findAll('span', class_ = 'TeamName')
        count = 0
        while count < len(games):
            game = f'{teams[games[count].text]}@{teams[games[count+1].text]}'
            urls.append([f'{playbyURL}{game}/',tempDate])
            count+=2
        tempDate+=1
    return urls

def getAssists(text):
    if len(text) == 1: return ['None', 'None']
    if '), ' in text[1]:
        #is an assist
        if 'Assist:' in text[1]:
            a1 = text[1].split('Assist: ')
            return [a1[1], 'None']
        else:
            ass = text[1].split('Assists: ')[1]
            ass = ass.split(' and ')
            a1 = ass[0]
            a2 = ass[1]
            return[a1,a2]
    else:
        return ['None', 'None']


def getGoalStats(game, gameDate, url):
    redTextGoal = game.find_all('span', class_='gametracker-row__item-red')
    goalCount = len(redTextGoal)
    goals = [] #list of all the goals scored
    for goal in redTextGoal:
        teams = url[-8:].replace('/','').replace('_','')#gets team ids from URL
        gameID = f'{gameDate}{teams}'
        p = goal.parent.parent.parent.parent.text[:3] #period the goal took place
        time = goal.previous_sibling.text #time goal was scored
        teamID = goal.previous_sibling.previous_sibling.text #the team ID

        if ' (' in goal.text:
            line = goal.text.split(' (')
        else:
            line = goal.text.split(' ,')
            
        scorer = line[0][5:]
        #the try section determins if there was any assists to the goal

        assists = getAssists(line)
        goalID = f'{gameDate}{time}{teamID}{goalCount}'
        goals.append([goalID, teamID, p, time, gameDate, scorer, assists,gameID])
        goalCount-=1
    return goals

def correctTime(time):
    if ':' in time: return time
    else: return f'00:{time[:2]}'
    
def calculateSeconds(time):
    split = time.split(':')
    mins = int(split[0]) * 60
    secs = int(split[1])
    return mins+secs

def periodTime(period):
    if period == '1ST': return 0
    if period == '2ND': return (20*60)
    if period == '3RD': return (40*60)
    if period == 'OVE': return (60*60)
    if period == 'SHO': return (65*60)


print('Getting Goals')
gameURLs = getGames(firstDate, lastDate)
allGoals = []
for url in gameURLs:
    headers = {'User-Agent': rendomHeader()}
    playbyplay = bs((requests.get(url[0], headers=headers)).content, 'html.parser')
    allGoals = allGoals + (getGoalStats(playbyplay,url[1],url[0]))

df = pd.DataFrame(allGoals)
df = df.rename(columns={0:'goalID', 1:'teamID', 2:'period', 3:'goalTime', 4:'goalDate', 5:'scorer', 6:'assists', 7:'gameID'})
df['goalDate'] = pd.to_datetime(df['goalDate'], format='%Y%m%d')

split = pd.DataFrame(df['assists'].to_list(), columns=['assist1', 'assist2'])
df = pd.concat([df, split], axis=1)
df = df.drop(['assists'], axis=1)
df = df.set_index(['goalID'])
df['goalTime'] = df['goalTime'].apply(correctTime) #converts time given in seconds to mins
df['seconds'] = df['goalTime'].apply(calculateSeconds)
df['periodTime'] = df['period'].apply(periodTime)
df['seconds'] = df['seconds'] + df['periodTime']
df = df.drop('periodTime', axis=1)
df.to_csv(f'{firstDate}-{lastDate}_goals.csv')

print('Done: File Saved')