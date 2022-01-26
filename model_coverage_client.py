import copy
import os
import select
import shutil
import signal
import sys
import time
import warnings
from pathlib import Path
from threading import Timer

import websockets
import json
import asyncio
from EXtraction import ExtractAll
from GeneticAlgorithm import GAGeneration, EncodedTestCase, DecodedTestCase
from TestCaseRandom import TestCaseRandom
from datetime import datetime
from AssertionExtraction import SingleAssertion
from map import get_map_info
from model_ga import Generation

import logging





min_fitness_list = []
ave_fitness_list = []


def to_json(obj):
    return json.dumps(obj, default=lambda o: o.__dict__, indent=4)



async def hello(scenario_msg, single_spec, generation_number=1, population_size=3, directory=None) -> object:
    uri = "ws://localhost:8000"
    async with websockets.connect(uri, max_size=None) as websocket:
        scenario_no = len(scenario_msg)
        init_msg = json.dumps({'CMD': "CMD_READY_FOR_NEW_TEST"})
        await websocket.send(init_msg)
        # for i in range(scenario_no):
        # logging.info('iteration: {}'.format(i))
        msg = await websocket.recv()
        msg = json.loads(msg)
        if msg['TYPE'] == 'READY_FOR_NEW_TEST' and msg['DATA']:
            now = datetime.now()
            dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
            with open(directory + '/Incompleted.txt', 'a') as f:
                f.write('Time: {} \n'.format(dt_string))
            with open(directory + '/bugTestCase.txt', 'a') as f:
                f.write('Time: {} \n'.format(dt_string))
            with open(directory + '/NoTrace.txt', 'a') as f:
                f.write('Time: {} \n'.format(dt_string))
            init_msg = json.dumps({'CMD': "CMD_READY_FOR_NEW_TEST"})
            await websocket.send(init_msg)
            for i in range(scenario_no):
                while True:
                    msg = await websocket.recv()
                    msg = json.loads(msg)
                    if msg['TYPE'] == 'READY_FOR_NEW_TEST':
                        if msg['DATA']:
                            logging.info('Running Predefined Test Case: {}'.format(i))
                            send_msg = {'CMD': "CMD_NEW_TEST", 'DATA': scenario_msg[i]}
                            await websocket.send(json.dumps(send_msg))
                        else:
                            time.sleep(3)
                            init_msg = json.dumps({'CMD': "CMD_READY_FOR_NEW_TEST"})
                            await websocket.send(init_msg)
                    elif msg['TYPE'] == 'KEEP_SERVER_AND_CLIENT_ALIVE':
                        send_msg = {'CMD': "KEEP_SERVER_AND_CLIENT_ALIVE", 'DATA': None}
                        await websocket.send(json.dumps(send_msg))
                    elif msg['TYPE'] == 'TEST_TERMINATED' or msg['TYPE'] == 'ERROR':
                        print("Try to reconnect!")
                        time.sleep(3)
                        init_msg = json.dumps({'CMD': "CMD_READY_FOR_NEW_TEST"})
                        await websocket.send(init_msg)
                    elif msg['TYPE'] == 'TEST_COMPLETED':
                        output_trace = msg['DATA']
                        now = datetime.now()
                        dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
                        file = directory + '/data/result-' + dt_string + '.json'
                        with open(file, 'w') as outfile:
                            json.dump(output_trace, outfile, indent=2)
                        if not output_trace['destinationReached']:
                            logging.info("Not reach the destination")
                            with open(directory + '/Incompleted.txt', 'a') as f:
                                json.dump(scenario_msg[i], f, indent=2)
                                f.write('\n')
                        if len(output_trace['trace']) > 1:
                            encoded_testcase = EncodedTestCase(output_trace, single_spec)
                            logging.info("      Fitness Value: {}".format(encoded_testcase.fitness))
                            del encoded_testcase.trace
                            if encoded_testcase.fitness < 0.0:
                                with open(directory + '/bugTestCase.txt', 'a') as bug_file:
                                    json.dump(output_trace, bug_file, indent=2)
                                    bug_file.write('\n')
                        elif len(output_trace['trace']) == 1:
                            logging.info(
                                "Is reached: {}, minimal distance: {}".format(output_trace['destinationReached'],
                                                                              output_trace['minEgoObsDist']))
                        else:
                            logging.info("No trace for the test cases")
                            with open(directory + '/NoTrace.txt', 'a') as f:
                                json.dump(scenario_msg[i], f, indent=2)
                                f.write('\n')
                        init_msg = json.dumps({'CMD': "CMD_READY_FOR_NEW_TEST"})
                        await websocket.send(init_msg)
                        break
            for i in range(4):
                ga_process = Generation(output_trace, num_generation=generation_number, size_population=population_size)
                ga_process.process()
                cases = ga_process.testcases
                covered_number = ga_process.covered_input_space['number']
                total_number = ga_process.input_space['number']
                logging.info("Model coverage is {}/{}".format(covered_number, total_number))

                test_case_dict = {'cases': cases}
                file_name = '/all_case_' + str(i) + '.json'
                with open(directory + file_name, 'w') as f:
                    json.dump(test_case_dict, f)

            # for i in range(len(cases)):
            #     current_testcases = cases[i]
            #     for j in range(len(current_testcases)):
            #         while True:
            #             msg = await websocket.recv()
            #             msg = json.loads(msg)
            #             print(msg['TYPE'])
            #             if msg['TYPE'] == 'READY_FOR_NEW_TEST':
            #                 if msg['DATA']:
            #                     logging.info('Running Generation: {}, Individual: {}'.format(i, j+1))
            #                     send_msg = {'CMD': "CMD_NEW_TEST", 'DATA': current_testcases[j]}
            #                     await websocket.send(json.dumps(send_msg))
            #                 else:
            #                     time.sleep(3)
            #                     init_msg = json.dumps({'CMD': "CMD_READY_FOR_NEW_TEST"})
            #                     await websocket.send(init_msg)
            #             elif msg['TYPE'] == 'TEST_TERMINATED' or msg['TYPE'] == 'ERROR':
            #                 print(msg)
            #                 print("Try to reconnect.")
            #                 time.sleep(3)
            #                 init_msg = json.dumps({'CMD': "CMD_READY_FOR_NEW_TEST"})
            #                 await websocket.send(init_msg)
            #             elif msg['TYPE'] == 'TEST_COMPLETED':
            #                 output_trace = msg['DATA']
            #                 now = datetime.now()
            #                 dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
            #                 file = directory + '/data/result-' + dt_string + '.json'
            #                 with open(file, 'w') as outfile:
            #                     json.dump(output_trace, outfile, indent=2)
            #                 logging.info("The number of states in the trace is {}".format(len(output_trace['trace'])))
            #                 if not output_trace['destinationReached']:
            #                     with open(directory + '/Incompleted.txt', 'a') as f:
            #                         json.dump(current_testcases[j], f, indent=2)
            #                         f.write('\n')
            #                 if len(output_trace['trace']) > 1:
            #                     encoded_testcase = EncodedTestCase(output_trace, single_spec)
            #                     logging.info("      Fitness Value: {}".format(encoded_testcase.fitness))
            #                     del encoded_testcase.trace
            #                     if encoded_testcase.fitness < 0.0:
            #                         with open(directory + '/bugTestCase.txt', 'a') as bug_file:
            #                             now = datetime.now()
            #                             dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
            #                             string_index = "Time:" + dt_string + "Generation: " + str(i) + ", Individual: " + str(j+1) + '\n'
            #                             bug_file.write(string_index)
            #                             json.dump(output_trace, bug_file, indent=2)
            #                             bug_file.write('\n')
            #                 elif len(output_trace['trace']) == 1:
            #                     logging.info("Only one state. Is reached: {}, minimal distance: {}".format(
            #                         output_trace['destinationReached'], output_trace['minEgoObsDist']))
            #                 else:
            #                     logging.info("No trace for the test cases!")
            #                     with open(directory + '/NoTrace.txt', 'a') as f:
            #                         now = datetime.now()
            #                         dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
            #                         f.write("Time: Generation: {}, Individual: {}".format(dt_string, i, j+1))
            #                         json.dump(current_testcases[j], f, indent=2)
            #                         f.write('\n')
            #                 init_msg = json.dumps({'CMD': "CMD_READY_FOR_NEW_TEST"})
            #                 await websocket.send(init_msg)
            #                 break


def spec_scenario(spec, testcase, generations=0, pop_size=1,file_directory=None):
    loop = asyncio.get_event_loop()
    scenario_specification = copy.deepcopy(spec)
    scenario_testcase = copy.deepcopy(testcase)
    msgs = [scenario_testcase]
    with open(file_directory + '/InitTestCase.txt', 'w') as f:
        json.dump(scenario_testcase, f, indent=2)
    loop.run_until_complete(
        asyncio.gather(hello(msgs, scenario_specification, generation_number=generations, population_size=pop_size, directory=file_directory)))


def test_scenario(direct, item):
    file = direct + item
    log_direct = "model_coverage_test_cases/" + Path(item).stem
    if not os.path.exists(log_direct):
        os.makedirs(log_direct)
    else:
        shutil.rmtree(log_direct)

    if not os.path.exists(log_direct + '/data'):
        os.makedirs(log_direct + '/data')

    logging_file = log_direct + '/test.log'
    file_handler = logging.FileHandler(logging_file, mode='w')
    stdout_handler = logging.StreamHandler(sys.stdout)
    logging.basicConfig(level=logging.INFO, handlers=[stdout_handler, file_handler], format='%(asctime)s, %(levelname)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
    logging.info("Current Test Case: {}".format(item))
    isGroundTruth = True
    extracted_data = ExtractAll(file, isGroundTruth)
    testcases = extracted_data.Get_TestCastINJsonList()
    all_specifications = extracted_data.Get_Specifications()
    maps = extracted_data.Get_AllMaps()

    for i in range(len(testcases)):
        test_case = testcases[i]
        scenario_name = test_case['ScenarioName']
        # logging.info("Current scenario is {}.\n".format(scenario_name))
        try:
            specifications_in_scenario = all_specifications[scenario_name]
            current_map = maps[scenario_name]
            ego_init_start = test_case['ego']['start']
            map_info = get_map_info(current_map)
            if "lane_position" in ego_init_start.keys():
                lane_position = ego_init_start['lane_position']
                ego_position = map_info.get_position([lane_position['lane'], lane_position['offset']])
            else:
                ego_position = (ego_init_start['position']['x'], ego_init_start['position']['y'], ego_init_start['position']['z'])
            for spec_index in range(len(specifications_in_scenario)):
                first_specification = specifications_in_scenario[spec_index]
                single_specification = SingleAssertion(first_specification, current_map, ego_position)
                logging.info("\n Evaluate Scenario {} with Assertion {}: {} \n ".format(scenario_name, spec_index, single_specification.specification))
                spec_scenario(spec=single_specification, testcase=test_case, generations=25, pop_size=20, file_directory=log_direct)
        except KeyError:
            spec_scenario(spec={}, testcase=test_case)



if __name__ == "__main__":
    direct = 'test_cases/traffic_rule_tests/'
    # arr = os.listdir(direct)
    # arr = sorted(arr)
    arr = ['Intersection_with_Single-Direction_Roads.txt', 'Intersection_with_Mixed-Direction_Roads.txt', 'Intersection_with_Double-Direction_Roads.txt']
    for item in arr:
        test_scenario(direct, item)




