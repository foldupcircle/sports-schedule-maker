# import gurobipy as gp
# from gurobipy import GRB

# from backend.utils.debug import debug

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
