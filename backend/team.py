from stadium import Stadium

class Team():
    def __init__(self, team_name: str, fanbase: int, division: str, home_stadium: Stadium) -> None:
        self.team_name = team_name
        self.fanbase = fanbase
        self.division = division
        self.home_stadium = home_stadium
        if division.startswith('Western Conference'): # NBA
            self.conference = 'Western Conference'
        elif division.startswith('Eastern Conference'): # NBA
            self.conference = 'Eastern Conference'
        #TODO 
        # Finish Conference or just make gpt write it out
        