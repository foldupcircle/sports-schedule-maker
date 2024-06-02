from stadium import Stadium

class Team():
    def __init__(self, team_name: str, fanbase: int, division: str, home_stadium: Stadium) -> None:
        self.team_name = team_name
        self.fanbase = fanbase
        self.division = division
        self.home_stadium = home_stadium
        