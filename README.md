# Distributed Data Replication System with gRPC (Push Model)

This project implements a simple distributed data replication system, utilizing the push model for propagating updates between nodes. gRPC is employed as the communication middleware between these processes. The system addresses requirements for a Distributed Systems course at UTFPR.

## System Overview

The system consists of five distinct processes: one client, one leader, and three replicas.

* **Client**:
    * Sends data to the leader for writing.
    * Queries data from the leader.

* **Leader**:
    * Receives data write requests from the client and is responsible for data replication.
    * Saves data to its local log, including `epoch` (leader's version) and `offset` (sequential number representing the entry's position within a specific epoch, indicating record order).
    * Sends the new entry to the replicas (Push model) and awaits acknowledgements (ACKs).
    * Upon receiving confirmation from the majority of replicas (quorum), sends a commit order for replicas to finalize the data write to the final database.
    * Only marks an entry as committed after receiving majority confirmation (quorum). Once committed, it confirms the write to the client.
    * Persists all data (intermediate and final) with `epoch` and `offset`.
    * Responds to client queries.

* **Replicas**:
    * Receive log entries from the leader and persistently store them locally as intermediate (uncommitted) data. This data cannot be considered final or be read until the leader's commit order is received.
    * Send an acknowledgement (ACK) to the leader.
    * Verify if the new entry is consistent with their local log. The entry's `epoch` and `offset` are expected to be an exact continuation of its own local log.
    * If consistent, they accept the new entry.
    * If inconsistent, the replica must truncate its local log by deleting entries from the conflicting `offset` to remove inconsistent or unconfirmed data. This discards divergent entries and returns the replica to a consistent state relative to the leader. Subsequently, it informs its current log state to the leader, allowing the leader to re-send the correct entries from the synchronization point to reconstruct the log.
    * Upon receiving the commit order from the leader, they finalize the write to the final database, making the data visible and reliable for reading.
    * Persist all data (intermediate and final) with `epoch` and `offset`.

## Prerequisites

To run this project, you will need to have the following installed:

* Python 3.6 or higher
* `pip` (Python package installer)

## Environment Setup

Follow the steps below to configure your development environment:

1.  **Clone Repository:**

2.  **Create and Activate a Virtual Environment (Recommended):**
    ```bash
    python3 -m venv venv_grpc_replication
    source venv_grpc_replication/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install grpcio grpcio-tools protobuf
    ```
