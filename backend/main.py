from datetime import date
import numpy as np

import pandas as pd
import nfl_data_py as nfl

from generate_matchups import determine_matchups
from utils.debug import debug
from old_solver import OldSolver
from high_level_solver import HighLevelSolver
from utils.solver_utils import get_formatted_matchups

def main():
    # year = int(date.today().strftime('%Y'))
    year = 2024
    matchups = determine_matchups('NFL', year)
    early_bye_teams_2023 = [
        'Cleveland Browns',
        'Los Angeles Chargers',
        'Seattle Seahawks',
        'Tampa Bay Buccaneers'
    ]
    # TODO: more after
    # Explore whether AI or optimization is better approach
    # Explore gurobi, or maybe use casadi :eyes:
    solver = HighLevelSolver(matchups, early_bye_teams_2023)
    solver.solve()
    results = get_formatted_matchups(solver.all_games, solver.games)
    # debug(x_sol)
    # debug(np.round(M_sol))
    
    return results
    # response = constraint_chain.invoke({'teams': json_teams, 'constraints': nfl_prompt})
    # print(response)
    # print(len(response.required_matchups))

if __name__ == '__main__':
    main()
