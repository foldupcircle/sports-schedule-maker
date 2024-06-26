import casadi as ca

class Solver():
    def __init__(self) -> None:
        self.opti = ca.Opti()
        self.x = self.opti.variable(1)
        self._add_cost()
        self._add_constraints()

    def _add_cost(self):
        cost = self.x
        self.opti.minimize(cost)
        self.opti.set_initial(self.x, 5)

    def _add_constraints(self):
        self.opti.subject_to(self.x >= 1)

    def solve(self):
        self.opti.solver('ipopt')
        sol = self.opti.solve()
        x_sol = sol.value(self.x)
        return x_sol
    