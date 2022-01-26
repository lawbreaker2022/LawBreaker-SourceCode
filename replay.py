import websockets
import json
import asyncio
from EXtraction import ExtractAll
from GeneticAlgorithm import GAGeneration, EncodedTestCase, DecodedTestCase
from TestCaseRandom import TestCaseRandom
from datetime import datetime
from monitor import Monitor
import re


async def hello(scenario_msg) -> object:
    uri = "ws://localhost:6666"
    async with websockets.connect(uri) as websocket:
        scenario_no = len(scenario_msg)
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
        if msg['TYPE'] == 'READY_FOR_NEW_TEST' and msg['DATA']:
            for i in range(scenario_no):
                print("Current Test Case: {}".format(i))
                send_msg = {'CMD': "CMD_NEW_TEST", 'DATA': scenario_msg[i]}
                await websocket.send(json.dumps(send_msg))
                while True:
                    msg_valid = await websocket.recv()
                    msg_valid = json.loads(msg_valid)
                    if msg_valid['TYPE'] == 'TEST_COMPLETED':
                        output_trace = msg_valid['DATA']
                        with open('result.json', 'w') as outfile:
                            json.dump(output_trace, outfile, indent=2)
                        print("The number of states in the trace is {}".format(len(output_trace['trace'])))
                        print("Is reached: {}, minimal distance: {}\n".format(output_trace['destinationReached'], output_trace['minEgoObsDist']))
                        break




def main():
    file = 'Incompleted.txt'
    with open(file) as f:
        lines = f.readlines()
        time_index = [index for index, s in enumerate(lines) if "Time" in s]
        testcase = []
        for i in range(time_index[-1] + 1, len(lines)):
            testcase.append(json.loads(lines[i]))
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(hello(testcase)))

def main1():
    file = 'data7.json'
    # file = 'issues/loss planning/2-loss_planning.json'
    with open(file) as f:
        testcase = json.load(f)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(hello([testcase])))


def read_bug_testcase(file):
    flist = open(file).readlines()
    case_set = []
    counter = 0
    buffer = ""
    for line in flist:
        if line.startswith("Time"):
            counter = 0
            if buffer != "":
                case_set.append(json.loads(buffer))
            buffer = ""
            continue
        else:
            buffer += line
            counter += 1
    return case_set



if __name__ == "__main__":
    # file_name = "round1/intersection2/bugTestCase.txt"
    # test_cases = read_bug_testcase(file_name)
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(asyncio.gather(hello(test_cases)))

    # main1()

    dir = '/home/xiaofei/Desktop/test/'
    file = dir + 'TestCase2.json'
    with open(file) as f:
        test = json.load(f)
    print(type(test))
