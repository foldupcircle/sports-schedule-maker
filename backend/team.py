from stadium import Stadium

class Team():
    def __init__(self, team_name: str, fanbase: int, division: str, home_stadium: Stadium) -> None:
        self.team_name = team_name
        self.fanbase = fanbase
        self.division = division
        self.home_stadium = home_stadium
        self.conference = self._set_conference(self.division)
        

    def _set_conference(self, division: str) -> None:
        if division.startswith('NFC'): # NFL
            return 'NFC'
        elif division.startswith('AFC'): # NFL
            return 'AFC'
        elif division.startswith('Western Conference'): # NBA
            return 'Western Conference'
        elif division.startswith('Eastern Conference'): # NBA
            return 'Eastern Conference'
        elif division.startswith('NL'):  # MLB
            return 'National League'
        elif division.startswith('AL'):  # MLB
            return 'American League'
        elif division == 'IPL':  # IPL doesn't have conferences, but we'll treat it uniformly
            return 'IPL'
        elif division == 'Premier League':  # EPL doesn't have conferences, but we'll treat it uniformly
            return 'Premier League'
        else:
            return 'Other'  # For any divisions not covered above or to handle unexpected inputs
        
