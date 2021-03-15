import logging

import grpc
import  service_pb2
import service_pb2_grpc
import json

def createStub():
    print('create stb')
    #service_pb2_grpc.GreeterStub(channel)
def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = service_pb2_grpc.BankStub(channel)
        response =stub.MsgDelivery(service_pb2.RequestMsg(type='query'))
        print(response.balance)
        response = stub.MsgDelivery(service_pb2.RequestMsg(type='deposit', amount=100))
        print(response.status)
        response = stub.MsgDelivery(service_pb2.RequestMsg(type='query'))
        print(response.balance)
        response = stub.MsgDelivery(service_pb2.RequestMsg(type='withdraw', amount=100))
        print(response.status)
        response = stub.MsgDelivery(service_pb2.RequestMsg(type='query'))
        print(response.balance)



if __name__ == '__main__':
    logging.basicConfig()
    run()