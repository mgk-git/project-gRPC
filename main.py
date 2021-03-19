import json
import os
import sys
import time
from builtins import int

import grpc
from concurrent import futures

import service_pb2_grpc
from Branch import Branch
from Customer import Customer
from multiprocessing import Process,Queue

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
branches=[]
customers=[]
port=50050;
ports = dict([(1, 50051), (2, 50052), (3, 50053)])



def start_server(branch):

    q.put(os.getpid())
    brnch = Branch(branch["id"], branch["balance"], q)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_BankServicer_to_server(brnch, server)
    server.add_insecure_port('[::]:'+str(ports[branch["id"]]))
    server.start()
    server.wait_for_termination()

def run_customer(customer):
    cstmr =Customer(customer["id"],customer["events"])
    cstmr.createStub()
    cstmr.executeEvents()


# Press the green button in the gutter to run the script.
print(__name__)
q = Queue()
if __name__ == '__main__':
    arg_size=len(sys.argv)
    print(arg_size)
    if arg_size<2:
        print("The input file is missing. Please provide.")
        exit(2)
    else:
        input_file=open(sys.argv[1])
        arr = json.loads(input_file.read())
        for x in arr:
            type= x["type"]
            if type=="customer":
                customers.append(x)
            elif type=="branch":
                branches.append(x)

    for branch in branches:
        p = Process(target=start_server, args=(branch,))
        p.start()
        time.sleep(2)
    time.sleep(5)


    for customer in customers:
        p = Process(target=run_customer,args=(customer,))
        p.start()

    print("End, Main")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
