import casadi as ca
import numpy as np
from typing import List, Tuple

from backend.data.solver_help import nfl_teams_to_indices, indices_to_nfl_teams
from backend.structure.team import Team
from backend.utils.debug import debug

class Solver():
    def __init__(self, total_games: int, matchups: List[Tuple[Team, Team]]) -> None:
        # Writing the solver for the NFL for now, will generalize later

        self.opti = ca.Opti()
        self.total_games = total_games
        self.matchups = matchups
        self.matchup_indices = np.array([[nfl_teams_to_indices[m[0].team_name], 
                                          nfl_teams_to_indices[m[1].team_name]] for m in self.matchups])

        # variables
        self.x = self.opti.variable(total_games, 2) # Represents the 272 time slots that matchups can go into
        self.Z = self.opti.variable(32, 18) # 32 teams, 18 weeks

        # Setting Up optimization problem
        self._add_cost()
        self._add_constraints()

    def _add_cost(self):
        cost = 0
        
        self.opti.minimize(cost)
        self.opti.set_initial(self.x, 5)

    def _add_constraints(self):
        def sorted_matrices(mat): # TODO: write code to sort a matrix's cols
            return ca.vertcat()
        self.opti.subject_to(self.x >= 1)

    def solve(self):
        self.opti.solver('ipopt')
        sol = self.opti.solve()
        x_sol = sol.value(self.x)
        return x_sol
    