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
from monitor import Monitor
import logging
from spec_coverage import failure_statement

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

    uri = "ws://localhost:8000"
    async with websockets.connect(uri, max_size=None) as websocket:
        init_msg = json.dumps({'CMD': "CMD_READY_FOR_NEW_TEST"})
        await websocket.send(init_msg)
        msg = await websocket.recv()
        msg = json.loads(msg)
        if msg['TYPE'] == 'READY_FOR_NEW_TEST' and msg['DATA']:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
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
            if len(scenario_msg) < population_size:
                test_case = scenario_msg[0]
                testcase = TestCaseRandom(test_case)
                testcase.testcase_random(population_size - len(scenario_msg))
                for i2 in range(len(testcase.cases) - 1):
                    scenario_msg.append(testcase.cases[i2 + 1])
            improved_trace = None
            covered_predicates = []
            for i in range(population_size):
                while True:
                    msg = await websocket.recv()
                    msg = json.loads(msg)
                    if msg['TYPE'] == 'READY_FOR_NEW_TEST':
                        if msg['DATA']:
                            logging.info('Running Generation: 0, Individual: {}'.format(i + 1))
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
                        dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
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
                            if 'Accident!' in output_trace["testFailures"]: 
                                with open(directory + '/exceptionTestCase.txt', 'a') as bug_file:
                                    now = datetime.now()
                                    dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
                                    string_index = "Time:" + dt_string + "Generation: " + str(0) + ", Individual: " + str(0) +", Bug: " + str(output_trace["testFailures"]) +'\n'
                                    bug_file.write(string_index)
                                    json.dump(output_trace, bug_file, indent=2)
                                    bug_file.write('\n')
                            if encoded_testcase.fitness <= 0.0:
                                cover_monitor = Monitor(output_trace, single_spec)
                                coverage_rate, coverage_statement,_ = cover_monitor.coverage_monitor()
                                logging.info("Coverage rate is: {}/{}, Covered Predicates are: {}".format(len(coverage_statement), len(all_predicates), coverage_statement))
                                del encoded_testcase.trace
                                new_predicate = newlist(covered_predicates, coverage_statement)
                                if len(new_predicate):
                                    covered_predicates = covered_predicates + new_predicate
                                    population.append(encoded_testcase)
                                    improved_trace = copy.deepcopy(output_trace)
                                    with open(directory + '/improvedTestCase.txt', 'a') as bug_file:
                                        now = datetime.now()
                                        dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
                                        string_index = "Time:" + dt_string + '\n'
                                        bug_file.write(string_index)
                                        string_index2 = "The detailed fitness values:" + str(encoded_testcase.muti_fitness) + '\n'
                                        bug_file.write(string_index2)
                                        json.dump(output_trace, bug_file, indent=2)
                                        bug_file.write('\n')
                            else:
                                logging.info("      Fitness Value: {}".format(encoded_testcase.fitness))
                        elif len(output_trace['trace']) == 1:
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
            coverage_rate = len(covered_predicates) / len(all_predicates)
            logging.info("total coverage rate: {}/{} = {}, covered predicates: {}\n".format(len(covered_predicates), len(all_predicates), coverage_rate, covered_predicates))
            all_covered_predicates = all_covered_predicates.union(set(covered_predicates))
            if generation_number:
                if len(population):
                    new_population_obj = GAGeneration(population)
                    new_population = new_population_obj.coverage_one_generation(population)
                    decoder = DecodedTestCase(new_population)
                    new_testcases = decoder.decoding()
                if len(new_testcases) < population_size:
                    if improved_trace is None:
                        improved_trace = output_trace
                    testcase = TestCaseRandom(improved_trace)
                    testcase.testcase_random(population_size - len(new_testcases))
                    for i2 in range(len(testcase.cases) - 1):
                        new_testcases.append(testcase.cases[i2 + 1])
                with open(directory + '/TestCase.txt', 'w') as outfile:
                    for i1 in range(len(new_testcases)):
                        json.dump(new_testcases[i1], outfile, indent=2)
                        outfile.write('\n')
                # Begin GA
                for generation in range(generation_number-1):
                    covered_predicates = []
                    improved_trace = None
                    population = []
                    next_new_testcases = []
                    if len(new_testcases) < population_size:
                        print('checking the number of test cases')
                    for j in range(len(new_testcases)):
                        # deal with each test case
                        while True:
                            msg = await websocket.recv()
                            msg = json.loads(msg)
                            # print(msg['TYPE'])
                            if msg['TYPE'] == 'READY_FOR_NEW_TEST':
                                if msg['DATA']:
                                    logging.info('Running Generation: {}, Individual: {}'.format(generation + 1, j + 1))
                                    send_msg = {'CMD': "CMD_NEW_TEST", 'DATA': new_testcases[j]}
                                    await websocket.send(json.dumps(send_msg))
                                else:
                                    time.sleep(3)
                                    init_msg = json.dumps({'CMD': "CMD_READY_FOR_NEW_TEST"})
                                    await websocket.send(init_msg)
                            elif msg['TYPE'] == 'KEEP_SERVER_AND_CLIENT_ALIVE':
                                send_msg = {'CMD': "KEEP_SERVER_AND_CLIENT_ALIVE", 'DATA': None}
                                await websocket.send(json.dumps(send_msg))
                            elif msg['TYPE'] == 'TEST_TERMINATED' or msg['TYPE'] == 'ERROR':
                                # print(msg)
                                print("Try to reconnect.")
                                time.sleep(3)
                                init_msg = json.dumps({'CMD': "CMD_READY_FOR_NEW_TEST"})
                                await websocket.send(init_msg)
                            elif msg['TYPE'] == 'TEST_COMPLETED':
                                output_trace = msg['DATA']
                                now = datetime.now()
                                dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
                                file = directory + '/data/result' + dt_string + '.json'
                                with open(file, 'w') as outfile:
                                    json.dump(output_trace, outfile, indent=2)
                                logging.info(
                                    "The number of states in the trace is {}".format(len(output_trace['trace'])))
                                if not output_trace['destinationReached']:
                                    with open(directory + '/Incompleted.txt', 'a') as f:
                                        json.dump(new_testcases[j], f, indent=2)
                                        f.write('\n')
                                if len(output_trace['trace']) > 1:
                                    encoded_testcase = EncodedTestCase(output_trace, single_spec)
                                    if 'Accident!' in output_trace["testFailures"]: 
                                        with open(directory + '/exceptionTestCase.txt', 'a') as bug_file:
                                            now = datetime.now()
                                            dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
                                            string_index = "Time:" + dt_string + "Generation: " + str(generation + 1) + ", Individual: " + str(j + 1) +", Bug: " + str(output_trace["testFailures"]) +'\n'
                                            bug_file.write(string_index)
                                            json.dump(output_trace, bug_file, indent=2)
                                            bug_file.write('\n')
                                    if encoded_testcase.fitness <= 0.0:
                                        cover_monitor = Monitor(output_trace, single_spec)
                                        coverage_rate, coverage_statement, _ = cover_monitor.coverage_monitor()
                                        logging.info("Coverage rate is: {}/{}, Covered Predicates are: {}".format(
                                            len(coverage_statement), len(all_predicates), coverage_statement))
                                        del encoded_testcase.trace
                                        new_predicate = newlist(covered_predicates, coverage_statement)
                                        if len(new_predicate):
                                            covered_predicates = covered_predicates + new_predicate
                                            population.append(encoded_testcase)
                                            improved_trace = copy.deepcopy(output_trace)
                                            with open(directory + '/improvedTestCase.txt', 'a') as bug_file:
                                                now = datetime.now()
                                                dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
                                                string_index = "Time:" + dt_string + "Generation: " + str(
                                                    generation + 1) + ", Individual: " + str(j + 1) + '\n'
                                                bug_file.write(string_index)
                                                string_index2 = "The detailed fitness values:" + str(encoded_testcase.muti_fitness) + '\n'
                                                bug_file.write(string_index2)
                                                json.dump(output_trace, bug_file, indent=2)
                                                bug_file.write('\n')
                                    else:
                                        logging.info("      Fitness Value: {}".format(encoded_testcase.fitness))
                                elif len(output_trace['trace']) == 1:
                                    logging.info("Only one state. Is reached: {}, minimal distance: {}".format(
                                        output_trace['destinationReached'], output_trace['minEgoObsDist']))
                                    # testcase = TestCaseRandom(output_trace)
                                    # testcase.testcase_random(1)
                                    # next_new_testcases.append(testcase.cases[-1])
                                else:
                                    # testcase = TestCaseRandom(output_trace)
                                    # testcase.testcase_random(1)
                                    # next_new_testcases.append(testcase.cases[-1])
                                    logging.info("No trace for the test cases!")
                                    with open(directory + '/NoTrace.txt', 'a') as f:
                                        now = datetime.now()
                                        dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
                                        f.write("Time: Generation: {}, Individual: {}".format(dt_string, generation + 1, j))
                                        json.dump(new_testcases[j], f, indent=2)
                                        f.write('\n')
                                init_msg = json.dumps({'CMD': "CMD_READY_FOR_NEW_TEST"})
                                await websocket.send(init_msg)
                                break
                    coverage_rate = len(covered_predicates) / len(all_predicates)
                    logging.info("total coverage rate: {}/{} = {}, covered predicates: {}\n".format(len(covered_predicates), len(all_predicates), coverage_rate, covered_predicates))
                    all_covered_predicates = all_covered_predicates.union(set(covered_predicates))
                    if len(population):
                        new_population_obj = GAGeneration(population)
                        new_population = new_population_obj.coverage_one_generation(population)
                        decoder = DecodedTestCase(new_population)
                        ga_new_testcases = decoder.decoding()
                        next_new_testcases.extend(ga_new_testcases)
                    if len(next_new_testcases) < population_size:
                        if improved_trace is None:
                            improved_trace = output_trace
                        testcase = TestCaseRandom(improved_trace)
                        testcase.testcase_random(population_size - len(next_new_testcases))
                        for i2 in range(len(testcase.cases) - 1):
                            next_new_testcases.append(testcase.cases[i2 + 1])
                    new_testcases = copy.deepcopy(next_new_testcases)
                    with open(directory + '/TestCase.txt', 'a') as outfile:
                        for i in range(len(new_testcases)):
                            try:
                                json.dump(new_testcases[i], outfile, indent=2)
                                outfile.write('\n')
                            except TypeError:
                                logging.info("Check the types of test cases")
                #  The last generation
                improved_trace = None
                covered_predicates = []
                generation += 2
                for j in range(len(new_testcases)):
                    while True:
                        msg = await websocket.recv()
                        msg = json.loads(msg)
                        # print(msg['TYPE'])
                        if msg['TYPE'] == 'READY_FOR_NEW_TEST':
                            if msg['DATA']:
                                logging.info('Running Generation: {}, Individual: {}'.format(generation, j + 1))
                                send_msg = {'CMD': "CMD_NEW_TEST", 'DATA': new_testcases[j]}
                                await websocket.send(json.dumps(send_msg))
                            else:
                                time.sleep(3)
                                init_msg = json.dumps({'CMD': "CMD_READY_FOR_NEW_TEST"})
                                await websocket.send(init_msg)
                        elif msg['TYPE'] == 'KEEP_SERVER_AND_CLIENT_ALIVE':
                            send_msg = {'CMD': "KEEP_SERVER_AND_CLIENT_ALIVE", 'DATA': None}
                            await websocket.send(json.dumps(send_msg))
                        elif msg['TYPE'] == 'TEST_TERMINATED' or msg['TYPE'] == 'ERROR':
                            # print(msg)
                            print("Try to reconnect.")
                            time.sleep(3)
                            init_msg = json.dumps({'CMD': "CMD_READY_FOR_NEW_TEST"})
                            await websocket.send(init_msg)

                        elif msg['TYPE'] == 'TEST_COMPLETED':
                            output_trace = msg['DATA']
                            now = datetime.now()
                            dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
                            file = directory + '/data/result' + dt_string + '.json'
                            with open(file, 'w') as outfile:
                                json.dump(output_trace, outfile, indent=2)
                            logging.info("The number of states in the trace is {}".format(len(output_trace['trace'])))
                            if not output_trace['destinationReached']:
                                with open(directory + '/Incompleted.txt', 'a') as f:
                                    json.dump(new_testcases[j], f, indent=2)
                                    f.write('\n')
                            if len(output_trace['trace']) > 1:
                                encoded_testcase = EncodedTestCase(output_trace, single_spec)
                                if 'Accident!' in output_trace["testFailures"]: 
                                    with open(directory + '/exceptionTestCase.txt', 'a') as bug_file:
                                        now = datetime.now()
                                        dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
                                        string_index = "Time:" + dt_string + "Generation: " + str(0) + ", Individual: " + str(0) +", Bug: " + str(output_trace["testFailures"]) +'\n'
                                        bug_file.write(string_index)
                                        json.dump(output_trace, bug_file, indent=2)
                                        bug_file.write('\n')
                                if encoded_testcase.fitness <= 0.0:
                                    cover_monitor = Monitor(output_trace, single_spec)
                                    coverage_rate, coverage_statement, _ = cover_monitor.coverage_monitor()
                                    logging.info("Coverage rate is: {}/{}, Covered Predicates are: {}".format(
                                        len(coverage_statement), len(all_predicates), coverage_statement))
                                    del encoded_testcase.trace
                                    new_predicate = newlist(covered_predicates, coverage_statement)
                                    if len(new_predicate):
                                        covered_predicates = covered_predicates + new_predicate
                                        population.append(encoded_testcase)
                                        improved_trace = copy.deepcopy(output_trace)
                                        with open(directory + '/improvedTestCase.txt', 'a') as bug_file:
                                            now = datetime.now()
                                            dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
                                            string_index = "Time:" + dt_string + "Generation: " + str(
                                                generation) + ", Individual: " + str(j + 1) + '\n'
                                            bug_file.write(string_index)
                                            string_index2 = "The detailed fitness values:" + str(encoded_testcase.muti_fitness) + '\n'
                                            bug_file.write(string_index2)
                                            json.dump(output_trace, bug_file, indent=2)
                                            bug_file.write('\n')
                                else:
                                    logging.info("      Fitness Value: {}".format(encoded_testcase.fitness))
                            elif len(output_trace['trace']) == 1:
                                logging.info("Only one state. Is reached: {}, minimal distance: {}".format(
                                    output_trace['destinationReached'], output_trace['minEgoObsDist']))
                                # testcase = TestCaseRandom(output_trace)
                                # testcase.testcase_random(1)
                                # next_new_testcases.append(testcase.cases[-1])
                            else:
                                # testcase = TestCaseRandom(output_trace)
                                # testcase.testcase_random(1)
                                # next_new_testcases.append(testcase.cases[-1])
                                logging.info("No trace for the test cases!")
                                with open(directory + '/NoTrace.txt', 'a') as f:
                                    now = datetime.now()
                                    dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
                                    f.write("Time: Generation: {}, Individual: {}".format(dt_string, generation, j))
                                    json.dump(new_testcases[j], f, indent=2)
                                    f.write('\n')
                            init_msg = json.dumps({'CMD': "CMD_READY_FOR_NEW_TEST"})
                            await websocket.send(init_msg)
                            break
                coverage_rate = len(covered_predicates) / len(all_predicates)
                logging.info("total coverage rate: {}/{} = {}, covered predicates: {}\n".format(len(covered_predicates), len(all_predicates), coverage_rate, covered_predicates))
                all_covered_predicates = all_covered_predicates.union(set(covered_predicates))
                logging.info("Final coverage rate: {}/{}".format(len(all_covered_predicates), len(all_predicates)))
                logging.info("Covered Predicates: {}".format(all_covered_predicates))


def spec_scenario(spec, testcase, generations=0, pop_size=1, file_directory=None):
    loop = asyncio.get_event_loop()
    scenario_specification = copy.deepcopy(spec)
    scenario_testcase = copy.deepcopy(testcase)
    msgs = [scenario_testcase]
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



def test_scenario(direct, item):
    file = direct + item
    # bug_file = 'rerun_for_videos/' + Path(item).stem + '/bugTestCase.txt'
    # bug_cases = read_bug_testcase(bug_file)
    # bug_cases = []

    log_direct ='coverage/' + Path(item).stem
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
    logging.info("Current Test Case: {}".format(item))
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
                # spec_scenario(spec=single_specification, testcase=bug_cases, generations=25, pop_size=20,
                              # file_directory=log_direct)
                spec_scenario(spec=single_specification, testcase=test_case, generations=25, pop_size=20, file_directory=log_direct)
                # print(testcase)
        except KeyError:
            spec_scenario(spec={}, testcase=test_case)


if __name__ == "__main__":
    direct = 'test_cases/traffic_rule_tests/'
    # arr = os.listdir(direct)
    # arr = sorted(arr)
    arr = ['Intersection_with_Single-Direction_Roads.txt', 'Intersection_with_Mixed-Direction_Roads.txt', 'Intersection_with_Double-Direction_Roads.txt']
    for item in arr:
        test_scenario(direct, item)


    # direct = 'test_cases/coverage_final/'
    # arr = os.listdir(direct)
    # arr = sorted(arr)
    # # arr = ['intersection5.txt']
    # # arr = ['change02.txt', 'change03.txt', 'change04.txt', 'change11.txt', 'change12.txt', 'change13.txt']
    # # arr = ['change11.txt', 'change12.txt', 'change13.txt']
    # for item in arr:
    #     test_scenario(direct, item)
