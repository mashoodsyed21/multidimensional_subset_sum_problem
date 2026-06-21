# Standalone Solvers

This directory provides standalone scripts to run the Dynamic Programming (DP) and Integer Linear Programming (ILP) solvers directly on specific instance data loaded from a text file, instead of generating random instances.

## Input File Format

Create a basic text file. The first non-empty/non-comment line must be the target vector. All subsequent lines will be parsed as the item vectors. 
You can use spaces or commas to delimit the numbers. Lines tracking with `#` are ignored as comments.

**Example `input.txt`**:
```
# Target vector
10 15 20

# Input vectors
1 2 3
4 5 6
5 8 11
0 2 0
```

## Running the Solvers

### Dynamic Programming Solver
```bash
python run_dp.py my_instance_file.txt
```

### ILP Solver
```bash
python run_ilp.py my_instance_file.txt
```
