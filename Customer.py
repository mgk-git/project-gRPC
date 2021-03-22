import time
import grpc
import service_pb2
import service_pb2_grpc

class Customer :
    bank_config = {1: 50051, 2: 50052, 3:50053}
    def __init__(self, id, events):
        # unique ID of the Customer
        self.id = id
        # events from the input
        self.events = events
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        # pointer for the stub
        self.stub = None

    def createStub(self):
        channel =grpc.insecure_channel('localhost:'+str(self.bank_config[self.id]))
        self.stub = service_pb2_grpc.BankStub(channel)


    def executeEvents(self):
        self.output = {"id":self.id,"recv":[]}
        for evnt in self.events :
            if evnt["interface"] == 'query':
                response = self.stub.MsgDelivery(service_pb2.RequestMsg(client_type='customer',type='query'))
                self.output["recv"].append({"interface":"query","result":response.status_msg,"money":response.balance})
            elif evnt["interface"] == 'withdraw':
                response = self.stub.MsgDelivery(service_pb2.RequestMsg(client_type='customer',type='withdraw',money=evnt["money"]))
                self.output["recv"].append({"interface":"withdraw","result":response.status_msg})
                print("withdraw1")

            elif evnt["interface"] == 'deposit':
                response = self.stub.MsgDelivery(service_pb2.RequestMsg(client_type='customer',type='deposit',money=evnt["money"]))
                self.output["recv"].append({"interface":"deposit","result":response.status_msg})

        # sleep to finish all the customers.
        time.sleep(5)
        print(self.output)
        response = self.stub.MsgDelivery(service_pb2.RequestMsg(client_type='customer', type='query'))
        self.output["recv"].append({"interface": "query", "result": response.status_msg, "money": response.balance})
        f = open("Output.txt", "a")
        f.write(str(self.output) +"\n")
        f.close()