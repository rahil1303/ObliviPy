from element import create_element_array, make_element, is_dummy

# Create an array of 5 dummy elements
A = create_element_array(5, fill_dummy=True)

# Replace first with real element
A[0] = make_element(42, aux=2)

# Check dummy status
print(A)
print("First is dummy?", is_dummy(A[0]))
print("Second is dummy?", is_dummy(A[1]))

from server import Server
from client import BucketObliviousSort
from element import make_element

# Setup parameters
N = 32             # Total number of elements
Z = 4              # Bucket size
seed = 42          # Fixed seed for reproducibility

# === Initialize Server ===
s = Server()
s.create_array("input", 0)

# Populate input array with real elements
for i in range(N):
    s.append("input", make_element(i))

# === Run Oblivious Sort ===
orp = BucketObliviousSort(server=s, input_name="input", bucket_size=Z, seed=seed)
output_name = orp.permute()

# === Show Final Result ===
print("\nFinal permuted array:")
for i in range(s.size(output_name)):
    print(s.get(output_name, i))

# === Server I/O Log Summary ===
print(f"\nTotal server I/Os: {len(s.get_log())}")
