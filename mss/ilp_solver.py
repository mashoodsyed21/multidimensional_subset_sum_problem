from __future__ import annotations

import time

import pulp

from .models import MSSInstance
from .dp_solver import SolverResult


class ILPSolver:
    """
    Feasibility ILP for MSS via PuLP / CBC.


    """

    def __init__(self, time_limit_s: float = 7200.0) -> None:
        if time_limit_s <= 0:
            raise ValueError(f"time_limit_s must be > 0, got {time_limit_s}")
        self.time_limit_s = time_limit_s

    def solve(self, instance: MSSInstance) -> SolverResult:
        start   = time.perf_counter()
        vectors = instance.vectors
        target  = instance.target
        n, d    = instance.n, instance.d

        prob = pulp.LpProblem("MSS_Feasibility", pulp.LpMinimize)
        x    = [pulp.LpVariable(f"x_{i}", cat=pulp.LpBinary) for i in range(n)]
        prob += 0

        for j in range(d):
            prob += pulp.lpSum(x[i] * vectors[i][j] for i in range(n)) == target[j]

        solver = pulp.PULP_CBC_CMD(msg=0, timeLimit=self.time_limit_s)
        prob.solve(solver)

        elapsed = time.perf_counter() - start

        if prob.status == pulp.LpStatusOptimal:
            witness = tuple(i for i in range(n) if (pulp.value(x[i]) or 0.0) > 0.5)

            return SolverResult(is_yes_instance=True, states_explored=-1,
                                runtime_s=elapsed, witness_indices=witness)

        return SolverResult(is_yes_instance=False, states_explored=-1,
                            runtime_s=elapsed, witness_indices=None)

    def verify_witness(self, instance: MSSInstance, witness: tuple[int, ...]) -> bool:
        """Check that the witness subset sums exactly to the target."""
        partial = [0] * instance.d
        for idx in witness:
            for j in range(instance.d):
                partial[j] += instance.vectors[idx][j]
        return tuple(partial) == instance.target

    def __repr__(self) -> str:
        return f"ILPSolver(time_limit_s={self.time_limit_s})"
