from server import Server
from element import Element
from bucket_orp import BucketORP
import random

def run_orp_get_log(input_values, N, Z):
    random.seed(42)  # ✅ makes random ops consistent across runs
    s = Server()
    s.create_array("input", N)

    for i in range(N):
        s.put("input", i, Element(key=input_values[i]))

    orp = BucketORP(server=s, input_name="input", bucket_size=Z)
    _ = orp.permute()

    return s.get_log()

def logs_are_equal(log1, log2):
    if len(log1) != len(log2):
        return False
    return all(a == b for a, b in zip(log1, log2))

def main():
    N = 100
    Z = 16

    input1 = list(range(N))             # Increasing order
    input2 = list(range(N-1, -1, -1))    # Decreasing order

    log1 = run_orp_get_log(input1, N, Z)
    log2 = run_orp_get_log(input2, N, Z)

    print(f"Log 1 length: {len(log1)}")
    print(f"Log 2 length: {len(log2)}")

    if logs_are_equal(log1, log2):
        print("✅ Access logs match — permutation is oblivious.")
    else:
        print("❌ Access logs differ — permutation is not oblivious.")

if __name__ == "__main__":
    main()
