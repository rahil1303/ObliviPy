# 🧪 gRPC-Setup: Oblivious Sort System

This directory contains the complete setup for a gRPC-based system that performs **oblivious permutation** using a simulated secure server.

---

## 📦 Folder Contents

| File / Folder                 | Purpose |
|------------------------------|---------|
| `bucket_orp.py`              | Core logic for oblivious permutation |
| `bucket_orp_debug.py`        | Same as above with debug output for internal steps |
| `client.py`                  | gRPC client to send sort requests and receive output |
| `server.py`                  | gRPC server exposing the `Permute` and `GetAccessLog` RPCs |
| `server_sim.py`              | Simulates secure memory with logging of access patterns |
| `element.py`                 | Defines `Element` objects used throughout the sorting pipeline |
| `main.py`                    | Standalone, non-gRPC test of the permutation process |
| `test_obliviousness_grpc.py` | Tests whether memory access patterns are the same across inputs |
| `test_patterns.py`           | Alternate obliviousness test without gRPC |
| `requirements.txt`           | Python dependencies for running the project |
| `proto/`                     | Contains `.proto` definitions used for gRPC |
| `oblivious_sort_pb2.py` / `oblivious_sort_pb2_grpc.py` | Auto-generated gRPC code |

---

## ✅ How to Use

### 1. Install Dependencies
```bash
pip install -r requirements.txt

