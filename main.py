import json
import sys
from builtins import int

import grpc
from concurrent import futures

import service_pb2_grpc
from Branch import Branch
from Customer import Customer
from multiprocessing import Process

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
branches=[]
customers=[]
port=50050;

def f(name):
    print('hello', name)

def start_server(port):
    # Use a breakpoint in the code line below to debug your script.
    print('Starting the process')
    branch_ids=[1,2,3,4]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_BankServicer_to_server(Branch(1,700,branch_ids), server)
    server.add_insecure_port('[::]:'+str(port))
    server.start()
    server.wait_for_termination()

def run_customer():
    customer =Customer(1,[])
    customer.createStub()
    customer.run()

# Press the green button in the gutter to run the script.
print(__name__)
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
                customer= Customer( x["id"], x["events"])
                customers.append(customer)
            elif type=="branch":
                branch=Branch(x["id"], x["balance"],[])
                branches.append(branch)

    for branch in branches:
        port=port+1
        p = Process(target=start_server, args=(port,))
        p.start()

    for customer in customers:
        p = Process(target=run_customer)
        p.start()

    print("End, Main")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
