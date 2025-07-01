import grpc
from concurrent import futures
import time

import saudacao_pb2
import saudacao_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class GreeterServicer(saudacao_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        print(f"Recebida requisição de: {request.name}")
        return saudacao_pb2.HelloReply(message=f"Olá, {request.name}!")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    saudacao_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        print("Servidor gRPC encerrado.")
        server.stop(0)

if __name__ == '__main__':
    serve()