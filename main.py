import grpc
from concurrent import futures

import service_pb2_grpc
import test
from Branch import Branch
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def start():
    # Use a breakpoint in the code line below to debug your script.
    print('Starting the process')
    branch_ids=[1,2,3,4]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_BankServicer_to_server(Branch(1,700,branch_ids), server)
    server.add_insecure_port('[::]:50051')
    server.start()

    server.wait_for_termination()


# Press the green button in the gutter to run the script.
print(__name__)
if __name__ == '__main__':
   start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
