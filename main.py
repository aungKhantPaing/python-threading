import argparse
import os
import matplotlib.pyplot as plt
import json
from statistics import mean, stdev
from parallel import process_parallel
from sequential import process_sequential

def run_benchmark(input_dir, num_runs=3):
    """Run multiple benchmark tests and collect results."""
    # os.makedirs(output_dir, exist_ok=True)
    
    benchmark_results = {
        'sequential': [],
        'parallel_2T1P': [],
        'parallel_4T1P': [],
        'parallel_8T1P': [],
    }
    
    files = os.listdir(input_dir)
    nFiles = len(files)
    nWorkers = [2, 4, 8]
    # if nFiles > 8:
    #     benchmark_results[f'parallel_{nFiles}'] = []
    #     nWorkers.append(nFiles)
      
    print(f"\nNumber of files: {nFiles}")
    print(f"Number of workers: {nWorkers}")
    print(f"Benchmark results: {benchmark_results}")

    # Run multiple benchmarks
    for run in range(num_runs):
        print(f"\nBenchmark Run {run + 1}/{num_runs}")
        
        # Sequential run
        print("\nRunning Sequential Processing...")
        seq_results, seq_total = process_sequential(input_dir)
        benchmark_results['sequential'].append(seq_total)
        
        # Parallel runs with different worker counts
        for workers in nWorkers:
            print(f"\nRunning Parallel Processing ({workers} workers)...")
            par_results, par_total = process_parallel(input_dir, max_workers=workers)
            benchmark_results[f'parallel_{workers}T1P'].append(par_total)

        # Parallet runs with max worker counts and CPUs
        workers = nFiles
        processes = os.cpu_count()
        benchmark_results[f'parallel_{workers}T{processes}P_max'] = []
        print(f"\nRunning Parallel Processing ({workers} workers, {processes} processes)...")
        par_results, par_total = process_parallel(input_dir, max_workers=workers, max_process=processes)
        benchmark_results[f'parallel_{workers}T{processes}P_max'].append(par_total)
    
    return benchmark_results

def generate_report(benchmark_results):
    """Generate and save performance report."""
    # Calculate statistics
    stats = {}
    for method, times in benchmark_results.items():
        stats[method] = {
            'mean': mean(times),
            'std': stdev(times) if len(times) > 1 else 0,
            'min': min(times),
            'max': max(times)
        }
    
    # Save raw results
    with open('benchmark_results.json', 'w') as f:
        json.dump(benchmark_results, f, indent=4)
    
    # Create performance plot
    methods = list(stats.keys())
    means = [stats[m]['mean'] for m in methods]
    errors = [stats[m]['std'] for m in methods]
    
    plt.figure(figsize=(10, 6))
    plt.bar(methods, means, yerr=errors, capsize=5)
    plt.title('File Compression Performance Comparison')
    plt.xlabel('Processing Method')
    plt.ylabel('Total Processing Time (seconds)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('performance_comparison.png')
    
    # Calculate speedup ratios
    sequential_time = stats['sequential']['mean']
    speedups = {
        method: sequential_time / stats[method]['mean']
        for method in methods if method != 'sequential'
    }
    
    # Create summary report
    report = {
        'statistics': stats,
        'speedup_ratios': speedups
    }
    
    with open('benchmark_report.json', 'w') as f:
        json.dump(report, f, indent=4)
    
    return stats, speedups

def main():
    parser = argparse.ArgumentParser(description="Benchmarking script for sequential and parallel processing.")
    parser.add_argument('input_dir', type=str, help='Directory containing input files')
    # parser.add_argument('output_dir', type=str, help='Directory to save output files')
    
    args = parser.parse_args()
    
    input_dir = args.input_dir
    # output_dir = args.output_dir
    
    print("Starting benchmark tests...")
    results = run_benchmark(input_dir, num_runs=3)
    
    print("\nGenerating performance report...")
    stats, speedups = generate_report(results)
    
    # Print summary
    print("\nPerformance Summary:")
    print("-" * 50)
    for method, stat in stats.items():
        print(f"\n{method.upper()}:")
        print(f"Average time: {stat['mean']:.2f}s ± {stat['std']:.2f}s")
        print(f"Range: {stat['min']:.2f}s - {stat['max']:.2f}s")
    
    print("\nSpeedup Ratios:")
    print("-" * 50)
    for method, speedup in speedups.items():
        print(f"{method}: {speedup:.2f}x faster than sequential")

if __name__ == "__main__":
    main()