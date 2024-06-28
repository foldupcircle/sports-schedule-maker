from datetime import date
import numpy as np

import pandas as pd
import nfl_data_py as nfl

from backend.generate_matchups import determine_matchups
from backend.utils.debug import debug
from backend.solver import Solver

def main():
    year = int(date.today().strftime('%Y'))
    matchups = determine_matchups('NFL', year)

    # TODO: more after
    # Explore whether AI or optimization is better approach
    # Explore gurobi, or maybe use casadi :eyes:
    solver = Solver(272, matchups)
    # x_sol, M_sol = solver.solve()
    # debug(x_sol)
    # debug(np.round(M_sol))


    # response = constraint_chain.invoke({'teams': json_teams, 'constraints': nfl_prompt})
    # print(response)
    # print(len(response.required_matchups))

if __name__ == '__main__':
    main()