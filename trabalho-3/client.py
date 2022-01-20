from __future__ import print_function

import logging

import grpc
import ar_cond_pb2
import ar_cond_pb2_grpc


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = ar_cond_pb2_grpc.ServiceArCondStub(channel)
        response = stub.TurnOnArCond(ar_cond_pb2.ArCondRequest(value='Júnior Lima'))
    print("Resposta recebida: " + response.message)


if __name__ == '__main__':
    logging.basicConfig()
    run()