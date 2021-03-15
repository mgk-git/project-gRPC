import grpc
from concurrent import futures
import time
import service_pb2
import service_pb2_grpc
import logging

class Branch(service_pb2_grpc.BankServicer):
    CONST_SUCCESS="Success"
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
        print(request.type)
        if request.type == 'query':
            return self.Query()
        elif request.type == 'deposit':
            return self.Deposit(request.amount)
        elif request.type == 'withdraw':
            return self.Withdraw(request.amount)
        else:
            print(request.type)
        return service_pb2.ReplyMsg(value=self.balance)

    def Query(self):
        return service_pb2.ReplyMsg(balance=self.balance)

    def Withdraw(self,amount):
        self.balance=self.balance-amount
        return service_pb2.ReplyMsg(status="Success")

    def Deposit(self,amount):
        self.balance = self.balance + amount
        return service_pb2.ReplyMsg(status="Success")
