import numpy as np
import os
import sys
import multiprocessing
import time
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from terrariaworld import TerrariaWorld

def main():
    wld = TerrariaWorld()
    wld.load_world()

    ellapsed = {}
    process_counts = [4, 6, 8, multiprocessing.cpu_count()]
    for count in process_counts:
        T = time.time()
        wld.save_world("test.wld", process_units=count)
        ellapsed[count] = time.time() - T
    
    for count in process_counts:
        print(f"MultiProcess Count : {count}, {ellapsed[count]} secs taken.")

    os.remove("test.wld")

if __name__ == "__main__":
    main()