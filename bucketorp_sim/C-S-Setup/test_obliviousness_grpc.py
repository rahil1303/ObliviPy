# test_obliviousness_grpc.py

import grpc
import oblivious_sort_pb2
import oblivious_sort_pb2_grpc


def get_access_log(stub):
    response = stub.GetAccessLog(oblivious_sort_pb2.AccessLogRequest(clear=True))
    return [(entry.op, entry.array, entry.index) for entry in response.log]


def logs_are_equal(log1, log2):
    if len(log1) != len(log2):
        return False
    return all(a == b for a, b in zip(log1, log2))


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = oblivious_sort_pb2_grpc.ObliviousSorterStub(channel)

    input1 = list(range(100))           # Increasing
    input2 = list(range(99, -1, -1))    # Decreasing

    # First request
    _ = stub.Permute(oblivious_sort_pb2.SortRequest(input=input1))
    log1 = get_access_log(stub)

    # Second request
    _ = stub.Permute(oblivious_sort_pb2.SortRequest(input=input2))
    log2 = get_access_log(stub)

    print(f"Log 1 length: {len(log1)}")
    print(f"Log 2 length: {len(log2)}")

    if logs_are_equal(log1, log2):
        print("✅ Access logs match — sort is oblivious.")
    else:
        print("❌ Access logs differ — NOT oblivious.")

if __name__ == "__main__":
    run()
