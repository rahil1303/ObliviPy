from server_sim import Server
from element import Element
from bucket_orp_m import BucketORP
import math
import time
import statistics

def next_power_of_2(n):
    return 1 if n == 0 else 2**(n - 1).bit_length()

def test_obliviousness(N, Z, B):
    inputs = [
        list(range(N)),              # Ascending
        list(range(N - 1, -1, -1))   # Descending
    ]

    logs = []
    for trial_input in inputs:
        s = Server()
        s.create_array("input", N)
        for i, val in enumerate(trial_input):
            s.put("input", i, Element(key=val))

        orp = BucketORP(server=s, input_name="input", bucket_size=Z, seed=42)
        try:
            orp.permute()
            logs.append(orp.access_log)
        except OverflowError as e:
            return False, f"Overflow: {str(e)}"

    return logs[0] == logs[1], len(logs[0])

def test_oblivious_and_overflow():
    N = 10000
    trials = 3

    print("Testing bucket overflow + obliviousness:")
    print("-" * 50)
    print(f"Input size: {N} elements")
    print(f"Trials per bucket size: {trials}")
    print("-" * 50)

    for Z in [256, 128, 64, 32, 16]:
        min_buckets = math.ceil(2 * N / Z)
        B = next_power_of_2(min_buckets)
        print(f"\nTesting with bucket size Z = {Z} (B = {B}):")

        overflow_count = 0
        for t in range(trials):
            try:
                s = Server()
                s.create_array("input", N)
                for i in range(N):
                    s.put("input", i, Element(key=i))

                orp = BucketORP(server=s, input_name="input", bucket_size=Z, seed=t)
                orp.permute()
                print(f"  Trial {t + 1}: Success ✓")

            except OverflowError as e:
                print(f"  Trial {t + 1}: OVERFLOW ✗")
                overflow_count += 1

        print(f"  Success rate: {(trials - overflow_count) / trials * 100:.1f}%")
        print(f"  Observed failure rate: {overflow_count / trials:.4f}")
        print(f"  Theoretical failure probability: {math.exp(-Z / 6):.4f}")

        if overflow_count == 0:
            is_oblivious, result = test_obliviousness(N, Z, B)
            if is_oblivious:
                print(f"  ✅ Oblivious access pattern confirmed (log length: {result})")
            else:
                print(f"  ❌ Non-oblivious or failed test (Reason: {result})")

        if overflow_count > trials // 2:
            print(f"\nBucket size Z = {Z} appears too small for reliable operation.")
            print(f"Recommended minimum Z: {Z * 2}")
            break

if __name__ == "__main__":
    test_oblivious_and_overflow()
