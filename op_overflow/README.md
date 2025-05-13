# Overflow Detection and Obliviousness Validation

This section of the repository is dedicated to testing **bucket overflow handling** and verifying **oblivious access patterns** in the local setup without gRPC.

---

## Folder Contents

| File                          | Purpose |
|-------------------------------|---------|
| `bucket_orp_m.py`            | Variant of BucketORP with modified or extended logging/debug hooks |
| `test_overflow_limits_d.py`  | Main script to test for bucket overflows and check obliviousness |
| `server_sim.py`              | Simulates secure memory server with access logging |
| `element.py`                 | Core `Element` class definition |
| `overflow_log.txt`           | Output log from overflow detection trials |

---

## 🔧 How to Use

### 1. Run the Overflow Check
```bash
python test_overflow_limits_d.py
```

This script:
- Tests a range of bucket sizes (Z = 256, 128, 64, 32, 16)
- Repeats the permutation 3 times per size
- Reports `OverflowError` if a bucket capacity is exceeded
- Compares observed failure rate vs theoretical overflow bound

Example output:
```
Testing bucket overflow + obliviousness:
Input size: 10000 elements
Z = 64: Trial 1: Success ✓
Z = 64: Trial 2: OVERFLOW ✗
...
Theoretical failure probability: 0.0025
```

---

## Additional Checks

If no overflows are observed for a given bucket size, the script then checks **obliviousness** by comparing memory access logs for two different input sequences:
- Ascending: `[0, 1, 2, ..., N-1]`
- Descending: `[N-1, ..., 2, 1, 0]`

If the access logs are **identical**, oblivious behavior is confirmed:
```
✅ Oblivious access pattern confirmed (log length: 25421)
```

---

## Output

- Detailed printouts appear in the terminal.
- You can optionally redirect output to `overflow_log.txt` if needed:
```bash
python test_overflow_limits_d.py > overflow_log.txt
```

---

## Reset Server State

The `Server` class in `server_sim.py` is reset on each trial to ensure isolation of access patterns.

---

