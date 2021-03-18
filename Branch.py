import threading

import grpc
from concurrent import futures
import time
import service_pb2
import service_pb2_grpc
import logging

class Branch(service_pb2_grpc.BankServicer):
    lock = threading.Lock()
    CONST_SUCCESS="Success"
    def __init__(self, id, balance, branches):
        self.id = id
        self.balance = balance
        self.branches = branches
        self.stubList = list()
        self.recvMsg = list()
        self.lock = threading.Lock()
        logging.basicConfig()




    def MsgDelivery(self, request, context):
        with self.lock:
            if request.type == 'query':
                return self.Query()
            elif request.type == 'deposit':
                return self.Deposit(request.amount)
            elif request.type == 'withdraw':
                return self.Withdraw(request.amount)
            else:
                print(request.type)
            return service_pb2.ReplyMsg(balance=self.balance)

    def Query(self):
        return service_pb2.ReplyMsg(status_code=200,status_msg="Success")

    def Withdraw(self,amount):
        self.balance=self.balance-amount
        return service_pb2.ReplyMsg(status_code=200,status_msg="Success")

    def Deposit(self,amount):
        self.balance = self.balance + amount
        return service_pb2.ReplyMsg(status_code=200,status_msg="Success")
