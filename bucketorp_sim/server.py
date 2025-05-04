# server.py

class Server:
    def __init__(self):
        self.memory = {}         # { array_name: [elements] }
        self.access_log = []     # list of (op, array_name, index)
        self.io_count = 0

    def create_array(self, name, size):
        self.memory[name] = [None] * size

    def put(self, name, index, element):
        self._log_access("put", name, index)
        self.memory[name][index] = element
        self.io_count += 1

    def get(self, name, index):
        self._log_access("get", name, index)
        self.io_count += 1
        return self.memory[name][index]

    def append(self, name, element):
        self._log_access("append", name, len(self.memory[name]))
        self.memory[name].append(element)
        self.io_count += 1

    def size(self, name):
        return len(self.memory.get(name, []))

    def reset_io(self):
        self.io_count = 0
        self.access_log.clear()

    def get_io(self):
        return self.io_count

    def get_log(self):
        return self.access_log

    def _log_access(self, operation, name, index):
        self.access_log.append((operation, name, index))
