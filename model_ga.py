import copy
import gc
import random
from typing import Any, Dict

from TestCaseExtraction import AllTestCase
from EXtraction import ExtractAll
from TestCaseExtraction import TestCase
import json
from random import gauss
import numpy as np
from map import get_map_info
from pedestrian_motion_checking import nearest
from config import get_npc_list, get_pedestrian_list, get_weather_list
from model_coverage import model_space, get_model_coverage, coverage_compare, init_model_coverage, remain_space
from GeneticAlgorithm import testcase_encode, list2d_convert, DecodedTestCase
from pedestrian_motion_checking import pedestrian_in_crosswalk
from TestCaseRandom import TestCaseRandom
import random

vehicle_list = get_npc_list()
pedestrian_list = get_pedestrian_list()
weather_list = get_weather_list()
offset_offset = 2.0


class ModelEncodedTestCase:
    def __init__(self, testcase, input_space, covered_input_space):
        self.testcase = copy.deepcopy(testcase)
        self.chromosome = testcase_encode(self.testcase)
        self.input_space = input_space
        self.covered_space = covered_input_space
        self.new_coverage = self._compute_coverage()

    def _compute_coverage(self):
        test_case_covered = get_model_coverage(self.testcase, self.input_space)
        return coverage_compare(test_case_covered, self.covered_space)


class Model_GA:
    def __init__(self, population_para, crossover_prob=1.0, mutation_prob=1.0):
        self.population = copy.deepcopy(population_para)  # a list of ModelEncodedTestCase
        self.p_cross = crossover_prob
        self.p_mutation = mutation_prob
        self.population_size = len(self.population)

    def selection(self):
        selected_population = []
        for i in range(self.population_size):
            if self.population[i].new_coverage:
                selected_population.append(self.population[i])
        return selected_population

    def _crossover(self, p1, p2):
        # crossover is only performed on speed for vehicles
        new_p1 = copy.deepcopy(p1)
        new_p2 = copy.deepcopy(p2)
        chm1 = new_p1.chromosome[0]['speed']
        chm2 = new_p2.chromosome[0]['speed']
        if len(chm1):
            chm1_convert = list2d_convert(chm1)
            chm2_convert = list2d_convert(chm2)
            cross_point = random.randint(1, chm1_convert.len)
            temp = chm1_convert.list1d[0:cross_point]
            chm1_convert.list1d[0:cross_point] = chm2_convert.list1d[0:cross_point]
            chm2_convert.list1d[0:cross_point] = temp
            new_p1.chromosome[0]['speed'] = chm1_convert.to_2d()
            new_p2.chromosome[0]['speed'] = chm2_convert.to_2d()
        try:
            chm1_p_speed = new_p1.chromosome[5]['speed']
            if len(chm1_p_speed):
                chm2_p_speed = new_p2.chromosome[5]['speed']
                cross_ped_speed_point = random.randint(1, len(chm1_p_speed))
                temp_speed = chm1_p_speed[0:cross_ped_speed_point]
                chm1_p_speed[0:cross_ped_speed_point] = chm2_p_speed[0:cross_ped_speed_point]
                chm2_p_speed[0:cross_ped_speed_point] = temp_speed
                new_p1.chromosome[5]['speed'] = chm1_p_speed
                new_p2.chromosome[5]['speed'] = chm2_p_speed
        except ValueError:
            print('checking')

        # if not new_p1.testcase['ego']['groundTruthPerception']:
        if True:
            # time crossover
            _chrm_time1 = new_p1.chromosome[1]
            _chrm_time2 = new_p2.chromosome[1]
            _time_point = random.randint(1, len(_chrm_time1))
            _temp = _chrm_time1[0:_time_point]
            _chrm_time1[0:_time_point] = _chrm_time2[0:_time_point]
            _chrm_time2[0:_time_point] = _temp
            new_p1.chromosome[1] = _chrm_time1
            new_p2.chromosome[1] = _chrm_time2

            # weather crossover
            _chrm_weather1 = new_p1.chromosome[2]
            _chrm_weather2 = new_p2.chromosome[2]
            _weather_point = random.randint(1, len(_chrm_weather1))
            _temp = _chrm_weather1[0:_weather_point]
            _chrm_weather1[0:_weather_point] = _chrm_weather2[0:_weather_point]
            _chrm_weather2[0:_weather_point] = _temp
            new_p1.chromosome[2] = _chrm_weather1
            new_p2.chromosome[2] = _chrm_weather2

            # vehicle type
            _chrm_v_type1 = new_p1.chromosome[3]
            _chrm_v_type2 = new_p2.chromosome[3]
            if len(_chrm_v_type1):
                _v_type_point = random.randint(1, len(_chrm_v_type1))
                _temp = _chrm_v_type1[0:_v_type_point]
                _chrm_v_type1[0:_v_type_point] = _chrm_v_type2[0:_v_type_point]
                _chrm_v_type2[0:_v_type_point] = _temp
                new_p1.chromosome[3] = _chrm_v_type1
                new_p2.chromosome[3] = _chrm_v_type2

            # pedestrian type
            _chrm_p_type1 = new_p1.chromosome[4]
            _chrm_p_type2 = new_p2.chromosome[4]
            if len(_chrm_p_type1):
                _p_type_point = random.randint(1, len(_chrm_p_type1))
                _temp = _chrm_p_type1[0:_p_type_point]
                _chrm_p_type1[0:_p_type_point] = _chrm_p_type2[0:_p_type_point]
                _chrm_p_type2[0:_p_type_point] = _temp
                new_p1.chromosome[4] = _chrm_p_type1
                new_p2.chromosome[4] = _chrm_p_type2
        return new_p1, new_p2

    def _mutation(self, p, lane_config, crosswalk_config):
        v_max = 20
        v_min = 0.5
        pv_max = 5
        pv_min = 0.05
        new_p = copy.deepcopy(p)
        speed_element = list2d_convert(new_p.chromosome[0]['speed'])
        offset_element = list2d_convert(new_p.chromosome[0]['offset'])
        # mutate speed
        for i in range(speed_element.len):
            mutated_speed = gauss(speed_element.list1d[i], 1)
            speed_element.list1d[i] = float(np.clip(mutated_speed, v_min, v_max))

        # ego vehicle offset
        _offset_count = 0
        _ego_offsets = offset_element.list2d[0]
        _ego = new_p.testcase['ego']
        _ego_start_lane = _ego['start']['lane_position']['lane']
        _ego_start_length = lane_config[_ego_start_lane]
        mutated_start_offset = float(
            np.clip(gauss(_ego_offsets[0], 1), offset_offset, _ego_start_length - offset_offset))
        offset_element.list1d[0] = mutated_start_offset
        _offset_count += 1
        # _ego_destination_lane = _ego['destination']['lane_position']['lane']
        # if _ego_start_lane == _ego_destination_lane:
        #     mutated_destination_offset = float(np.clip(gauss(_ego_offsets[1], 1), mutated_start_offset, _ego_start_length - offset_offset))
        # else:
        #     _ego_destination_length = lane_config[_ego_destination_lane]
        #     mutated_destination_offset = float(np.clip(gauss(_ego_offsets[1], 1), offset_offset, _ego_destination_length - offset_offset))
        # offset_element.list1d[_offset_count] = mutated_destination_offset
        # _offset_count += 1

        # npc offsets
        no_npc = len(new_p.testcase['npcList'])
        for index_npc in range(no_npc):
            npc_offset = offset_element.list2d[index_npc + 1]
            npc = copy.deepcopy(new_p.testcase['npcList'][index_npc])
            _npc_start_lane = npc['start']['lane_position']['lane']
            _npc_start_length = lane_config[_npc_start_lane]
            mutated_npc_started_offset = gauss(npc_offset[0], 1)
            if _ego_start_lane == _npc_start_lane:
                _diff_dis = mutated_npc_started_offset - offset_element.list1d[0]
                if -8 <= _diff_dis <= 0:
                    mutated_npc_started_offset = offset_element.list1d[0] - 8
                elif 0 <= _diff_dis <= 8:
                    mutated_npc_started_offset = offset_element.list1d[0] + 8
            # mutated_npc_started_offset = float(np.clip(mutated_npc_started_offset, offset_offset, _npc_start_length - offset_offset))
            offset_element.list1d[_offset_count] = float(
                np.clip(mutated_npc_started_offset, offset_offset, _npc_start_length - offset_offset))
            if _ego_start_lane == _npc_start_lane and np.abs(
                    offset_element.list1d[_offset_count] - offset_element.list1d[0]) < 7.9:
                print("something is wrong.")
            _offset_count += 1

            current_lane = _npc_start_lane
            current_length = _npc_start_length
            for wp in range(len(npc['motion'])):
                wp_i = npc['motion'][wp]
                wp_lane = wp_i['lane_position']['lane']
                mutated_offset = gauss(npc_offset[1 + wp], 1)
                if wp_lane == current_lane:
                    mutated_offset = float(np.clip(mutated_offset, offset_element.list1d[_offset_count - 1],
                                                   current_length - offset_offset))
                    offset_element.list1d[_offset_count] = mutated_offset
                    _offset_count += 1
                else:
                    current_lane = wp_lane
                    current_length = lane_config[wp_lane]
                    mutated_offset = float(
                        np.clip(mutated_offset, offset_offset, current_length - offset_offset))
                    offset_element.list1d[_offset_count] = mutated_offset
                    _offset_count += 1
            if npc['destination'] is not None:
                npc_destination_lane = npc['destination']['lane_position']['lane']
                mutated_offset = gauss(npc_offset[-1], 1)
                if npc_destination_lane == current_lane:
                    mutated_offset = float(np.clip(mutated_offset, offset_element.list1d[_offset_count - 1],
                                                   current_length - offset_offset))
                    offset_element.list1d[_offset_count] = mutated_offset
                else:
                    npc_destination_length = lane_config[npc_destination_lane]
                    mutated_offset = float(
                        np.clip(mutated_offset, offset_offset, npc_destination_length - offset_offset))
                    offset_element.list1d[_offset_count] = mutated_offset
                _offset_count += 1

        new_p.chromosome[0]['speed'] = speed_element.to_2d()
        new_p.chromosome[0]['offset'] = offset_element.to_2d()

        # pedestrian
        no_ped = len(new_p.testcase['pedestrianList'])
        if no_ped:
            _chrm_ped = new_p.chromosome[5]
            position_value = _chrm_ped['position']
            speed_value = _chrm_ped['speed']
            new_chrm_ped = {'position': [], 'speed': []}
            for _i in range(len(position_value)):
                _position = position_value[_i]
                _new_position = (gauss(_position[0], 1), gauss(_position[1], 1))
                new_chrm_ped['position'].append(_new_position)
                _mutated_speed = gauss(speed_value[_i], 1)
                new_chrm_ped['speed'].append(float(np.clip(_mutated_speed, pv_min, pv_max)))
            _, new_chrm_ped['position'] = pedestrian_in_crosswalk(new_chrm_ped['position'], crosswalk_config)
            new_p.chromosome[5] = copy.deepcopy(new_chrm_ped)

        # if not new_p.testcase['ego']['groundTruthPerception']:
        if True:
            # mutate time
            new_p.chromosome[1] = [random.randint(0, 23), random.randint(0, 59)]
            # mutate weather
            if len(new_p.chromosome[2]) != 3:
                print("wrong weather features.")
            new_p.chromosome[2] = list(np.random.uniform(0, 1, len(new_p.chromosome[2])))
            # mutate vehicle type
            if no_npc:
                new_p.chromosome[3] = [vehicle_list[item] for item in
                                       np.random.randint(0, len(vehicle_list), len(new_p.chromosome[3]))]
            # mutate pedestrian type
            if no_ped:
                new_p.chromosome[4] = [pedestrian_list[item] for item in
                                       np.random.randint(0, len(pedestrian_list), len(new_p.chromosome[4]))]
        return new_p

    def model_coverage_one_generation(self):
        selected_population = self.selection()
        _new_population = []
        map_name = self.population[0].testcase['map']
        map_info = get_map_info(map_name)
        lane_info = map_info.get_lane_config()
        crosswalk_info = map_info.get_crosswalk_config()
        for i in range(0, len(selected_population), 2):
            if i + 1 <= len(selected_population) - 1:
                p1 = copy.deepcopy(selected_population[i])
                p2 = copy.deepcopy(selected_population[i + 1])
                if random.random() < self.p_cross:
                    p1, p2 = self._crossover(p1, p2)
                if random.random() < self.p_mutation:
                    p1 = self._mutation(p1, lane_info, crosswalk_info)
                if random.random() < self.p_mutation:
                    p2 = self._mutation(p2, lane_info, crosswalk_info)
                _new_population.append(p1)
                _new_population.append(p2)
            else:
                new_p = copy.deepcopy(selected_population[i])
                _new_population.append(new_p)
        return _new_population

def greedy_generation(testcase, input_space, covered_space):
    '''
                Args:
                    covered_space/all_coverage:
                                {'weather': weather_elements, -->dict
                                  'time': self.time_elements, --> list
                                  'ego_type': self.ego_type_elements, -->list
                                  'ego_lane': self.ego_lane_elements, -->dict
                                  'npc_type': self.npc_type_elements, -->list
                                  'npc_lane': self.npc_lane_elements, -->dict
                                  'pedestrian_type': self.pedestrian_type_elements, -->list
                                  'number': self._get_elements_len()
                                  }

                Returns:
                '''
    _testcase = copy.deepcopy(testcase)
    rest_space = remain_space(covered_space=covered_space, input_space=input_space)
    # weather
    rest_weather = rest_space['weather']
    for key in rest_weather.keys():
        if len(rest_space['weather'][key]):
            weather_interval = rest_space['weather'][key][0]
            weather_value = random.randrange(weather_interval[0], weather_interval[1])
            _testcase['weather'][key] = weather_value
    # time
    rest_time = rest_space['time']
    if len(rest_time):
        time_interval = rest_time[0]
        p = random.random()
        if p < 0.5:
            _testcase['time']['hour'] = time_interval[0]
        else:
            _testcase['time']['hour'] = time_interval[1]
    # ego type
    rest_ego_type = rest_space['ego_type']
    if len(rest_ego_type):
        _testcase['ego']['name'] = rest_ego_type[0]
    # ego lane
    rest_ego_lane = rest_space['ego_lane']
    for key in rest_ego_lane.keys():
        rest_ego_segment = rest_ego_lane[key]
        if len(rest_ego_segment):
            ego_range = rest_ego_segment[0]
            _testcase['ego']['start']['lane_position']['offset'] = random.randrange(ego_range[0], ego_range[1])
    return _testcase


class Generation:
    def __init__(self, init_trace, num_generation, size_population):
        self.init_trace = init_trace
        self.input_space = model_space(init_trace).space
        self.covered_input_space = init_model_coverage()
        self.generation_number = num_generation
        self.population_size = size_population
        _init_testcase = self._population_initialization()
        self.testcases = [_init_testcase]

    def _population_initialization(self):
        testcase = TestCaseRandom(self.init_trace)
        testcase.testcase_random(self.population_size)
        return testcase.cases[1:]

    def encode_population(self, testcases):
        _population = []
        for i in range(len(testcases)):
            _individual = ModelEncodedTestCase(testcases[i], self.input_space, self.covered_input_space)
            _population.append(_individual)
        return _population

    def decode_population(self, population):
        decoder = DecodedTestCase(population)
        _testcases = decoder.decoding()
        return _testcases

    def process(self):
        for i in range(self.generation_number):
            current_testcase = self.testcases[i]
            _current_population = self.encode_population(current_testcase)
            model_ga = Model_GA(_current_population)
            next_population = model_ga.model_coverage_one_generation()
            new_testcases = self.decode_population(next_population)
            if len(new_testcases) < self.population_size:
                if len(new_testcases):
                    testcase = TestCaseRandom(self.init_trace)
                else:
                    testcase = TestCaseRandom(current_testcase[0])
                testcase.testcase_random(self.population_size-len(new_testcases))
                new_testcases = new_testcases + testcase.cases[1:]
            self.testcases.append(new_testcases)




if __name__ == "__main__":
    file_name = 'result1.json'
    with open(file_name) as f:
        data = json.load(f)
        ga_process = Generation(data, 5, 4)
        print(ga_process.input_space['number'])
        ga_process.process()
        cases = ga_process.testcases
        print(len(cases))
        # print(testcase.cases[i])
