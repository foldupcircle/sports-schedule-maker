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
    def __init__(self, matchups: List[Tuple[Team, Team]], early_bye_week_teams: List[str]) -> None:
        self.m = gp.Model('mip1')
        self.matchup_indices = self._sort_matrix(np.array([[nfl_teams_to_indices[m[0].team_name], 
                                          nfl_teams_to_indices[m[1].team_name]] for m in matchups]))

        self.all_games = gp.tuplelist(create_matchup_tuplelist(self.matchup_indices))
        debug(self.all_games)

        self.early_bye_teams = [nfl_teams_to_indices[team_name] for team_name in early_bye_week_teams]
        debug(self.early_bye_teams)

        # Add Gurobi Variables
        self.games = self.m.addVars(self.all_games, vtype=GRB.BINARY) # Variables for all possible games
        self.bv = self.m.addMVar((2, 8), vtype=GRB.BINARY) # Helper binaries for 2, 4, 6 week bye week constraint

    def _add_cost(self):
        # Weights
        travel_weight = 1
        three_game_road_trip_weight = 10
        two_games_finish_weight = 5
        two_games_start = 5
        road_games_against_bye_weight = 5
        well_spread_division_series_weight = 1
        cost = gp.LinExpr()
        for team in range(32):
            cost += self.games.sum('*', team) # TODO: According to Figma
            
        self.m.setObjective(cost, GRB.MINIMIZE)

    def _add_constraints(self):
        self._add_bye_week_constraints()
        self._add_matchup_played_constraints()

    def _add_matchup_played_constraints(self):
        # Each matchup MUST be played once and only once
        self.m.addConstrs(self.games.sum(i, j, '*') for i, j in self.all_games)

        # Each Week MUST have 16 Games (BYEs Included)
        self.m.addConstrs(self.games.sum('*', '*', i) == 16 for i in range(18))

        # Each Team MUST play one and only one game every week
        self.m.addConstrs(self.games.sum('*', i, j) + self.games.sum(i, '*', j) for i in range(32) for j in range(18))

        # Last Week is all Divisional Games, Getting all divsional matchups
        division_matchups = []
        for matchup in self.matchup_indices:
            team1_div = NFL_TEAMS_DICT[indices_to_nfl_teams[matchup[0]]].division
            team2_div = NFL_TEAMS_DICT[indices_to_nfl_teams[matchup[1]]].division
            if team1_div == team2_div:
                division_matchups.append(matchup)
        total_div_games_last_week = gp.LinExpr()
        for teams in division_matchups:
            total_div_games_last_week += self.games.sum(teams[0], teams[1], 17)
        self.m.addConstr(total_div_games_last_week == 16)

    def _add_bye_week_constraints(self):
        # Weeks 1, 2, 3, 4, 8, 13, 15, 16, 17, 18 CAN’T have bye weeks
        non_bye_weeks = [1, 2, 3, 4, 8, 13, 15, 16, 17, 18]
        self.m.addConstrs(self.games.sum('*', -1, i) == 0 for i in non_bye_weeks)

        # Every team only has 1 bye week
        self.m.addConstrs(self.games.sum(i, -1, '*') == 1 for i in range(32))

        # Only 2, 4, or 6 teams on bye at a time
        bye_weeks = [5, 6, 7, 9, 10, 11, 12, 14]
        for i in range(8):
            bin_sum = self.bv[:, i].sum().item()
            self.m.addConstrs(self.games.sum('*', -1, bye_weeks[i]) == 30 - (2 * bin_sum))

        # Earliest bye week teams last year can’t get early bye this year (Week 5 is the earliest bye)
        self.m.addConstrs(self.games.sum(team, -1, 5) == 0 for team in self.early_bye_teams)
        
    def _sort_matrix(self, mat: np.array) -> np.array:
        sorted_mat = np.vstack((sorted([col for col in mat], key=lambda x: x[0])))
        return sorted_mat

    def solve(self):
        self.m.optimize()
        print_tupledict('ALL MATCHUPS', self.games)
