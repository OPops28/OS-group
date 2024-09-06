#!/bin/bash

# Define the base results directory
BASE_RESULTS_DIR="results"

# Remove the existing results directory to start fresh
if [ -d "$BASE_RESULTS_DIR" ]; then
    echo "Deleting existing results directory..."
    rm -rf "$BASE_RESULTS_DIR"
fi

# Function to run simulations and save results in appropriate directories
run_simulations() {
    local trace=$1
    local algorithm=$2
    local frames=(8 16 32 64 128 256)

    # Extract trace name without the extension for folder naming
    local trace_name="${trace%.*}"

    # Create a directory for this trace and algorithm
    local output_dir="${BASE_RESULTS_DIR}/${trace_name}/${algorithm}"
    mkdir -p "$output_dir"

    for frame in "${frames[@]}"; do
        local output_file="${output_dir}/${frame}.txt"

        if [[ "$algorithm" == "rand" ]]; then
            # Run the simulation at least 5 times for the "rand" algorithm
            for i in {1..5}; do
                echo "Run #$i: python3 memsim.py $trace $frame $algorithm quiet" | tee -a "$output_file"
                python3 memsim.py "$trace" "$frame" "$algorithm" quiet >> "$output_file"
                echo "" >> "$output_file"
            done
        else
            # Run once for other algorithms
            echo "Running: python3 memsim.py $trace $frame $algorithm quiet" | tee -a "$output_file"
            python3 memsim.py "$trace" "$frame" "$algorithm" quiet >> "$output_file"
            echo "" >> "$output_file"
        fi
    done
}

# Define trace files and algorithms
traces=("swim.trace" "bzip.trace" "gcc.trace" "sixpack.trace")
algorithms=("rand" "lru" "clock")

# Run simulations for each combination of trace and algorithm
for trace in "${traces[@]}"; do
    for algorithm in "${algorithms[@]}"; do
        run_simulations "$trace" "$algorithm"
    done
done

echo "All simulations completed. Results are organized in the '$BASE_RESULTS_DIR' folder."
