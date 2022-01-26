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



def newlist(parent_list, list1):
    new_element = [element for element in list1 if element not in parent_list]
    return new_element


def to_json(obj):
    return json.dumps(obj, default=lambda o: o.__dict__, indent=4)


async def hello(scenario_msg, single_spec, generation_number=1, population_size=3, directory=None) -> object:

    maximun = len(single_spec.sub_violations)
    remaining_sub_violations = single_spec.sub_violations

    seed = dict()
    mapping = dict()
    for item in remaining_sub_violations:
        mapping[item] = -1000
        seed[item] = None

    # print(mapping)
    # print(seed)
    
    # spec_str = single_spec.translated_statement
    # negative_predicate_obj = failure_statement(spec_str)
    # all_predicates = negative_predicate_obj.neg_predicate()
    # all_covered_predicates = set()

    uri = "ws://localhost:8000"
    async with websockets.connect(uri,  max_size= 300000000, ping_interval=None) as websocket:
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

            #process with the initial generation(random)
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
                            asyncio.sleep(3)
                            init_msg = json.dumps({'CMD': "CMD_READY_FOR_NEW_TEST"})
                            await websocket.send(init_msg)
                    elif msg['TYPE'] == 'KEEP_SERVER_AND_CLIENT_ALIVE':
                        send_msg = {'CMD': "KEEP_SERVER_AND_CLIENT_ALIVE", 'DATA': None}
                        await websocket.send(json.dumps(send_msg))
                    elif msg['TYPE'] == 'TEST_TERMINATED' or msg['TYPE'] == 'ERROR':
                        print("Try to reconnect!")
                        asyncio.sleep(3)
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
                                encoded_testcase.compute_muti_fitness()
                                with open(directory + '/AccidentTestCase.txt', 'a') as bug_file:
                                    now = datetime.now()
                                    dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
                                    string_index = "Time:" + dt_string + "Generation: " + str(0) + ", Individual: " + str(i + 1) +", Bug: " + str(output_trace["testFailures"]) +'\n'
                                    bug_file.write(string_index)
                                    string_index2 = "The detailed fitness values:" + str(encoded_testcase.muti_fitness) + '\n'
                                    bug_file.write(string_index2)
                                    json.dump(output_trace, bug_file, indent=2)
                                    bug_file.write('\n')   
                            covered = []
                            if encoded_testcase.fitness <= 0.0:
                                if encoded_testcase.muti_fitness == {}:
                                    encoded_testcase.compute_muti_fitness()
                                monitor = Monitor(output_trace, 0)
                                for spec in remaining_sub_violations:                                  
                                    fitness0 = monitor.continuous_monitor2(spec)                                                                         
                                    if fitness0 >= 0.0:
                                        covered.append(spec)
                                        # logging.info("Coverage rate is: {}/{}, Covered Predicates are: {}".format(len(coverage_statement), len(all_predicates), coverage_statement))
                                        with open(directory + '/improvedTestCase.txt', 'a') as bug_file:
                                            now = datetime.now()
                                            dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
                                            string_index = "Time:" + dt_string + "Generation: " + str(0) + ", Individual: " + str(i + 1) +'\n'
                                            bug_file.write(string_index)
                                            string_index2 = "The detailed fitness values:" + str(encoded_testcase.muti_fitness) + '\n'
                                            bug_file.write(string_index2)
                                            coverage_rate = 1- len(remaining_sub_violations) / maximun
                                            string_index3 = "total coverage rate: {}/{} = {}, new covered predicates: {}\n".format((maximun - len(remaining_sub_violations)), maximun, coverage_rate, spec)
                                            bug_file.write(string_index3)
                                            # bug_file.write(spec)
                                            json.dump(output_trace, bug_file, indent=2)
                                            bug_file.write('\n')                                           
                                    else:
                                        if mapping[spec] < fitness0:
                                            seed[spec] = encoded_testcase
                                            mapping[spec] = fitness0
                                for itme in covered:
                                    remaining_sub_violations.remove(itme)
                                    del seed[itme]
                                    del mapping[itme]
                            # covered = []
                            else:
                                logging.info("      Fitness Value: {}".format(encoded_testcase.fitness))
                                monitor = Monitor(output_trace, 0)
                                for spec in remaining_sub_violations:                                  
                                    fitness0 = monitor.continuous_monitor2(spec)     
                                    assert fitness0 < 0.0                                                                     
                                    if fitness0 >= 0.0:
                                        covered.append(spec)
                                        # logging.info("Coverage rate is: {}/{}, Covered Predicates are: {}".format(len(coverage_statement), len(all_predicates), coverage_statement))
                                        with open(directory + '/improvedTestCase.txt', 'a') as bug_file:
                                            now = datetime.now()
                                            dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
                                            string_index = "Time:" + dt_string + "Generation: " + str(0) + ", Individual: " + str(i + 1) +'\n'
                                            bug_file.write(string_index)
                                            string_index2 = "The detailed fitness values:" + str(encoded_testcase.muti_fitness) + '\n'
                                            bug_file.write(string_index2)
                                            coverage_rate = 1- len(remaining_sub_violations) / maximun
                                            string_index3 = "total coverage rate: {}/{} = {}, new covered predicates: {}\n".format((maximun - len(remaining_sub_violations)), maximun, coverage_rate, spec)
                                            bug_file.write(string_index3)
                                            # bug_file.write(spec)
                                            json.dump(output_trace, bug_file, indent=2)
                                            bug_file.write('\n')                                           
                                    else:
                                        if mapping[spec] < fitness0:
                                            seed[spec] = encoded_testcase
                                            mapping[spec] = fitness0
                                for itme in covered:
                                    remaining_sub_violations.remove(itme)
                                    del seed[itme]
                                    del mapping[itme]
                            del encoded_testcase.trace 
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
            coverage_rate = 1- len(remaining_sub_violations) / maximun
            logging.info("total coverage rate: {}/{} = {}, uncovered predicates: {}\n".format((maximun - len(remaining_sub_violations)), maximun, coverage_rate, remaining_sub_violations))
            mapping = sorted(mapping.items(), key=lambda item: item[1], reverse=True)
            mapping = dict(mapping)
            # print(mapping)
            if generation_number:
                for key in mapping:
                    # if len(population) < population_size:
                    population.append(seed[key])
                    population[-1].fitness = mapping[key]
                    # else:
                    #     assert population[-1].fitness >= mapping[key]
                new_population_obj = GAGeneration(population)
                new_population = new_population_obj.one_generation_law_breaking(population_size)
                decoder = DecodedTestCase(new_population)
                next_new_testcases = decoder.decoding()
                new_testcases = copy.deepcopy(next_new_testcases)
                print(len(new_testcases))
                assert len(new_testcases)==population_size
                # if len(new_testcases) < population_size:
                #     print("??????????????")
                #     if improved_trace is None:
                #         improved_trace = output_trace
                #     testcase = TestCaseRandom(improved_trace)
                #     testcase.testcase_random(population_size - len(new_testcases))
                #     for i2 in range(len(testcase.cases) - 1):
                #         new_testcases.append(testcase.cases[i2 + 1])
                with open(directory + '/TestCase.txt', 'w') as outfile:
                    for i1 in range(len(new_testcases)):
                        json.dump(new_testcases[i1], outfile, indent=2)
                        outfile.write('\n')

                # Begin GA
                for generation in range(generation_number-1):
                    # covered_predicates = []
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
                                    asyncio.sleep(3)
                                    init_msg = json.dumps({'CMD': "CMD_READY_FOR_NEW_TEST"})
                                    await websocket.send(init_msg)
                            elif msg['TYPE'] == 'KEEP_SERVER_AND_CLIENT_ALIVE':
                                send_msg = {'CMD': "KEEP_SERVER_AND_CLIENT_ALIVE", 'DATA': None}
                                await websocket.send(json.dumps(send_msg))
                            elif msg['TYPE'] == 'TEST_TERMINATED' or msg['TYPE'] == 'ERROR':
                                # print(msg)
                                print("Try to reconnect.")
                                asyncio.sleep(3)
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
                                    # del encoded_testcase.trace                       
                                    if 'Accident!' in output_trace["testFailures"]: 
                                        # if encoded_testcase.muti_fitness == {}:
                                        encoded_testcase.compute_muti_fitness()
                                        with open(directory + '/AccidentTestCase.txt', 'a') as bug_file:
                                            now = datetime.now()
                                            dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
                                            string_index = "Time:" + dt_string + "Generation: " + str(generation) + ", Individual: " + str(j+1) +", Bug: " + str(output_trace["testFailures"]) +'\n'
                                            bug_file.write(string_index)
                                            string_index2 = "The detailed fitness values:" + str(encoded_testcase.muti_fitness) + '\n'
                                            bug_file.write(string_index2)
                                            json.dump(output_trace, bug_file, indent=2)
                                            bug_file.write('\n')   
                                    covered = []
                                    if encoded_testcase.fitness <= 0.0:
                                        if encoded_testcase.muti_fitness == {}:
                                            encoded_testcase.compute_muti_fitness()
                                        monitor = Monitor(output_trace, 0)
                                        for spec in remaining_sub_violations:                                  
                                            fitness0 = monitor.continuous_monitor2(spec)                                                                          
                                            if fitness0 >= 0.0:
                                                covered.append(spec)
                                                # logging.info("Coverage rate is: {}/{}, Covered Predicates are: {}".format(len(coverage_statement), len(all_predicates), coverage_statement))
                                                with open(directory + '/improvedTestCase.txt', 'a') as bug_file:
                                                    now = datetime.now()
                                                    dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
                                                    string_index = "Time:" + dt_string + "Generation: " + str(generation) + ", Individual: " + str(j + 1) +'\n'
                                                    bug_file.write(string_index)
                                                    string_index2 = "The detailed fitness values:" + str(encoded_testcase.muti_fitness) + '\n'
                                                    bug_file.write(string_index2)
                                                    coverage_rate = 1- len(remaining_sub_violations) / maximun
                                                    string_index3 = "total coverage rate: {}/{} = {}, new covered predicates: {}\n".format((maximun - len(remaining_sub_violations)), maximun, coverage_rate, spec)
                                                    bug_file.write(string_index3)
                                                    # bug_file.write(spec)
                                                    json.dump(output_trace, bug_file, indent=2)
                                                    bug_file.write('\n')                                           
                                            else:
                                                if mapping[spec] < fitness0:
                                                    seed[spec] = encoded_testcase
                                                    mapping[spec] = fitness0
                                        for itme in covered:
                                            remaining_sub_violations.remove(itme)
                                            del seed[itme]
                                            del mapping[itme]
                                    # covered = []
                                    else:
                                        logging.info("      Fitness Value: {}".format(encoded_testcase.fitness))
                                        monitor = Monitor(output_trace, 0)
                                        for spec in remaining_sub_violations:                                  
                                            fitness0 = monitor.continuous_monitor2(spec)   
                                            assert fitness0 < 0.0                                                                      
                                            if fitness0 >= 0.0:
                                                covered.append(spec)
                                                # logging.info("Coverage rate is: {}/{}, Covered Predicates are: {}".format(len(coverage_statement), len(all_predicates), coverage_statement))
                                                with open(directory + '/improvedTestCase.txt', 'a') as bug_file:
                                                    now = datetime.now()
                                                    dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
                                                    string_index = "Time:" + dt_string + "Generation: " + str(generation) + ", Individual: " + str(j + 1) +'\n'
                                                    bug_file.write(string_index)
                                                    string_index2 = "The detailed fitness values:" + str(encoded_testcase.muti_fitness) + '\n'
                                                    bug_file.write(string_index2)
                                                    coverage_rate = 1- len(remaining_sub_violations) / maximun
                                                    string_index3 = "total coverage rate: {}/{} = {}, new covered predicates: {}\n".format((maximun - len(remaining_sub_violations)), maximun, coverage_rate, spec)
                                                    bug_file.write(string_index3)
                                                    # bug_file.write(spec)
                                                    json.dump(output_trace, bug_file, indent=2)                              
                                            else:
                                                if mapping[spec] < fitness0:
                                                    seed[spec] = encoded_testcase
                                                    mapping[spec] = fitness0
                                        for itme in covered:
                                            remaining_sub_violations.remove(itme)
                                            del seed[itme]
                                            del mapping[itme]
                                    del encoded_testcase.trace 
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
                    coverage_rate = 1- len(remaining_sub_violations) / maximun
                    logging.info("total coverage rate: {}/{} = {}, uncovered predicates: {}\n".format((maximun - len(remaining_sub_violations)), maximun, coverage_rate, remaining_sub_violations))
                    mapping = sorted(mapping.items(), key=lambda item: item[1], reverse=True)
                    mapping = dict(mapping)
                    # print(mapping)
                    for key in mapping:
                        population.append(seed[key])
                        population[-1].fitness = mapping[key]
                    new_population_obj = GAGeneration(population)
                    new_population = new_population_obj.one_generation_law_breaking(population_size)
                    decoder = DecodedTestCase(new_population)
                    next_new_testcases = decoder.decoding()
                    new_testcases = copy.deepcopy(next_new_testcases)
                    assert len(new_testcases)==population_size
                    # if len(next_new_testcases) < population_size:
                    #     if improved_trace is None:
                    #         improved_trace = output_trace
                    #     testcase = TestCaseRandom(improved_trace)
                    #     testcase.testcase_random(population_size - len(next_new_testcases))
                    #     for i2 in range(len(testcase.cases) - 1):
                    #         next_new_testcases.append(testcase.cases[i2 + 1])
                    # new_testcases = copy.deepcopy(next_new_testcases)
                    with open(directory + '/TestCase.txt', 'a') as outfile:
                        for i in range(len(new_testcases)):
                            try:
                                json.dump(new_testcases[i], outfile, indent=2)
                                outfile.write('\n')
                            except TypeError:
                                logging.info("Check the types of test cases")
                #  The last generation
                # improved_trace = None
                # covered_predicates = []
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
                                # del encoded_testcase.trace                       
                                if 'Accident!' in output_trace["testFailures"]: 
                                    encoded_testcase.compute_muti_fitness()
                                    with open(directory + '/AccidentTestCase.txt', 'a') as bug_file:
                                        now = datetime.now()
                                        dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
                                        string_index = "Time:" + dt_string + "Generation: " + str(generation) + ", Individual: " + str(j + 1) +", Bug: " + str(output_trace["testFailures"]) +'\n'
                                        bug_file.write(string_index)
                                        string_index2 = "The detailed fitness values:" + str(encoded_testcase.muti_fitness) + '\n'
                                        bug_file.write(string_index2)
                                        json.dump(output_trace, bug_file, indent=2)
                                        bug_file.write('\n')   
                                covered = []
                                if encoded_testcase.fitness <= 0.0:
                                    if encoded_testcase.muti_fitness == {}:
                                        encoded_testcase.compute_muti_fitness()
                                    # population.append(encoded_testcase)
                                    monitor = Monitor(output_trace, 0)
                                    for spec in remaining_sub_violations:                                  
                                        fitness0 = monitor.continuous_monitor2(spec)                                                                       
                                        if fitness0 >= 0.0:
                                            covered.append(spec)
                                            # logging.info("Coverage rate is: {}/{}, Covered Predicates are: {}".format(len(coverage_statement), len(all_predicates), coverage_statement))
                                            with open(directory + '/improvedTestCase.txt', 'a') as bug_file:
                                                now = datetime.now()
                                                dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
                                                string_index = "Time:" + dt_string + "Generation: " + str(generation) + ", Individual: " + str(j + 1) +'\n'
                                                bug_file.write(string_index)
                                                string_index2 = "The detailed fitness values:" + str(encoded_testcase.muti_fitness) + '\n'
                                                bug_file.write(string_index2)
                                                coverage_rate = 1- len(remaining_sub_violations) / maximun
                                                string_index3 = "total coverage rate: {}/{} = {}, new covered predicates: {}\n".format((maximun - len(remaining_sub_violations)), maximun, coverage_rate, spec)
                                                # bug_file.write(spec)
                                                json.dump(output_trace, bug_file, indent=2)
                                                bug_file.write('\n')                                           
                                        else:
                                            if mapping[spec] < fitness0:
                                                seed[spec] = encoded_testcase
                                                mapping[spec] = fitness0
                                    for itme in covered:
                                        remaining_sub_violations.remove(itme)
                                        del seed[itme]
                                        del mapping[itme]
                                # covered = []
                                else:
                                    logging.info("      Fitness Value: {}".format(encoded_testcase.fitness))
                                    monitor = Monitor(output_trace, 0)
                                    for spec in remaining_sub_violations:                                  
                                        fitness0 = monitor.continuous_monitor2(spec)  
                                        assert fitness0 < 0.0                                                                   
                                        if fitness0 >= 0.0:
                                            covered.append(spec)
                                            # logging.info("Coverage rate is: {}/{}, Covered Predicates are: {}".format(len(coverage_statement), len(all_predicates), coverage_statement))
                                            with open(directory + '/improvedTestCase.txt', 'a') as bug_file:
                                                now = datetime.now()
                                                dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
                                                string_index = "Time:" + dt_string + "Generation: " + str(generation) + ", Individual: " + str(j + 1) +'\n'
                                                bug_file.write(string_index)
                                                string_index2 = "The detailed fitness values:" + str(encoded_testcase.muti_fitness) + '\n'
                                                bug_file.write(string_index2)
                                                coverage_rate = 1- len(remaining_sub_violations) / maximun
                                                string_index3 = "total coverage rate: {}/{} = {}, new covered predicates: {}\n".format((maximun - len(remaining_sub_violations)), maximun, coverage_rate, spec)
                                                bug_file.write(string_index3)
                                                # bug_file.write(spec)
                                                json.dump(output_trace, bug_file, indent=2)
                                        #         bug_file.write('\n')                                           
                                        else:
                                            if mapping[spec] < fitness0:
                                                seed[spec] = encoded_testcase
                                                mapping[spec] = fitness0
                                    for itme in covered:
                                        remaining_sub_violations.remove(itme)
                                        del seed[itme]
                                        del mapping[itme]
                                del encoded_testcase.trace 
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
                coverage_rate = 1- len(remaining_sub_violations) / maximun
                logging.info("total coverage rate: {}/{} = {}, covered predicates: {}\n".format((maximun - len(remaining_sub_violations)), maximun, coverage_rate, remaining_sub_violations))



def spec_scenario(spec, testcase, generations=0, pop_size=1, file_directory=None):
    loop = asyncio.get_event_loop()
    scenario_specification = copy.deepcopy(spec)
    scenario_testcase = copy.deepcopy(testcase)
    msgs = [scenario_testcase]
    loop.run_until_complete(
        asyncio.gather(hello(msgs, scenario_specification, generation_number=generations, population_size=pop_size,
                             directory=file_directory)))



def test_scenario(direct, item):
    file = direct + item

    log_direct ='Embed_Law_Into_Apollo-AFTER57-1/' + Path(item).stem
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
                spec_scenario(spec=single_specification, testcase=test_case, generations=20, pop_size=20, file_directory=log_direct)
                # print(testcase)
        except KeyError:
            spec_scenario(spec={}, testcase=test_case)


if __name__ == "__main__":
    # arr = ['Intersection_with_Single-Direction_Roads.txt', 'lane_change_in_the_same_road.txt', 'Intersection_with_Double-Direction_Roads.txt']
    direct = 'test_cases/traffic_rule_tests/'
    # direct = 'test_cases/Violations/'
    arr = ['lane_change_in_the_same_road.txt', 'Intersection_with_Double-Direction_Roads.txt', 'Single-Direction-1.txt']
    # 'Single-Direction-1.txt', 'lane_change-1.txt', 'Double-Direction-1.txt']
    # arr = ['Intersection_with_Double-Direction_Roads.txt', \
    # 'lane_change-1.txt', 'Double-Direction-1.txt']
    # arr = ['stuck1.txt']
    # arr = ['Intersection_with_Double-Direction_Roads.txt']
    for item in arr:
        test_scenario(direct, item)

