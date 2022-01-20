from concurrent import futures
import logging

import grpc
import ar_cond_pb2
import ar_cond_pb2_grpc


class Greeter(ar_cond_pb2_grpc.ServiceArCondServicer):

    def TurnOnArCond(self, request, context):
        return ar_cond_pb2.ArCondReply(message='Teste server Ar, %s!' % request.value)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ar_cond_pb2_grpc.add_ServiceArCondServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
