import grpc
import oblivious_sort_pb2
import oblivious_sort_pb2_grpc

def get_access_log(stub, clear=True):
    response = stub.GetAccessLog(oblivious_sort_pb2.AccessLogRequest(clear=clear))
    return [(entry.op, entry.array, entry.index) for entry in response.log]

def logs_are_equal(log1, log2):
    return len(log1) == len(log2) and all(a == b for a, b in zip(log1, log2))

def test_obliviousness_at_n(stub, n):
    input1 = list(range(n))                # Increasing
    input2 = list(range(n - 1, -1, -1))     # Decreasing

    stub.Permute(oblivious_sort_pb2.SortRequest(input=input1))
    log1 = get_access_log(stub)

    stub.Permute(oblivious_sort_pb2.SortRequest(input=input2))
    log2 = get_access_log(stub)

    return logs_are_equal(log1, log2), len(log1)

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = oblivious_sort_pb2_grpc.ObliviousSorterStub(channel)

    for n in [100, 200, 300, 400, 500, 600, 800, 1000, 1500, 2000, 3000, 4000, 5000]:
        print(f"🔎 Testing n = {n} ...")
        is_oblivious, log_len = test_obliviousness_at_n(stub, n)

        if is_oblivious:
            print(f"✅ Oblivious for n = {n} (log length: {log_len})")
        else:
            print(f"❌ Obliviousness breaks at n = {n} (log length: {log_len})")
            break

if __name__ == "__main__":
    run()
