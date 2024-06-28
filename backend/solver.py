import gurobipy as gp
from gurobipy import GRB
import numpy as np
import scipy.sparse as sp
from typing import List, Tuple

from backend.data.solver_help import nfl_teams_to_indices, indices_to_nfl_teams
from backend.structure.team import Team
from backend.utils.debug import debug

class Solver():
    def __init__(self, total_games: int, matchups: List[Tuple[Team, Team]]) -> None:
        # Writing the solver for the NFL for now, will generalize later

        self.m = gp.Model('mip1')
        self.total_games = total_games
        self.matchups = matchups
        self.matchup_indices = self._sort_matrix(np.array([[nfl_teams_to_indices[m[0].team_name], 
                                          nfl_teams_to_indices[m[1].team_name]] for m in self.matchups]))

        # variables
        self.time_slots = self.m.addMVar((272, 2), vtype=GRB.INTEGER) # Represents the 272 time slots that matchups can go into
        self.grid = self.m.addMVar((32, 18), vtype=GRB.INTEGER) # 32 teams, 18 weeks
        self.host = self.m.addMVar((32, 18), vtype=GRB.INTEGER) # Corresponding home/away matrix

        # TODO: Next Steps
        # Set up basic constraints to match these variables up
        # Add cost for a few of the soft constraints
        # Run gurobi and validate

        # Setting Up optimization problem
        self._add_cost()
        self._add_constraints()

    def _add_cost(self):
        pass

    def _add_constraints(self):
        pass

    def _sort_matrix(self, mat: np.array) -> np.array:
        sorted_mat = np.vstack((sorted([col for col in mat], key=lambda x: x[0])))
        debug(sorted_mat)
        return sorted_mat
    
    def solve(self):
        pass    