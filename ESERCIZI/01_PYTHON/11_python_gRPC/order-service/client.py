import grpc
import order_management_pb2
import order_management_pb2_grpc

import time
import sys


def run(port):

    # Create the channel
    channel = grpc.insecure_channel('localhost:' + str(port))

    # Obtaining teh stub
    stub = order_management_pb2_grpc.OrderManagementStub(channel)

    # Create some Orders with no id: the id is assigned by the service
    orders = []

    orders.append(order_management_pb2.Order(price=2450.50,
                                        items=['Item - A', 'Item - B', 'Item - C'],
                                        description='This is a Sample order - 1 : description.', 
                                        destination='San Jose, CA'))

    orders.append(order_management_pb2.Order(price=1000, 
                                        items=['Item - A', 'Item - B'], 
                                        description='Sample order description.',
                                        destination='Naples'))
    
    orders.append(order_management_pb2.Order(price=1000, 
                                        items=['Item - C'], 
                                        description='Sample order description.',
                                        destination='Rome'))

    orders.append(order_management_pb2.Order(price=1000, 
                                        items=['Item - A', 'Item - E'], 
                                        description='Sample order description.',
                                        destination='Milan'))
    
    orders.append(order_management_pb2.Order(price=1000, 
                                        items=['Item - F', 'Item - G'], 
                                        description='Sample order description.'))   


    # Iterate on the Orders
    for order in orders:

        # Unary RPC : Adding an Order
        response = stub.addOrder(order)
        print('[CLIENT] Add order response :', response)

        # Unary RPC : Getting an Order 
        order = stub.getOrder(response)
        print("[CLIENT] Order service response: ", order)

    # Server Streaming : Search for an item
    for order_search_result in stub.searchOrders(order_management_pb2.StringMessage(value='Item - A')):
        print('[CLIENT] Search Result : ', order_search_result)

    # Bi-di Streaming : Process Orders for shipment
    proc_order_iterator = generate_orders_for_processing() # Generate Orders for shipment
    for shipment in stub.processOrders(proc_order_iterator): # Send the request
        print('[CLIENT] Shipment : ', shipment)


def generate_orders_for_processing():

    # Generating some order: two of them have the same destination
    ord1 = order_management_pb2.Order(
        id='104', price=2332,
        items=['Item - A', 'Item - B'],  
        description='Updated desc', 
        destination='San Jose, CA')
    
    ord2 = order_management_pb2.Order(
        id='105', price=3000, 
        description='Updated desc', 
        destination='San Francisco, CA')
    
    ord3 = order_management_pb2.Order(
        id='106', price=2560, 
        description='Updated desc', 
        destination='San Francisco, CA')
    
    ord4 = order_management_pb2.Order(
        id='107', price=2560, 
        description='Updated desc', 
        destination='Mountain View, CA')
    
    list = []
    list.append(ord1)
    list.append(ord2)
    list.append(ord3)
    list.append(ord4)

    # yield the order
    for processing_orders in list:
        yield processing_orders


# Start client
if __name__ == "__main__":

    try:
        port = sys.argv[1]
    except IndexError:
        print("Please, specify PORT arg...")

    run(port)