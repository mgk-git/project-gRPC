import json
import os
import sys
import time
from multiprocessing.dummy import current_process

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
    cstmr.createStub()
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
            elif type=="branch":
                branches.append(x)

    for branch in branches:
        p = Process(target=start_server, args=(branch,))
        p.start()
        branch_processes.append(p)
        #sleep for 2 sec after each branch process has  started.
        time.sleep(2)

    #Sleep for 2 secs after all the branches started.
    time.sleep(5)

    for customer in customers:
        p = Process(target=run_customer,args=(customer,))
        p.start()
        customer_processes.append(p)

    time.sleep(10) #sleep for 10 sec, so that all the events are executed.

    log_array=[]
    event_array=[]


    f = open('Output_tmp.txt', )
    while True:
        # Get next line from file
        line = f.readline()
        # if line is empty
        # end of file is reached
        if not line:
            break
        print(line)
        json_obj= json.loads(line)
        pid_found=False
        event_found=False
        for i in log_array:
            if json_obj["pid"] == i.get("pid"):
                i["data"].append({'id':json_obj["id"],'name':json_obj["name"],'clock':json_obj["clock"]})
                pid_found=True

        if pid_found == False:
            log_array.append({'pid':json_obj['pid'],'data': [{'id':json_obj["id"],'name':json_obj["name"],'clock':json_obj["clock"]}]})



        for i in event_array:

            if json_obj["id"] == i.get("eventid"):
                i["data"].append({'clock': json_obj["clock"], 'name': json_obj["name"]})
                event_found = True


        if event_found == False:
            event_array.append({'eventid': json_obj['id'],
                              'data': [{'clock': json_obj["clock"], 'name': json_obj["name"]}]})

    f.close()
    log_array.append(event_array)
    output = open("Output.txt", "a")
    json.dump(log_array, output,indent=1)
    output.close()

    for p in customer_processes:
        p.kill()

    for b in branch_processes:
        b.kill()

    print("End ")





