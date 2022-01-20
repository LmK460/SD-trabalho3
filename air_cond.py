import logging

import grpc
import air_cond_pb2
import air_cond_pb2_grpc
from google.protobuf import empty_pb2
from concurrent import futures

class AirCondServicer(air_cond_pb2_grpc.AirCondServicer):
    def __init__(self) -> None:
        self.state = air_cond_pb2.AirCondState.MEDIUM
    
    def getState(self, request, context):
        message = air_cond_pb2.AirCondState()
        message.state = self.state
        return message

    def setState(self, request, context):
        response = empty_pb2.Empty()

        '''if request.state == air_cond_pb2.AirCondState.WEAK:
            context.set_details('aaaaaa')
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return response#'''

        self.state = request.state
        print('estado mudado para {}'.format(request))
        return response
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    air_cond_pb2_grpc.add_AirCondServicer_to_server(
        AirCondServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__=='__main__':
    logging.basicConfig()
    serve()