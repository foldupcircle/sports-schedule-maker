# import gurobipy as gp
# from gurobipy import GRB

# from backend.utils.debug import debug

# def print_MVars(model: gp.Model) -> None:
#     try:
#         vars = model.getVars()
#         debug(vars[0])
#         for v in 
#         print(f"{name}:")
#         for i in range(min(2, mvar.shape[0])):  # Ensure we only access existing rows
#             row_values = [mvar[i, j].X for j in range(mvar.shape[1])]
#             print(' '.join(map(str, row_values)))

#         # Check the model status and handle accordingly
#         if model.Status == GRB.OPTIMAL:
#             # Print the first two rows of the MVars
#             print("mvar1:")
#             for i in range(3):
#                 for j in range(3):
#                     print(f"mvar1[{i},{j}] = {mvar1[i, j].x}")
#         elif model.Status == GRB.INF_OR_UNBD:
#             raise RuntimeError("Model is infeasible or unbounded.")
#         elif model.Status == GRB.INFEASIBLE:
#             raise RuntimeError("Model is infeasible.")
#         elif model.Status == GRB.UNBOUNDED:
#             raise RuntimeError("Model is unbounded.")
#         else:
#             raise RuntimeError(f"Optimization ended with status {model.Status}.")

#     except gp.GurobiError as e:
#         debug(f"Gurobi error: {e.errno} - {e}")

#     except AttributeError as e:
#         print(f"Attribute error: {e}")
