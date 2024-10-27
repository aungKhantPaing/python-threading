import os
from time import time
from task import compress_file_parallel, compress_file
from statistics import mean, stdev

def worker_sequential(file_path, prefix=""):
    """Worker function to compress a single file and return timing information."""
    file_size_in_MB = os.path.getsize(file_path) / (1024 * 1024)
    start_time = time()
    
    print(f"{prefix}Compressing ({file_size_in_MB:.2f} MB) {file_path}")
    compress_file(file_path)
    
    end_time = time()
    elapsed_time = end_time - start_time
    print(f"{prefix}Compression completed - Time taken: {elapsed_time:.2f}s")
    
    return {
        'file': os.path.basename(file_path),
        'size_mb': file_size_in_MB,
        'time': elapsed_time
    }

def process_sequential(input_dir):
    """Process files sequentially and return timing results."""
    results = []
    files = os.listdir(input_dir)
    nFiles = len(files)
    
    start_time = time()
    for i, filename in enumerate(files, start=1):
        prefix = f"Sequential - File {i}/{nFiles}: "
        file_path = os.path.join(input_dir, filename)
        result = worker_sequential(file_path, prefix)
        results.append(result)
    
    total_time = time() - start_time
    return results, total_time