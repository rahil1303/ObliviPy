from server import Server
from element import Element
from bucket_orp import BucketORP

# --- SANITY TEST (Litmus Check) ---
print("=== Server Litmus Test ===")
s_test = Server()
s_test.create_array("A", 5)
s_test.put("A", 2, "Hello")
print(s_test.get("A", 2))         # Should print: Hello
print(s_test.get_log())           # Should print: [('put', 'A', 2), ('get', 'A', 2)]
print()

# --- BUCKET ORP SETUP ---
print("=== Oblivious Permutation ===")
N = 100                   # Number of elements
Z = 16                    # Bucket size (Z)
INPUT_NAME = "input"

s = Server()
s.create_array(INPUT_NAME, N)

for i in range(N):
    s.put(INPUT_NAME, i, Element(key=i))

# Run ORP
orp = BucketORP(server=s, input_name=INPUT_NAME, bucket_size=Z)
output_name = orp.permute()

# Print permuted result
print(f"\nFinal permuted array ({output_name}):")
for i in range(s.size(output_name)):
    print(s.get(output_name, i))

# I/O Summary
print(f"\nTotal server I/Os: {s.get_io()}")
print(f"Access log entries: {len(s.get_log())}")
 