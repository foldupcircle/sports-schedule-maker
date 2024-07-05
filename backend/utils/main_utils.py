from typing import List, Tuple, Dict
import pandas as pd

from backend.structure.team import Team
from backend.data.nfl_teams_abb import nfl_teams_abb
from backend.utils.debug import debug
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

def check_matchup(schedule: pd.DataFrame, home_team_name: str, away_team_name: str) -> bool:
    '''
    Check if the match between the two teams with one being home and other being away happened in the given schedule
    '''
    home_team_name = nfl_teams_abb[home_team_name]
    away_team_name = nfl_teams_abb[away_team_name]
    game = schedule.loc[(schedule['home_team'] == home_team_name) & 
                        (schedule['game_type'] == 'REG') & 
                        (schedule['away_team'] == away_team_name)]
    if game.empty: return False
    elif len(game) == 1: return True
    else: raise ValueError('There must be 0 or 1 occurences of this game. Expected value received.')
    
# def
#     self.per_team_matchups = {}
#         for matchup in self.matchup_indices:
#             for num in matchup:
#                 if num not in self.per_team_matchups.keys():
#                     self.per_team_matchups[num] = []
#                 self.per_team_matchups[num].append(matchup)