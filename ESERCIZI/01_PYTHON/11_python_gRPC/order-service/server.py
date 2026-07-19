from concurrent import futures
import time
import uuid
import sys

import grpc
import order_management_pb2_grpc
import order_management_pb2


class OrderManagementServicer(order_management_pb2_grpc.OrderManagementServicer): 

    def __init__(self):
        
        self.orderDict = {}                                                          

    # Unary RPC
    def getOrder(self, request, context):
        print(f"[SERVER] Received getOrder {request.value}")
        order = self.orderDict.get(request.value)
        if order is not None: 
            print(f"[SERVER] Order {request.value} found")
            return order
        else: 
            # Error handling: populate the context with an error code and error message
            print('[SERVER] Order not found ' + request.value)
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Order : ', request.value, ' Not Found.')
            return order_management_pb2.Order()


    # Unary RPC
    def addOrder(self, request, context):
        print("[SERVER] Received addOrder")
        id = uuid.uuid1() # Used to generate a unique id from the MAC address
        
        request.id = str(id) # Insert the id in the Order
        self.orderDict[request.id] = request # Save the Order in the dictionary

        response = order_management_pb2.StringMessage(value=str(id)) # Create the response with the generated id
        print(self.orderDict)

        print(f"[SERVER] Order added with id: {id}")
        
        return response


    # Server Streaming 
    def searchOrders(self, request, context): 
        print(f"[SERVER] Received searchOrders with {request.value}") 
        matching_orders = self.searchInventory(request.value) # Search the item in the Orders

        print(f"[SERVER] Found {len(matching_orders)} orders")
        for order in matching_orders: # yield the orders obtained from the search
            yield order


    # Bi-di Streaming 
    def processOrders(self, request_iterator, context):
        print('[SERVER] Received processOrders')

        location_dict = {}

        # Iterate on the oreders in the request
        for order in request_iterator:

            # Check if the location is already present in the dictionary of locations
            if order.destination not in location_dict.keys():
                location_dict[order.destination] = [order] # If not, create an entry in the dictionary where the key is the location
                                                           # and the value is a list of order (here containing just one order)
                #print(location_dict[order.destination])
                
            else: # If yes, append the order to the list of order for the location
                location_dict[order.destination].append(order)
                #print(location_dict[order.destination])
                
        print(f'[SERVER] Generating {len(location_dict)} shipment/s')    
        # Iterate on the dictionary of locations
        for key, values in location_dict.items():

            shipment_id = uuid.uuid1() # Generate an unique id for the shipment
            shipment = order_management_pb2.CombinedShipment( # Generate the shipment with the list of orders for the current location
                                    id=str(shipment_id), 
                                    status='PROCESSED', 
                                    orders=location_dict[key]) 

            
            yield shipment


    # Local function 
    def searchInventory(self, query):
        matchingOrders = []    

        # Iterate on the orders in the dictionary
        for order_id, order in self.orderDict.items(): 
            for itm in order.items: # Iterate on the items in the current order 
                
                if query in itm: # Check if the item is in the current order
                    matchingOrders.append(order) # If yes, append the order in the list of matching orders
                    break

        return matchingOrders
 

# Creating gRPC Server - NOTE:  options=(('grpc.so_reuseport', 0) allows raising an exception if a port is already used
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=(('grpc.so_reuseport', 0),))
order_management_pb2_grpc.add_OrderManagementServicer_to_server(OrderManagementServicer(), server)

port = 0 # with port = 0, the gRPC runtime will choose a port

port = server.add_insecure_port('[::]:' + str(port)) 
print('Starting server. Listening on port ' + str(port))

server.start()

server.wait_for_termination()
