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
from backend.utils.solver_utils import print_tupledict

class Solver():
    def __init__(self, total_games: int, matchups: List[Tuple[Team, Team]]) -> None:
        # Writing the solver for the NFL for now, will generalize later

        self.m = gp.Model('mip1')
        self.total_games = total_games
        self.num_teams = 32
        self.total_weeks = 18
        self.matchups = matchups
        self.matchup_indices = self._sort_matrix(np.array([[nfl_teams_to_indices[m[0].team_name], 
                                          nfl_teams_to_indices[m[1].team_name]] for m in self.matchups]))
        debug(len(self.matchup_indices))
        self.per_team_matchups = {}
        for matchup in self.matchup_indices:
            for num in matchup:
                if num not in self.per_team_matchups.keys():
                    self.per_team_matchups[num] = []
                self.per_team_matchups[num].append(matchup)
        pprint(self.per_team_matchups)

        # Variables
        num_networks = 10
        self.networks = self.m.addVars(self.num_teams, self.total_weeks, lb=1, ub=num_networks, vtype=GRB.INTEGER) # Represents the network each game will be broadcasted on and at what time
        self.grid = self.m.addVars(self.num_teams, self.total_weeks, lb=-1, ub=31, vtype=GRB.INTEGER) # 32 teams, 18 weeks
        self.host = self.m.addVars(self.num_teams, self.total_weeks, lb=0, ub=1, vtype=GRB.BINARY) # Corresponding home/away matrix
        self.b = self.m.addMVar((32, 18), vtype=GRB.BINARY, name='intermediate_binary') # To make sure the bye weeks are synced
        self.bv = self.m.addMVar((2, 8), vtype=GRB.BINARY, name='binary_even_bye_week_helpers') # To make sure every week, there are an even number of teams getting a bye week
        

        # TODO: Next Steps
        # Set constraints to match up the matchups
        # Add cost for a few of the soft constraints
        # Run gurobi and validate

        # Setting Up optimization problem
        # self._add_cost()
        # self._add_constraints()

    def _add_cost(self):
        cost = self.grid.sum() + self.host.sum() + self.networks.sum()
        self.m.setObjective(cost, GRB.MINIMIZE)

    def _add_constraints(self):
        # Setting BYE Weeks to 0 in host and adding home/away total constraints
        C = 1e2
        for i in range(self.num_teams):
            # self.m.addConstr(self.host.sum(axis=1)[i] == home_games, name='num_home_games')
            self.m.addConstr(self.b[i, :].sum() == 17, name='team_total_games') # Every team plays 17 games

            for j in range(self.total_weeks):
                # If grid item is nonnegative, b should be 1; If grid item is negative, b should be 0
                self.m.addConstr(self.grid[i, j] >= -C * (1 - self.b[i, j]), name="nonneg_constraint")
                self.m.addConstr(self.grid[i, j] <= C * self.b[i, j] - 1e-6, name="neg_constraint")

                # # If value in self.grid is -1 (BYE Week), it should be 0 in host matrix
                self.m.addConstr((self.b[i, j] == 0) >> (self.host[i, j] == 0), name='binary_to_bye')

                # BYE Weeks should be on weeks 5-7, 9-12, 14
                if j+1 in [1, 2, 3, 4, 8, 13, 15, 16, 17, 18]:
                    self.m.addConstr(self.grid[i, j] >= 0, name='no_bye_week')
            
            home_games = 9 if NFL_TEAMS_DICT[indices_to_nfl_teams[i]].conference == 'NFC' else 8
            self.m.addConstr(self.host.sum(i, '*') == home_games)

        # There should be exactly 32 (576-32=544) BYE Weeks, 1 per row, 2, 4, or 6 per col
        self.m.addConstr(self.b.sum() == 544, name='exactly_32_BYE_weeks')
        list_indices = [5, 6, 7, 9, 10, 11, 12, 14] # When BYE weeks are given
        for j in range(len(list_indices)):
            col_sum = self.b[:, list_indices[j]-1].sum().item()
            bin_sum = self.bv[:, j].sum().item()
            self.m.addConstr(col_sum == 26 + 2*bin_sum)

            # In bye weeks, number of home teams are different
            host_col_sum = self.host.sum('*', list_indices[j]-1)
            self.m.addConstr(host_col_sum == 15 - bin_sum)

        for j in range(18): # In non-bye weeks, there will be 16 home games and 16 away
            if j + 1 not in list_indices:
                col_sum = self.host.sum('*', j)
                self.m.addConstr(col_sum == 16)

    def _sort_matrix(self, mat: np.array) -> np.array:
        sorted_mat = np.vstack((sorted([col for col in mat], key=lambda x: x[0])))
        return sorted_mat
    
    def solve(self):
        self.m.optimize()
        # Assuming x is your tupledict
        print_tupledict('NETWORKS', self.networks)
        print_tupledict('GRID', self.grid)
        print_tupledict('HOME/AWAY', self.host)
