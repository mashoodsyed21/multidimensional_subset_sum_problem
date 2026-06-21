from __future__ import annotations

from dataclasses import dataclass

Vector = tuple[int, ...]


@dataclass(frozen=True)
class ExperimentConfig:
    d: int
    m: int
    n_start: int
    n_stop: int
    n_step: int
    trials: int
    vec_ub_divisor: int = 4
    base_seed: int = 42
    print_witnesses: bool = False

    def __post_init__(self) -> None:
        _validate_config(self)


@dataclass(frozen=True)
class PhaseRow:
    n: int
    trials: int
    yes_count: int
    no_count: int
    yes_rate: float
    runtime_mean_s: float
    runtime_median_s: float
    states_mean: float
    states_median: float
    witnesses: str = ""
    all_instances: str = ""


@dataclass(frozen=True)
class MSSInstance:
    vectors: tuple[Vector, ...]
    target: Vector
    n: int
    d: int


def _validate_positive(name: str, value: int) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be > 0, got {value}")


def _validate_config(cfg: ExperimentConfig) -> None:
    _validate_positive("d", cfg.d)
    _validate_positive("m", cfg.m)
    _validate_positive("n_start", cfg.n_start)
    _validate_positive("n_stop", cfg.n_stop)
    _validate_positive("n_step", cfg.n_step)
    _validate_positive("trials", cfg.trials)
    _validate_positive("vec_ub_divisor", cfg.vec_ub_divisor)
    if cfg.n_start > cfg.n_stop:
        raise ValueError("n_start must be <= n_stop")
