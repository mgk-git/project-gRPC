import threading
import grpc
import service_pb2
import service_pb2_grpc
import logging

class Branch(service_pb2_grpc.BankServicer):
    lock = threading.Lock()
    bank = [(1, 50051),(2, 50052),(3, 50053)]
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
            elif request.type == 'withdraw':
                self.Withdraw(request.money)
                if request.client_type == 'customer':
                    for stb in self.getOtherBranchStubs():
                        stb.MsgDelivery(service_pb2.RequestMsg(client_type='branch',type='withdraw',money=request.money))
                return service_pb2.ReplyMsg(status_code=200, status_msg="Success")

            elif request.type == 'deposit':
                self.Deposit(request.money)
                if request.client_type == 'customer':
                    for stb in self.getOtherBranchStubs():
                        stb.MsgDelivery(service_pb2.RequestMsg(client_type='branch',type='withdraw',money=request.money))
                return service_pb2.ReplyMsg(status_code=200, status_msg="Success")
            return service_pb2.ReplyMsg(balance=self.balance)

    def Query(self):
        return service_pb2.ReplyMsg(status_code=200,status_msg="Success",balance=self.balance)

    def Withdraw(self,amount):
        self.balance=self.balance-amount
        return service_pb2.ReplyMsg(status_code=200,status_msg="Success")

    def Deposit(self,amount):
        self.balance = self.balance + amount
        return service_pb2.ReplyMsg(status_code=200,status_msg="Success")

    def getOtherBranchStubs(self):
        if len(self.stubList)>0 :
            return self.stubList
        else:
            for brn in self.bank:
                if self.id != brn[0]:
                    channel = grpc.insecure_channel('localhost:' + str(brn[1]))
                    self.stubList.append(service_pb2_grpc.BankStub(channel))
            return self.stubList


