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
        self.matchup_indices = self._sort_matrix(np.array([[nfl_teams_to_indices[m[0].team_name], 
                                          nfl_teams_to_indices[m[1].team_name]] for m in self.matchups]))

        # variables
        self.m = self.opti.variable(total_games, 2) # Represents the 272 time slots that matchups can go into
        self.Z = self.opti.variable(32, 18) # 32 teams, 18 weeks

        # Setting Up optimization problem
        self._add_cost()
        self._add_constraints()

    def _add_cost(self):
        cost = 0
        
        self.opti.minimize(cost)

    def _add_constraints(self):
        # All matchups must come from the predetermined matchups and must be distinct
        test_matrix = ca.DM([
            [5, 10],
            [15, 20],
            [25, 30]
        ])
        debug(test_matrix[0, :])
        debug(self.matchup_indices == test_matrix[0, :])
        # for matchup in self.matchup_indices:
        #     debug(matchup)
        # self.opti.subject_to()

    def _sort_matrix(self, mat: np.array) -> ca.DM:
        sorted_mat = ca.vertcat(ca.DM((sorted([col for col in mat], key=lambda x: x[0]))))
        return sorted_mat
    
    def solve(self):
        self.opti.solver('ipopt')
        sol = self.opti.solve()
        # x_sol = sol.value(self.x)
        # return x_sol
    