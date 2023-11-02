import pandas as pd
import functions as fn
import requests
from bs4 import BeautifulSoup as bs

firstDate = 20231027
lastDate = 20231031

teams = {'Boston' : 'BOS','Buffalo' : 'BUF','Detroit' : 'DET','Florida' : 'FLA','Montreal' : 'MON','Ottawa' : 'OTT','Tampa Bay' :  'TB','Toronto' : 'TOR','Arizona' : 'ARI','Chicago' : 'CHI','Colorado' : 'COL','Dallas' : 'DAL','Minnesota' : 'MIN','Nashville' : 'NSH','St. Louis' : 'STL','Winnipeg' : 'WPG','Carolina' : 'CAR','Columbus' : 'CLB','N.Y. Islanders' : 'NYI','N.Y. Rangers' : 'NYR','New Jersey' :  'NJ','Philadelphia' : 'PHI','Pittsburgh' : 'PIT','Washington' : 'WAS','Anaheim' : 'ANA','Calgary' : 'CGY','Edmonton' : 'EDM','Los Angeles' :  'LA','San Jose' :  'SJ','Seattle' : 'SEA','Vancouver' : 'VAN','Vegas' : 'VGK'}

df = pd.DataFrame(fn.getGoals(firstDate,lastDate))
df = df.rename(columns={0:'goalID', 1:'teamID', 2:'period', 3:'goalTime', 4:'goalDate', 5:'scorer', 6:'assists', 7:'gameID'})
df['goalDate'] = pd.to_datetime(df['goalDate'], format='%Y%m%d')

split = pd.DataFrame(df['assists'].to_list(), columns=['assist1', 'assist2'])
df = pd.concat([df, split], axis=1)
df = df.drop(['assists'], axis=1)
df = df.set_index(['goalID'])
df['goalTime'] = df['goalTime'].apply(fn.correctTime) #converts time given in seconds to mins
df['seconds'] = df['goalTime'].apply(fn.calculateSeconds)
df['periodTime'] = df['period'].apply(fn.periodTime)
df['seconds'] = df['seconds'] + df['periodTime']
df = df.drop('periodTime', axis=1)
df.to_csv(f'{firstDate}-{lastDate}_goals.csv')

print('Done: File Saved')