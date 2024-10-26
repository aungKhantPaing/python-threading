import threading
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
    print(f"Number of files to compress: {nFiles}")

    threads = []
    # Iterate over files in the input directory
    for i, filename in enumerate(files):
        prefix = f"File {i}/{nFiles}: "
        file_path = os.path.join(input_dir, filename)

        thread = threading.Thread(target=worker, args=(file_path, prefix))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("All workers have finished")

if __name__ == "__main__":
    main()
