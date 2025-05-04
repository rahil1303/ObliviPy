import numpy as np
import random
from collections import defaultdict
from element import make_element, is_dummy, element_dtype
from server import Server

class BucketObliviousSort:
    def __init__(self, server, input_name, bucket_size, seed=42):
        self.server = server
        self.input_name = input_name
        self.Z = bucket_size
        self.N = server.size(input_name)
        self.B = (self.N + self.Z - 1) // self.Z
        self.inv_pi = {}  # Optional
        random.seed(seed)

    def permute(self):
        self.assign_bins()
        buckets = self.split_into_buckets()
        routed = self.merge_split_routing(buckets)
        output = self.final_shuffle(routed)
        return output

    def assign_bins(self):
        """Assign each element a random bin (0 to B-1) using aux field."""
        for i in range(self.N):
            elem = self.server.get(self.input_name, i)
            elem['aux'] = random.randint(0, self.B - 1)
            self.server.put(self.input_name, i, elem)

    def split_into_buckets(self):
        """Group elements into buckets based on bin ID (aux)."""
        # Create empty buckets
        for b in range(self.B):
            self.server.create_array(f"bucket_{b}", 0)

        # Distribute elements
        for i in range(self.N):
            elem = self.server.get(self.input_name, i)
            bucket_id = elem['aux']
            self.server.append(f"bucket_{bucket_id}", elem)

        # Pad each bucket to size Z
        for b in range(self.B):
            bucket_name = f"bucket_{b}"
            while self.server.size(bucket_name) < self.Z:
                self.server.append(bucket_name, make_element(-1, -1))

        return [f"bucket_{b}" for b in range(self.B)]

    def merge_split_routing(self, bucket_names):
        """Perform log(B) rounds of oblivious merge-split routing."""
        current = bucket_names[:]
        rounds = int(np.ceil(np.log2(self.B)))

        for r in range(rounds):
            next_round = []

            for i in range(0, len(current), 2):
                left_name = current[i]
                right_name = current[i+1] if i+1 < len(current) else None

                # Load both buckets
                left = [self.server.get(left_name, j) for j in range(self.Z)]
                if right_name:
                    right = [self.server.get(right_name, j) for j in range(self.Z)]
                else:
                    right = [make_element(-1, -1)] * self.Z

                # Convert to structured NumPy array
                merged = np.array(left + right, dtype=element_dtype)

                # Create masks
                is_dummy_mask = (merged['key'] == -1) & (merged['aux'] == -1)
                bit_mask = ((merged['aux'] >> r) & 1)

                # Route real elements based on bit
                out0 = merged[(bit_mask == 0) | is_dummy_mask]
                out1 = merged[(bit_mask == 1) & ~is_dummy_mask]

                # Pad both to size Z
                pad0 = self.Z - len(out0)
                pad1 = self.Z - len(out1)

                if pad0 > 0:
                    out0 = np.append(out0, [make_element(-1, -1)] * pad0)
                if pad1 > 0:
                    out1 = np.append(out1, [make_element(-1, -1)] * pad1)

                # Write to new buckets
                out0_name = f"route_r{r}_b{i}"
                out1_name = f"route_r{r}_b{i+1}"

                self.server.create_array(out0_name, 0)
                self.server.create_array(out1_name, 0)

                for elem in out0:
                    self.server.append(out0_name, elem)
                for elem in out1:
                    self.server.append(out1_name, elem)

                next_round.extend([out0_name, out1_name])

            current = next_round

        return current

    def final_shuffle(self, routed_bucket_names):
        """Collect all real elements and perform a final random shuffle."""
        output_name = "output_array"
        self.server.create_array(output_name, 0)

        real_elements = []

        for bucket_name in routed_bucket_names:
            for i in range(self.Z):
                elem = self.server.get(bucket_name, i)
                if not is_dummy(elem):
                    real_elements.append(elem)

        random.shuffle(real_elements)

        for i, elem in enumerate(real_elements):
            self.inv_pi[i] = elem['key']  # Optional for inverse lookup
            self.server.append(output_name, elem)

        return output_name

    def get_inv_pi(self, i):
        return self.inv_pi.get(i, None)

