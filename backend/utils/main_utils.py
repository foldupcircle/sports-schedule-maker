from typing import List
import pandas as pd

from team import Team
from backend.data.leagues import NFL_TEAMS_DICT, NBA_TEAMS_DICT, MLB_TEAMS_DICT, IPL_TEAMS_DICT, EPL_TEAMS_DICT
from backend.utils.debug import debug

def convert_teams_to_dict(teams: List[Team]):
    team_arr = [{'team_name': team.team_name, 
                 'home_stadium_name': team.home_stadium.name, 
                 'division': team.division, 
                 'conference': team.conference} 
                 for team in teams]
    return team_arr

def choose_league(league: str):
    teams = []
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

def determine_matchups(league: str):
    '''
    Generate all 272 games that need to happen, here's the breakdown
    1. 6 games against division opponents, home and away
    2. 4 games against every team in another div, same conf (rotates yearly) -> past_season_data.py
    3. 4 games against every team in another div, other conf (rotates yearly) -> past_season_data.py
    4. 2 games against teams from the other 2 divs within same conf (based on last year's standings)
    5. 1 game against a team from a div in the other conf (based on last year's standings)
        The conference that hosts this game rotates by year. 2024 is NFC
    '''
    league = 'NFL'
    teams, games = choose_league(league)
    debug(len(teams), games)

    total_games = (len(teams) * games) / 2
    debug(total_games)

    # Initially store as dictionary, so it's easy to check for dups
    matchups = {}

    for team in teams:
        matchups.append(())
