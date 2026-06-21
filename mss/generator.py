from __future__ import annotations

import random

from .models import MSSInstance, Vector


class InstanceGenerator:

    def generate(self, n: int, d: int, m: int, rng: random.Random, vec_ub_divisor: int = 4) -> MSSInstance:
        if n <= 0:
            raise ValueError(f"n must be > 0, got {n}")
        if d <= 0:
            raise ValueError(f"d must be > 0, got {d}")
        if m <= 0:
            raise ValueError(f"m must be > 0, got {m}")
        if vec_ub_divisor <= 0:
            raise ValueError(f"vec_ub_divisor must be > 0, got {vec_ub_divisor}")

        ub = m // vec_ub_divisor
        vectors: tuple[Vector, ...] = tuple(
            tuple(rng.randint(0, ub) for _ in range(d))
            for _ in range(n)
        )

        target: Vector = tuple(rng.randint(m, 2 * m) for _ in range(d))

        return MSSInstance(vectors=vectors, target=target, n=n, d=d)

    def __repr__(self) -> str:
        return "InstanceGenerator()"
