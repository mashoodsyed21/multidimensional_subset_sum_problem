import sys
from pathlib import Path

# Add parent directory to path to allow importing mss
sys.path.append(str(Path(__file__).parent.parent))

from parse_utils import parse_instance_file
from mss.ilp_solver import ILPSolver

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_ilp.py <instance_file>")
        sys.exit(1)
        
    instance_file = sys.argv[1]

    try:
        instance = parse_instance_file(instance_file)
    except Exception as e:
        print(f"Error parsing instance: {e}")
        sys.exit(1)

    print(f"Loaded instance with target={instance.target}, n={instance.n}, d={instance.d}")
    
    # 2 hours (7200 seconds)
    solver = ILPSolver(time_limit_s=7200.0, verbose=False)
    result = solver.solve(instance)
    
    print("--- Results ---")
    print(f"Is Yes Instance: {result.is_yes_instance}")
    print(f"Runtime: {result.runtime_s:.4f} s")
    if result.is_yes_instance:
        print(f"Witness indices: {result.witness_indices}")
        # Verify witness
        is_valid = solver.verify_witness(instance, result.witness_indices)
        print(f"Witness verified correctly: {is_valid}")
        
if __name__ == "__main__":
    main()
