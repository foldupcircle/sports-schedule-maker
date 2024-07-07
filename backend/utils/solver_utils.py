# import gurobipy as gp
# from gurobipy import GRB
from typing import List, Tuple
from backend.utils.debug import debug

def print_tupledict(name, tuple_dict):
    # Assuming x is your tupledict with two indices, e.g., x[i, j]
    x = tuple_dict

    # Extract unique indices for rows and columns
    rows = sorted(set(key[0] for key in x.keys()))
    columns = sorted(set(key[1] for key in x.keys()))

    # Create a matrix-like structure to hold the values
    matrix = []
    for row in rows:
        matrix_row = []
        for col in columns:
            # Check if the variable exists in the tupledict, otherwise use a placeholder (e.g., 0)
            if (row, col) in x:
                matrix_row.append(int(x[row, col].X))
            else:
                matrix_row.append(0)
        matrix.append(matrix_row)

    # Print the matrix
    print("Name of TupleDict: ", name)
    print("     ", "  |  ".join(map(str, columns)))
    print("     " + "-" * (6 * len(columns) - 1))
    for row, matrix_row in zip(rows, matrix):
        print(f"{row}:  ", "  |  ".join(map(str, matrix_row)))
    print()

def create_matchup_tuplelist(matchups: List[Tuple[int, int]]) -> List[Tuple[int, int, int]]:
    res = []
    
    for week in range(18):
        # Add all matchups with all possible weeks
        for matchup in matchups:
            res.append((matchup[0], matchup[1], week))

        # Add bye week possibilities with the following format: (team, -1, week)
        for team in range(32):
            res.append((team, -1, week))

    return res

def create_per_team_matchups(matchup_indices: List[List[int]]):
    per_team_matchups = {}
    for matchup in matchup_indices:
        for i, num in enumerate(matchup):
            if num not in per_team_matchups:
                per_team_matchups[num] = [[], []]
            per_team_matchups[num][0].append(matchup[1-i])
            per_team_matchups[num][1].append(i)
    return per_team_matchups

def process_per_team_matchups(per_team_matchups):
    # Home/Away Alteration, Sorting, and Adding BYE Week based on team number
    for key in per_team_matchups.keys():
        # Home/Away Alteration
        list1 = per_team_matchups[key][0]
        list2 = per_team_matchups[key][1]
        for i in range(len(list1)):
            if list2[i] == 0:
                list1[i] += 32

        # Add BYE Week and Set to Original Dict
        list1.append(-1)
        list2.append(0)
        per_team_matchups[key][0] = list1
        per_team_matchups[key][1] = list2

        # Sorting
        zipped_lists = list(zip(per_team_matchups[key][0], per_team_matchups[key][1]))
        zipped_lists.sort()
        sorted_list1, sorted_list2 = zip(*zipped_lists)
        sorted_list1 = list(sorted_list1)
        sorted_list2 = list(sorted_list2)
        per_team_matchups[key][0] = sorted_list1
        per_team_matchups[key][1] = sorted_list2

        # Print Final Output
        debug(per_team_matchups[key][0])
        debug(per_team_matchups[key][1])
    return per_team_matchups