SELECT 
goalDate,
count(DISTINCT gameID) as games,
count(*) as goals,
(cast(count(goalDate) as float) / CAST (count(DISTINCT gameID) as float)) as goalsPerGame
from nhl.dbo.goals g
GROUP BY goalDate 
ORDER by goalDate 