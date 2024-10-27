import math
import os
import gzip
import shutil
from pygz import PigzFile

output_dir = 'output/'

def compress_file(file_path, output_dir='output/'):
    # Skip directories
    if os.path.isdir(file_path):
        return
    
    file_name = os.path.basename(file_path)
    
    # Define the output gzip file path
    gzip_path = os.path.join(output_dir, f"{file_name}.gz")
    
    # Compress the file using gzip
    with open(file_path, 'rb') as f_in:
        with gzip.open(gzip_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

def compress_file_parallel(file_path, threads, output_dir='output/'):
    # Skip directories
    if os.path.isdir(file_path):
        return
    
    file_name = os.path.basename(file_path)
    
    # Define the output gzip file path
    gzip_path = os.path.join(output_dir, f"{file_name}.gz")
    
    # Compress the text file using pygz
    with open(file_path, 'rt') as f_in:
        with PigzFile(path=gzip_path, mode='wt', threads=threads) as f_out:
            shutil.copyfileobj(f_in, f_out)
