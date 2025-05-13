from element import Element
import random
import math
from collections import defaultdict

class BucketORP:
    def __init__(self, server, input_name, bucket_size, seed=42):
        self.server = server
        self.input_name = input_name
        self.bucket_size = bucket_size
        self.N = self.server.size(input_name)

        # B = smallest power of 2 >= 2n/Z
        min_buckets = math.ceil(2 * self.N / self.bucket_size)
        self.B = 1 << (min_buckets - 1).bit_length()

        self.inv_pi = {}
        self.rng = random.Random(seed)
        self.access_log = []

    def permute(self):
        print(f"[INFO] Permute starting for N = {self.N}, Z = {self.bucket_size}, B = {self.B}")
        self.random_bin_assignment()
        buckets = self.split_into_buckets()
        routed = self.merge_split_routing(buckets)
        output = self.final_shuffle(routed)
        return output

    def random_bin_assignment(self):
        logB = math.ceil(math.log2(self.B))
        for i in range(self.N):
            elem = self.server.get(self.input_name, i)
            elem.aux = self.rng.getrandbits(logB)
            self.server.put(self.input_name, i, elem)

    def split_into_buckets(self):
        for b in range(self.B):
            self.server.create_array(f"bucket_{b}", 0)

        for i in range(self.N):
            elem = self.server.get(self.input_name, i)
            bucket_id = elem.aux % self.B
            self.server.append(f"bucket_{bucket_id}", elem)

        for b in range(self.B):
            bucket_name = f"bucket_{b}"
            current_size = self.server.size(bucket_name)
            while current_size < self.bucket_size:
                self.server.append(bucket_name, Element(-1, -1))
                current_size += 1

        return [f"bucket_{b}" for b in range(self.B)]

    def merge_split_routing(self, buckets):
        current_buckets = buckets[:]
        rounds = math.ceil(math.log2(self.B))

        for r in range(rounds):
            print(f"[INFO] MergeSplit Round {r}")
            next_buckets = []

            # DEBUG: track real element count per output bucket in Round 0
            if r == 0:
                real_counts_debug = defaultdict(int)

            for i in range(0, len(current_buckets), 2):
                left_name = current_buckets[i]
                right_name = current_buckets[i+1] if i+1 < len(current_buckets) else None

                left = [self.server.get(left_name, j) for j in range(self.bucket_size)]
                right = [self.server.get(right_name, j) for j in range(self.bucket_size)] if right_name else [Element(-1, -1) for _ in range(self.bucket_size)]

                merged = left + right

                out0, out1 = [], []

                for elem in merged:
                    if elem.aux == -1:
                        out0.append(elem)
                    else:
                        bit = (elem.aux >> r) & 1
                        if bit:
                            out1.append(elem)
                        else:
                            out0.append(elem)

                real_count_0 = sum(1 for e in out0 if e.aux != -1)
                real_count_1 = sum(1 for e in out1 if e.aux != -1)

                if r == 0:
                    real_counts_debug[f"{i}_0"] = real_count_0
                    real_counts_debug[f"{i}_1"] = real_count_1

                # Skip overflow check in final round
                if r != rounds - 1:
                    if real_count_0 > self.bucket_size or real_count_1 > self.bucket_size:
                        raise OverflowError(
                            f"\n❌ BUCKET OVERFLOW (Round {r}, pair {i}/{i+1})\n"
                            f"   → Bucket 0: {real_count_0} real elems\n"
                            f"   → Bucket 1: {real_count_1} real elems\n"
                            f"   Limit: {self.bucket_size}"
                        )

                while len(out0) < self.bucket_size:
                    out0.append(Element(-1, -1))
                while len(out1) < self.bucket_size:
                    out1.append(Element(-1, -1))

                out0 = out0[:self.bucket_size]
                out1 = out1[:self.bucket_size]

                out0_name = f"route_r{r}_b{i}"
                out1_name = f"route_r{r}_b{i+1}"

                self.server.create_array(out0_name, 0)
                self.server.create_array(out1_name, 0)

                for elem in out0:
                    self.server.append(out0_name, elem)
                for elem in out1:
                    self.server.append(out1_name, elem)

                next_buckets.extend([out0_name, out1_name])

            if r == 0:
                print("[DEBUG] Round 0 real element distribution:")
                for k, v in real_counts_debug.items():
                    print(f"  Output bucket {k}: {v} real elements")

            current_buckets = next_buckets

        return current_buckets

    def final_shuffle(self, routed_buckets):
        output_name = "output_array"
        self.server.create_array(output_name, 0)

        real_elements = []
        for bucket_name in routed_buckets:
            for i in range(self.bucket_size):
                elem = self.server.get(bucket_name, i)
                if elem.aux != -1:
                    real_elements.append(elem)

        self.rng.shuffle(real_elements)

        for i, elem in enumerate(real_elements):
            self.inv_pi[i] = elem.key
            self.server.append(output_name, elem)

        return output_name

    def get_inv_pi(self, i):
        return self.inv_pi.get(i, None)
