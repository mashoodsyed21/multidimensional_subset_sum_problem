
from __future__ import annotations


BASE_SEED = 2026
TRIALS_PER_N = 30
ILP_TIME_LIMIT_SECONDS = 7200.0     
DP_LOG_INTERVAL_SECONDS = 3.0      
VEC_UB_DIVISOR = 2
PRINT_WITNESSES_TO_CONSOLE = False


DP_SWEEP_CONFIGS = [
    # d=3 with multiple values of m
    (3, 10, 5, 40, 5),
    (3, 20, 5, 40, 5),
    (3, 50, 5, 40, 5),

    # dimension 4, 5, 6 with different n behavior
    (4, 20, 5, 40, 5),
    (5, 20, 5, 40, 5),
    (6, 20, 5, 40, 5),

    # large dimension 10 - increased n_stop to 40
    (10, 20, 5, 40, 5),
]

ILP_SWEEP_CONFIGS = [
    # d=3 with multiple values of m
    (3, 10, 5, 40, 5),
    (3, 20, 5, 40, 5),
    (3, 50, 5, 40, 5),

    # dimension 4, 5, 6 with different n behavior
    (4, 20, 5, 40, 5),
    (5, 20, 5, 40, 5),
    (6, 20, 5, 40, 5),

    # large dimension 10 - increased n_stop to 40
    (10, 20, 5, 40, 5),
]
