# bucket_orp.py

from element import Element
import random
import math


class BucketORP:
    def __init__(self, server, input_name, bucket_size, seed = 42):
        self.server = server
        self.input_name = input_name
        self.bucket_size = bucket_size
        self.N = self.server.size(input_name)
        self.B = (self.N + bucket_size - 1) // bucket_size  # total buckets
        self.inv_pi = {}  # optional
        random.seed(seed)

    def permute(self):
        self.random_bin_assignment()
        buckets = self.split_into_buckets()
        routed = self.merge_split_routing(buckets)
        output = self.final_shuffle(routed)
        return output  # name of final permuted array

    def random_bin_assignment(self):
        for i in range(self.N):
            elem = self.server.get(self.input_name, i)
            bin_id = random.randint(0, self.B - 1)
            elem.aux = bin_id
            self.server.put(self.input_name, i, elem)


    def split_into_buckets(self):
        # Step 1: create empty buckets
        for b in range(self.B):
            self.server.create_array(f"bucket_{b}", 0)

        # Step 2: distribute elements
        for i in range(self.N):
            elem = self.server.get(self.input_name, i)
            bucket_id = elem.aux
            self.server.append(f"bucket_{bucket_id}", elem)

        # Step 3: pad with dummies
        for b in range(self.B):
            bucket_name = f"bucket_{b}"
            current_size = self.server.size(bucket_name)
            while current_size < self.bucket_size:
                dummy = Element(key=-1, aux=-1)
                self.server.append(bucket_name, dummy)
                current_size += 1

        # Return list of bucket names
        return [f"bucket_{b}" for b in range(self.B)]


    def merge_split_routing(self, buckets):

        current_buckets = buckets[:]
        rounds = math.ceil(math.log2(self.B))

        for r in range(rounds):
            next_buckets = []

            for i in range(0, len(current_buckets), 2):
                left_name = current_buckets[i]
                right_name = current_buckets[i+1] if i+1 < len(current_buckets) else None

                # Read both buckets fully
                left = [self.server.get(left_name, j) for j in range(self.bucket_size)]
                right = [self.server.get(right_name, j) for j in range(self.bucket_size)] if right_name else [Element(-1, -1) for _ in range(self.bucket_size)]

                merged = left + right

                # Prepare output buckets
                out0_name = f"route_r{r}_b{i}"
                out1_name = f"route_r{r}_b{i+1}"
                self.server.create_array(out0_name, 0)
                self.server.create_array(out1_name, 0)

                # Determine routing based on current bit in aux
                out0, out1 = [], []
                for elem in merged:
                    if elem.aux == -1:
                        out0.append(elem)
                    else:
                        bit = (elem.aux >> r) & 1
                        (out1 if bit else out0).append(elem)

                # Pad both outputs to bucket_size
                for out, name in [(out0, out0_name), (out1, out1_name)]:
                    while len(out) < self.bucket_size:
                        out.append(Element(-1, -1))
                    for elem in out:
                        self.server.append(name, elem)

                next_buckets.extend([out0_name, out1_name])

            current_buckets = next_buckets

        return current_buckets


    def final_shuffle(self, routed_buckets):
        output_name = "output_array"
        self.server.create_array(output_name, 0)

        real_elements = []

        # Collect all real elements from routed buckets
        for bucket_name in routed_buckets:
            for i in range(self.bucket_size):
                elem = self.server.get(bucket_name, i)
                if elem.aux != -1:  # skip dummies
                    real_elements.append(elem)

            # Shuffle real elements randomly
        random.shuffle(real_elements)

        # Optional: maintain inverse mapping for verification
        for i, elem in enumerate(real_elements):
            self.inv_pi[i] = elem.key
            self.server.append(output_name, elem)

        return output_name


    def get_inv_pi(self, i):
        return self.inv_pi.get(i, None)
