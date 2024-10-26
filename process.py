from concurrent.futures import ProcessPoolExecutor
import multiprocessing
from task import compress_file
import os
from time import time

def worker(file_path, prefix):
    file_size_in_MB = os.path.getsize(file_path) / (1024 * 1024)
    start_time = time()
    print(f"{prefix}Compressing ({file_size_in_MB:.2f} MB) {file_path}")

    compress_file(file_path)
        
    end_time = time()
    elapsed_time = end_time - start_time
    print(f"{prefix}Compression completed - Time taken: {elapsed_time:.2f}s")


def main():
    input_dir = 'data/uncompressed'
    output_dir = 'data/compressed'

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    files = os.listdir(input_dir)
    nFiles = len(files)
    nCpus = multiprocessing.cpu_count()
    print(f"Number of files to compress: {nFiles}")
    print(f"Number of CPUs: {nCpus}")

    with ProcessPoolExecutor(max_workers=nCpus) as executor:
        futures = []
        # Iterate over files in the input directory
        for i, filename in enumerate(files, start=1):
            prefix = f"File {i}/{nFiles}: "
            file_path = os.path.join(input_dir, filename)

            future = executor.submit(worker, file_path, prefix)
            futures.append(future)
        
        # Wait for all futures to complete
        for future in futures:
            future.result()

    print("All workers have finished")

if __name__ == "__main__":
    main()

