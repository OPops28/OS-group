import subprocess
import matplotlib.pyplot as plt
import shutil
import os

# Define the parameters for the experiments
algorithms = ['rand', 'lru', 'clock']
experiments = {
    'bzip.trace': [8, 16, 32, 48, 64, 80, 96, 112, 128, 160, 192, 256, 320, 384],
    'swim.trace': [160, 192, 256, 320, 384, 448, 512, 640, 768, 896, 1024, 1152, 1280, 1408, 1536, 1664, 1792, 1920, 2048, 2176, 2304, 2432, 2560, 2688],
    'gcc.trace': [256, 320, 384, 448, 512, 640, 768, 896, 1024, 1152, 1280, 1408, 1536, 1664, 1792, 1920, 2048, 2176, 2304, 2432, 2560, 2688, 2816, 2944, 3072],
    'sixpack.trace': [256, 320, 384, 448, 512, 640, 768, 896, 1024, 1152, 1280, 1408, 1536, 1664, 1792, 1920, 2048, 2176, 2304, 2432, 2560, 2688, 2816, 2944, 3072, 3200, 3328, 3456, 3584],
}
mode = 'quiet'

# Delete directories if they exist and create them again
def create_clean_directory(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

create_clean_directory('results')
create_clean_directory('plots')

def run_simulations(trace, frames, algorithm, runs=1):
    """Runs the simulator and returns the results as a tuple (disk_reads, disk_writes, page_fault_rate)."""
    print(f'Running simulations for {trace} with {frames} frames using {algorithm} algorithm...')
    total_reads = 0
    total_writes = 0
    total_fault_rate = 0.0
    cmd = ['python3', 'memsim.py', trace, str(frames), algorithm, mode]

    for i in range(runs):
        # Run the simulator
        result = subprocess.run(cmd, capture_output=True, text=True)
        # Parsing the output
        output_lines = result.stdout.splitlines()
        disk_reads = int(output_lines[2].split(': ')[1])
        disk_writes = int(output_lines[3].split(': ')[1])
        page_fault_rate = float(output_lines[4].split(': ')[1])
        # Accumulate the results
        total_reads += disk_reads
        total_writes += disk_writes
        total_fault_rate += page_fault_rate
    # Calculate the average results
    avg_reads = total_reads / runs
    avg_writes = total_writes / runs
    avg_fault_rate = total_fault_rate / runs
    
    return avg_reads, avg_writes, avg_fault_rate

def save_results(trace, algorithm, frames, results):
    """Saves the results to a text file."""
    print(f'Saving results for {trace} with {frames} frames using {algorithm} algorithm...')
    filename = f'results/{trace}_{algorithm}.txt'
    # Write the results to a text file
    with open(filename, 'a') as f:
        f.write(f'Frames: {frames}, Disk Reads: {results[0]}, Disk Writes: {results[1]}, Page Fault Rate: {results[2]}\n')

def plot_results(results, trace):
    """Plots the results for a specific trace."""
    print(f'Plotting results for {trace}...')

    # Plot Disk Reads vs Number of Frames
    plt.figure(figsize=(10, 6))
    for algorithm, data in results.items():
        frame_sizes = list(data.keys())
        disk_reads = [data[frames][0] for frames in frame_sizes]
        plt.plot(frame_sizes, disk_reads, marker='o', label=algorithm)
    plt.xlabel('Number of Frames')
    plt.ylabel('Disk Reads')
    plt.title(f'Disk Reads vs Number of Frames for {trace}')
    plt.legend()
    plt.grid(True, which="both", ls="--", linewidth=0.5)
    plt.savefig(f'plots/{trace}_disk_reads.png', dpi=300)
    plt.close()

    # Plot Disk Writes vs Number of Frames
    plt.figure(figsize=(10, 6))
    for algorithm, data in results.items():
        frame_sizes = list(data.keys())
        disk_writes = [data[frames][1] for frames in frame_sizes]
        plt.plot(frame_sizes, disk_writes, marker='o', label=algorithm)
    plt.xlabel('Number of Frames')
    plt.ylabel('Disk Writes')
    plt.title(f'Disk Writes vs Number of Frames for {trace}')
    plt.legend()
    plt.grid(True, which="both", ls="--", linewidth=0.5)
    plt.savefig(f'plots/{trace}_disk_writes.png', dpi=300)
    plt.close()

    # Plot Page Fault Rate vs Number of Frames
    plt.figure(figsize=(10, 6))
    for algorithm, data in results.items():
        frame_sizes = list(data.keys())
        page_fault_rates = [data[frames][2] for frames in frame_sizes]
        plt.plot(frame_sizes, page_fault_rates, marker='o', label=algorithm)
    plt.xlabel('Number of Frames')
    plt.ylabel('Page Fault Rate')
    plt.title(f'Page Fault Rate vs Number of Frames for {trace}')
    plt.legend()
    plt.grid(True, which="both", ls="--", linewidth=0.5)
    plt.savefig(f'plots/{trace}_page_fault_rate.png', dpi=300)
    plt.close()

def plot_results_precise(results, trace):
    """Plots the results for a specific trace with enhanced precision for comparison."""
    print(f'Plotting results for {trace} with enhanced precision...')

    # Plot Disk Reads vs Number of Frames with log scale
    plt.figure(figsize=(10, 6))
    for algorithm, data in results.items():
        frame_sizes = sorted(data.keys())
        disk_reads = [data[frames][0] for frames in frame_sizes]
        plt.plot(frame_sizes, disk_reads, marker='o', label=algorithm)
    plt.yscale('log') # Use log scale for better visualization
    plt.xlabel('Number of Frames')
    plt.ylabel('Disk Reads (Log Scale)')
    plt.title(f'Disk Reads vs Number of Frames for {trace}')
    plt.legend()
    plt.grid(True, which="both", ls="--", linewidth=0.5)
    plt.savefig(f'plots/{trace}_disk_reads_precise.png', dpi=300)
    plt.close()

    # Plot Disk Writes vs Number of Frames with log scale
    plt.figure(figsize=(10, 6))
    for algorithm, data in results.items():
        frame_sizes = sorted(data.keys())
        disk_writes = [data[frames][1] for frames in frame_sizes]
        plt.plot(frame_sizes, disk_writes, marker='o', label=algorithm)
    plt.yscale('log') # Use log scale for better visualization
    plt.xlabel('Number of Frames')
    plt.ylabel('Disk Writes (Log Scale)')
    plt.title(f'Disk Writes vs Number of Frames for {trace}')
    plt.legend()
    plt.grid(True, which="both", ls="--", linewidth=0.5)
    plt.savefig(f'plots/{trace}_disk_writes_precise.png', dpi=300)
    plt.close()

    # Plot Page Fault Rate vs Number of Frames with log scale
    plt.figure(figsize=(10, 6))
    for algorithm, data in results.items():
        frame_sizes = sorted(data.keys())
        page_fault_rates = [data[frames][2] for frames in frame_sizes]
        plt.plot(frame_sizes, page_fault_rates, marker='o', label=algorithm)
    plt.yscale('log') # Use log scale for better visualization
    plt.xlabel('Number of Frames')
    plt.ylabel('Page Fault Rate (Log Scale)')
    plt.title(f'Page Fault Rate vs Number of Frames for {trace}')
    plt.legend()
    plt.grid(True, which="both", ls="--", linewidth=0.5)
    plt.savefig(f'plots/{trace}_page_fault_rate_precise.png', dpi=300)
    plt.close()


# Run experiments and collect results
for trace, frame_sizes in experiments.items():
    trace_results = {algo: {} for algo in algorithms}
    for algo in algorithms:
        for frames in frame_sizes:
            runs = 10 if algo == 'rand' else 1
            results = run_simulations(trace, frames, algo, runs)
            trace_results[algo][frames] = results
            save_results(trace, algo, frames, results)
    plot_results(trace_results, trace)
    plot_results_precise(trace_results, trace)

print("Experiments completed, results and plots saved.")
