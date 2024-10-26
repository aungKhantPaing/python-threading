from task import do_task, compress_file
import os
import time

def main():
    input_dir = 'data/uncompressed'
    output_dir = 'data/compressed'

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    files = os.listdir(input_dir)
    print(f"Number of files to compress: {len(files)}")

    # Iterate over files in the input directory
    for i, filename in enumerate(files):
        prefix = f"File {i}/{len(files)}: "
        file_path = os.path.join(input_dir, filename)
        file_size_in_MB = os.path.getsize(file_path) / (1024 * 1024)
        start_time = time.time()
        print(f"{prefix}Compressing ({file_size_in_MB:.2f} MB) {file_path}")

        compress_file(file_path)
            
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"{prefix}Compression completed - Time taken: {elapsed_time:.2f}s")


if __name__ == "__main__":
    main()
