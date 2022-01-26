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

import logging

# logging.basicConfig(level=level, handlers=[stdout_handler, file_handler],format='%(asctime)s, %(levelname)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.FileHandler('test.log', 'a'))
# logger.addHandler(logging.StreamHandler(sys.stdout))




min_fitness_list = []
ave_fitness_list = []


def to_json(obj):
    return json.dumps(obj, default=lambda o: o.__dict__, indent=4)



async def hello(scenario_msg, single_spec, generation_number=1, population_size=3, directory=None) -> object:
    uri = "ws://localhost:8000"
    async with websockets.connect(uri,  max_size= 300000000, ping_interval=None) as websocket:
        scenario_no = len(scenario_msg)
        init_msg = json.dumps({'CMD': "CMD_READY_FOR_NEW_TEST"})
        await websocket.send(init_msg)
        # for i in range(scenario_no):
        # logging.info('iteration: {}'.format(i))
        msg = await websocket.recv()
        msg = json.loads(msg)
        if msg['TYPE'] == 'READY_FOR_NEW_TEST' and msg['DATA']:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            with open(directory + '/Incompleted.txt', 'a') as f:
                f.write('Time: {} \n'.format(dt_string))
            with open(directory + '/bugTestCase.txt', 'a') as f:
                f.write('Time: {} \n'.format(dt_string))
            with open(directory + '/exceptionTestCase.txt', 'a') as f:
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
                            logging.info("      Fitness Value: {}".format(encoded_testcase.fitness))
                            del encoded_testcase.trace
                            if encoded_testcase.fitness <= 0.0:
                                with open(directory + '/bugTestCase.txt', 'a') as bug_file:
                                    string_index2 = "The detailed fitness values:" + str(encoded_testcase.muti_fitness) + '\n'
                                    bug_file.write(string_index2)
                                    json.dump(output_trace, bug_file, indent=2)
                                    bug_file.write('\n')                                   
                            population.append(encoded_testcase)
                            if output_trace["testFailures"]!= []: 
                                with open(directory + '/exceptionTestCase.txt', 'a') as bug_file:
                                    now = datetime.now()
                                    dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
                                    string_index = "Time:" + dt_string + "Generation: " + str(0) + ", Individual: " + str(0) +", Bug: " + str(output_trace["testFailures"]) +'\n'
                                    bug_file.write(string_index)
                                    json.dump(output_trace, bug_file, indent=2)
                                    bug_file.write('\n')
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
                    # while True:
                    #     msg_valid = await websocket.recv()
                    #     msg_valid = json.loads(msg_valid)
                    #     # print("Received Message: " + msg_valid['TYPE'])
                    #     # if msg_valid['TYPE'] == 'ERROR' or 'TEST_STARTED':
                    #     #     print(msg_valid)
                    #     if msg_valid['TYPE'] == 'TEST_TERMINATED' or msg_valid['TYPE'] == 'ERROR':
                    #         print("Try to reconnect!")
                    #         init_msg = json.dumps({'CMD': "CMD_READY_FOR_NEW_TEST"})
                    #         await websocket.send(init_msg)
                    #         time.sleep(3)
                    #         msg = await websocket.recv()
                    #         msg = json.loads(msg)
                    #         if msg['TYPE'] == 'READY_FOR_NEW_TEST' and msg['DATA']:
                    #             send_msg = {'CMD': "CMD_NEW_TEST", 'DATA': scenario_msg[i]}
                    #             await websocket.send(json.dumps(send_msg))
                    #         continue
                    #     elif msg_valid['TYPE'] == 'TEST_COMPLETED':
                    #         output_trace = msg_valid['DATA']
                    #         now = datetime.now()
                    #         dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
                    #         file = directory + '/data/result' + dt_string + '.json'
                    #         with open(file, 'w') as outfile:
                    #             json.dump(output_trace, outfile, indent=2)
                    #         if not output_trace['destinationReached']:
                    #             logging.info("Not reach the destination")
                    #             with open(directory + '/Incompleted.txt', 'a') as f:
                    #                 json.dump(scenario_msg[i], f, indent=2)
                    #                 f.write('\n')
                    #         if len(output_trace['trace']) > 1:
                    #             encoded_testcase = EncodedTestCase(output_trace, single_spec)
                    #             logging.info("      Fitness Value: {}".format(encoded_testcase.fitness))
                    #             del encoded_testcase.trace
                    #             if encoded_testcase.fitness < 0.0:
                    #                 with open(directory + '/bugTestCase.txt', 'a') as bug_file:
                    #                     json.dump(output_trace, bug_file, indent=2)
                    #                     bug_file.write('\n')
                    #             population.append(encoded_testcase)
                    #         elif len(output_trace['trace']) == 1:
                    #             logging.info("Is reached: {}, minimal distance: {}".format(output_trace['destinationReached'], output_trace['minEgoObsDist']))
                    #             testcase = TestCaseRandom(output_trace)
                    #             testcase.testcase_random(1)
                    #             new_testcases.append(testcase.cases[-1])
                    #         else:
                    #             logging.info("No trace for the test cases")
                    #             with open(directory + '/NoTrace.txt', 'a') as f:
                    #                 json.dump(scenario_msg[i], f, indent=2)
                    #                 f.write('\n')
                    #             testcase = TestCaseRandom(output_trace)
                    #             testcase.testcase_random(1)
                    #             new_testcases.append(testcase.cases[-1])
                    #         init_msg = json.dumps({'CMD': "CMD_READY_FOR_NEW_TEST"})
                    #         await websocket.send(init_msg)
                    #         break
            # new_population_obj = ga.GAGeneration(population)
            if generation_number:
                if len(population):
                    decoder = DecodedTestCase(population)
                    new_testcases = decoder.decoding()

                if len(new_testcases) < population_size:
                    testcase = TestCaseRandom(output_trace)
                    testcase.testcase_random(population_size - scenario_no)
                    for i2 in range(len(testcase.cases) - 1):
                        new_testcases.append(testcase.cases[i2 + 1])
                with open(directory + '/TestCase.txt', 'w') as outfile:
                    for i1 in range(len(new_testcases)):
                        json.dump(new_testcases[i1], outfile, indent=2)
                        outfile.write('\n')
            # Begin GA
                for generation in range(generation_number):
                    generation_fitness = float('inf')
                    ave_fitness = 0
                    if len(new_testcases) < population_size:
                        logging.info('Test case decreases')
                    population = []
                    next_new_testcases = []
                    for j in range(len(new_testcases)):
                        # deal with each test case
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
                                    asyncio.sleep(3)
                                    init_msg = json.dumps({'CMD': "CMD_READY_FOR_NEW_TEST"})
                                    await websocket.send(init_msg)
                            elif msg['TYPE'] == 'TEST_TERMINATED' or msg['TYPE'] == 'ERROR':
                                print(msg)
                                print("Try to reconnect.")
                                asyncio.sleep(3)
                                init_msg = json.dumps({'CMD': "CMD_READY_FOR_NEW_TEST"})
                                await websocket.send(init_msg)
                            elif msg['TYPE'] == 'KEEP_SERVER_AND_CLIENT_ALIVE':
                                send_msg = {'CMD': "KEEP_SERVER_AND_CLIENT_ALIVE", 'DATA': None}
                                await websocket.send(json.dumps(send_msg))
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
                                    logging.info("      Fitness Value: {}".format(encoded_testcase.fitness))
                                    ave_fitness += encoded_testcase.fitness
                                    if encoded_testcase.fitness < generation_fitness:
                                        generation_fitness = encoded_testcase.fitness
                                    del encoded_testcase.trace
                                    if encoded_testcase.fitness <= 0.0:
                                        with open(directory + '/bugTestCase.txt', 'a') as bug_file:
                                            now = datetime.now()
                                            dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
                                            string_index = "Time:" + dt_string + "Generation: " + str(generation) + ", Individual: " + str(j+1) + '\n'
                                            bug_file.write(string_index)
                                            string_index2 = "The detailed fitness values:" + str(encoded_testcase.muti_fitness) + '\n'
                                            bug_file.write(string_index2)
                                            json.dump(output_trace, bug_file, indent=2)
                                            bug_file.write('\n')
                                    population.append(encoded_testcase)
                                    if output_trace["testFailures"]!= []: 
                                        with open(directory + '/exceptionTestCase.txt', 'a') as bug_file:
                                            now = datetime.now()
                                            dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
                                            string_index = "Time:" + dt_string + "Generation: " + str(generation) + ", Individual: " + str(j+1) +", Bug: " + str(output_trace["testFailures"]) +'\n'
                                            bug_file.write(string_index)
                                            json.dump(output_trace, bug_file, indent=2)
                                            bug_file.write('\n')
                                elif len(output_trace['trace']) == 1:
                                    logging.info("Only one state. Is reached: {}, minimal distance: {}".format(output_trace['destinationReached'], output_trace['minEgoObsDist']))
                                    testcase = TestCaseRandom(output_trace)
                                    testcase.testcase_random(1)
                                    next_new_testcases.append(testcase.cases[-1])
                                else:
                                    testcase = TestCaseRandom(output_trace)
                                    testcase.testcase_random(1)
                                    next_new_testcases.append(testcase.cases[-1])
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
                        # logging.info('Running Generation: {}, Individual: {}'.format(generation, j+1))
                        # send_msg = {'CMD': "CMD_NEW_TEST", 'DATA': new_testcases[j]}
                        # await websocket.send(json.dumps(send_msg))
                        # while True:
                        #     msg_valid = await websocket.recv()
                        #     msg_valid = json.loads(msg_valid)
                        #     # print("Received Message: " + msg_valid['TYPE'])
                        #     # if msg_valid['TYPE'] == 'ERROR' or 'TEST_STARTED':
                        #     #     print(msg_valid)
                        #     if msg_valid['TYPE'] == 'TEST_TERMINATED' or msg_valid['TYPE'] == 'ERROR':
                        #         print(msg_valid)
                        #         print("Try to reconnect.")
                        #         time.sleep(3)
                        #         init_msg = json.dumps({'CMD': "CMD_READY_FOR_NEW_TEST"})
                        #         await websocket.send(init_msg)
                        #         msg = await websocket.recv()
                        #         msg = json.loads(msg)
                        #         if msg['TYPE'] == 'READY_FOR_NEW_TEST' and msg['DATA']:
                        #             send_msg = {'CMD': "CMD_NEW_TEST", 'DATA': new_testcases[j]}
                        #             await websocket.send(json.dumps(send_msg))
                        #         continue
                        #     elif msg_valid['TYPE'] == 'TEST_COMPLETED':
                        #         output_trace = msg_valid['DATA']
                        #         now = datetime.now()
                        #         dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
                        #         file = directory + '/data/result' + dt_string + '.json'
                        #         with open(file, 'w') as outfile:
                        #             json.dump(output_trace, outfile, indent=2)
                        #         logging.info("The number of states in the trace is {}".format(len(output_trace['trace'])))
                        #         if not output_trace['destinationReached']:
                        #             with open(directory + '/Incompleted.txt', 'a') as f:
                        #                 json.dump(new_testcases[j], f, indent=2)
                        #                 f.write('\n')
                        #         if len(output_trace['trace']) > 1:
                        #             encoded_testcase = EncodedTestCase(output_trace, single_spec)
                        #             logging.info("      Fitness Value: {}".format(encoded_testcase.fitness))
                        #             ave_fitness += encoded_testcase.fitness
                        #             if encoded_testcase.fitness < generation_fitness:
                        #                 generation_fitness = encoded_testcase.fitness
                        #             del encoded_testcase.trace
                        #             if encoded_testcase.fitness < 0.0:
                        #                 with open(directory + '/bugTestCase.txt', 'a') as bug_file:
                        #                     now = datetime.now()
                        #                     dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
                        #                     string_index = "Time:" + dt_string + "Generation: " + str(generation) + ", Individual: " + str(j+1) + '\n'
                        #                     bug_file.write(string_index)
                        #                     json.dump(output_trace, bug_file, indent=2)
                        #                     bug_file.write('\n')
                        #             population.append(encoded_testcase)
                        #         elif len(output_trace['trace']) == 1:
                        #             logging.info("Only one state. Is reached: {}, minimal distance: {}".format(output_trace['destinationReached'], output_trace['minEgoObsDist']))
                        #             testcase = TestCaseRandom(output_trace)
                        #             testcase.testcase_random(1)
                        #             next_new_testcases.append(testcase.cases[-1])
                        #         else:
                        #             testcase = TestCaseRandom(output_trace)
                        #             testcase.testcase_random(1)
                        #             next_new_testcases.append(testcase.cases[-1])
                        #             logging.info("No trace for the test cases!")
                        #             with open(directory + '/NoTrace.txt', 'a') as f:
                        #                 now = datetime.now()
                        #                 dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
                        #                 f.write("Time: Generation: {}, Individual: {}".format(dt_string, generation, j))
                        #                 json.dump(new_testcases[j], f, indent=2)
                        #                 f.write('\n')
                        #         break
                    min_fitness_list.append(generation_fitness)
                    ave_fitness_list.append(ave_fitness/population_size)
                    logging.info("The minimal fitness in generation {} is {}.".format(generation, generation_fitness))
                    logging.info("The average fitness in generation {} is {}.".format(generation, ave_fitness/population_size))
                    if len(population):
                        new_population_obj = GAGeneration(population)
                        new_population = new_population_obj.one_generation()
                        decoder = DecodedTestCase(new_population)
                        ga_new_testcases = decoder.decoding()
                        next_new_testcases.extend(ga_new_testcases)
                    new_testcases = copy.deepcopy(next_new_testcases)
                    with open(directory + '/TestCase.txt', 'a') as outfile:
                        for i in range(len(new_testcases)):
                            try:
                                json.dump(new_testcases[i], outfile, indent=2)
                                outfile.write('\n')
                            except TypeError:
                                logging.info("Check the types of test cases")
            #  The last generation
                ave_fitness = 0
                generation_fitness = float('inf')
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
                                asyncio.sleep(3)
                                init_msg = json.dumps({'CMD': "CMD_READY_FOR_NEW_TEST"})
                                await websocket.send(init_msg)
                        elif msg['TYPE'] == 'TEST_TERMINATED' or msg['TYPE'] == 'ERROR':
                            print(msg)
                            print("Try to reconnect.")
                            asyncio.sleep(3)
                            init_msg = json.dumps({'CMD': "CMD_READY_FOR_NEW_TEST"})
                            await websocket.send(init_msg)
                        elif msg['TYPE'] == 'KEEP_SERVER_AND_CLIENT_ALIVE':
                            send_msg = {'CMD': "KEEP_SERVER_AND_CLIENT_ALIVE", 'DATA': None}
                            await websocket.send(json.dumps(send_msg))
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
                                logging.info("      Fitness Value: {}".format(encoded_testcase.fitness))
                                ave_fitness += encoded_testcase.fitness
                                if encoded_testcase.fitness < generation_fitness:
                                    generation_fitness = encoded_testcase.fitness
                                del encoded_testcase.trace
                                if encoded_testcase.fitness <= 0.0:
                                    with open(directory + '/bugTestCase.txt', 'a') as bug_file:
                                        now = datetime.now()
                                        dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
                                        string_index = "Time:" + dt_string + "Generation: " + str(
                                            generation) + ", Individual: " + str(j + 1) + '\n'
                                        bug_file.write(string_index)
                                        string_index2 = "The detailed fitness values:" + str(encoded_testcase.muti_fitness) + '\n'
                                        bug_file.write(string_index2)
                                        json.dump(output_trace, bug_file, indent=2)
                                        bug_file.write('\n')
                                population.append(encoded_testcase)
                                if output_trace["testFailures"]!= []: 
                                    with open(directory + '/exceptionTestCase.txt', 'a') as bug_file:
                                        now = datetime.now()
                                        dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
                                        string_index = "Time:" + dt_string + "Generation: " + str("last") + ", Individual: " + str(j+1) +", Bug: " + str(output_trace["testFailures"]) +'\n'
                                        bug_file.write(string_index)
                                        json.dump(output_trace, bug_file, indent=2)
                                        bug_file.write('\n')
                            elif len(output_trace['trace']) == 1:
                                logging.info("Only one state. Is reached: {}, minimal distance: {}".format(
                                    output_trace['destinationReached'], output_trace['minEgoObsDist']))
                                testcase = TestCaseRandom(output_trace)
                                testcase.testcase_random(1)
                                next_new_testcases.append(testcase.cases[-1])
                            else:
                                testcase = TestCaseRandom(output_trace)
                                testcase.testcase_random(1)
                                next_new_testcases.append(testcase.cases[-1])
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
                    # logging.info('Generation: {}, Individual: {}'.format(generation + 1, j+1))
                    # send_msg = {'CMD': "CMD_NEW_TEST", 'DATA': new_testcases[j]}
                    # await websocket.send(json.dumps(send_msg))
                    # while True:
                    #     msg_valid = await websocket.recv()
                    #     msg_valid = json.loads(msg_valid)
                    #     # print("Received Message: " + msg_valid['TYPE'])
                    #     # if msg_valid['TYPE'] == 'ERROR' or 'TEST_STARTED':
                    #     #     print(msg_valid)
                    #     if msg_valid['TYPE'] == 'TEST_TERMINATED' or msg_valid['TYPE'] == 'ERROR':
                    #         print("Try to reconnect!")
                    #         time.sleep(3)
                    #         init_msg = json.dumps({'CMD': "CMD_READY_FOR_NEW_TEST"})
                    #         await websocket.send(init_msg)
                    #         msg = await websocket.recv()
                    #         msg = json.loads(msg)
                    #         if msg['TYPE'] == 'READY_FOR_NEW_TEST' and msg['DATA']:
                    #             send_msg = {'CMD': "CMD_NEW_TEST", 'DATA': new_testcases[j]}
                    #             await websocket.send(json.dumps(send_msg))
                    #         continue
                    #     elif msg_valid['TYPE'] == 'TEST_COMPLETED':
                    #         output_trace = msg_valid['DATA']
                    #         now = datetime.now()
                    #         dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
                    #         file = directory + '/data/result' + dt_string + '.json'
                    #         with open(file, 'w') as outfile:
                    #             json.dump(output_trace, outfile, indent=2)
                    #         if not output_trace['destinationReached']:
                    #             with open(directory + '/Incompleted.txt', 'a') as f:
                    #                 json.dump(new_testcases[j], f, indent=2)
                    #                 f.write('\n')
                    #         if len(output_trace['trace']) > 1:
                    #             encoded_testcase = EncodedTestCase(output_trace, single_spec)
                    #             logging.info("      Fitness Value: {}".format(encoded_testcase.fitness))
                    #             if encoded_testcase.fitness < generation_fitness:
                    #                 generation_fitness = encoded_testcase.fitness
                    #             del encoded_testcase.trace
                    #             ave_fitness += encoded_testcase.fitness
                    #             if encoded_testcase.fitness < 0.0:
                    #                 with open(directory + '/bugTestCase.txt', 'a') as bug_file:
                    #                     string_index = "Generation: " + str(generation + 1) + ", Individual: " + str(j+1) + '\n'
                    #                     bug_file.write(string_index)
                    #                     json.dump(output_trace, bug_file, indent=2)
                    #                     bug_file.write('\n')
                    #         elif len(output_trace['trace']) == 1:
                    #             logging.info("Is reached: {}, minimal distance: {}".format(output_trace['destinationReached'], output_trace['minEgoObsDist']))
                    #         else:
                    #             logging.info("No trace for the test cases!")
                    #             with open(directory + '/NoTrace.txt', 'a') as f:
                    #                 json.dump(new_testcases[j], f, indent=2)
                    #                 f.write('\n')
                    #         break
                min_fitness_list.append(generation_fitness)
                ave_fitness_list.append(ave_fitness/population_size)
                logging.info("The minimal fitness for the last generation is {}.".format(generation_fitness))
                logging.info("The average fitness for the last generation is {}.".format(ave_fitness/population_size))
                # logging.info("Minimal fitness: {}".format(min_fitness_list))
                # logging.info("Average fitness: {}".format(ave_fitness_list))


def spec_scenario(spec, testcase, generations=0, pop_size=1,file_directory=None):
    loop = asyncio.get_event_loop()
    scenario_specification = copy.deepcopy(spec)
    scenario_testcase = copy.deepcopy(testcase)
    msgs = [scenario_testcase]
    # scenario_specification = 0
    with open(file_directory + '/InitTestCase.txt', 'w') as f:
        json.dump(scenario_testcase, f, indent=2)
    loop.run_until_complete(
        asyncio.gather(hello(msgs, scenario_specification, generation_number=generations, population_size=pop_size, directory=file_directory)))


def test_scenario(direct, item, scenario_spec):
    file = direct + item
    # file0 = FileStream(file)
    with open(file) as json_file:
        file0 = json.load(json_file)

    log_direct = 'bugs/' + Path(item).stem
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
    # isGroundTruth = True
    # extracted_data = ExtractAll(file, isGroundTruth)
    # testcases = extracted_data.Get_TestCastINJsonList()
    # all_specifications = extracted_data.Get_Specifications()
    # maps = extracted_data.Get_AllMaps()

    test_case = file0
    scenario_name = test_case['ScenarioName']
        # logging.info("Current scenario is {}.\n".format(scenario_name))
    try:
        specifications_in_scenario = scenario_spec[scenario_name]
        current_map = "san_francisco"
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
            # single_spec = SingleAssertion(scenario_spec[scenario_name][0], "san_francisco")
            # single_specification = single_spec
            spec_scenario(spec=single_specification, testcase=test_case,generations=0, pop_size=2, file_directory=log_direct)
    except KeyError:
        spec_scenario(spec={}, testcase=test_case)



if __name__ == "__main__":
    input_file = 'input-test.txt'
    # input_file = 'test_cases/final/intersection2.txt'
    # # input_file = 'test_cases/intersection/intersection1.txt'
    isGroundTruth = True
    extracted_script = ExtractAll(input_file,isGroundTruth)
    scenario_spec = extracted_script.Get_Specifications()
    # single_spec = SingleAssertion(scenario_spec[scenario_name][0], "san_francisco")

    direct = 'rerun_for_videos/'
    item = 'test.json'
    test_scenario(direct, item, scenario_spec)




