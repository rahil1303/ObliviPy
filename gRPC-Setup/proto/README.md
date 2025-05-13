# 📄 Proto Definitions — gRPC Messages and Services

This folder contains the protocol buffer (`.proto`) definitions for the **Oblivious Sorter** gRPC service. It defines the messages and RPCs used by the client and server to communicate for oblivious permutation and access log tracking.

---

## 🧠 Service: `ObliviousSorter`

```proto
service ObliviousSorter {
  rpc Permute (SortRequest) returns (SortReply);
  rpc GetAccessLog (AccessLogRequest) returns (AccessLogReply);
}
```

### RPCs

- **`Permute`**: Sends an integer array to the server and receives the sorted (oblivious) result along with performance metrics.
- **`GetAccessLog`**: Returns the list of memory access operations performed, useful for verifying obliviousness.

---

## 📦 Message Types

### `SortRequest`
```proto
repeated int32 input = 1;
```
- The input array to be permuted/sorted.

### `SortReply`
```proto
repeated int32 output = 1;
int32 io_count = 2;
double time_taken = 3;
```
- The output array, number of memory accesses, and execution time.

---

### `AccessLogRequest`
```proto
bool clear = 1;
```
- If `true`, the server will clear the access log after returning it.

### `AccessEntry`
```proto
string op = 1;
string array = 2;
int32 index = 3;
```
- Represents a single memory operation (e.g., `"get"`, `"put"`, `"append"`) on a named array and index.

### `AccessLogReply`
```proto
repeated AccessEntry log = 1;
```
- Full list of access operations captured during the last run.

---

## ⚙️ Regenerate Python Bindings

If you make changes to `oblivious_sort.proto`, regenerate the gRPC Python code with:

```bash
python -m grpc_tools.protoc -I=proto --python_out=. --grpc_python_out=. proto/oblivious_sort.proto
```

This will create:
- `oblivious_sort_pb2.py`
- `oblivious_sort_pb2_grpc.py`

---

## 📁 Location

This file is located in: `proto/oblivious_sort.proto`

