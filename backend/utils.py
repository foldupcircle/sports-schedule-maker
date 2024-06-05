import pprint
from typing import List
import pandas as pd

from team import Team
from leagues import NFL_TEAMS_DICT

def convert_teams_to_dict(teams: List[Team]):
    team_arr = [{'team_name': team.team_name, 
                 'home_stadium_name': team.home_stadium.name, 
                 'division': team.division, 
                 'conference': team.conference} 
                 for team in teams]
    return team_arr

def process_last_years_schedule(df: pd.DataFrame) -> None:
    print(df.tail())
    print(df.iloc[100])
    
    for i in df.shape[0]:
        if df.iloc[i].game_type != 'REG':
            continue
        

