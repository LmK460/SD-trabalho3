import logging

import grpc
from lamp_pb2 import LampState
import lamp_pb2_grpc
from google.protobuf import empty_pb2

from concurrent import futures

class LampServicer(lamp_pb2_grpc.LampServicer):
    def __init__(self) -> None:
        self.state = LampState.OFF
    
    def getState(self, request, context):
        message = LampState()
        message.state = self.state
        return message

    def setState(self, request, context):
        response = empty_pb2.Empty()

        self.state = request.state
        print('estado mudado para {}'.format(request))
        return response
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    lamp_pb2_grpc.add_LampServicer_to_server(
        LampServicer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()

if __name__=='__main__':
    logging.basicConfig()
    serve()