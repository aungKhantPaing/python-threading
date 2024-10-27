from concurrent.futures import ThreadPoolExecutor
from task import compress_file_parallel
import os
from time import time

def worker_parallel(file_path, max_process, prefix=""):
    """Worker function to compress a single file and return timing information."""
    file_size_in_MB = os.path.getsize(file_path) / (1024 * 1024)
    start_time = time()
    
    print(f"{prefix}Compressing ({file_size_in_MB:.2f} MB) {file_path}")
    compress_file_parallel(file_path, threads=max_process)
    
    end_time = time()
    elapsed_time = end_time - start_time
    print(f"{prefix}Compression completed - Time taken: {elapsed_time:.2f}s")
    
    return {
        'file': os.path.basename(file_path),
        'size_mb': file_size_in_MB,
        'time': elapsed_time
    }

def process_parallel(input_dir, max_workers=None, max_process=1):
    """Process files in parallel and return timing results."""
    results = []
    files = os.listdir(input_dir)
    nFiles = len(files)
    
    if max_workers is None:
        max_workers = nFiles
    
    start_time = time()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for i, filename in enumerate(files, start=1):
            prefix = f"Parallel({max_workers}T{max_process}P) - File {i}/{nFiles}: "
            file_path = os.path.join(input_dir, filename)
            future = executor.submit(worker_parallel, file_path, max_process, prefix)
            futures.append(future)
        
        for future in futures:
            result = future.result()
            results.append(result)
    
    total_time = time() - start_time
    return results, total_time