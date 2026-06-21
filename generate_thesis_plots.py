import os
import csv
import glob
import matplotlib.pyplot as plt

RESULTS_DIR = "results"
PLOTS_DIR = "plots"

def ensure_plots_dir():
    if not os.path.exists(PLOTS_DIR):
        os.makedirs(PLOTS_DIR)

def read_csv_data(filepath):
    data = {"n": [], "yes_rate": [], "runtime_mean": [], "states_mean": []}
    if not os.path.exists(filepath):
        return None
    
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
            n_idx = header.index("n")
            yes_rate_idx = header.index("yes_rate")
            rt_idx = header.index("runtime_mean_s")
            states_idx = header.index("states_mean")
        except (ValueError, StopIteration):
            return None
            
        for row in reader:
            if not row or len(row) <= max(n_idx, yes_rate_idx, rt_idx, states_idx):
                continue
            # stop parsing if we hit the raw instances printouts
            if str(row[0]).startswith("===") or not str(row[0]).isdigit():
                break
            try:
                data["n"].append(int(row[n_idx]))
                data["yes_rate"].append(float(row[yes_rate_idx]))
                data["runtime_mean"].append(float(row[rt_idx]))
                data["states_mean"].append(float(row[states_idx]))
            except ValueError:
                break
    return data

def plot_1_yes_rate_by_dimension():
    plt.figure(figsize=(8, 5))
    dimensions = [3, 4, 5, 6, 10]
    m = 20
    
    for d in dimensions:
        filepath = os.path.join(RESULTS_DIR, f"limit_test_d{d}_m{m}_DP-Solver.csv")
        data = read_csv_data(filepath)
        if data and data["n"]:
            plt.plot(data["n"], data["yes_rate"], marker='o', label=f"d={d}")

    plt.xlabel("Subset size n")
    plt.ylabel("YES-rate")
    plt.title("YES-rate as a function of n for different dimensions (m=20)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "fig_yes_rate_by_dimension_m20.png"), dpi=300)
    plt.close()

def plot_2_dp_states_by_dimension():
    plt.figure(figsize=(8, 5))
    dimensions = [3, 4, 5, 6, 10]
    m = 20
    
    for d in dimensions:
        filepath = os.path.join(RESULTS_DIR, f"limit_test_d{d}_m{m}_DP-Solver.csv")
        data = read_csv_data(filepath)
        if data and data["n"]:
            # Filter out zeros to avoid log issues
            ns = [n for n, s in zip(data["n"], data["states_mean"]) if s > 0]
            states = [s for s in data["states_mean"] if s > 0]
            if ns:
                plt.plot(ns, states, marker='s', label=f"d={d}")

    plt.yscale("log")
    plt.xlabel("Subset size n")
    plt.ylabel("Average DP states (log scale)")
    plt.title("Average number of stored DP states for different dimensions (m=20)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6, which="both")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "2_dp_states_by_dimension.png"), dpi=300)
    plt.close()

def plot_3_yes_rate_by_m():
    plt.figure(figsize=(8, 5))
    m_values = [10, 20, 50]
    d = 3
    
    for m in m_values:
        filepath = os.path.join(RESULTS_DIR, f"limit_test_d{d}_m{m}_DP-Solver.csv")
        data = read_csv_data(filepath)
        if data and data["n"]:
            plt.plot(data["n"], data["yes_rate"], marker='^', label=f"m={m}")

    plt.xlabel("Subset size n")
    plt.ylabel("YES-rate")
    plt.title("YES-rate as a function of n for different scaling parameters (d=3)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "3_yes_rate_by_m.png"), dpi=300)
    plt.close()

def plot_4_runtime_dp_vs_ilp():
    plt.figure(figsize=(8, 5))
    d, m = 10, 20
    
    dp_file = os.path.join(RESULTS_DIR, f"limit_test_d{d}_m{m}_DP-Solver.csv")
    ilp_file = os.path.join(RESULTS_DIR, f"limit_test_d{d}_m{m}_ILP-Solver.csv")
    
    dp_data = read_csv_data(dp_file)
    ilp_data = read_csv_data(ilp_file)
    
    if dp_data and dp_data["n"]:
        plt.plot(dp_data["n"], dp_data["runtime_mean"], marker='o', label="DP Solver", color="blue")
    if ilp_data and ilp_data["n"]:
        plt.plot(ilp_data["n"], ilp_data["runtime_mean"], marker='s', label="ILP Solver", color="red")

    plt.xlabel("Subset size n")
    plt.ylabel("Average runtime (seconds)")
    plt.title(f"Runtime comparison of DP and ILP (d={d}, m={m})")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "4_runtime_dp_vs_ilp.png"), dpi=300)
    plt.close()

def plot_5_dp_runtime_vs_states():
    plt.figure(figsize=(8, 5))
    
    # Gather data from all DP files
    dp_files = glob.glob(os.path.join(RESULTS_DIR, "*_DP-Solver.csv"))
    all_states = []
    all_runtimes = []
    
    for f in dp_files:
        data = read_csv_data(f)
        if data:
            for s, r in zip(data["states_mean"], data["runtime_mean"]):
                if s > 0 and r > 0:
                    all_states.append(s)
                    all_runtimes.append(r)
                    
    plt.scatter(all_states, all_runtimes, alpha=0.6, color="purple", edgecolors="k")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Average DP states")
    plt.ylabel("Average runtime (seconds)")
    plt.title("Relationship between DP states and runtime (log-log scale)")
    plt.grid(True, linestyle="--", alpha=0.6, which="both")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "5_dp_runtime_vs_states.png"), dpi=300)
    plt.close()

def main():
    ensure_plots_dir()
    print("Generating Plot 1: YES-rate by dimension...")
    plot_1_yes_rate_by_dimension()
    print("Generating Plot 2: DP states by dimension...")
    plot_2_dp_states_by_dimension()
    print("Generating Plot 3: YES-rate by m...")
    plot_3_yes_rate_by_m()
    print("Generating Plot 4: Runtime DP vs ILP (d=10, m=20)...")
    plot_4_runtime_dp_vs_ilp()
    print("Generating Plot 5: DP runtime vs DP states...")
    plot_5_dp_runtime_vs_states()
    print("All plots generated successfully in the 'plots/' directory.")

if __name__ == "__main__":
    main()
