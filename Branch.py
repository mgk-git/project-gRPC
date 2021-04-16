import json
import threading
import grpc
import service_pb2
import service_pb2_grpc

class Branch(service_pb2_grpc.BankServicer):
    lock = threading.Lock()
    bank = [(1, 50051),(2, 50052),(3, 50053)]

    def __init__(self, id, balance, branches):
        self.id = id
        self.balance = balance
        self.branches = branches
        self.stubList = list()
        self.f=None
        self.clock = 0


    def MsgDelivery(self, request, context):
        if request.type == 'query':
            return service_pb2.ReplyMsg(status_code=200,status_msg="Success",balance=self.Query())
        elif request.type == 'withdraw':
            self.Withdraw(request)
            return service_pb2.ReplyMsg(status_code=200, status_msg="Success",clock=self.clock)
        elif request.type == 'deposit':
            self.Deposit(request)
            return service_pb2.ReplyMsg(status_code=200, status_msg="Success",clock=self.clock)


    def Query(self):
        return self.balance

    def Withdraw(self, request):
        if request.client_type == 'customer':
            self.Event_Request()
            self.log(request.id, 'withdraw_request')
            self.Event_Execute('withdraw', request.money)
            self.log(request.id, 'withdraw_execute')
            self.Propogate_Withdraw(request)
            self.Event_Response()
            self.log(request.id, 'withdraw_rseponse')
        elif request.client_type == 'branch':
            self.Propagate_Request(request)
            self.log(request.id, 'withdraw_broadcast_request')
            self.Propogate_Execute('withdraw',request.money)
            self.log(request.id, 'withdraw_broadcast_execute')


    def Deposit(self, request):
        if request.client_type == 'customer':
            self.Event_Request()
            self.log(request.id, 'deposit_request')
            self.Event_Execute('deposit', request.money)
            self.log(request.id, 'deposit_execute')
            self.Propogate_Deposit(request)
            self.Event_Response()
            self.log(request.id, 'deposit_rseponse')
        elif request.client_type == 'branch':
            self.Propagate_Request(request)
            self.log(request.id, 'deposit_broadcast_request')
            self.Propogate_Execute('deposit', request.money)
            self.log(request.id, 'deposit_broadcast_execute')



    def Propogate_Withdraw(self,request):
        self.Propagate_Send(request)
        self.log(request.id, 'withdraw_broadcast_response')


    def Propogate_Deposit(self,request):
        self.Propagate_Send(request)
        self.log(request.id, 'deposit_broadcast_response')


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


    def Event_Request(self):
        self.Update_clock(None)

    def Event_Response(self):
        self.Update_clock(None)

    def Event_Execute(self,evnt,amount):
        self.Update_clock(None)
        if evnt == 'withdraw':
            self.balance = self.balance - amount
        elif evnt == 'deposit':
            self.balance=self.balance+amount

    def Propagate_Request(self,request):
        self.Update_clock(request.clock)

    def Propagate_Send(self,request):
        self.Update_clock(None)
        self.stubList = self.getOtherBranchStubs()
        for stb in self.stubList:
            propagation_response =stb.MsgDelivery(service_pb2.RequestMsg(id = request.id, client_type='branch', type=request.type, money=request.money,clock=self.clock))
            self.Propogate_Response(propagation_response)

    def Propogate_Execute(self,evnt,amount):
        self.Update_clock(None)
        if evnt == 'withdraw':
            self.balance = self.balance - amount
        elif evnt == 'deposit':
            self.balance = self.balance + amount

    def Propogate_Response(self,propagation_response):
            self.Update_clock(propagation_response.clock)

    def Update_clock(self,remote_clock):
        with self.lock:
            if remote_clock is None:
                self.clock = self.clock+1;
            else:
                self.clock=max(self.clock,remote_clock)+1

    def log(self,req_id,name):
        evnt = {'pid': str(self.id)}
        evnt['id'] = req_id
        evnt['name'] = name
        evnt['clock'] = self.clock
        self.f = open("Output_tmp.txt", "a")
        json.dump(evnt, self.f)
        self.f.write("\n")
        self.f.close()

