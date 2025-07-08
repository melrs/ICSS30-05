import grpc
import argparse
import time
import replication_data_pb2
import replication_data_pb2_grpc

class ReplicationClient:
    def __init__(self, leader_address):
        self.leader_address = leader_address
        self.channel = grpc.insecure_channel(leader_address)
        self.stub = replication_data_pb2_grpc.ReplicationServiceStub(self.channel)
        print(f"[Client] Conectado ao líder em {self.leader_address}")

    def write_data(self, payload):
        entry = replication_data_pb2.DataEntry(payload=payload)
        request = replication_data_pb2.WriteRequest(entry=entry)
        
        try:
            print(f"[Client] Enviando 'WriteData' com payload '{payload}' para o líder...")
            response = self.stub.WriteData(request)
            if response.success:
                print(f"[Client] Resposta do líder (Escrita): {response.message}")
            else:
                print(f"[Client] Resposta do líder (Falha na Escrita): {response.message}")
        except grpc.RpcError as e:
            print(f"[Client] Erro RPC ao escrever dados: {e.details()}")
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                print("[Client] Servidor líder pode não estar disponível. Verifique se ele está rodando.")

    def read_data(self):
        request = replication_data_pb2.ReadRequest(latest=True)
        
        try:
            print("[Client] Enviando 'ReadData' para o líder...")
            response = self.stub.ReadData(request)
            if response.found:
                print(f"[Client] Resposta do líder (Leitura): Último dado: Epoch={response.entry.epoch}, Offset={response.entry.offset}, Payload='{response.entry.payload}'")
            else:
                print(f"[Client] Resposta do líder (Leitura): {response.message}")
        except grpc.RpcError as e:
            print(f"[Client] Erro RPC ao ler dados: {e.details()}")
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                print("[Client] Servidor líder pode não estar disponível. Verifique se ele está rodando.")

def main():
    parser = argparse.ArgumentParser(description="gRPC Client for Data Replication Project")
    parser.add_argument("--leader_address", type=str, default="localhost:50051", help="Endereço do líder (host:port)")
    args = parser.parse_args()

    client = ReplicationClient(args.leader_address)

    while True:
        print("\n--- Cliente de Replicação ---")
        print("1. Escrever novo dado para o líder")
        print("2. Ler último dado do líder")
        print("3. Sair")
        
        choice = input("Escolha uma opção: ")

        if choice == '1':
            data_payload = input("Digite o dado (texto simples): ")
            client.write_data(data_payload)
        elif choice == '2':
            client.read_data()
        elif choice == '3':
            print("Saindo do cliente.")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")
        time.sleep(0.5)

if __name__ == '__main__':
    main()