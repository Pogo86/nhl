class Player:
    def __init__(self,playerID,first,last,number,position,shot,height,weight,dob,birthplace,team):
        self.ID = playerID
        self.first = first
        self.last = last
        self.number = number
        self.position = position
        self.shot = shot
        self.height = height
        self.weight = weight
        self.dob = dob
        self.birthplace = birthplace
        self.team = team
        self.goals = 0

    def fullName(self):
        return f'{self.first} {self.last}'
    
    def addGoal(self):
        self.goals +=1

    def getGoals(self):
        return(self.goals)
    
    def getTeam(self):
        return(self.team)

    @classmethod
    def from_list(cls, player_list):
        playerID = player_list[0]
        first = player_list[1]
        last = player_list[2]
        number = player_list[3]
        position = player_list[4]
        shot = player_list[5]
        height = player_list[6]
        weight = player_list[7]
        dob = player_list[8]
        birthplace = player_list[9]
        team = player_list[10]
        return cls(playerID,first,last,number,position,shot,height,weight,dob,birthplace,team)
    

class Team:
    def __init__(self,teamID,teamName, cofrence, devision):
        self.ID = teamID
        self.name = teamName
        self.confrene = cofrence
        self.devision = devision
        self.goals = 0
        self.points = 0

    def incrementGoal(self, amount):
        self.goals += amount
    def incrementScore(self, finish):
        if finish == 'w':self.points += 2
        if finish == 'otl':self.points +=1
        