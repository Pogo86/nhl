SELECT 
DISTINCT gl.gameID,
gl.goalDate as gameDate,
gl.teamID,
count(gl.teamID) as goals,
ga.winner 
from nhl.dbo.goals gl
join nhl.dbo.game ga on gl.gameID = ga.gameID  
GROUP by gl.gameID, gl.teamID, gl.goalDate, ga.winner 
ORDER BY gl.goalDate, gl.gameID, gl.teamID 