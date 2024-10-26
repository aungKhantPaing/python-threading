import math
import os
import gzip
import shutil

def calculate_factorial():
    # Perform a more time-consuming task: calculate the factorial of a large number multiple times
    for _ in range(10):
        result = math.factorial(100000)
    return result

def compress_file(file_path):
    # Skip directories
    if os.path.isdir(file_path):
        return
    
    file_name = os.path.basename(file_path)
    output_dir = 'data/compressed'
    
    # Define the output gzip file path
    gzip_path = os.path.join(output_dir, f"{file_name}.gz")
    
    # Compress the file using gzip
    with open(file_path, 'rb') as f_in:
        with gzip.open(gzip_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)



def compress_files():
    input_dir = 'data/uncompressed'
    output_dir = 'data/compressed'

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Iterate over files in the input directory
    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        
        # Skip directories
        if os.path.isdir(file_path):
            continue
        
        # Define the output gzip file path
        gzip_path = os.path.join(output_dir, f"{filename}.gz")
        
        # Compress the file using gzip
        with open(file_path, 'rb') as f_in:
            with gzip.open(gzip_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

do_task = compress_files
