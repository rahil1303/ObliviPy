import grpc
from concurrent import futures

from server_sim import Server
from element import Element
from bucket_orp import BucketORP

import oblivious_sort_pb2
import oblivious_sort_pb2_grpc
import time


s = Server() 


class MyObliviousSorter(oblivious_sort_pb2_grpc.ObliviousSorterServicer):
    def Permute(self, request, context):
        input_list = request.input
        N = len(input_list)
        Z = 16

        s.reset_io()
        s.create_array("input", N)
        for i, val in enumerate(input_list):
            s.put("input", i, Element(key=val))

        start = time.time()
        orp = BucketORP(server=s, input_name="input", bucket_size=Z)
        output_name = orp.permute()
        end = time.time()


        # input_list = request.input
        # N = len(input_list)
        # Z = 16  # Bucket size

        # # Simulated secure memory server
        # s.create_array("input", N)

        # for i, val in enumerate(input_list):
        #     s.put("input", i, Element(key=val))

        # # Run Bucket Oblivious Random Permutation
        # orp = BucketORP(server=s, input_name="input", bucket_size=Z)
        # output_name = orp.permute()

        # Gather output
#        result = []
#        for i in range(s.size(output_name)):
#            e = s.get(output_name, i)
#            result.append(e.key)


        # Gather output and sort it locally
        real_elements = []
        for i in range(s.size(output_name)):
            e = s.get(output_name, i)
            real_elements.append(e)

        real_elements.sort(key=lambda e: e.key)

        result = [e.key for e in real_elements]

        # return oblivious_sort_pb2.SortReply(output=result)
        return oblivious_sort_pb2.SortReply(output=result, io_count=s.get_io(), time_taken=round(end - start, 6))
    def GetAccessLog(self, request, context):
        log = s.get_log()
        entries = [
            oblivious_sort_pb2.AccessEntry(op=op, array=array, index=index)
            for (op, array, index) in log
        ]

        if request.clear:
            s.reset_io()

        return oblivious_sort_pb2.AccessLogReply(log=entries)

    


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    oblivious_sort_pb2_grpc.add_ObliviousSorterServicer_to_server(MyObliviousSorter(), server)
    server.add_insecure_port('[::]:50051')
    print("🔌 gRPC Server running on port 50051...")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
