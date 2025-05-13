from server_sim import Server
from element import Element
from bucket_orp_m import BucketORP
import math
import time
import statistics

# Helper function to get next power of 2
def next_power_of_2(n):
    return 1 if n == 0 else 2**(n - 1).bit_length()

def test_bucket_overflow_limits():
    """
    This test function determines the practical limits of obliviousness
    by gradually reducing bucket size until overflows occur.
    """
    N = 10000  # Number of elements
    trials = 3

    print("Testing bucket overflow limits:")
    print("-" * 50)
    print(f"Input size: {N} elements")
    print(f"Trials per bucket size: {trials}")
    print("-" * 50)

    # Test with decreasing bucket sizes
    for Z in [256, 128, 64, 32, 16, 8]:
        print(f"\nTesting with bucket size Z = {Z}:")

        min_buckets = math.ceil(2 * N / Z)
        B = next_power_of_2(min_buckets)
        print(f"Using {B} buckets (min required: {min_buckets})")

        overflow_count = 0
        times = []

        for t in range(trials):
            start_time = time.time()
            try:
                s = Server()
                s.create_array("input", N)
                for i in range(N):
                    s.put("input", i, Element(key=i))

                orp = BucketORP(server=s, input_name="input", bucket_size=Z, seed=t)
                output_name = orp.permute()

                end_time = time.time()
                times.append(end_time - start_time)
                print(f"  Trial {t+1}: Success \u2713  ({times[-1]:.4f}s, {s.get_io()} I/Os)")

            except OverflowError as e:
                end_time = time.time()
                overflow_count += 1
                print(f"  Trial {t+1}: OVERFLOW \u2717  ({end_time - start_time:.4f}s)")

        success_rate = (trials - overflow_count) / trials * 100
        if times:
            avg_time = statistics.mean(times)
            print(f"  Success rate: {success_rate:.1f}%")
            print(f"  Average time for successful runs: {avg_time:.4f}s")
        else:
            print(f"  Success rate: 0% (all trials overflowed)")

        print(f"  Observed failure rate: {overflow_count/trials:.4f}")
        print(f"  Theoretical failure probability: {math.exp(-Z/6):.4f}")

        if overflow_count > trials // 2:
            print(f"\nBucket size Z = {Z} appears to be too small for reliable operation with {N} elements.")
            print(f"Recommended minimum Z value: {Z*2}")
            break

if __name__ == "__main__":
    test_bucket_overflow_limits()
