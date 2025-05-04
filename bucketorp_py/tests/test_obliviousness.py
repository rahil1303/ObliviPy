import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import random
from server import Server
from client import BucketObliviousSort
from element import make_element

def run_oblivious_sort(input_keys, Z, seed=42):
    s = Server()
    s.create_array("input", 0)
    for k in input_keys:
        s.append("input", make_element(k))

    sorter = BucketObliviousSort(s, "input", Z, seed)
    sorter.permute()
    return s.get_log()

# === Test Parameters ===
N = 100
Z = 16

# Generate two different input permutations
input1 = list(range(N))
random.shuffle(input1)

input2 = list(range(N))
random.shuffle(input2)

# Run and compare logs
log1 = run_oblivious_sort(input1, Z)
log2 = run_oblivious_sort(input2, Z)

# === Compare Access Patterns ===
print("Log 1 length:", len(log1))
print("Log 2 length:", len(log2))

if log1 == log2:
    print("✅ Access logs match — permutation is oblivious.")
else:
    print("❌ Access logs differ — permutation is not oblivious.")
