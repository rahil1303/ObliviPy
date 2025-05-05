# Bucket Oblivious Sort (Option A - bucketorp_sim)

This repository provides a minimal and educational Python re-implementation of the Bucket Oblivious Sort algorithm, adapted from the original C++ reference. It focuses on simplicity, readability, and modular structure, serving as a foundation for future extensions and comparative benchmarking.

---

## 🗂 Directory Overview

| File             | Description                                                |
|------------------|------------------------------------------------------------|
| `bucket_orp.py`  | Main class containing the `BucketORP` oblivious sort logic |
| `element.py`     | Element class definition used in sorting                   |
| `server.py`      | Simulated server environment with data storage & logging   |
| `main.py`        | Basic run/test file to invoke the sorting algorithm        |
| `permutation.py` | Utility for shuffling or generating permutations. Not used |
| `test_patterns.py` | Script to compare access pattern logs                    |
| `requirements.txt` | Python dependencies. If any, not imported.               |

---

### Basic Sort Execution

python main.py


### Run Access Pattern Tests
To test whether the access pattern is oblivious:

python test_patterns.py

