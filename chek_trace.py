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
from GeneticAlgorithm import GAGeneration, EncodedTestCase, DecodedTestCase, get_testcase
from TestCaseRandom import TestCaseRandom
from datetime import datetime
from AssertionExtraction import SingleAssertion
from map import get_map_info
from monitor import Monitor
import logging
from spec_coverage import failure_statement
from natsort import natsorted

# logging.basicConfig(level=level, handlers=[stdout_handler, file_handler],format='%(asctime)s, %(levelname)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.FileHandler('test.log', 'a'))
# logger.addHandler(logging.StreamHandler(sys.stdout))




def newlist(parent_list, list1):
    new_element = [element for element in list1 if element not in parent_list]
    return new_element


def to_json(obj):
    return json.dumps(obj, default=lambda o: o.__dict__, indent=4)


async def hello(scenario_msg, single_spec, generation_number=1, population_size=3, directory=None) -> object:
    spec_str = single_spec.translated_statement
    negative_predicate_obj = failure_statement(spec_str)
    all_predicates = negative_predicate_obj.neg_predicate()
    all_covered_predicates = set()

    uri = "ws://localhost:6666"
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
            population = []
            new_testcases = []
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
                    elif msg['TYPE'] == 'TEST_TERMINATED' or msg['TYPE'] == 'ERROR':
                        print("Try to reconnect!")
                        time.sleep(3)
                        init_msg = json.dumps({'CMD': "CMD_READY_FOR_NEW_TEST"})
                        await websocket.send(init_msg)
                    elif msg['TYPE'] == 'TEST_COMPLETED':
                        output_trace = msg['DATA']
                        now = datetime.now()
                        dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
                        file = directory + '/data/result' + dt_string + '.json'
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
                            population.append(encoded_testcase)
                        elif len(output_trace['trace']) == 1:
                            logging.info(
                                "Is reached: {}, minimal distance: {}".format(output_trace['destinationReached'],
                                                                              output_trace['minEgoObsDist']))
                            testcase = TestCaseRandom(output_trace)
                            testcase.testcase_random(1)
                            new_testcases.append(testcase.cases[-1])
                        else:
                            logging.info("No trace for the test cases")
                            with open(directory + '/NoTrace.txt', 'a') as f:
                                json.dump(scenario_msg[i], f, indent=2)
                                f.write('\n')
                            testcase = TestCaseRandom(output_trace)
                            testcase.testcase_random(1)
                            new_testcases.append(testcase.cases[-1])
                        init_msg = json.dumps({'CMD': "CMD_READY_FOR_NEW_TEST"})
                        await websocket.send(init_msg)
                        break

def spec_scenario(spec, testcase, generations=0, pop_size=1, file_directory=None):
    loop = asyncio.get_event_loop()
    scenario_specification = copy.deepcopy(spec)
    msgs = copy.deepcopy(testcase)
    loop.run_until_complete(
        asyncio.gather(hello(msgs, scenario_specification, generation_number=generations, population_size=pop_size,
                             directory=file_directory)))

def read_bug_testcase(bug_file):
    with open(bug_file) as f:
        lines = f.readlines()
        time_index = [index for index, s in enumerate(lines) if "Time" in s]
        testcases = []
        for i in range(1, len(time_index)-1):
            case_str = ''
            for j in range(time_index[i]+1, time_index[i+1]):
                case_str += lines[j]
            case = json.loads(case_str)
            del case['testFailures']
            del case['testResult']
            del case['timeOfDay']
            del case['destinationReached']
            del case['minEgoObsDist']
            del case['nearestGtObs']
            del case['completed']
            del case['groundTruthPerception']
            del case['recordingPath']
            testcases.append(case)
        case_str = ''
        for j in range(time_index[-1] + 1, len(lines)):
            case_str += lines[j]
        case = json.loads(case_str)
        del case['testFailures']
        del case['testResult']
        del case['timeOfDay']
        del case['destinationReached']
        del case['minEgoObsDist']
        del case['nearestGtObs']
        del case['completed']
        del case['groundTruthPerception']
        del case['recordingPath']
        testcases.append(case)
        return testcases

def read_testcase_from_trace(trace_direct):
    traces = os.listdir(trace_direct)
    traces = natsorted(traces)
    testcases = []
    for trace in traces:
        if trace.endswith('.json'):
            trace_file = trace_direct + trace
            with open(trace_file) as f:
                content = json.load(f)
                test_case = get_testcase(content)
                testcases.append(test_case)
    file = trace_direct + 'testcase.json'
    with open(file, 'w') as outfile:
        json.dump(testcases, outfile, indent=2)
    # return testcases






def test_scenario(direct, item, bug_cases, trace_directory):

    file = direct + item
    log_direct = trace_directory + Path(item).stem
    if not os.path.exists(log_direct):
        os.makedirs(log_direct)
    else:
        shutil.rmtree(log_direct)

    if not os.path.exists(log_direct + '/data'):
        os.makedirs(log_direct + '/data')

    logging_file = log_direct + '/test.log'
    file_handler = logging.FileHandler(logging_file, mode='w')
    stdout_handler = logging.StreamHandler(sys.stdout)
    logging.basicConfig(level=logging.INFO, handlers=[stdout_handler, file_handler],
                        format='%(asctime)s, %(levelname)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
    # if 'ga_3' in trace_directory:
    #     logging.info("Current Round: ga_3, Current Test Case: {}".format(item))
    # elif 'ga_4' in trace_directory:
    #     logging.info("Current Round: ga_4, Current Test Case: {}".format(item))
    # elif 'ga_5' in trace_directory:
    #     logging.info("Current Round: ga_3, Current Test Case: {}".format(item))
    isGroundTruth = True
    extracted_data = ExtractAll(file, isGroundTruth)
    origin_case = extracted_data.Get_TestCastINJsonList()
    all_specifications = extracted_data.Get_Specifications()
    maps = extracted_data.Get_AllMaps()

    for i in range(len(origin_case)):
        test_case = origin_case[i]
        scenario_name = test_case['ScenarioName']
        logging.info("Current scenario is {}.\n".format(scenario_name))
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
                spec_scenario(spec=single_specification, testcase=bug_cases, generations=25, pop_size=20,
                              file_directory=log_direct)
        except KeyError:
            spec_scenario(spec={}, testcase=test_case)


if __name__ == "__main__":

    direct = 'test_cases/final/'
    test_rounds = ['random_5']
    # test_rounds = ['random_2']
    # test_rounds = ['ga_3', 'ga_4', 'ga_5', 'random_1', 'random_2', 'random_3', 'random_4', 'random_5']
    scenarios = ['lanechange1.txt'] # 'lanechange3.txt', 'overtaking1.txt'
    for scenario in scenarios:
        for test_round in test_rounds:
            print('current round: {}, current scenario: {}'.format(test_round, scenario))
            trace_directory = '/run/user/1002/gvfs/smb-share:server=synology_nas.local,share=zhouyuan/' + test_round + '/' + Path(scenario).stem + '/results/'
            try:
                trace_file = trace_directory + 'testcase.json'
                with open(trace_file) as f:
                    bug_cases = json.load(f)
            except FileNotFoundError:
                read_testcase_from_trace(trace_directory)
                trace_file = trace_directory + 'testcase.json'
                with open(trace_file) as f:
                    bug_cases = json.load(f)

            print("number of test cases: {}".format(len(bug_cases)))
            test_scenario(direct, scenario, bug_cases, trace_directory)





    # # remain_case = bug_cases[24:]
    #
    # arr = os.listdir(direct)
    # arr = sorted(arr)
    # # arr = ['overtaking1.txt']
    # # arr = ['change02.txt', 'change03.txt', 'change04.txt', 'change11.txt', 'change12.txt', 'change13.txt']
    # # arr = ['change11.txt', 'change12.txt', 'change13.txt']
    # arr = ['intersection1.txt']
    # for item in arr:
    #     test_scenario(direct, item, bug_cases, test_round)
