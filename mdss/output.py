from __future__ import annotations

import csv
import math
from dataclasses import asdict
from pathlib import Path
from typing import Sequence

import matplotlib.pyplot as plt

from .experiment import ExperimentRunner
from .models import ExperimentConfig, PhaseRow


class ResultExporter:
    """Writes PhaseRow results to CSV files and phase-transition plots."""

    def __init__(self, out_dir: str | Path = "results") -> None:
        self.out_dir = Path(out_dir)

    def export_csv(self, rows: Sequence[PhaseRow], filename: str) -> Path:
        if not rows:
            raise ValueError("rows must not be empty")
        path = self._ensure_path(filename)
        with path.open("w", newline="", encoding="utf-8") as f:
            fieldnames = list(asdict(rows[0]).keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(asdict(row))
        return path

    def plot_yes_rate(
        self,
        rows: Sequence[PhaseRow],
        title: str,
        filename: str,
        *,
        dpi: int = 150,
    ) -> Path:
        if not rows:
            raise ValueError("rows must not be empty")
        x = [r.n          for r in rows]
        y = [r.yes_rate   for r in rows]

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(x, y, "o-")
        ax.set_xlabel("n  (number of vectors)")
        ax.set_ylabel("YES rate")
        ax.set_title(title)
        ax.set_ylim(-0.05, 1.05)
        ax.grid(True, alpha=0.3)

        path = self._ensure_path(filename)
        fig.savefig(path, dpi=dpi)
        plt.close(fig)
        return path

    def run_and_export(
        self,
        cfg: ExperimentConfig,
        *,
        tag: str,
        solver=None,
        verbose: bool = True,
    ) -> list[PhaseRow]:
        runner = ExperimentRunner(cfg=cfg, solver=solver, verbose=verbose)
        rows   = runner.run()
        csv_path  = self.export_csv(rows, filename=f"{tag}.csv")
        plot_path = self.plot_yes_rate(rows, title=f"Phase Transition – {tag}", filename=f"{tag}.png")
        
        # Export witnesses to a text file
        txt_path = self._ensure_path(f"{tag}_witnesses.txt")
        with txt_path.open("w", encoding="utf-8") as f:
            f.write(f"Witness Details for {tag}\n")
            f.write("=" * 60 + "\n")
            for row in rows:
                if row.witnesses:
                    f.write(f"{row.witnesses}\n")
                    f.write("-" * 60 + "\n")
                    
        # Export all generated instances to another text file
        inst_path = self._ensure_path(f"{tag}_instances.txt")
        with inst_path.open("w", encoding="utf-8") as f:
            f.write(f"All Generated Instances for {tag}\n")
            f.write("=" * 60 + "\n")
            for row in rows:
                if getattr(row, "all_instances", ""):
                    f.write(f"{row.all_instances}\n")
                    f.write("-" * 60 + "\n")
                    
        if verbose:
            print(f"  CSV      -> {csv_path}")
            print(f"  Plot     -> {plot_path}")
            print(f"  Witnesses-> {txt_path}")
            print(f"  Instances-> {inst_path}")
        return rows

    def _ensure_path(self, filename: str) -> Path:
        self.out_dir.mkdir(parents=True, exist_ok=True)
        return self.out_dir / filename

    def __repr__(self) -> str:
        return f"ResultExporter(out_dir={str(self.out_dir)!r})"


class LimitTester:
    """Runs a phase-transition sweep for one dimension and prints a summary."""

    def __init__(
        self,
        exporter: ResultExporter | None = None,
        trials: int = 10,
        base_seed: int = 2026,
        solver=None,
    ) -> None:
        self.exporter  = exporter or ResultExporter()
        self.trials    = trials
        self.base_seed = base_seed
        self.solver    = solver

    def test(
        self,
        d: int,
        m: int,
        n_start: int,
        n_stop: int,
        n_step: int = 5,
        vec_ub_divisor: int = 4,
        print_witnesses: bool = False,
    ) -> list[PhaseRow]:
        solver_name = "DP-Solver" if "DPSolver" in str(type(self.solver)) else "ILP-Solver"
        tag = f"limit_test_d{d}_m{m}_{solver_name}"

        vec_ub = m // vec_ub_divisor
        tgt_min, tgt_max = m, 2 * m

        cfg  = ExperimentConfig(
            d=d, m=m, n_start=n_start, n_stop=n_stop, n_step=n_step,
            trials=self.trials, vec_ub_divisor=vec_ub_divisor, base_seed=self.base_seed,
            print_witnesses=print_witnesses,
        )
        
        # --- NEW, PROFESSIONAL ENGLISH HEADER ---
        print(f"\n{'=' * 80}")
        print(f"[ SOLVER ]     : {solver_name}")
        print(f"[ PARAMETERS ] : Dimension d = {d}  |  Scaling Factor m = {m}")
        print(f"[ DOMAIN ]     : Vectors in [0, {vec_ub}]^d  |  Target Vector in [{tgt_min}, {tgt_max}]^d")
        print(f"{'=' * 80}")
        
        rows = self.exporter.run_and_export(cfg, tag=tag, solver=self.solver, verbose=True)

        # Evaluation of the phase transition
        best = min(rows, key=lambda r: abs(r.yes_rate - 0.5))
        print(f"\n  >>> Closest to 50% Feasibility: n = {best.n} (YES-Rate: {best.yes_rate:.1%})")
        print(f"  >>> Avg. Runtime at this n:     {best.runtime_mean_s:.3f} s")
        if "ILP" not in solver_name:
            print(f"  >>> Avg. States Explored:       {best.states_mean:,.0f}")
            
        return rows

    def __repr__(self) -> str:
        return (
            f"LimitTester(trials={self.trials}, base_seed={self.base_seed}, "
            f"exporter={self.exporter!r})"
        )
