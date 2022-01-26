import copy

import websockets
import json
import asyncio
from EXtraction import ExtractAll
from GeneticAlgorithm import GAGeneration, EncodedTestCase, DecodedTestCase
from TestCaseRandom import TestCaseRandom
from datetime import datetime
from AssertionExtraction import SingleAssertion
from map import get_map_info

min_fitness_list = []
ave_fitness_list = []


def to_json(obj):
    return json.dumps(obj, default=lambda o: o.__dict__, indent=4)


async def fuzzing(scenario_msg, single_spec, generation_number=1, population_size=3) -> object:
    uri = "ws://localhost:8000"
    async with websockets.connect(uri, max_size= 300000000) as websocket:
        scenario_no = len(scenario_msg)
        # print(scenario_msg)
        init_msg = json.dumps({'CMD': "CMD_READY_FOR_NEW_TEST"})
        
        # print(init_msg)
        await websocket.send(init_msg)

        # print('0')
        # for i in range(scenario_no):
        # print('iteration: {}'.format(i))
        msg = await websocket.recv()
        # print('1')
        # print(msg)

        msg = json.loads(msg)

        # print(msg['TYPE'])
        # while True:
        #     msg = await websocket.recv()
        #     msg = json.loads(msg)
        #     if msg['TYPE'] == 'READY_FOR_NEW_TEST' and msg['DATA']:
        #         break
        if msg['TYPE'] == 'READY_FOR_NEW_TEST' and msg['DATA']:
            # print('!!!!!!!!!!!')

            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            with open('log/Incompleted.txt', 'a') as f:
                f.write('Time: {} \n'.format(dt_string))
            with open('log/bugTestCase.txt', 'a') as f:
                f.write('Time: {} \n'.format(dt_string))
            with open('log/NoTrace.txt', 'a') as f:
                f.write('Time: {} \n'.format(dt_string))
            population = []
            new_testcases = []
            for i in range(scenario_no):
                print('Running Predefined Test Case: {}'.format(i))
                send_msg = {'CMD': "CMD_NEW_TEST", 'DATA': scenario_msg[i]}
                await websocket.send(json.dumps(send_msg))
                print('Send success, wait for response')
                while True:
                    msg_valid = await websocket.recv()
                    msg_valid = json.loads(msg_valid)
                    # print('???????')

                    if msg_valid['TYPE'] == 'TEST_COMPLETED':
                        output_trace = msg_valid['DATA']
                        now = datetime.now()
                        dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
                        file = 'data/result' + dt_string + '.json'
                        with open(file, 'w') as outfile:
                            json.dump(output_trace, outfile, indent=2)
                        if not output_trace['destinationReached']:
                            print("Not reach the destination")
                            with open('log/Incompleted.txt', 'a') as f:
                                json.dump(scenario_msg[i], f, indent=2)
                                f.write('\n')
                        if len(output_trace['trace']) > 1:
                            encoded_testcase = EncodedTestCase(output_trace, single_spec)
                            print("      Fitness Value: {}".format(encoded_testcase.fitness))
                            del encoded_testcase.trace
                            if encoded_testcase.fitness < 0.0:
                                with open('log/bugTestCase.txt', 'a') as bug_file:
                                    json.dump(output_trace, bug_file, indent=2)
                                    bug_file.write('\n')
                            population.append(encoded_testcase)
                        elif len(output_trace['trace']) == 1:
                            print("Is reached: {}, minimal distance: {}".format(output_trace['destinationReached'], output_trace['minEgoObsDist']))
                            testcase = TestCaseRandom(output_trace)
                            testcase.testcase_random(1)
                            new_testcases.append(testcase.cases[-1])
                        else:
                            print("No trace for the test cases")
                            with open('log/NoTrace.txt', 'a') as f:
                                json.dump(scenario_msg[i], f, indent=2)
                                f.write('\n')
                            testcase = TestCaseRandom(output_trace)
                            testcase.testcase_random(1)
                            new_testcases.append(testcase.cases[-1])
                        break
                    elif msg_valid['TYPE'] == 'KEEP_SERVER_AND_CLIENT_ALIVE':
                        send_msg = {'CMD': "KEEP_SERVER_AND_CLIENT_ALIVE", 'DATA': None}
                        await websocket.send(json.dumps(send_msg))
                    else:
                        print("Server return unexpected message! Opps!")
                    #     pass
                        # send_msg = {'CMD': "CMD_NEW_TEST", 'DATA': scenario_msg[i]}
                        # await websocket.send(json.dumps(send_msg))
                        # msg_valid = await websocket.recv()
                        # msg_valid = json.loads(msg_valid)
            # new_population_obj = ga.GAGeneration(population)
            if len(population):
                decoder = DecodedTestCase(population)
                new_testcases = decoder.decoding()

            if len(new_testcases) < population_size:
                testcase = TestCaseRandom(output_trace)
                testcase.testcase_random(population_size - scenario_no)
                for i2 in range(len(testcase.cases) - 1):
                    new_testcases.append(testcase.cases[i2 + 1])
            with open('log/TestCase.txt', 'w') as outfile:
                for i1 in range(len(new_testcases)):
                    json.dump(new_testcases[i1], outfile, indent=2)
               

            if generation_number:
                # Begin GA
                generation = 0
                for generation in range(generation_number):
                    generation_fitness = float('inf')
                    ave_fitness = 0
                    if len(new_testcases) < population_size:
                        print('Test case decreases')
                    population = []
                    next_new_testcases = []
                    for j in range(len(new_testcases)):
                        print('Running Generation: {}, Individual: {}'.format(generation, j+1))
                        send_msg = {'CMD': "CMD_NEW_TEST", 'DATA': new_testcases[j]}
                        await websocket.send(json.dumps(send_msg))
                        while True:
                            msg_valid = await websocket.recv()
                            msg_valid = json.loads(msg_valid)
                            if msg_valid['TYPE'] == 'TEST_COMPLETED':
                                output_trace = msg_valid['DATA']
                                now = datetime.now()
                                dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
                                file = 'data/result' + dt_string + '.json'
                                with open(file, 'w') as outfile:
                                    json.dump(output_trace, outfile, indent=2)
                                print("The number of states in the trace is {}".format(len(output_trace['trace'])))
                                if not output_trace['destinationReached']:
                                    with open('log/Incompleted.txt', 'a') as f:
                                        json.dump(new_testcases[j], f, indent=2)
                                        f.write('\n')
                                if len(output_trace['trace']) > 1:
                                    encoded_testcase = EncodedTestCase(output_trace, single_spec)
                                    print("      Fitness Value: {}".format(encoded_testcase.fitness))
                                    ave_fitness += encoded_testcase.fitness
                                    if encoded_testcase.fitness < generation_fitness:
                                        generation_fitness = encoded_testcase.fitness
                                    del encoded_testcase.trace
                                    if encoded_testcase.fitness < 0.0:
                                        with open('log/bugTestCase.txt', 'a') as bug_file:
                                            string_index = "Generation: " + str(generation) + ", Individual: " + str(j+1) + '\n'
                                            bug_file.write(string_index)
                                            json.dump(output_trace, bug_file, indent=2)
                                            bug_file.write('\n')
                                    population.append(encoded_testcase)
                                elif len(output_trace['trace']) == 1:
                                    print("Only one state. Is reached: {}, minimal distance: {}".format(output_trace['destinationReached'], output_trace['minEgoObsDist']))
                                    testcase = TestCaseRandom(output_trace)
                                    testcase.testcase_random(1)
                                    next_new_testcases.append(testcase.cases[-1])
                                else:
                                    testcase = TestCaseRandom(output_trace)
                                    testcase.testcase_random(1)
                                    next_new_testcases.append(testcase.cases[-1])
                                    print("No trace for the test cases!")
                                    with open('log/NoTrace.txt', 'a') as f:
                                        f.write("Generation: {}, Individual: {}".format(generation, j))
                                        json.dump(new_testcases[j], f, indent=2)
                                        f.write('\n')
                                break
                            elif msg_valid['TYPE'] == 'KEEP_SERVER_AND_CLIENT_ALIVE':
                                send_msg = {'CMD': "KEEP_SERVER_AND_CLIENT_ALIVE", 'DATA': None}
                                await websocket.send(json.dumps(send_msg))
                            else:
                                print("Server return unexpected message! Opps!")
                    min_fitness_list.append(generation_fitness)
                    ave_fitness_list.append(ave_fitness/population_size)
                    print("The minimal fitness in generation {} is {}.".format(generation, generation_fitness))
                    print("The average fitness in generation {} is {}.".format(generation, ave_fitness/population_size))
                    if len(population):
                        new_population_obj = GAGeneration(population)
                        new_population = new_population_obj.one_generation()
                        decoder = DecodedTestCase(new_population)
                        ga_new_testcases = decoder.decoding()
                        next_new_testcases.extend(ga_new_testcases)
                    new_testcases = copy.deepcopy(next_new_testcases)
                    with open('log/TestCase.txt', 'a') as outfile:
                        for i in range(len(new_testcases)):
                            try:
                                json.dump(new_testcases[i], outfile, indent=2)
                                outfile.write('\n')
                            except TypeError:
                                print("Check the types of test cases")
                #  The last generation
                ave_fitness = 0
                for j in range(len(new_testcases)):
                    generation_fitness = float('inf')
                    print('Generation: {}, Individual: {}'.format(generation + 1, j+1))
                    send_msg = {'CMD': "CMD_NEW_TEST", 'DATA': new_testcases[j]}
                    await websocket.send(json.dumps(send_msg))
                    while True:
                        msg_valid = await websocket.recv()
                        msg_valid = json.loads(msg_valid)
                        if msg_valid['TYPE'] == 'TEST_COMPLETED':
                            output_trace = msg_valid['DATA']
                            now = datetime.now()
                            dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
                            file = 'data/result' + dt_string + '.json'
                            with open(file, 'w') as outfile:
                                json.dump(output_trace, outfile, indent=2)
                            if not output_trace['destinationReached']:
                                with open('log/Incompleted.txt', 'a') as f:
                                    json.dump(new_testcases[j], f, indent=2)
                                    f.write('\n')
                            if len(output_trace['trace']) > 1:
                                encoded_testcase = EncodedTestCase(output_trace, single_spec)
                                print("      Fitness Value: {}".format(encoded_testcase.fitness))
                                if encoded_testcase.fitness < generation_fitness:
                                    generation_fitness = encoded_testcase.fitness
                                del encoded_testcase.trace
                                ave_fitness += encoded_testcase.fitness
                                if encoded_testcase.fitness < 0.0:
                                    with open('log/bugTestCase.txt', 'a') as bug_file:
                                        string_index = "Generation: " + str(generation + 1) + ", Individual: " + str(j+1) + '\n'
                                        bug_file.write(string_index)
                                        json.dump(output_trace, bug_file, indent=2)
                                        bug_file.write('\n')
                            elif len(output_trace['trace']) == 1:
                                print("Is reached: {}, minimal distance: {}".format(output_trace['destinationReached'], output_trace['minEgoObsDist']))
                            else:
                                print("No trace for the test cases!")
                                with open('log/NoTrace.txt', 'a') as f:
                                    json.dump(new_testcases[j], f, indent=2)
                                    f.write('\n')
                            break
                        elif msg_valid['TYPE'] == 'KEEP_SERVER_AND_CLIENT_ALIVE':
                            send_msg = {'CMD': "KEEP_SERVER_AND_CLIENT_ALIVE", 'DATA': None}
                            await websocket.send(json.dumps(send_msg))
                        else:
                            print("Server return unexpected message! Opps!")
                min_fitness_list.append(generation_fitness)
                ave_fitness_list.append(ave_fitness/population_size)
                print("The minimal fitness for the last generation is {}.".format(generation_fitness))
                print("The average fitness for the last generation is {}.".format(generation, ave_fitness/population_size))
                print("Minimal fitness: {}".format(min_fitness_list))
                print("Average fitness: {}".format(ave_fitness_list))

            # for generation in range(3):
            #     new_population_obj = ga.GAGeneration(population)
            #     new_testcases = new_population_obj.decoding()
            #     for j in range(len(new_testcases)):
            #         print(new_testcases[j])

            # if msg_valid['TYPE'] == 'TEST' and msg_valid['DATA'] == 'COMPLETED':
            #     break
            # elif msg_valid['TYPE'] == 'TEST_COMPLETED':
            #     break

            # with open('scenario_test.json') as f:
            #     data = json.load(f)
            #     print(data)
            #     print(type(data))
            #     send_msg = {'CMD': "CMD_NEW_TEST", 'DATA': data}
            #     await websocket.send(json.dumps(send_msg))
            #     while True:
            #         msg_valid = await websocket.recv()
            #         print(msg_valid)
            #         msg_valid = json.loads(msg_valid)
            #         if msg_valid['TYPE'] == 'TEST' and msg_valid['DATA'] == 'COMPLETED':
            #             break


def spec_scenario(spec, testcase, generations=0, pop_size=1):
    loop = asyncio.get_event_loop()
    scenario_specification = copy.deepcopy(spec)
    scenario_testcase = copy.deepcopy(testcase)
    msgs = [scenario_testcase]
    # with open('log/InitTestCase.txt', 'w') as f:
    #     json.dump(scenario_testcase, f, indent=2)
    loop.run_until_complete(
        asyncio.gather(fuzzing(msgs, scenario_specification, generation_number=generations, population_size=pop_size)))


if __name__ == "__main__":
    file = 'input-test.txt'
    # file = 'test_cases/lane_changing/change3.txt'
    # file = 'test_cases/overtaking/overtaking6.txt'
    # file = 'test_cases/intersection/intersection.txt'
    # file = 'test_cases/lane_following/following4.txt'
    isGroundTruth = True
    extracted_data = ExtractAll(file, isGroundTruth)
    # agents = extracted_data.Get_AllAgents()
    # print(agents)
    testcases = extracted_data.Get_TestCastINJsonList()
    all_specifications = extracted_data.Get_Specifications()
    maps = extracted_data.Get_AllMaps()
    # all_spec = extracted_data.Get_SpecificationINScenario()
    for i in range(len(testcases)):

        print('len(testcases):'+ str(len(testcases)))
        test_case = testcases[i]
        scenario_name = test_case['ScenarioName']
        print("Current scenario is {}.\n".format(scenario_name))
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

                print('len(specifications_in_scenario)'+ str(len(specifications_in_scenario)))
                first_specification = specifications_in_scenario[0]
                single_specification = SingleAssertion(first_specification, current_map, ego_position)
                print("Evaluation Scenario {} with Assertion {}\n".format(scenario_name, single_specification.specification))
                spec_scenario(spec=single_specification, testcase=test_case, generations=50, pop_size=10)
        except KeyError:
            spec_scenario(spec={}, testcase=test_case)


        # for i in range(len(specifications_in_scenario)):
        #     single_specification = SingleAssertion(specifications_in_scenario[i])
        #     spec_scenario(spec={}, testcase=test_case)
        # scenario_safety_spec = {'safety specs': [all_spec[scenario_name]['safety specs'][0]]}


