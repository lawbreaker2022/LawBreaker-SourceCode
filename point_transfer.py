import websockets
import json
import asyncio


uri = "ws://localhost:6666"
async def tansfer(point_msg):
    async with websockets.connect(uri) as websocket:
        init_msg = json.dumps({'CMD': "CMD_READY_FOR_NEW_TEST"})
        await websocket.send(init_msg)
        # for i in range(scenario_no):
        # print('iteration: {}'.format(i))
        msg = await websocket.recv()
        msg = json.loads(msg)
        # while True:
        #     msg = await websocket.recv()
        #     msg = json.loads(msg)
        #     if msg['TYPE'] == 'READY_FOR_NEW_TEST' and msg['DATA']:
        #         break
        if msg['TYPE'] == 'READY_FOR_NEW_TEST':
            send_msg = {"CMD": "CMD_GPS_TO_MAP", 'DATA': {'lane_position': {'lane': 'lane_1155', 'offset': 3}}}
            await websocket.send(json.dumps(send_msg))
            while True:
                received_msg = await websocket.recv()
                print(json.loads(received_msg))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    file = 'point_msg.json'
    with open(file) as f:
        data = json.load(f)
    msg = data['DATA']
    loop.run_until_complete(asyncio.gather(tansfer(msg)))



