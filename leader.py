import grpc
from concurrent import futures
import time
import replication_data_pb2
import replication_data_pb2_grpc
import threading
import os

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
LEADER_PORT = 50051
REPLICA_PORTS = [50052, 50053, 50054]
MINIMUM_QUORUM = 2

class LeaderServicer(replication_data_pb2_grpc.ReplicationServiceServicer):
    def __init__(self):

        self.last_written_data = None
        self.current_offset = 0
        self.current_epoch = 0
        self.replica_stubs = []
        self._connect_to_replicas()

        print("[Leader] Servidor inicializado. Aguardando chamadas do cliente.")

    def _connect_to_replicas(self):
        for i, port in enumerate(REPLICA_PORTS):
            replica_id = i + 1
            try:
                channel = grpc.insecure_channel(f'localhost:{port}')
                stub = replication_data_pb2_grpc.ReplicationServiceStub(channel)
                grpc.channel_ready_future(channel).result(timeout=5)
                self.replica_stubs.append((replica_id, stub))
                print(f"[Leader] Conectado com sucesso à Réplica {replica_id} na porta {port}.")
            except grpc.RpcError as e:
                print(f"[Leader] ERRO: Não foi possível conectar à Réplica {replica_id} na porta {port}. Detalhes: {e.details()}")
            except futures.TimeoutError:
                print(f"[Leader] ERRO: Tempo esgotado ao conectar à Réplica {replica_id} na porta {port}.")
        
        if not self.replica_stubs:
            print(f"[Leader] ATENÇÃO: Nenhuma réplica conectada. A replicação não ocorrerá.")


    def WriteData(self, request, context):
        payload = request.entry.payload
        print(f"[Leader] Recebida WriteData do cliente com payload: '{payload}'")
        

        self.current_offset += 1
        new_entry = replication_data_pb2.DataEntry(
            epoch=self.current_epoch,
            offset=self.current_offset,
            payload=payload
        )
        self.last_written_data = new_entry
        acks = []
        if not self.replica_stubs:
            print("[Leader] Nenhuma réplica conectada. Dados não serão replicados.")
            return replication_data_pb2.WriteResponse(success=False, message="Nenhuma réplica conectada. Dados não foram gravados.")
        
        for replica_id, stub in self.replica_stubs:
            print(f"[Leader] Enviando entrada de log para a Réplica {replica_id}: Epoch={new_entry.epoch}, Offset={new_entry.offset}, Payload='{new_entry.payload}'")
            try:
                response = stub.ReplicateLog(new_entry)
                if response.consistent:
                    print(f"[Leader] Réplica {replica_id} confirmou a replicação (Epoch: {response.epoch}, Offset: {response.offset}).")
                    acks.append(replica_id)
                else:
                    print(f"[Leader] Réplica {replica_id} não confirmou a replicação (Epoch: {response.epoch}, Offset: {response.offset}).")
            except grpc.RpcError as e:
                print(f"[Leader] ERRO: Falha ao replicar com a Réplica {replica_id}. Detalhes: {e.details()}")
                return replication_data_pb2.WriteResponse(success=False, message=f"Falha ao replicar com a Réplica {replica_id}. Dados não foram efetivamente gravados.")

        if acks < MINIMUM_QUORUM:
            print(f"[Leader] Replicação não confirmada. Quorum mínimo de {MINIMUM_QUORUM} não alcançado. Apenas {acks} confirmações recebidas.")
            return replication_data_pb2.WriteResponse(success=False, message="Replicação não confirmada. Dados não foram efetivamente gravados.")
        
        for replica_id in acks:
            print(f"[Leader] Enviando commit para a Réplica {replica_id} (Epoch: {new_entry.epoch}, Offset: {new_entry.offset}).")
            try:
                commit_response = self.replica_stubs[replica_id - 1][1].CommitData(
                    replication_data_pb2.CommitRequest(epoch=new_entry.epoch, offset=new_entry.offset)
                )
                if commit_response.success:
                    print(f"[Leader] Commit confirmado pela Réplica {replica_id}.")
                else:
                    print(f"[Leader] ERRO: Commit falhou na Réplica {replica_id}.")
            except grpc.RpcError as e:
                print(f"[Leader] ERRO: Falha ao enviar commit para a Réplica {replica_id}. Detalhes: {e.details()}")

        print(f"[Leader] Dados gravados com sucesso. Epoch: {new_entry.epoch}, Offset: {new_entry.offset}, Payload: '{new_entry.payload}'")
        return replication_data_pb2.WriteResponse(
            success=True,
            message=f"Dados gravados com sucesso. Epoch: {new_entry.epoch}, Offset: {new_entry.offset}, Payload: '{new_entry.payload}'"
        )   
    
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
    finally:
        for replica_id, stub in LeaderServicer().replica_stubs:
            if stub._channel:
                stub.channel.close()
                
if __name__ == '__main__':
    serve_leader()