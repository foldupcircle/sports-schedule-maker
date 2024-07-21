import gurobipy as gp
from gurobipy import GRB
import numpy as np
from typing import List, Tuple
from pprint import pprint
from math import e

from data.solver_help import nfl_teams_to_indices, indices_to_nfl_teams
from structure.team import Team
from utils.debug import debug
from data.leagues import NFL_TEAMS_DICT
from utils.solver_utils import (
    print_tupledict, 
    print_tupledict_3, 
    create_matchup_tuplelist, 
    haversine, 
    get_team_home_stadium
)

class HighLevelSolver():
    def __init__(self, matchups: List[Tuple[Team, Team]], early_bye_week_teams: List[str]) -> None:
        self.m = gp.Model('mip1')
        self.m.setParam('Seed', 1234)
        self.matchup_indices = self._sort_matrix(np.array([[nfl_teams_to_indices[m[0].team_name], 
                                          nfl_teams_to_indices[m[1].team_name]] for m in matchups]))

        self.early_bye_teams = [nfl_teams_to_indices[team_name] for team_name in early_bye_week_teams]
        debug(self.early_bye_teams)
        full_tuplelist = create_matchup_tuplelist(self.matchup_indices)
        self.all_games = gp.tuplelist(self._prune_matchups(full_tuplelist))
        debug(len(self.all_games))
        # debug(self.all_games)

        # Add Gurobi Variables
        self.games = self.m.addVars(self.all_games, vtype=GRB.BINARY) # Variables for all possible games
        self.bv = self.m.addMVar((2, 8), vtype=GRB.BINARY) # Helper binaries for 2, 4, 6 week bye week constraint
        self.b3 = self.m.addMVar((32, 15), vtype=GRB.BINARY) # Helper binaries for 3-game road trip cost
        self._set_weights()
        self._add_constraints()
        self._add_cost()

    def _prune_matchups(self, matchups: List[Tuple[int, int, int]]):
        all_games = []

        non_bye_weeks = [1, 2, 3, 4, 8, 13, 15, 16, 17, 18]
        for match in matchups:
            # # remove all bye week matchups for non-bye weeks
            # if match[1] == -1 and (match[2] + 1) in non_bye_weeks:
            #     continue

            # remove all early bye week teams from last season to have an early bye this season
            if (match[1] == -1) and (match[0] in self.early_bye_teams) and match[2] == 4:
                continue
            
            # remove all non-div games for the last week
            # if match[2] == 17 and match[1] != -1:
            #     team1_div = NFL_TEAMS_DICT[indices_to_nfl_teams[match[0]]].division
            #     team2_div = NFL_TEAMS_DICT[indices_to_nfl_teams[match[1]]].division
            #     if team1_div != team2_div:
            #         continue

            all_games.append(match)
        # all_games = matchups
        return all_games

    def _set_weights(self, travel: float=0.001, 
                     three_game_road_trip: float=10, 
                     two_games_start: float=1,
                     two_games_finish: float=1,
                     road_games_against_bye: float=1,
                     well_spread_division_series: float=0.5):
        self.travel_weight = travel
        self.three_game_road_trip_weight = three_game_road_trip
        self.two_games_finish_weight = two_games_finish
        self.two_games_start_weight = two_games_start
        self.road_games_against_bye_weight = road_games_against_bye
        self.well_spread_division_series_weight = well_spread_division_series

    def _get_travel_distance(self, w, potential_games_this_week, potential_games_next_week):
        total_distance = 0
        for home_team_idx1, away_team_idx1, week1 in potential_games_this_week:
            if away_team_idx1 == -1: continue
            if week1 != w: continue
            game_loc1 = get_team_home_stadium(home_team_idx1)
            var1 = self.games.select(home_team_idx1, away_team_idx1, w)[0]
            for home_team_idx2, away_team_idx2, week2 in potential_games_next_week:
                if away_team_idx2 == -1: continue
                if week2 != w + 1: continue
                game_loc2 = get_team_home_stadium(home_team_idx2)
                var2 = self.games.select(home_team_idx2, away_team_idx2, w + 1)[0]
                distance = haversine(game_loc1, game_loc2)
                # debug(distance)
                coeff = int(self.travel_weight * distance)
                if coeff == 0: continue
                total_distance += coeff * (var1 * var2)
                # debug(total_distance)
        return total_distance

    def _add_cost(self):
        cost = gp.LinExpr()
        non_bye_weeks = [1, 2, 3, 4, 8, 13, 15, 16, 17, 18]
        for team in range(32):
            # Travel Time Calculation
            travel_distance = gp.LinExpr()
            potential_games_this_week = [game for game in self.all_games 
                if (game[0] == team or game[1] == team) and game[2] == 0]
            for w in range(17):
                potential_games_next_week = [game for game in self.all_games 
                    if (game[0] == team or game[1] == team) and game[2] == w + 1]
                travel_distance += self._get_travel_distance(w, 
                                                             potential_games_this_week, 
                                                             potential_games_next_week)
                potential_games_this_week = potential_games_next_week

                # 3-game Road Trip Cost
                if w >= 1 and w <= 15:
                    cost += self.three_game_road_trip_weight * self.b3[team, w - 1].item()

                # Min teams playing road gm. ag. teams coming off bye
                if w + 1 not in non_bye_weeks:
                    first_game = self.games.sum(team, -1, w)
                    second_game = self.games.sum(team, '*', w + 1)
                    cost += self.road_games_against_bye_weight * (first_game * second_game)

            # 2-game road start
            first_game = self.games.sum('*', team, 0)
            second_game = self.games.sum('*', team, 1)
            cost += self.two_games_start_weight * (first_game * second_game)

            # 2-game road finish
            first_game = self.games.sum('*', team, 16)
            second_game = self.games.sum('*', team, 17)
            cost += self.two_games_finish_weight * (first_game * second_game)
            
            # Add travel to cost
            # cost += travel_distance # this is messing up cost
        self.m.setObjective(cost, GRB.MINIMIZE)

    def _add_constraints(self):
        self._add_matchup_played_constraints()
        self._add_bye_week_constraints()
        self._three_game_road_trip_contraints()

    def _add_matchup_played_constraints(self):
        # Each matchup MUST be played once and only once
        self.m.addConstrs(self.games.sum(i, j, '*') == 1 for i, j, _ in self.all_games)

        # Each Week MUST have 16 Games (BYEs Included)
        bye_weeks = [5, 6, 7, 9, 10, 11, 12, 14]
        for i in range(18):
            if i + 1 in bye_weeks: 
                idx = bye_weeks.index(i + 1)
                bin_sum = self.bv[:, idx].sum().item() + 1
            else: bin_sum = 0
            self.m.addConstr(self.games.sum('*', '*', i) == 16 + bin_sum)

        # Each Team MUST play one and only one game every week
        self.m.addConstrs(self.games.sum('*', i, j) + self.games.sum(i, '*', j) == 1 for i in range(32) for j in range(18))

        # Last Week is all Divisional Games, Getting all divisional matchups
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
        self.m.addConstrs(self.games.sum('*', -1, i - 1) == 0 for i in non_bye_weeks)

        # Every team only has 1 bye week
        self.m.addConstrs(self.games.sum(i, -1, '*') == 1 for i in range(32))

        # Only 2, 4, or 6 teams on bye at a time
        bye_weeks = [5, 6, 7, 9, 10, 11, 12, 14]
        for i in range(8):
            bin_sum = self.bv[:, i].sum().item()
            self.m.addConstr(self.games.sum('*', -1, bye_weeks[i] - 1) == ((2 * bin_sum) + 2))

        # Earliest bye week teams last year can’t get early bye this year (Week 5 is the earliest bye)
        # self.m.addConstrs(self.games.sum(team, -1, 4) == 0 for team in self.early_bye_teams)
    
    def _three_game_road_trip_contraints(self):
        for team in range(32):
            for w in range(15):
                x1 = self.games.sum('*', team, w)
                x2 = self.games.sum('*', team, w + 1)
                x3 = self.games.sum('*', team, w + 2)
                b = self.b3[team, w]
                self.m.addConstr(b <= x1, "c1")
                self.m.addConstr(b <= x2, "c2")
                self.m.addConstr(b <= x3, "c3")
                self.m.addConstr(b >= x1 + x2 + x3 - 2, "c4")

    def _sort_matrix(self, mat: np.array) -> np.array:
        sorted_mat = np.vstack((sorted([col for col in mat], key=lambda x: x[0])))
        return sorted_mat

    def solve(self):
        self.m.optimize()
        # print_tupledict_3('ALL MATCHUPS', self.games)
