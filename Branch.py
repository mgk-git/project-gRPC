import grpc
from concurrent import futures
import time
import service_pb2
import service_pb2_grpc
import Calculator
import logging

class Branch(service_pb2_grpc.BankServicer):
    def __init__(self, id, balance, branches):
        self.id = id
        self.balance = balance
        self.branches = branches
        self.stubList = list()
        self.recvMsg = list()
        logging.basicConfig()

    def SayHello(self, request, context):
        # print(self.balance)
        return service_pb2.HelloReply(message='Hello1111111, %s!' % request.name)

    def MsgDelivery(self, request, context):
        return service_pb2.ReplyMsg(value=self.balance)
