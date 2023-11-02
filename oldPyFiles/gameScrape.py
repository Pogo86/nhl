import pandas as pd
import functions as fn

startDate = 20231028
endDate = 20231031

print(f'getting game data from {startDate} to {endDate}')

# gets the game data
df = pd.DataFrame(fn.getGames(startDate,endDate))
df = df.rename(columns={0:'visitors', 1:'home', 2:'gameID', 3:'gameDate'})
# gets the winner of each game
dfw = pd.DataFrame(fn.getWinners(startDate, endDate))
dfw = dfw.rename(columns={0:'winner'})
# joins the 2 tables
df = pd.concat([df,dfw], axis=1, join='inner')
# sets index to the game ID
df = df.set_index('gameID')
# sets the date to a date dtype
df['gameDate'] = pd.to_datetime(df['gameDate'], format='%Y%m%d')
# saves as a csv
df.to_csv(f'{startDate}-{endDate}_games.csv')

print('Done: File Saved')