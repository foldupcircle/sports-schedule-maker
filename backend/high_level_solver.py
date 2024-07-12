import gurobipy as gp
from gurobipy import GRB
import numpy as np
from typing import List, Tuple
from pprint import pprint
from math import exp

from backend.data.solver_help import nfl_teams_to_indices, indices_to_nfl_teams
from backend.structure.team import Team
from backend.utils.debug import debug
from backend.data.leagues import NFL_TEAMS_DICT
from backend.utils.solver_utils import (
    print_tupledict, 
    print_tupledict_3, 
    create_matchup_tuplelist, 
    haversine, 
    get_team_home_stadium
)

class HighLevelSolver():
    def __init__(self, matchups: List[Tuple[Team, Team]], early_bye_week_teams: List[str]) -> None:
        self.m = gp.Model('mip1')
        self.matchup_indices = self._sort_matrix(np.array([[nfl_teams_to_indices[m[0].team_name], 
                                          nfl_teams_to_indices[m[1].team_name]] for m in matchups]))

        self.all_games = gp.tuplelist(create_matchup_tuplelist(self.matchup_indices))
        debug(len(self.all_games))
        # debug(self.all_games)

        self.early_bye_teams = [nfl_teams_to_indices[team_name] for team_name in early_bye_week_teams]
        debug(self.early_bye_teams)

        # Add Gurobi Variables
        self.games = self.m.addVars(self.all_games, vtype=GRB.BINARY) # Variables for all possible games
        self.bv = self.m.addMVar((2, 8), vtype=GRB.BINARY) # Helper binaries for 2, 4, 6 week bye week constraint
        
        self._set_helpers()
        self._add_constraints()
        self._add_cost()

    def _set_weights(self, travel: float, 
                     three_game_road_trip: float, 
                     two_games_start: float,
                     two_games_finish: float,
                     road_games_against_bye: float,
                     well_spread_division_series: float):
        self.travel_weight = travel
        self.three_game_road_trip_weight = three_game_road_trip
        self.two_games_finish_weight = two_games_finish
        self.two_games_start_weight = two_games_start
        self.road_games_against_bye_weight = road_games_against_bye
        self.well_spread_division_series_weight = well_spread_division_series

    def _set_helpers(self):
        self.sigmoid_2_5 = lambda x: 1 / (1 + exp(-10000 * (x - 2.5)))
        self.two_game_formula = lambda x, y: 1 - ((x - y)**2)

    def _get_distance(self, team, w):
        potential_away_games = [game for game in self.all_games 
                                if (game[0] == team or game[1] == team) and game[2] == w]
        location_lat = 0
        location_lon = 0
        for home_team_idx, away_team_idx, _ in potential_away_games:
            game_loc = get_team_home_stadium(home_team_idx)
            var = self.games.select(home_team_idx, away_team_idx, w)[0]
            location_lat += var * game_loc[0]
            location_lon += var * game_loc[1]
        return location_lat, location_lon

    def _add_cost(self):
        cost = gp.LinExpr()
        for team in range(32):
            # Travel Time Calculation
            travel_distance = 0
            current_loc = self._get_location(team, 0)
            for w in range(17):
                next_loc = self._get_location(team, w)
                travel_distance += haversine(current_loc, next_loc)

                # Set the current location to next week's location for next iteration
                current_loc = next_loc

                # 3-game Road Trip Cost
                if w <= 16:
                    sum_three_games = self.games.sum('*', team, w)
                    sum_three_games += self.games.sum('*', team, w + 1)
                    sum_three_games += self.games.sum('*', team, w + 2)
                    cost += self.three_game_road_trip_weight * self.sigmoid_2_5(sum_three_games)

                # Min teams playing road gm. ag. teams coming off bye
                first_game = self.games.sum(team, -1, w)
                second_game = self.games.sum(team, '*', w)
                cost += self.road_games_against_bye_weight * self.two_game_formula(first_game, second_game)

            # 2-game road start
            first_game = self.games.sum('*', team, 0)
            second_game = self.games.sum('*', team, 1)
            cost += self.two_games_start_weight * self.two_game_formula(first_game, second_game)

            # 2-game road finish
            first_game = self.games.sum('*', team, 16)
            second_game = self.games.sum('*', team, 17)
            cost += self.two_games_finish_weight * self.two_game_formula(first_game, second_game)
            
            # Add travel to cost
            cost += self.travel_weight * travel_distance

        self.m.setObjective(cost, GRB.MINIMIZE)

    def _add_constraints(self):
        self._add_bye_week_constraints()
        self._add_matchup_played_constraints()

    def _add_matchup_played_constraints(self):
        # Each matchup MUST be played once and only once
        self.m.addConstrs(self.games.sum(i, j, '*') == 1 for i, j, _ in self.all_games)

        # Each Week MUST have 16 Games (BYEs Included)
        self.m.addConstrs(self.games.sum('*', '*', i) == 16 for i in range(18))

        # Each Team MUST play one and only one game every week
        self.m.addConstrs(self.games.sum('*', i, j) + self.games.sum(i, '*', j) == 1 for i in range(32) for j in range(18))

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
            debug(bye_weeks[i])
            self.m.addConstr(self.games.sum('*', -1, bye_weeks[i] - 1) == (30 - (2 * bin_sum)))

        # Earliest bye week teams last year can’t get early bye this year (Week 5 is the earliest bye)
        self.m.addConstrs(self.games.sum(team, -1, 5) == 0 for team in self.early_bye_teams)
        
    def _sort_matrix(self, mat: np.array) -> np.array:
        sorted_mat = np.vstack((sorted([col for col in mat], key=lambda x: x[0])))
        return sorted_mat

    def solve(self):
        self.m.optimize()
        # print_tupledict_3('ALL MATCHUPS', self.games)
