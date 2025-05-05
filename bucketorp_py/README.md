# Bucket Oblivious Sort (Option B - bucketorp_py)

This implementation provides a Pythonic and modular version of Bucket Oblivious Sort using simple function-based design. It is built to parallel the logic of the original C++ codebase, but focuses more on readability and high-level experimentation for benchmarking oblivious sorting algorithms.

---

## 🗂 Project Structure

| File/Folder       | Description                                                   |
|-------------------|---------------------------------------------------------------|
| `client.py`       | Core implementation of the `BucketObliviousSort` logic        |
| `server.py`       | Simulated server layer managing array storage and logging     |
| `element.py`      | Helper for creating and managing elements to be sorted        |
| `utils.py`        | Utility functions for common operations (e.g., shuffling)      |
| `main.py`         | Run entry point for basic permutation execution               |
| `tests/`          | Folder containing access log comparison and test scripts      |

---

### Basic Sorting Execution

python main.py

### Access Pattern Test

python tests/test_obliviousness.py


