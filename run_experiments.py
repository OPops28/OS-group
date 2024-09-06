import subprocess
import matplotlib.pyplot as plt
import os

# Define the parameters for the experiments
memory_traces = ['swim.trace', 'bzip.trace', 'gcc.trace', 'sixpack.trace']
page_replacement_algorithms = ['rand', 'lru', 'clock']
frame_sizes = [8, 16, 32, 64, 128, 256]
mode = 'quiet'

# Create directories to save results
os.makedirs('results', exist_ok=True)
os.makedirs('plots', exist_ok=True)

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
    plt.figure()
    for algorithm, data in results.items():
        frame_sizes = list(data.keys())
        page_fault_rates = [data[frames][2] for frames in frame_sizes]
        # Plot the results
        plt.plot(frame_sizes, page_fault_rates, marker='o', label=algorithm)

    plt.xlabel('Number of Frames')
    plt.ylabel('Page Fault Rate')
    plt.title(f'Page Fault Rate vs Number of Frames for {trace}')
    plt.legend()
    plt.grid(True)
    
    plt.savefig(f'plots/{trace}_performance.png')
    plt.close()

# Run experiments and collect results
for trace in memory_traces:
    trace_results = {algo: {} for algo in page_replacement_algorithms}
    
    for algorithm in page_replacement_algorithms:
        for frames in frame_sizes:
            if algorithm == 'rand':
                results = run_simulations(trace, frames, algorithm, runs=5)
            else:
                results = run_simulations(trace, frames, algorithm, runs=1)
            trace_results[algorithm][frames] = results
            save_results(trace, algorithm, frames, results)
    
    plot_results(trace_results, trace)

print("Experiments completed, results and plots saved.")
