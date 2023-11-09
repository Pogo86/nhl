import random
import requests
from bs4 import BeautifulSoup as bs

teams = {'Boston' : 'BOS','Buffalo' : 'BUF','Detroit' : 'DET','Florida' : 'FLA','Montreal' : 'MON','Ottawa' : 'OTT','Tampa Bay' :  'TB','Toronto' : 'TOR','Arizona' : 'ARI','Chicago' : 'CHI','Colorado' : 'COL','Dallas' : 'DAL','Minnesota' : 'MIN','Nashville' : 'NSH','St. Louis' : 'STL','Winnipeg' : 'WPG','Carolina' : 'CAR','Columbus' : 'CLB','N.Y. Islanders' : 'NYI','N.Y. Rangers' : 'NYR','New Jersey' :  'NJ','Philadelphia' : 'PHI','Pittsburgh' : 'PIT','Washington' : 'WAS','Anaheim' : 'ANA','Calgary' : 'CGY','Edmonton' : 'EDM','Los Angeles' :  'LA','San Jose' :  'SJ','Seattle' : 'SEA','Vancouver' : 'VAN','Vegas' : 'LV'}


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
            print(f'{"."*i}')
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


# returns a list of game URLS
def getGameURL(startDate, endDate):
    tempDate = startDate
    urls = []
    while tempDate <= endDate:
        url = f'https://www.cbssports.com/nhl/schedule/{tempDate}'
        headers = {'User-Agent': randomHeader()}
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

# decides if a goal has assists, and returns an array
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

# returns an array of goals for each game
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
        print(f'{"." * goalCount}')
        goalCount-=1
    return goals


def getGoals(firstDate, lastDate):
    gameURLs = getGameURL(firstDate, lastDate)
    allGoals = []
    for url in gameURLs:
        headers = {'User-Agent': randomHeader()}
        playbyplay = bs((requests.get(url[0], headers=headers)).content, 'html.parser')
        allGoals = allGoals + (getGoalStats(playbyplay,url[1],url[0]))
    return allGoals


# checks if a time is given in mm:ss format
def correctTime(time):
    if ':' in time: return time
    else: return f'00:{time[:2]}'

# converts from mm:ss format to a int in seconds
def calculateSeconds(time):
    split = time.split(':')
    mins = int(split[0]) * 60
    secs = int(split[1])
    return mins+secs

# calculates the period time
def periodTime(period):
    if period == '1ST': return 0
    if period == '2ND': return (20*60)
    if period == '3RD': return (40*60)
    if period == 'OVE': return (60*60)
    if period == 'SHO': return (65*60)

def conferenceConvert(c):
    c=c.lower()
    if c == 'w': return('Western')
    if c == 'e': return('Eastern')
    pass
def devisionConvert(d):
    d=d.lower()
    if d == 'a': return('Atlantic')
    if d == 'm': return('Metropolitan')
    if d == 'c': return('Central')
    if d == 'p': return('Pacific')
    pass