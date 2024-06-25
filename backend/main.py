from datetime import date

import pandas as pd
import nfl_data_py as nfl

from backend.generate_matchups import determine_matchups
from backend.utils.debug import debug

def main():
    year = int(date.today().strftime('%Y'))
    matchups = determine_matchups('NFL', year)

    # TODO: more after
    # Explore whether AI or optimization is better approach
    # Explore gurobi, or maybe use casadi :eyes:


    # response = constraint_chain.invoke({'teams': json_teams, 'constraints': nfl_prompt})
    # print(response)
    # print(len(response.required_matchups))

if __name__ == '__main__':
    main()