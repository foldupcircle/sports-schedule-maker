import gurobipy as gp
from gurobipy import GRB
import numpy as np
import scipy.sparse as sp
from typing import List, Tuple

from backend.data.solver_help import nfl_teams_to_indices, indices_to_nfl_teams
from backend.structure.team import Team
from backend.utils.debug import debug
from backend.data.leagues import NFL_TEAMS_DICT

class Solver():
    def __init__(self, total_games: int, matchups: List[Tuple[Team, Team]]) -> None:
        # Writing the solver for the NFL for now, will generalize later

        self.m = gp.Model('mip1')
        self.total_games = total_games
        self.matchups = matchups
        self.matchup_indices = self._sort_matrix(np.array([[nfl_teams_to_indices[m[0].team_name], 
                                          nfl_teams_to_indices[m[1].team_name]] for m in self.matchups]))

        # variables
        self.networks = self.m.addMVar((32, 18), 0, 31, vtype=GRB.INTEGER, name='network_time_slots') # Represents the network each game will be broadcasted on and at what time
        self.grid = self.m.addMVar((32, 18), -2, 31, vtype=GRB.INTEGER, name='weekly_schedule') # 32 teams, 18 weeks
        self.host = self.m.addMVar((32, 18), 0, 31, vtype=GRB.BINARY, name='home/away') # Corresponding home/away matrix

        # TODO: Next Steps
        # Set up basic constraints to match these variables up
        # Add cost for a few of the soft constraints
        # Run gurobi and validate

        # Setting Up optimization problem
        self._add_cost()
        self._add_constraints()

    def _add_cost(self):
        cost = self.grid.sum() + self.host.sum() + self.networks.sum()
        self.m.setObjective(cost, GRB.MAXIMIZE)

    def _add_constraints(self):
        # Setting BYE Weeks to 0 in host and adding home/away total constraints
        for i in range(self.host.shape[0]):
            home_games = 9 if NFL_TEAMS_DICT[indices_to_nfl_teams[i]].conference == 'NFC' else 8
            # debug(self.host[i, :].sum())
            debug(i)
            self.m.addConstr(self.host.sum(axis=1)[i] == home_games)
            for j in range(self.host.shape[1]):
                # Because of how piecewise functions work, I have to do this, add slack variable for -2 case
                self.m.addGenConstrPWL(self.grid[i, j], self.host[i, j], [-2, -1], [1, 0])

    def _sort_matrix(self, mat: np.array) -> np.array:
        sorted_mat = np.vstack((sorted([col for col in mat], key=lambda x: x[0])))
        return sorted_mat
    
    def solve(self):
        self.m.optimize()
        var_name = 'network_time_slots'
        debug(self.m.getVarByName(var_name))
        for v in self.m.getVars():
            if v.VarName.startswith(('week')):
                debug(v.VarName)
                debug(v.X)
