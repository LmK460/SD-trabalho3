import logging

import grpc
from watering_can_pb2 import WateringCanState
import watering_can_pb2_grpc
from google.protobuf import empty_pb2

from concurrent import futures

class WateringCanServicer(watering_can_pb2_grpc.WateringCanServicer):
    def __init__(self) -> None:
        self.state = WateringCanState.OFF
    
    def getState(self, request, context):
        message = WateringCanState()
        message.state = self.state
        return message

    def setState(self, request, context):
        response = empty_pb2.Empty()

        self.state = request.state
        print('estado mudado para {}'.format(request))
        return response
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    watering_can_pb2_grpc.add_WateringCanServicer_to_server(
        WateringCanServicer(), server)
    server.add_insecure_port('[::]:50053')
    server.start()
    server.wait_for_termination()

if __name__=='__main__':
    logging.basicConfig()
    serve()