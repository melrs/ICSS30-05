import grpc

import saudacao_pb2
import saudacao_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = saudacao_pb2_grpc.GreeterStub(channel)

        request = saudacao_pb2.HelloRequest(name='Mundo gRPC')

        try:
            response = stub.SayHello(request)
            print(f"Resposta do servidor: {response.message}")
        except grpc.RpcError as e:
            print(f"Erro ao chamar o serviço: {e.code()} - {e.details()}")

if __name__ == '__main__':
    run()