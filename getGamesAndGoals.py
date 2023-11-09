import pandas as pd
import functions as fn

startDate = 20231010
endDate = 20231108

print(f'getting game data from {startDate} to {endDate}')

# gets the game data
df = pd.DataFrame(fn.getGames(startDate,endDate))
df = df.rename(columns={0:'visitors', 1:'home', 2:'gameID', 3:'gameDate'})
# gets the winner of each game
dfw = pd.DataFrame(fn.getWinners(startDate, endDate))
dfw = dfw.rename(columns={0:'winner'})
# joins the 2 tables
df = pd.concat([df,dfw], axis=1, join='inner')
# checks for SO
dfot = pd.DataFrame(fn.getOT(startDate, endDate))
dfot = dfot.rename(columns={0:'SO'})
# joins the 2 tables
df = pd.concat([df,dfot], axis=1, join='inner')
# sets index to the game ID
df = df.set_index('gameID')
# sets the date to a date dtype
df['gameDate'] = pd.to_datetime(df['gameDate'], format='%Y%m%d')
# saves as a csv
df.to_csv(f'{startDate}-{endDate}_games.csv')

print('Done: Game Data Saved')
print('.......................................................')
print(f'getting goal data from {startDate} to {endDate}')
'''
# gets the data for all goals in the time frame
df = pd.DataFrame(fn.get_goals(startDate,endDate))
# renames columns
df = df.rename(columns={0:'goalID', 1:'teamID', 2:'period', 3:'goalTime', 4:'goalDate', 5:'scorer', 6:'assists', 7:'gameID'})
# sets goalDate to a date Dtype
df['goalDate'] = pd.to_datetime(df['goalDate'], format='%Y%m%d')
# create a temp table to split the assisst into 2 columns
split = pd.DataFrame(df['assists'].to_list(), columns=['assist1', 'assist2'])
# joint to temp table to the original
df = pd.concat([df, split], axis=1)
# drops the old assists column
df = df.drop(['assists'], axis=1)
# sets the goalID column as the table index
df = df.set_index(['goalID'])
# converts times given in only seconds 'ss' to mins 'mm:ss'
df['goalTime'] = df['goalTime'].apply(fn.correctTime) 
# caculates the goal time in seconds
df['seconds'] = df['goalTime'].apply(fn.calculateSeconds)
# takes the period and retuns an amount of seconds
df['periodTime'] = df['period'].apply(fn.periodTime)
# adds the poeriod time to the seconds timne
df['seconds'] = df['seconds'] + df['periodTime']
# drops the period time column
df = df.drop('periodTime', axis=1)
#n saves file
df.to_csv(f'{startDate}-{endDate}_goals.csv')

print('Done: Goal data saved')'''