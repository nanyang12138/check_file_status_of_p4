#!/usr/bin/env python3

import os  
import subprocess  
import sys  
import pdb

def get_perforce_files(directory):  
    p4 = "/tool/pandora64/bin/p4"
    try:  
        result = subprocess.run([p4, 'have', f'{directory}/...'], capture_output=True, text=True)  

        if result.returncode != 0:  
            print(f"Error: {result.stderr}")  
            sys.exit(1) 

        perforce_files = set()  
        for line in result.stdout.splitlines():  
            parts = line.split(' - ')  
            if len(parts) > 0:  
                perforce_files.add(parts[1].strip())  
          
        return perforce_files  
    except Exception as e:  
        print(f"Error retrieving Perforce files: {e}")  
        return set()  
  
def check_directory(directory):  
    perforce_files = get_perforce_files(directory) 
    
    for root, _, files in os.walk(directory):  
        for file in files:  
            abs_file_path = os.path.abspath(os.path.join(root, file))  
            if abs_file_path not in perforce_files and f"{os.environ['STEM']}/import" not in abs_file_path and f"{os.environ['OUT_HOME']}" not in abs_file_path:  
                print(f"{abs_file_path} is NOT in Perforce.")  
  
if __name__ == "__main__": 
    if len(sys.argv) < 2:  
        print("Usage: python script.py <directory_to_check>")  
        sys.exit(1)  

    directory_to_check = sys.argv[1]  
    check_directory(directory_to_check)  
