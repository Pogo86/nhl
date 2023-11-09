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

    def get_fullName(self):
        return f'{self.first} {self.last}'
    
    def set_goal(self):
        self.goals +=1

    def get_goals(self):
        return(self.goals)
    
    def get_team(self):
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
        self.gamePlayed = 0
        self.gameWon = 0
        self.gameLoss = 0
        self.otLoss = 0
        self.points = 0

    def __str__(self):
        return (f'Team Name : {self.name}, Points : {self.points}\nDevision : {self.devision}, Confrence :{self.confrene} \nGames Played {self.gamePlayed}, won {self.gameWon}, lossed {self.gameLoss}, Overtime Losses {self.otLoss} \nWin percentage of {self.get_winPercent()}')

    def set_goal(self, amount):
        self.goals += amount


    def set_Result(self, finish):
        if finish == 'w':
            self.points += 2
            self.gameWon +=1
        if finish == 'otl':
            self.points +=1
            self.otLoss +=1
        if finish == 'l':
            self.gameLoss +=1
        self.gamePlayed +=1

    def get_Result(self):
        return self.name, self.gameWon, self.gameLoss, self.otLoss
    
    def get_points(self):
        return self.points
    
    def get_winPercent(self):
        return self.gameWon / self.gamePlayed
        
    def get_devision(self):
        return self.devision
    
    def get_confrene(self):
        return self.confrene
    
    def get_id(self):
        return self.ID