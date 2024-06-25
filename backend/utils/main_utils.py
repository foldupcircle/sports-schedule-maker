from typing import List, Tuple, Dict
import pandas as pd

from backend.structure.team import Team
from backend.data.leagues import NFL_TEAMS_DICT, NBA_TEAMS_DICT, MLB_TEAMS_DICT, IPL_TEAMS_DICT, EPL_TEAMS_DICT

def convert_teams_to_dict(teams: List[Team]):
    team_arr = [{'team_name': team.team_name, 
                 'home_stadium_name': team.home_stadium.name, 
                 'division': team.division, 
                 'conference': team.conference} 
                 for team in teams]
    return team_arr

def choose_league(league: str) -> Tuple[Dict[str, Team], int]:
    teams = {}
    games = 0
    if league == 'NFL':
        teams = NFL_TEAMS_DICT
        games = 17
    elif league == 'NBA':
        teams = NBA_TEAMS_DICT
        games = 82
    elif league == 'MLB':
        teams = MLB_TEAMS_DICT
        games = 162
    elif league == 'IPL':
        teams = IPL_TEAMS_DICT
        games = 14
    elif league == 'EPL':
        teams = EPL_TEAMS_DICT
        games = 38
    else:
        raise ValueError('Input must be one of: NFL, NBA, MLB, IPL, EPL')
    return teams, games
