from websocket import create_connection


import numpy
import wsaccel
import json
import math 


def turn_on_all_the_modules():
    uri = "ws://localhost:8888/websocket"
    # websocket.enableTrace(True)
    apollo = create_connection(uri)
    init_msg = json.dumps({ 'type': 'HMIAction', 'action': "SETUP_MODE" })
    apollo.send(init_msg)

    print("Open already")

    print("Receiving...")
    result =  apollo.recv()
    print("Received '%s'" % result)
    apollo.close()


def turn_off_all_the_modules():
    uri = "ws://localhost:8888/websocket"
    # websocket.enableTrace(True)
    apollo = create_connection(uri)
    init_msg = json.dumps({ 'type': 'HMIAction', 'action': "RESET_MODE" })
    apollo.send(init_msg)

    print("Open already")

    print("Receiving...")
    result =  apollo.recv()
    print("Received '%s'" % result)
    apollo.close()



def enter_auto_mode():
    uri = "ws://localhost:8888/websocket"
    # websocket.enableTrace(True)
    apollo = create_connection(uri)
    init_msg = json.dumps({ 'type': 'HMIAction', 'action': "ENTER_AUTO_MODE" })
    apollo.send(init_msg)

    print("Open already")

    print("Receiving...")
    result =  apollo.recv()
    print("Received '%s'" % result)
    apollo.close()


def disengage():
    uri = "ws://localhost:8888/websocket"
    # websocket.enableTrace(True)
    apollo = create_connection(uri)
    init_msg = json.dumps({ 'type': 'HMIAction', 'action': "DISENGAGE" })
    apollo.send(init_msg)

    print("Open already")

    print("Receiving...")
    result =  apollo.recv()
    print("Received '%s'" % result)
    apollo.close()


def change_mode_of_apollo(mode: str):
    uri = "ws://localhost:8888/websocket"
    # websocket.enableTrace(True)
    apollo = create_connection(uri)
    init_msg = json.dumps({ 'type': 'HMIAction', 'action': "CHANGE_MODE", 'value': mode })
    apollo.send(init_msg)

    print("Open already")

    print("Receiving...")
    result =  apollo.recv()
    print("Received '%s'" % result)
    apollo.close()


def change_map_of_apollo(mapp: str):
    uri = "ws://localhost:8888/websocket"
    # websocket.enableTrace(True)
    apollo = create_connection(uri)
    init_msg = json.dumps({ 'type': 'HMIAction', 'action': "CHANGE_MAP", 'value': mapp })
    apollo.send(init_msg)

    print("Open already")

    print("Receiving...")
    result =  apollo.recv()
    print("Received '%s'" % result)
    apollo.close()



def change_vehicle_of_apollo(vehicle: str):
    uri = "ws://localhost:8888/websocket"
    # websocket.enableTrace(True)
    apollo = create_connection(uri)
    init_msg = json.dumps({ 'type': 'HMIAction', 'action': "CHANGE_VEHICLE", 'value': vehicle })
    apollo.send(init_msg)

    print("Open already")

    print("Receiving...")
    result =  apollo.recv()
    print("Received '%s'" % result)
    apollo.close()




def open_module_of_apollo(module: str):
    uri = "ws://localhost:8888/websocket"
    # websocket.enableTrace(True)
    apollo = create_connection(uri)
    init_msg = json.dumps({ 'type': 'HMIAction', 'action': "START_MODULE", 'value': module })
    apollo.send(init_msg)

    print("Open already")

    print("Receiving...")
    result =  apollo.recv()
    print("Received '%s'" % result)
    apollo.close()




def stop_module_of_apollo(module: str):
    uri = "ws://localhost:8888/websocket"
    # websocket.enableTrace(True)
    apollo = create_connection(uri)
    init_msg = json.dumps({ 'type': 'HMIAction', 'action': "STOP_MODULE", 'value': module })
    apollo.send(init_msg)

    print("Open already")

    print("Receiving...")
    result =  apollo.recv()
    print("Received '%s'" % result)
    apollo.close()








def get_HMIStatus():
    uri = "ws://localhost:8888/websocket"
    # websocket.enableTrace(True)
    apollo = create_connection(uri)
    init_msg = json.dumps({ 'type': 'HMIStatus' })
    apollo.send(init_msg)

    print("Open already")

    print("Receiving...")
    result =  apollo.recv()
    # print("Received '%s'" % result)
    apollo.close()
    return result


def get_RequestSimulationWorld():
    uri = "ws://localhost:8888/websocket"
    # websocket.enableTrace(True)
    apollo = create_connection(uri)
    init_msg = json.dumps({ 'type': "RequestSimulationWorld", 'planning': True })
    apollo.send(init_msg)

    print("Open already")

    print("Receiving...")
    result =  apollo.recv()
    # print("Received '%s'" % result)
    apollo.close()
    print(result)
    return result




def send_routing_request(start_point:dict,end_point:dict,heading1,waypoint1 = []):
    uri = "ws://localhost:8888/websocket"
    # websocket.enableTrace(True)
    apollo = create_connection(uri)
    init_msg = json.dumps({ 'type': 'SendRoutingRequest', \
                            'start': { \
                                'x': start_point['x'],\
                                'y': start_point['y'],\
                                'z': start_point['z'],\
                                'heading': heading1 / 180 * math.pi\
                                     }, \
                            'end': { \
                                'x': end_point['x'],\
                                'y': end_point['y'],\
                                'z': end_point['z'],},\
                            'waypoint':waypoint1\
                        })
    apollo.send(init_msg)

    print("Open already")

    # print("Receiving...")
    result =  apollo.recv()
    # print("Received '%s'" % result)
    apollo.close()
    return result   





# def on_message(wsapp, message):
#     msg = json.loads(message)
#     print('type = '+ str(msg['type']))
#     if msg['type'] == 'SimulationWorld':
#         pass
#         # print('SimulationWorld')
#         # print(msg)
#     elif msg['type'] == 'HMIStatus':
#         # wsapp.send(json.dumps({ 'type': 'RequestSimulationWorld' }))
#         # result=wsapp.recv()
#         # get_RequestSimulationWorld()
#         # print('HMIStatus')
#         # print(msg)
#         pass
#     else:
#         pass
#         # print('Some other type!!!!!!!!!!!!!!!')
#         # print(msg['type'])
#         # print(msg)
#     # elif message['type'] == 'Object':
#     #     print('Object')
#     #     print(message)


# def on_error(wsapp, error):
#     print(error)

# def on_close(wsapp):
#     print("### closed ###")

# def on_open(wsapp):
#     # wsapp.send(json.dumps({ 'type': 'HMIAction', 'action': "START_MODULE", 'value': "Planning" }))
#     pass





# def creat_long_life_connection_to_apollo():
#     print('creat_long_life_connection_to_apollo')
#     # websocket.enableTrace(True)
#     # wsapp = websocket.WebSocketApp("ws://localhost:9090/websocket",  
#     #                         on_open = on_open,
#     #                         on_message = on_message,
#     #                         on_error = on_error,
#     #                         on_close = on_close)
#     # wsapp.run_forever()

#     HOST = '127.0.0.1'  # The server's hostname or IP address
#     PORT = 9090        # The port used by the server

#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        

#         sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)

#         SEND_BUF_SIZE = 1024*1024
#         RECV_BUF_SIZE = 1024*1024
#         sock.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF,SEND_BUF_SIZE)
#         sock.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,RECV_BUF_SIZE)
#         sock.settimeout(1)

#         sock.connect((HOST, PORT))
#         teste='Just a test'
#         sock.send(teste.encode("ascii"))
#         a=sock.recv()
#         print(a)







































def open_planning_of_apollo():
    uri = "ws://localhost:8888/websocket"
    # websocket.enableTrace(True)
    apollo = create_connection(uri)
    init_msg = json.dumps({ 'type': 'HMIAction', 'action': "START_MODULE", 'value': "Planning" })
    apollo.send(init_msg)

    print("Open already")

    print("Receiving...")
    result =  apollo.recv()
    print("Received '%s'" % result)
    apollo.close()



def open_camera_of_apollo():
    uri = "ws://localhost:8888/websocket"
    # websocket.enableTrace(True)
    apollo = create_connection(uri)
    init_msg = json.dumps({ 'type': 'HMIAction', 'action': "START_MODULE", 'value': "Camera" })
    apollo.send(init_msg)

    print("Open already")

    print("Receiving...")
    result =  apollo.recv()
    print("Received '%s'" % result)
    apollo.close()

def open_traffic_light_of_apollo():
    uri = "ws://localhost:8888/websocket"
    # websocket.enableTrace(True)
    apollo = create_connection(uri)
    init_msg = json.dumps({ 'type': 'HMIAction', 'action': "START_MODULE", 'value': "Traffic Light" })
    apollo.send(init_msg)

    print("Open already")

    print("Receiving...")
    result =  apollo.recv()
    print("Received '%s'" % result)
    apollo.close()

def open_canbus_of_apollo():
    uri = "ws://localhost:8888/websocket"
    # websocket.enableTrace(True)
    apollo = create_connection(uri)
    init_msg = json.dumps({ 'type': 'HMIAction', 'action': "START_MODULE", 'value': "Canbus" })
    apollo.send(init_msg)

    print("Open already")

    print("Receiving...")
    result =  apollo.recv()
    print("Received '%s'" % result)
    apollo.close()

def open_prediction_of_apollo():
    uri = "ws://localhost:8888/websocket"
    # websocket.enableTrace(True)
    apollo = create_connection(uri)
    init_msg = json.dumps({ 'type': 'HMIAction', 'action': "START_MODULE", 'value': "Prediction" })
    apollo.send(init_msg)

    print("Open already")

    print("Receiving...")
    result =  apollo.recv()
    print("Received '%s'" % result)
    apollo.close()

def open_transform_of_apollo():
    uri = "ws://localhost:8888/websocket"
    # websocket.enableTrace(True)
    apollo = create_connection(uri)
    init_msg = json.dumps({ 'type': 'HMIAction', 'action': "START_MODULE", 'value': "Transform" })
    apollo.send(init_msg)

    print("Open already")

    print("Receiving...")
    result =  apollo.recv()
    print("Received '%s'" % result)
    apollo.close()

def open_routing_of_apollo():
    uri = "ws://localhost:8888/websocket"
    # websocket.enableTrace(True)
    apollo = create_connection(uri)
    init_msg = json.dumps({ 'type': 'HMIAction', 'action': "START_MODULE", 'value': "Routing" })
    apollo.send(init_msg)

    print("Open already")

    print("Receiving...")
    result =  apollo.recv()
    print("Received '%s'" % result)
    apollo.close()

def open_control_of_apollo():
    uri = "ws://localhost:8888/websocket"
    # websocket.enableTrace(True)
    apollo = create_connection(uri)
    init_msg = json.dumps({ 'type': 'HMIAction', 'action': "START_MODULE", 'value': "Control" })
    apollo.send(init_msg)

    print("Open already")

    print("Receiving...")
    result =  apollo.recv()
    print("Received '%s'" % result)
    apollo.close()

def open_perception_of_apollo():
    uri = "ws://localhost:8888/websocket"
    # websocket.enableTrace(True)
    apollo = create_connection(uri)
    init_msg = json.dumps({ 'type': 'HMIAction', 'action': "START_MODULE", 'value': "Perception" })
    apollo.send(init_msg)

    print("Open already")

    print("Receiving...")
    result =  apollo.recv()
    print("Received '%s'" % result)
    apollo.close()

def open_third_party_perception_of_apollo():
    uri = "ws://localhost:8888/websocket"
    # websocket.enableTrace(True)
    apollo = create_connection(uri)
    init_msg = json.dumps({ 'type': 'HMIAction', 'action': "START_MODULE", 'value': "Third Party Perception" })
    apollo.send(init_msg)

    print("Open already")

    print("Receiving...")
    result =  apollo.recv()
    print("Received '%s'" % result)
    apollo.close()