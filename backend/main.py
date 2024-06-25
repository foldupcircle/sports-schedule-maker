import json
from datetime import date

import pandas as pd
import nfl_data_py as nfl

from backend.data.leagues import NFL_TEAMS_DICT, NBA_TEAMS_DICT, MLB_TEAMS_DICT, IPL_TEAMS_DICT, EPL_TEAMS_DICT
from backend.utils.main_utils import convert_teams_to_dict
from backend.generate_matchups import determine_matchups
from backend.utils.debug import debug

def main():
    # league = str(input('Enter League: '))
    year = int(date.today().strftime('%Y'))

    # json_teams = json.dumps(convert_teams_to_dict(teams))
    df = nfl.import_schedules([2023])

    # TODO: 
    # Get standings from previous year
    # Determine which games need to be played

    matchups = determine_matchups('NFL', year)
    debug(matchups)

    # Determine 17th game for each team
    # Detemine final list of 272 regular season games

    # TODO: more after
    # Explore whether AI or optimization is better approach
    # Explore gurobi, or maybe use casadi :eyes:


    # response = constraint_chain.invoke({'teams': json_teams, 'constraints': nfl_prompt})
    # print(response)
    # print(len(response.required_matchups))

if __name__ == '__main__':
    main()