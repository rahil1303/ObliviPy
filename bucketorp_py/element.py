import numpy as np

# Define the structured dtype for an element
element_dtype = np.dtype([
    ('key', np.int32),
    ('aux', np.int32)
])

# Create a new element array of given size
def create_element_array(size, fill_dummy=False):
    arr = np.zeros(size, dtype=element_dtype)
    if fill_dummy:
        arr['key'] = -1
        arr['aux'] = -1
    return arr

# Create a single element
def make_element(key, aux=-1):
    return np.array((key, aux), dtype=element_dtype)

# Utility function: check if an element is a dummy
def is_dummy(elem):
    return elem['key'] == -1 and elem['aux'] == -1
