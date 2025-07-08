import grpc
from concurrent import futures
import time
import replication_data_pb2
import replication_data_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
LEADER_PORT = 50051
class LeaderServicer(replication_data_pb2_grpc.ReplicationServiceServicer):
    def __init__(self):

        self.last_written_data = None
        self.current_offset = 0
        self.current_epoch = 0
        print("[Leader] Servidor inicializado. Aguardando chamadas do cliente.")

    def WriteData(self, request, context):
        payload = request.entry.payload
        print(f"[Leader] Recebida WriteData do cliente com payload: '{payload}'")
        

        self.current_offset += 1
        self.last_written_data = replication_data_pb2.DataEntry(
            epoch=self.current_epoch,
            offset=self.current_offset,
            payload=payload
        )
        
        print(f"[Leader] Dado '{payload}' recebido gravado (Epoch: {self.current_epoch}, Offset: {self.current_offset}).")
        return replication_data_pb2.WriteResponse(success=True, message="Dado recebido pelo líder ista!")

    def ReadData(self, request, context):
        print(f"[Leader] Recebida ReadData do cliente.")
        
        if self.last_written_data:
            print(f"[Leader] Retornando o último dado: '{self.last_written_data.payload}'")
            return replication_data_pb2.ReadResponse(
                entry=self.last_written_data,
                found=True,
                message="Último dado retornado."
            )
        else:
            print("[Leader] Nenhum dado encontrado para leitura.")
            return replication_data_pb2.ReadResponse(found=False, message="Nenhum dado encontrado no líder ista.")

    def ReplicateLog(self, request, context):
        print(f"[Leader] (Ignorando) Recebida chamada ReplicateLog (Época: {request.epoch}, Offset: {request.offset}, Payload: '{request.payload}').")
        return replication_data_pb2.Acknowledge(replica_id=0, epoch=request.epoch, offset=request.offset, consistent=True)

    def CommitData(self, request, context):
        print(f"[Leader] (Ignorando) Recebida chamada CommitData (Época: {request.epoch}, Offset: {request.offset}).")
        return replication_data_pb2.CommitResponse(success=True, message="Commitado com sucesso.")


def serve_leader():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    replication_data_pb2_grpc.add_ReplicationServiceServicer_to_server(LeaderServicer(), server)
    server.add_insecure_port(f'[::]:{LEADER_PORT}')
    print(f"Servidor Líder ista iniciado na porta {LEADER_PORT}...")
    
    server.start()
    
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        print("Servidor Líder ista encerrado.")
        server.stop(0)

if __name__ == '__main__':
    serve_leader()