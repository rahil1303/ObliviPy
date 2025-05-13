# ObliviPy — Oblivious Permutation & Sort Experiments

This repository contains multiple implementations and experimental setups for Bucket Oblivious Random Permutation (ORP) and related oblivious sort logic.

---

## Repository Structure

| Folder / File     | Description |
|-------------------|-------------|
| `bucketorp_py/`   | Pythonic implementation with functional style (Option B) |
| `bucketorp_sim/`  | Object-oriented implementation, closely following the paper (Option A) |
| `gRPC-Setup/`     | Full gRPC client-server setup for remote oblivious permutation and access log testing |
| `op_overflow/`    | Scripts for testing overflow limits and theoretical failure rates |
| `README.md`       | This file |

Each subdirectory contains its own `README.md` describing local purpose, files, and usage instructions.

---

## ⚙️ Requirements

- Python 3.7+
- `numpy`

You can install the dependencies via:

```bash
pip install numpy
