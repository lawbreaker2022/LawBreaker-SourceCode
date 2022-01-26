import websockets
import json
import asyncio
import websocket
from websocket import create_connection
from lgsvl_method import *

import pickle

# from glob import glob
# from base64 import b64encode

from modules.control.proto import control_cmd_pb2
from modules.drivers.gnss.proto import imu_pb2
from modules.localization.proto import imu_pb2 as corrected_imu

# from PythonAPImaster import lgsvl
import lgsvl
from environs import Env

import math
import random


def open_planning():
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


async def print_devices():
    uri = "ws://localhost:8000"
    async with websockets.connect(uri) as websocket:
        # scenario_no = len(scenario_msg)
        init_msg = json.dumps({'CMD': "CMD_READY_FOR_NEW_TEST"})
        # init_msg = json.dumps({ type: 'HMIAction', action: "START_MODULE", value: "Planning" })
            
        print(init_msg)
        await websocket.send(init_msg)

        print('send(init_msg)')
            # for i in range(scenario_no):
            # print('iteration: {}'.format(i))
        msg = await websocket.recv()
        print('1')
        print('recv():')
        print(msg)


        # msg = json.loads(msg)

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(print_devices())
    loop.close()

if __name__ == '__main__':
    # open_planning()
    # main()
    # aaa = CyberBridgeInstance()
    # aaa.AddSubscriber("apollo.control.ControlCommand","/apollo/control")
    # a =  b'\n \t\x9a\xe6\x15_"0\xd8A\x12\x07control\x18\xc0\xfc1 \x00(\x000\x00B\x02\x08\x00\x19\x00\x00\x00\x00\x00\x00\x00\x00!\x1eV\xd3\xab\x0b\xccL@1\x00\x00\x00\x00\x00\x00Y@9*\xe0\xe5h2Uv?Q{\xfd\xeft\xca\x91\xd1\xbf\xa0\x01\x01\xb2\x01\x84\x06\n\xd4\x02\t\x00\x00\x00\x00\x00\x00\x00\x00\x11<\xb3\xe9\xc5k\xf6=?\x19<\xb3\xe9\xc5k\xf6=?!<\xb3\xe9\xc5k\xf6=?)\x00\x00\x00\x00\x00\x00\x00\x001\xd1\xb7&)-\xc7#\xbf9J\x8d\xbe4\x08,\x0f\xbfA\x00\x00\x00\x00\x00\x00\x00\x00I\xd1\xb7&)-\xc7#\xbfQ\x00\x00\x00\x00\x00\x00\x00\x00Y{\xfd\xeft\xca\x91\xd1\xbfa{\xfd\xeft\xca\x91\xd1\xbfi{\xfd\xeft\xca\x91\xd1\xbfq\x00\x00\x00`-\xc7#?y\x1eV\xd3\xab\x0b\xccL\xc0\x81\x01\x00\x00\x00\x00\x00\x00\x00\x00\x89\x01\x1eV\xd3\xab\x0b\xccL@\x90\x01\x00\x99\x01\x1f\xd0U\xf5\xa9\x8d\xd4?\xa1\x01<\xb3\xe9\xc5k\xf6=\xbf\xa9\x01<\xb3\xe9\xc5k\xf6=?\xb0\x01\x00\xc1\x01\xfd(\xee7V\xf8\x17?\xc9\x01\xd1\xb7&)-\xc7#?\xd1\x01\x00\x00\x00\x00\x00\x00\x00\x00\xd9\x01\x00\x00\x00\x00\x00\x00\x00\x00\xe1\x01\x00\x00\x00\x00\x00\x00\x00\x00\xe9\x01\x00\x00\x00\x00\x00\x00\x00\x00\xf1\x01\x00\x00\x00\x00\x00\x00\x00\x00\xf9\x01\x00\x00\x00\x00\x00\x00\x00\x00\x82\x02\x14\n\x12\t\xa4\x14z\x0f\xac\xea!A\x11\xe6y+e\xfd\x98OA\x8a\x02\x14\n\x12\t\xb8\xdb\xeaI\xad\xea!A\x11V\xffxQ\xfd\x98OA\x92\x02\x14\n\x12\t\xec?7J\xad\xea!A\x11\x99.tQ\xfd\x98OA\x12\xb7\x02\tv^\x94\xa7>\xb8\xb9\xbf\x11\xd8Wvq\xc1\xd0\xd8\xbf\x19@>J\x99\xc9\xc5\xd8\xbf!\x0003X\xb0\xefE?)\x00\x00\x00\x00\x00\x00\x00\x001\xd7\t\xc9\x9d\xb4\x1d{>9S\x13\xc0\xe7\t\xb6.\xbcA*\xe0\xe5h2Uv?I\x91\xca\x16\xf2_\'\xc0\xbcQ\xdb\xb2\xc8\xccf\xd8\xb3?Yp\x91\x03\x9a>\xf5\xcc\xbda\x07\xdc\xd5sU~|\xbfi\x00\x00\x00\x00\x00\x00\x00\x80q\x9ejQu\x81\x10\xb2?y\x00\x00\x00`2Uv?\x81\x01\x00\x00\x00`-\xc7#?\x89\x01~jQu\x81\x10\xb2?\x91\x01\x00\x00\x00\x00\x00\x00\x00\x00\x99\x01\x00\x00\x00\x00\x00\x00\x00\x00\xa1\x01\x00\x00\x00\x00\x00\x00\x00\x80\xa9\x01\x00\x00\x00\x00\x00\x00\x00\x00\xb1\x01\x00\x00\x00\x00\x00\x00\x00\x00\xb9\x01\x00\x00\x00\x00\x00\x00\x00\x00\xc1\x01\x00\x00\x00\x00\x00\x00\x00\x00\xc9\x01\x00\x00\x00\x00\x00\x00\x00\x00\xd1\x01\x00\x00\x00\x00\x00\x00\x00\x00\xd9\x01\x00\x00\x00\x00\x00\x00\x00\x00\xe1\x01v^\x94\xa7>\xb8\xb9\xbf\xe9\x01\x0003X\xb0\xefE?\xf2\x01\x14\n\x12\t\xec?7J\xad\xea!A\x11\x99.tQ\xfd\x98OA\xf9\x01\x00\x00\x00\x00\x00\x00\x00\x00\x88\x02\x00\x1aq\n\x1b\t5z\x10_"0\xd8A\x12\x0clocalization\x18\xab\x84\x0e\x12\x16\t\x07J\xb79"0\xd8A\x12\x07chassis\x18\xe2\x81\x0b\x1a\x1c\t4~\x12_"0\xd8A\x12\x08planning\x18\x91\x0c \x00(\x000\x00"\x1c\t\x07\xec-@"0\xd8A\x12\x08planning\x18\xc1\x02 \x00(\x000\x00\xba\x01\x02\x08\x00\xc2\x01\x1d\t\x83\xc3\x0b"RK\'@\x11\x00\x00\x00\x00 )\x1b@\x11\x00\x00\x00\x00\xc8\x84\xdc?\x18\x01\xd2\x01\x02\x08\x02'
    # ctl = control_cmd_pb2.ControlCommand()
    # ctl.ParseFromString(a)

    # print('ControlCommand')
    # print(ctl)


    # b = b'\n\r\t\x8c5\xb99"0\xd8A\x18\xc2\xc0p\x11\xe9&9\xde\xd2z\xd3A\x1d\n\xd7#<"\x1b\t\x00\x00\x00\xa0\xaey\xbc\xbf\x11\x00\x00\x00 \x06Q\xd3?\x19\x00\x00\x00\x80\x1c\x9c#@*\x1b\t\x00\x00\x00\x00\x80N\xae\xbe\x11\x00\x00\x00\x00\xc0\xd9\xac>\x19\x00\x00\x00\x00\xe0\xe0\xd7>'
    # imu = imu_pb2.Imu()
    # imu.ParseFromString(b)
    # print('Imu')
    # print(imu)

    # corrected_imu1 = corrected_imu.CorrectedImu()
    # corrected_imu1.ParseFromString(b)
    # print('corrected_imu')
    # print(corrected_imu1)

    print("Python API Quickstart #5: Ego vehicle driving in circle")
    env = Env()

    sim = lgsvl.Simulator(address = "169.254.42.175", port = 8181)

    if sim.current_scene == lgsvl.wise.DefaultAssets.map_borregasave:
        sim.reset()
    else:
        sim.load(lgsvl.wise.DefaultAssets.map_borregasave)

    spawns = sim.get_spawn()

    state = lgsvl.AgentState()
    state.transform = spawns[0]
    forward = lgsvl.utils.transform_to_forward(spawns[0])
    state.transform.position += 5 * forward  # 5m forwards
    ego = sim.add_agent(env.str("LGSVL__VEHICLE_0", lgsvl.wise.DefaultAssets.ego_lincoln2017mkz_apollo5), lgsvl.AgentType.EGO, state)

    print("Current time = ", sim.current_time)
    print("Current frame = ", sim.current_frame)

    # input("Press Enter to start driving for 30 seconds")

    # VehicleControl objects can only be applied to EGO vehicles
    # You can set the steering (-1 ... 1), throttle and braking (0 ... 1), handbrake and reverse (bool)
    print('Why?')
    c = lgsvl.VehicleControl()
    print('Why?')
    c.throttle = 0.3
    c.steering = -1.0
    # a True in apply_control means the control will be continuously applied ("sticky"). False means the control will be applied for 1 frame
    ego.apply_control(c, True)

    print('Why?')

    sim.run(30)


# apollo_path = "/path/to/apollo"
# bin_file = os.path.join(apollo_path, "protobuf/data.bin")

# with open(os.path.join(apollo_path, "protobuf/data.txt"), "w+") as fout:
#     fout.write("public static readonly string Value = string.Concat(\n")
#     with open(bin_file, "rb") as fin:
#         b = b64encode(fin.read())
#         arr = []
#         while b:
#             arr.append('    "{}"'.format(b[:60].decode('utf-8')))
#             b = b[60:]
#         fout.write(",\n".join(arr))
#     fout.write('\n);')