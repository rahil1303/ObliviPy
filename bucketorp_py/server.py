import numpy as np
from collections import defaultdict
from element import element_dtype

class Server:
    def __init__(self):
        self.storage = {}               # Dict: name → np.ndarray
        self.access_log = []            # List of (op, array_name, index)

    def create_array(self, name, size, fill_dummy=False):
        """Initialize an array with dummy or zeroed elements."""
        from element import create_element_array
        self.storage[name] = create_element_array(size, fill_dummy)

    def get(self, name, index):
        """Simulate oblivious read."""
        self.access_log.append(('get', name, index))
        return self.storage[name][index]

    def put(self, name, index, value):
        """Simulate oblivious write."""
        self.access_log.append(('put', name, index))
        self.storage[name][index] = value

    def append(self, name, value):
        """Append value to array (used for buckets)."""
        arr = self.storage[name]
        new_arr = np.append(arr, np.array([value], dtype=element_dtype))
        self.storage[name] = new_arr
        self.access_log.append(('append', name, len(arr)))  # log previous last index

    def size(self, name):
        return len(self.storage[name])

    def get_log(self):
        return self.access_log

    def reset_log(self):
        self.access_log = []
