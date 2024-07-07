import gurobipy as gp
from gurobipy import GRB
import numpy as np
import scipy.sparse as sp
from typing import List, Tuple
from pprint import pprint

from backend.data.solver_help import nfl_teams_to_indices, indices_to_nfl_teams
from backend.structure.team import Team
from backend.utils.debug import debug
from backend.data.leagues import NFL_TEAMS_DICT
from backend.utils.solver_utils import print_tupledict, create_matchup_tuplelist

class HighLevelSolver():
    def __init__(self, matchups: List[Tuple[Team, Team]]) -> None:
        self.m = gp.Model('mip1')
        self.matchups = matchups
        self.matchup_indices = self._sort_matrix(np.array([[nfl_teams_to_indices[m[0].team_name], 
                                          nfl_teams_to_indices[m[1].team_name]] for m in self.matchups]))

        all_matchup_possibilities = create_matchup_tuplelist(self.matchup_indices)
        debug(all_matchup_possibilities)

    def _add_cost(self):
        pass

    def _add_constraints(self):
        pass

    def _sort_matrix(self, mat: np.array) -> np.array:
        sorted_mat = np.vstack((sorted([col for col in mat], key=lambda x: x[0])))
        return sorted_mat

    def solve(self):
        pass