import json
import os
import sys
import time
import grpc
from concurrent import futures
import service_pb2_grpc
from Branch import Branch
from Customer import Customer
from multiprocessing import Process,Queue


branches=[]
customers=[]

branch_processes=[]
customer_processes=[]

#ports configuration
bank_config = {1: 50051, 2: 50052, 3: 50053}

# to share process ids
q = Queue()

def start_server(branch):
    q.put(os.getpid())
    brnch = Branch(branch["id"], branch["balance"], q)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_BankServicer_to_server(brnch, server)
    server.add_insecure_port('[::]:'+str(bank_config[branch["id"]]))
    server.start()
    server.wait_for_termination()

def run_customer(customer):
    cstmr =Customer(customer["id"],customer["events"])
    #cstmr.createStub()
    cstmr.executeEvents()

if __name__ == '__main__':
    arg_size=len(sys.argv)
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
            elif type=="bank":
                branches.append(x)

    for branch in branches:
        p = Process(target=start_server, args=(branch,))
        p.start()
        branch_processes.append(p)
        #sleep for 2 sec after each branch process has  started.
        time.sleep(2)

    #Sleep for 2 secs after all the branches started.
    time.sleep(2)

    for customer in customers:
        p = Process(target=run_customer,args=(customer,))
        customer_processes.append(p)
        p.start()

    # Sleep for 5 secs, so that all the events are executed. Then stop processes.
    time.sleep(5)
    for p in customer_processes:
        p.kill()

    for b in branch_processes:
        b.kill()

    print("End ")