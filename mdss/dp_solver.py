from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Sequence
import logging

from .models import MDSSInstance, Vector


@dataclass(frozen=True)
class SolverResult:
    is_yes_instance: bool
    states_explored: int
    runtime_s: float
    witness_indices: tuple[int, ...] | None = None


class DPSolver:
    """Reachability-only DP solver. Prunes any partial sum exceeding the target."""

    def __init__(self) -> None:
        pass

    def solve(self, instance: MDSSInstance) -> SolverResult:
        start = time.perf_counter()
        is_yes, states, witness = self._run_dp(instance.vectors, instance.target)
        return SolverResult(
            is_yes_instance=is_yes,
            states_explored=states,
            runtime_s=time.perf_counter() - start,
            witness_indices=witness,
        )

    def _run_dp(self, vectors: Sequence[Vector], target: Vector) -> tuple[bool, int, tuple[int, ...] | None]:
        d = len(target)
        zero: Vector = tuple(0 for _ in range(d))
        
        reachable: dict[Vector, int] = {zero: -1}
        total = len(vectors)

        for i, vec in enumerate(vectors):

            new_sums: dict[Vector, int] = {}
            for current in reachable:
                candidate = tuple(x + y for x, y in zip(current, vec))
                if not all(c <= t for c, t in zip(candidate, target)):
                    continue
                    
                if candidate == target:
                    reachable.update(new_sums)
                    reachable[candidate] = i
                    
                    witness = []
                    curr = target
                    while curr != zero:
                        idx = reachable[curr]
                        if idx == -1:
                            break
                        witness.append(idx)
                        curr = tuple(c - v for c, v in zip(curr, vectors[idx]))
                        
                    witness.reverse()
                    return True, len(reachable), tuple(witness)
                    
                if candidate not in reachable and candidate not in new_sums:
                    new_sums[candidate] = i

            if new_sums:
                reachable.update(new_sums)

        return False, len(reachable), None

    def __repr__(self) -> str:
        return "DPSolver()"
