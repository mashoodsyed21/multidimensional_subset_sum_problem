from __future__ import annotations

import random
import statistics
from typing import Protocol, runtime_checkable

# Optional tqdm for the outer loop
try:
    from tqdm import tqdm
    has_tqdm = True
except ImportError:
    has_tqdm = False

from .generator import InstanceGenerator
from .models import ExperimentConfig, MDSSInstance, PhaseRow
from .dp_solver import DPSolver, SolverResult


@runtime_checkable
class Solver(Protocol):
    def solve(self, instance: MDSSInstance) -> SolverResult: ...


class ExperimentRunner:
    """Sweeps over a range of n values and aggregates trial results."""


    _HEADER = (
        f"  {'n':>5} | {'YES%':>8} | {'Avg/Run (s)':>12} | {'Total (s)':>10} | {'States':>12}"
    )
    _SEP = "  " + "-" * 72

    def __init__(
        self,
        cfg: ExperimentConfig,
        solver: Solver | None = None,
        verbose: bool = True,
    ) -> None:
        self.cfg        = cfg
        self.verbose    = verbose
        self._solver    = solver if solver is not None else DPSolver(verbose=False)
        self._generator = InstanceGenerator()

    def run(self) -> list[PhaseRow]:
        cfg = self.cfg
        n_values = list(range(cfg.n_start, cfg.n_stop + 1, cfg.n_step))
        
        if self.verbose:
            print()
            print(f"  Experiment Suite: d={cfg.d}, m={cfg.m}, {cfg.trials} trials per n, n in [{cfg.n_start}..{cfg.n_stop}]")
            print(self._SEP)
            print(self._HEADER)
            print(self._SEP)

        rows: list[PhaseRow] = []
        
        # tqdm Outer-Loop (falls verfügbar und verbose)
        iterable = n_values
        if self.verbose and has_tqdm:
            iterable = tqdm(n_values, desc=f"  Progress (d={cfg.d}, m={cfg.m})", unit="step", leave=False, colour="green")

        for n in iterable:
            row = self._evaluate_n(n)
            rows.append(row)
            
            if self.verbose:
                state_str = f"{row.states_mean:>12,.0f}" if row.states_mean > 0 else f"{'  -':>12}"
                total_s = row.runtime_mean_s * cfg.trials
                line = (
                    f"  {row.n:>5} | {row.yes_rate:>7.1%} | "
                    f"{row.runtime_mean_s:>11.3f}s | {total_s:>9.3f}s | {state_str}"
                )
                if has_tqdm:
                    tqdm.write(line)
                else:
                    print(line)
                    
                if row.witnesses and self.cfg.print_witnesses:
                    if has_tqdm:
                        tqdm.write(row.witnesses)
                    else:
                        print(row.witnesses)
                    
        if self.verbose:
            grand_total = sum(r.runtime_mean_s * cfg.trials for r in rows)
            print(self._SEP)
            print(f"  Total wall-clock time for this sweep: {grand_total:.2f}s")
            print(self._SEP)
            
        return rows

    def _evaluate_n(self, n: int) -> PhaseRow:
        cfg       = self.cfg
        yes_count = 0
        runtimes: list[float] = []
        states:   list[int]   = []
        
        # Accumulate all witness strings here
        witness_blocks: list[str] = []
        
        # Accumulate all generated instance vectors here
        instance_blocks: list[str] = []

        for trial in range(cfg.trials):
            rng      = random.Random(cfg.base_seed + (n * 1_000_003) + trial)
            instance = self._generator.generate(
                n=n, d=cfg.d, m=cfg.m, 
                rng=rng, vec_ub_divisor=cfg.vec_ub_divisor
            )
            
            # Log the full instance
            inst_lines = [
                f"\n=== Trial {trial + 1}/{cfg.trials} for n={n} ===",
                f"Target: {instance.target}",
                f"Vectors:"
            ]
            for idx, vec in enumerate(instance.vectors):
                inst_lines.append(f"  v[{idx}]: {vec}")
            instance_blocks.append("\n".join(inst_lines))
            
            result   = self._solver.solve(instance)

            if result.is_yes_instance:
                yes_count += 1
                if result.witness_indices is not None:
                    lines = [
                        f"\n      -> YES-Instance for n={n} (Trial {trial + 1}/{cfg.trials}):",
                        f"         Target:  {instance.target}",
                        f"         Vectors:"
                    ]
                    for idx in result.witness_indices:
                        lines.append(f"           - v[{idx}]: {instance.vectors[idx]}")
                    witness_blocks.append("\n".join(lines))
                    
            runtimes.append(result.runtime_s)
            states.append(max(0, result.states_explored))

        all_witnesses_str = "\n".join(witness_blocks)
        all_instances_str = "\n".join(instance_blocks)

        return PhaseRow(
            n=n, trials=cfg.trials,
            yes_count=yes_count, no_count=cfg.trials - yes_count,
            yes_rate=yes_count / cfg.trials,
            runtime_mean_s=float(statistics.fmean(runtimes)) if runtimes else 0.0,
            runtime_median_s=float(statistics.median(runtimes)) if runtimes else 0.0,
            states_mean=float(statistics.fmean(states)) if states else 0.0,
            states_median=float(statistics.median(states)) if states else 0.0,
            witnesses=all_witnesses_str,
            all_instances=all_instances_str,
        )

    def __repr__(self) -> str:
        return (
            f"ExperimentRunner(cfg={self.cfg!r}, "
            f"solver={self._solver!r}, verbose={self.verbose})"
        )
