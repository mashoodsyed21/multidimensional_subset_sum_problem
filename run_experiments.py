"""
DynamicProgrammingSolver.py
===========================
Entry point for MSS phase-transition experiments.
Reads all test parameters from `config.py`.
"""
from __future__ import annotations

import config
from mss import DPSolver, ILPSolver, LimitTester, ResultExporter


def main() -> None:
    print("=" * 84)
    print("MSS  -  DP vs ILP  |  Phase-Transition Limit Testing")
    print("=" * 84)

    exporter = ResultExporter(out_dir="results")

    print("\n>>> Part 1: Exact Solution Approach (Dynamic Programming)")
    dp_solver = DPSolver()
    dp_tester = LimitTester(
        exporter=exporter, 
        trials=config.TRIALS_PER_N, 
        base_seed=config.BASE_SEED,
        solver=dp_solver
    )

    for d, m, n_start, n_stop, n_step in config.DP_SWEEP_CONFIGS:
        dp_tester.test(
            d=d, m=m, 
            n_start=n_start, n_stop=n_stop, n_step=n_step,
            vec_ub_divisor=config.VEC_UB_DIVISOR,
            print_witnesses=config.PRINT_WITNESSES_TO_CONSOLE
        )

    # =========================================================================
    # Part 2: ILP Solver
    # =========================================================================
    print("\n>>> Part 2: Mathematical Optimization (ILP via PuLP/CBC)")
    ilp_solver = ILPSolver(
        time_limit_s=config.ILP_TIME_LIMIT_SECONDS
    )
    ilp_tester = LimitTester(
        exporter=exporter, 
        trials=config.TRIALS_PER_N, 
        base_seed=config.BASE_SEED, 
        solver=ilp_solver
    )

    for d, m, n_start, n_stop, n_step in config.ILP_SWEEP_CONFIGS:
        ilp_tester.test(
            d=d, m=m, 
            n_start=n_start, n_stop=n_stop, n_step=n_step,
            vec_ub_divisor=config.VEC_UB_DIVISOR,
            print_witnesses=config.PRINT_WITNESSES_TO_CONSOLE
        )


if __name__ == "__main__":
    main()