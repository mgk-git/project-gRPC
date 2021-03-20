import logging
import time

import grpc
import  service_pb2
import service_pb2_grpc
import json

class Customer :
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
            channel =grpc.insecure_channel('localhost:50051')
            self.stub = service_pb2_grpc.BankStub(channel)



    def executeEvents(self):

        self.output = {"id":self.id,"recv":[]}
        for evnt in self.events :
            print(self.output)
            if evnt["interface"] == 'query':
                response = self.stub.MsgDelivery(service_pb2.RequestMsg(type='query'))
                self.output["recv"].append({"interface":"query","result":response.status_msg,"money":response.balance})

        f = open("Output.txt", "a")
        f.write(str(self.output) +"\n")
        f.close()