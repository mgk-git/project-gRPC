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
        self.write_set = set([])

    def getStub(self,dest):
        channel =grpc.insecure_channel('localhost:'+str(self.bank_config[dest]))
        return service_pb2_grpc.BankStub(channel)

    def executeEvents(self):
        self.output = {"id":self.id,"recv":[]}
        for evnt in self.events :
            if evnt["interface"] == 'query':
                response = self.getStub(evnt["dest"]).MsgDelivery(service_pb2.RequestMsg(client_type='customer',type='query'))
                #self.output["recv"].append({"id":self.id,"balance":response.balance})
                f = open("Output.txt", "a")
                f.write(str({"id":self.id,"balance":response.balance}))
                f.close()
            elif evnt["interface"] == 'withdraw':
                response = self.getStub(evnt["dest"]).MsgDelivery(service_pb2.RequestMsg(client_type='customer',type='withdraw',money=evnt["money"],w_set=service_pb2.write_set(w_id=self.write_set)))
                #self.output["recv"].append({"interface":"withdraw","result":response.status_msg})
                self.write_set.add(response.write_id)

            elif evnt["interface"] == 'deposit':
                response = self.getStub(evnt["dest"]).MsgDelivery(service_pb2.RequestMsg(client_type='customer',type='deposit',money=evnt["money"],w_set=service_pb2.write_set(w_id=self.write_set)))
                self.write_set.add(response.write_id)
                #self.output["recv"].append({"interface":"deposit","result":response.status_msg})

        # sleep to finish all the customers.
        time.sleep(5)

       # response = self.stub.MsgDelivery(service_pb2.RequestMsg(client_type='customer', type='query'))
        #self.output["recv"].append({"interface": "query", "result": response.status_msg, "money": response.balance})
