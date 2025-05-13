# client/client.py

import grpc
import oblivious_sort_pb2
import oblivious_sort_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = oblivious_sort_pb2_grpc.ObliviousSorterStub(channel)

    test_data = [8, 3, 4, 1, 99, 42, 23]
    response = stub.Permute(oblivious_sort_pb2.SortRequest(input=test_data))

    print("🎯 Original:", test_data)
    print("🔁 Permuted:", response.output)
    print("📦 Total I/Os:", response.io_count)
    print("⏱️ Time Taken:", response.time_taken, "seconds")


if __name__ == '__main__':
    run()
