# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: replication_data.proto
# Protobuf Python Version: 6.31.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    6,
    31,
    0,
    '',
    'replication_data.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x16replication_data.proto\x12\nreplicacao\";\n\tDataEntry\x12\r\n\x05\x65poch\x18\x01 \x01(\x03\x12\x0e\n\x06offset\x18\x02 \x01(\x03\x12\x0f\n\x07payload\x18\x03 \x01(\t\"4\n\x0cWriteRequest\x12$\n\x05\x65ntry\x18\x01 \x01(\x0b\x32\x15.replicacao.DataEntry\"1\n\rWriteResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"T\n\x0b\x41\x63knowledge\x12\x12\n\nreplica_id\x18\x01 \x01(\x03\x12\r\n\x05\x65poch\x18\x02 \x01(\x03\x12\x0e\n\x06offset\x18\x03 \x01(\x03\x12\x12\n\nconsistent\x18\x04 \x01(\x08\".\n\rCommitRequest\x12\r\n\x05\x65poch\x18\x01 \x01(\x03\x12\x0e\n\x06offset\x18\x02 \x01(\x03\"2\n\x0e\x43ommitResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"\x1d\n\x0bReadRequest\x12\x0e\n\x06latest\x18\x01 \x01(\x08\"T\n\x0cReadResponse\x12$\n\x05\x65ntry\x18\x01 \x01(\x0b\x32\x15.replicacao.DataEntry\x12\r\n\x05\x66ound\x18\x02 \x01(\x08\x12\x0f\n\x07message\x18\x03 \x01(\t2\x9a\x02\n\x12ReplicationService\x12@\n\tWriteData\x12\x18.replicacao.WriteRequest\x1a\x19.replicacao.WriteResponse\x12>\n\x0cReplicateLog\x12\x15.replicacao.DataEntry\x1a\x17.replicacao.Acknowledge\x12\x43\n\nCommitData\x12\x19.replicacao.CommitRequest\x1a\x1a.replicacao.CommitResponse\x12=\n\x08ReadData\x12\x17.replicacao.ReadRequest\x1a\x18.replicacao.ReadResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'replication_data_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_DATAENTRY']._serialized_start=38
  _globals['_DATAENTRY']._serialized_end=97
  _globals['_WRITEREQUEST']._serialized_start=99
  _globals['_WRITEREQUEST']._serialized_end=151
  _globals['_WRITERESPONSE']._serialized_start=153
  _globals['_WRITERESPONSE']._serialized_end=202
  _globals['_ACKNOWLEDGE']._serialized_start=204
  _globals['_ACKNOWLEDGE']._serialized_end=288
  _globals['_COMMITREQUEST']._serialized_start=290
  _globals['_COMMITREQUEST']._serialized_end=336
  _globals['_COMMITRESPONSE']._serialized_start=338
  _globals['_COMMITRESPONSE']._serialized_end=388
  _globals['_READREQUEST']._serialized_start=390
  _globals['_READREQUEST']._serialized_end=419
  _globals['_READRESPONSE']._serialized_start=421
  _globals['_READRESPONSE']._serialized_end=505
  _globals['_REPLICATIONSERVICE']._serialized_start=508
  _globals['_REPLICATIONSERVICE']._serialized_end=790
# @@protoc_insertion_point(module_scope)
