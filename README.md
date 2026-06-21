# Multidimensional Subset Sum Problem (MSS)

This repository provides a Python-based framework to solve the **Multidimensional Subset Sum Problem (MSS)**. Developed as part of a bachelor's thesis, it enables systematic benchmarks, phase-transition limit testing, and comparative analysis of different algorithmic approachesâ€”specifically **Exact Dynamic Programming** versus **Integer Linear Programming (ILP)**.

## What is the Multidimensional Subset Sum Problem?
The MSS is a multi-dimensional generalization of the classic Subset Sum (and Knapsack) problem. Given a set of $n$ vectors in a $d$-dimensional integer space $\mathbb{Z}^d$ and a target vector $t \in \mathbb{Z}^d$, the goal is to find a subset of vectors that sums up exactly to the target $t$.

## Project Structure

- `mss/`: The core library package. Contains data models, the instance generator, the DP solver, the ILP solver, and utilities for limit testing and exporting results.
- `config.py`: Central configuration file. Allows you to define hyperparameters, trials per configuration, and sweep ranges ($d$, $n$, seed, bounds) for the automated benchmarks.
- `run_experiments.py`: The main entry point to run systematic benchmarks and limit-testing sweeps based on `config.py`.
- `standalone_solvers/`: Contains CLI utilities to run solvers on specific, manually-defined instance text files instead of generated ones.
- `results/`: Directory where benchmark results (CSV reports) are exported.

## Prerequisites

- **Python 3.8+** (Using a virtual environment is highly recommended)
- **External Packages**: The ILP solver relies on `PuLP` (with the default CBC solver), and the exporter uses `matplotlib` for generating performance plots.

## Installation

Install all required dependencies using `pip`:
```bash
pip install -r requirements.txt
```

## Usage

### 1. Running Batch Experiments (Benchmarking)
To run systematic benchmarks and limit tests for your thesis:

1. Open `config.py` and customize your sweep parameters in `DP_SWEEP_CONFIGS` and `ILP_SWEEP_CONFIGS` (e.g., dimension $d$, range of element counts $n$, bounds, and trial counts).
2. Execute the main experiment runner:
   ```bash
   python run_experiments.py
   ```
3. The benchmarks will execute sequentially, displaying real-time updates in the console. Detailed CSV reports will be saved directly in the `results/` folder.

### 2. Solving a Specific, Custom Instance
If you want to solve a single, custom vector set:

1. Create a text file (e.g., `my_instance.txt`) where the first non-comment line is the target vector, and all subsequent lines are the candidate item vectors (numbers can be space- or comma-separated).
2. Navigate to `standalone_solvers/` and run either solver:
   ```bash
   cd standalone_solvers
   
   # Using the Dynamic Programming Solver:
   python run_dp.py my_instance.txt
   
   # Using the ILP Solver:
   python run_ilp.py my_instance.txt
   ```
   *(For details on the input file format, refer to the `README.md` inside the `standalone_solvers/` directory.)*
