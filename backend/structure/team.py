from datetime import date

from structure.stadium import Stadium
from data.past_season_data import division_data

class Team():
    def __init__(self, team_name: str, fanbase: int, division: str, home_stadium: Stadium) -> None:
        self.team_name = team_name
        self.fanbase = fanbase
        self.division = division
        self.home_stadium = home_stadium
        self.conference = self._set_conference(division)
        if self.conference == 'NFC' or self.conference == 'AFC':
            self.inter_conference = self._set_inter_conference_division(division)
            self.intra_conference = self._set_intra_conference_division(division)

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
        
    def _set_inter_conference_division(self, division: str):
        return division_data['inter_conference'][division][3]
    
    def _set_intra_conference_division(self, division: str) -> str:
        return division_data['intra_conference'][division][2]
    
    def year_intra_conf(self, year: int):
        current_year = int(date.today().strftime('%Y'))
        # There are edge cases here to solve, will do later
        return division_data['intra_conference'][self.division][(current_year - year - 1) % 3] # Assuming 2024 is current year