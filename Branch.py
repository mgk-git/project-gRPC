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
        self.stubList=self.getOtherBranchStubs()
       # with self.lock:
        self.recvMsg.append(request)
        print(request.client_type)
        if request.type == 'query':
            return service_pb2.ReplyMsg(status_code=200,status_msg="Success",balance=self.Query())
        elif request.type == 'withdraw':
            self.Withdraw(request.money)
            if request.client_type == 'customer':
                self.Propogate_Withdraw(request.money)
            return service_pb2.ReplyMsg(status_code=200, status_msg="Success")

        elif request.type == 'deposit':
            self.Deposit(request.money)
            if request.client_type == 'customer':
                self.Propogate_Deposit(request.money)
                return service_pb2.ReplyMsg(status_code=200, status_msg="Success")
            return service_pb2.ReplyMsg(balance=self.balance)

    def Query(self):
        return self.balance

    def Withdraw(self,amount):
        self.balance=self.balance-amount


    def Deposit(self,amount):
        self.balance = self.balance + amount


    def Propogate_Withdraw(self,amount):
        for stb in self.stubList:
            stb.MsgDelivery(service_pb2.RequestMsg(client_type='branch',type='withdraw',money=amount))

    def Propogate_Deposit(self,amount):
        for stb in self.stubList:
            stb.MsgDelivery(service_pb2.RequestMsg(client_type='branch',type='deposit',money=amount))

    def getOtherBranchStubs(self):
        with self.lock:
            if len(self.stubList)>0 :
                return self.stubList
            else:
                for brn in self.bank:
                    if self.id != brn[0]:
                        channel = grpc.insecure_channel('localhost:' + str(brn[1]))
                        self.stubList.append(service_pb2_grpc.BankStub(channel))
                return self.stubList


