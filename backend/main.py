import json
import nfl_data_py as nfl
import pandas as pd

from leagues import NFL_TEAMS_DICT, NBA_TEAMS_DICT, MLB_TEAMS_DICT, IPL_TEAMS_DICT, EPL_TEAMS_DICT
from ai_chains import constraint_chain
from test_prompts import nfl_prompt
from utils import convert_teams_to_dict, process_last_years_schedule

def main():
    # league = str(input('Enter League: '))
    league = 'NFL'
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
    print(len(teams), games)

    # json_teams = json.dumps(convert_teams_to_dict(teams))
    df = nfl.import_schedules([2023])
    # print(df.iloc[256])
    process_last_years_schedule(df)

    # response = constraint_chain.invoke({'teams': json_teams, 'constraints': nfl_prompt})
    # print(response)
    # print(len(response.required_matchups))

if __name__ == '__main__':
    main()