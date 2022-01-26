import copy
import json
import logging
import os
import sys

from config import get_npc_list, get_pedestrian_list, get_ego_list, get_map_list, get_weather_list
from map import get_map_info
from GeneticAlgorithm import get_testcase


class model_space:
    def __init__(self, init_trace):
        self.scenario = copy.deepcopy(get_testcase(init_trace))
    # def __init__(self, init_test_case):
    #     self.scenario = copy.deepcopy(init_test_case)
        _map_info = get_map_info(self.scenario['map'])
        self.lane_config = _map_info.get_lane_config()
        self.weather_elements = dict()
        self._get_weather()
        self.time_elements = [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9), (10, 11), (12, 13), (14, 15), (16, 17), (18, 19), (20, 21), (22, 23)]
        self.ego_type_elements = get_ego_list()
        self.ego_lane_elements = dict()
        self._get_ego_lane_element()
        self.npc_type_elements = get_npc_list()
        self.npc_lane_elements = dict()
        self._get_npc_lane_elements()
        self.pedestrian_type_elements = get_pedestrian_list()
        self.space = {'weather': self.weather_elements,
                      'time': self.time_elements,
                      'ego_type': self.ego_type_elements,
                      'ego_lane': self.ego_lane_elements,
                      'npc_type': self.npc_type_elements,
                      'npc_lane': self.npc_lane_elements,
                      'pedestrian_type': self.pedestrian_type_elements,
                      'number': self._get_elements_len()}

    def _get_weather(self):
        weather_types = get_weather_list()
        for weather in weather_types:
            self.weather_elements[weather] = [(0.0, 0.2), (0.2, 0.4), (0.4, 0.6), (0.6, 0.8), (0.8, 1)]

    def _get_ego_lane_element(self):
        lane_id = self.scenario['ego']['start']['lane_position']['lane']
        lane_len = self.lane_config[lane_id]
        if lane_len < 30:
            self.ego_lane_elements[lane_id] = [(0, lane_len)]
        elif lane_len < 90:
            lane_len_1 = (0, lane_len/2)
            lane_len_2 = (lane_len/2, lane_len)
            self.ego_lane_elements[lane_id] = [lane_len_1, lane_len_2]
        else:
            lane_len_1 = (0, lane_len / 3)
            lane_len_2 = (lane_len / 3, 2 * lane_len/3)
            lane_len_3 = (2 * lane_len / 3 + 0.5, lane_len)
            self.ego_lane_elements[lane_id] = [lane_len_1, lane_len_2, lane_len_3]

    def _npc_lane_classification(self, lane_id):
        lane_len = self.lane_config[lane_id]
        if lane_len < 30:
            self.npc_lane_elements[lane_id] = [(0, lane_len)]
        elif lane_len < 90:
            lane_len_1 = (0, lane_len/2)
            lane_len_2 = (lane_len/2, lane_len)
            self.npc_lane_elements[lane_id] = [lane_len_1, lane_len_2]
        else:
            lane_len_1 = (0, lane_len / 3)
            lane_len_2 = (lane_len / 3, 2 * lane_len/3)
            lane_len_3 = (2 * lane_len / 3, lane_len)
            self.npc_lane_elements[lane_id] = [lane_len_1, lane_len_2, lane_len_3]

    def _get_npc_lane_elements(self):
        _lanes = set()
        for i in range(len(self.scenario['npcList'])):
            _npc = self.scenario['npcList'][i]
            _state_lane = _npc['start']['lane_position']['lane']
            _lanes.add(_state_lane)
            for j in range(len(_npc['motion'])):
                _motion_state = _npc['motion'][j]
                try:
                    _lane_id = _motion_state['lane_position']['lane']
                except KeyError:
                    print(_motion_state)
                _lanes.add(_lane_id)
            if _npc['destination'] is not None:
                _des_lane_id = _npc['destination']['lane_position']['lane']
                _lanes.add(_des_lane_id)

        for _lane in _lanes:
            self._npc_lane_classification(_lane)

    def _get_elements_len(self):
        element_number = 0
        for key in self.weather_elements.keys():
            element_number += len(self.weather_elements[key])
        element_number += len(self.time_elements)
        element_number += len(self.ego_type_elements)
        for key in self.ego_lane_elements.keys():
            element_number += len(self.ego_lane_elements[key])
        element_number += len(self.npc_type_elements)
        for key in self.npc_lane_elements.keys():
            element_number += len(self.npc_lane_elements[key])
        element_number += len(self.pedestrian_type_elements)
        return element_number



def check_range(value, interval):
    low_boundary = interval[0]
    upper_boundary = interval[1]
    if low_boundary <= value <= upper_boundary:
        return True
    else:
        return False

def compute_coverage(coverage_element):
    '''

    Args:
        coverage_element: {'weather': weather_elements, -->dict
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
    number = 0
    for key in coverage_element['weather'].keys():
        number += len(coverage_element['weather'][key])
    number += len(coverage_element['time'])
    number += len(coverage_element['ego_type'])
    for key in coverage_element['ego_lane'].keys():
        number += len(coverage_element['ego_lane'][key])
    number += len(coverage_element['npc_type'])
    for key in coverage_element['npc_lane'].keys():
        number += len(coverage_element['npc_lane'][key])
    number += len(coverage_element['pedestrian_type'])
    return number


def get_model_coverage(test_case, scenario_space):
    covered_dic = dict()
    covered_dic['weather'] = dict()
    covered_dic['time'] = []
    covered_dic['ego_type'] = []
    covered_dic['ego_lane'] = dict()
    covered_dic['npc_type'] = []
    covered_dic['npc_lane'] = dict()
    covered_dic['pedestrian_type'] = []

    # weather
    _weather = test_case['weather']
    for key in _weather.keys():
        covered_dic['weather'][key] = []
        value = _weather[key]
        for interval in scenario_space['weather'][key]:
            if check_range(value, interval):
                covered_dic['weather'][key].append(interval)
                break

    # time
    _hour = test_case['time']['hour']
    for item in scenario_space['time']:
        if _hour in item:
            covered_dic['time'].append(item)
            break

    # ego vehicle
    _ego_type = test_case['ego']['name']
    covered_dic['ego_type'].append(_ego_type)
    _ego_lane_id = test_case['ego']['start']['lane_position']['lane']
    _ego_lane_offset = test_case['ego']['start']['lane_position']['offset']
    for interval in scenario_space['ego_lane'][_ego_lane_id]:
        if check_range(_ego_lane_offset, interval):
            covered_dic['ego_lane'][_ego_lane_id] = [interval]
            break

    # npc list
    _npc_types = copy.deepcopy(scenario_space['npc_type'])
    _npc_space = copy.deepcopy(scenario_space['npc_lane'])

    for i in range(len(test_case['npcList'])):
        npc_i = test_case['npcList'][i]
        if npc_i['name'] in _npc_types:
            covered_dic['npc_type'].append(npc_i['name'])
            _npc_types.remove(npc_i['name'])
        npc_i_start_lane_id = npc_i['start']['lane_position']['lane']
        npc_i_start_lane_offset = npc_i['start']['lane_position']['offset']
        for interval in _npc_space[npc_i_start_lane_id]:
            if check_range(npc_i_start_lane_offset, interval):
                try:
                    covered_dic['npc_lane'][npc_i_start_lane_id].append(interval)
                except KeyError:
                    covered_dic['npc_lane'][npc_i_start_lane_id] = []
                    covered_dic['npc_lane'][npc_i_start_lane_id].append(interval)
                _npc_space[npc_i_start_lane_id].remove(interval)
                break
            if len(_npc_space[npc_i_start_lane_id]) == 0:
                break
        for j in range(len(npc_i['motion'])):
            _state_lane_position = npc_i['motion'][j]['lane_position']
            _lane_id = _state_lane_position['lane']
            _lane_offset = _state_lane_position['offset']
            for interval in _npc_space[_lane_id]:
                if not isinstance(interval, tuple):
                    print(interval)
                if check_range(_lane_offset, interval):
                    try:
                        covered_dic['npc_lane'][_lane_id].append(interval)
                    except KeyError:
                        covered_dic['npc_lane'][_lane_id] = []
                        covered_dic['npc_lane'][_lane_id].append(interval)
                    _npc_space[_lane_id].remove(interval)
                    break
                if len(_npc_space[_lane_id]) == 0:
                    break
        if npc_i['destination'] is not None:
            _npc_des_position = npc_i['destination']['lane_position']
            _npc_des_id = _npc_des_position['lane']
            _npc_des_offset = _npc_des_position['offset']
            for interval in _npc_space[_npc_des_id]:
                if check_range(_npc_des_offset, interval):
                    try:
                        covered_dic['npc_lane'][_npc_des_id].append(interval)
                    except KeyError:
                        covered_dic['npc_lane'][_npc_des_id] = []
                        covered_dic['npc_lane'][_npc_des_id].append(interval)
                    _npc_space[_npc_des_id].remove(interval)
                    break
                if len(_npc_space[_npc_des_id]) == 0:
                    break
    # pesdestrian
    ped_type = copy.deepcopy(scenario_space['pedestrian_type'])
    for i in range(len(test_case['pedestrianList'])):
        if test_case['pedestrianList'][i]['name'] in ped_type:
            covered_dic['pedestrian_type'].append(test_case['pedestrianList'][i]['name'])
            ped_type.remove(test_case['pedestrianList'][i]['name'])

    total_number = compute_coverage(covered_dic)
    covered_dic['number'] = total_number
    return covered_dic


def list_compare(list1, list2):
    diff_list = list(set(list1) - set(list2))
    return diff_list, len(diff_list)


def init_model_coverage():
    have_covered = dict()
    have_covered['weather'] = dict()
    have_covered['time'] = list()
    have_covered['ego_type'] = list()
    have_covered['ego_lane'] = dict()
    have_covered['npc_type'] = list()
    have_covered['npc_lane']= dict()
    have_covered['pedestrian_type'] = list()
    have_covered['number'] = 0
    return have_covered


def coverage_compare(single_coverage, all_coverage):
    '''
        Args:
            single_coverage/all_coverage:
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
    new_covered_number = 0

    # weather
    _weather_1 = single_coverage['weather']
    _weather_2 = all_coverage['weather']
    for _key in _weather_1:
        _value1 = _weather_1[_key]
        try:
            _value2 = _weather_2[_key]
        except KeyError:
            _value2 = []
        _diff_weather, _diff_number = list_compare(_value1, _value2)
        all_coverage['weather'][_key] = _value2 + _diff_weather
        new_covered_number += _diff_number

    # time
    _time_1 = single_coverage['time']
    _time_2 = all_coverage['time']
    _diff_time, _diff_number = list_compare(_time_1, _time_2)
    all_coverage['time'] = _time_2 + _diff_time
    new_covered_number += _diff_number

    # ego type
    _ego_type_1 = single_coverage['ego_type']
    _ego_type_2 = all_coverage['ego_type']
    _diff_ego_type, _diff_number = list_compare(_ego_type_1, _ego_type_2)
    all_coverage['ego_type'] = _ego_type_2 + _diff_ego_type
    new_covered_number += _diff_number

    # ego lane
    _ego_lane_1 = single_coverage['ego_lane']
    _ego_lane_2 = all_coverage['ego_lane']
    for key in _ego_lane_1.keys():
        _value1 = _ego_lane_1[key]
        try:
            _value2 = _ego_lane_2[key]
        except KeyError:
            _value2 = []
        _diff_ego_lane, _diff_number = list_compare(_value1, _value2)
        all_coverage['ego_lane'][key] = _value2 + _diff_ego_lane
        new_covered_number += _diff_number

    _npc_type_1 = single_coverage['npc_type']
    _npc_type_2 = all_coverage['npc_type']
    _diff_npc_type, _diff_number = list_compare(_npc_type_1, _npc_type_2)
    all_coverage['npc_type'] = _npc_type_2 + _diff_npc_type
    new_covered_number += _diff_number

    _npc_lane_1 = single_coverage['npc_lane']
    _npc_lane_2 = all_coverage['npc_lane']
    for key in _npc_lane_1.keys():
        _value_1 = _npc_lane_1[key]
        try:
            _value_2 = _npc_lane_2[key]
        except KeyError:
            _value_2 = []
        _diff_npc_lane, _diff_number = list_compare(_value_1, _value_2)
        all_coverage['npc_lane'][key] = _value_2 + _diff_npc_lane
        new_covered_number += _diff_number

    _pedestrian_type_1 = single_coverage['pedestrian_type']
    _pedestrian_type_2 = all_coverage['pedestrian_type']
    _diff_pedestrian_type, _diff_number = list_compare(_pedestrian_type_1, _pedestrian_type_2)
    all_coverage['pedestrian_type'] = _pedestrian_type_2 + _diff_pedestrian_type
    new_covered_number += _diff_number
    if new_covered_number:
        all_coverage['number'] = all_coverage['number'] + new_covered_number
        coverage_flag = True
    else:
        coverage_flag = False

    return coverage_flag


def remain_space(covered_space, input_space):
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
    remain_space = init_model_coverage()

    # weather
    _weather_1 = covered_space['weather']
    _weather_2 = input_space['weather']
    for _key in _weather_1:
        _value1 = _weather_1[_key]
        _value2 = _weather_2[_key]
        _diff_weather, _diff_number = list_compare(_value2, _value1)
        remain_space['weather'][_key] = _diff_weather
        remain_space['number'] += _diff_number

    # time
    _time_1 = covered_space['time']
    _time_2 = input_space['time']
    _diff_time, _diff_number = list_compare(_time_2, _time_1)
    remain_space['time'] = _diff_time
    remain_space['number'] += _diff_number

    # ego type
    _ego_type_1 = covered_space['ego_type']
    _ego_type_2 = input_space['ego_type']
    _diff_ego_type, _diff_number = list_compare(_ego_type_2, _ego_type_1)
    remain_space['ego_type'] = _diff_ego_type
    remain_space['number'] += _diff_number

    # ego lane
    _ego_lane_1 = covered_space['ego_lane']
    _ego_lane_2 = input_space['ego_lane']
    for key in _ego_lane_1.keys():
        _value1 = _ego_lane_1[key]
        _value2 = _ego_lane_2[key]
        _diff_ego_lane, _diff_number = list_compare(_value2, _value1)
        remain_space['ego_lane'][key] = _diff_ego_lane
        remain_space['number'] += _diff_number

    _npc_type_1 = covered_space['npc_type']
    _npc_type_2 = input_space['npc_type']
    _diff_npc_type, _diff_number = list_compare(_npc_type_2, _npc_type_1)
    remain_space['npc_type'] = _diff_npc_type
    remain_space['number'] += _diff_number

    _npc_lane_1 = covered_space['npc_lane']
    _npc_lane_2 = input_space['npc_lane']
    for key in _npc_lane_1.keys():
        _value_1 = _npc_lane_1[key]
        _value_2 = _npc_lane_2[key]
        _diff_npc_lane, _diff_number = list_compare(_value_2, _value_1)
        remain_space['npc_lane'][key] = _diff_npc_lane
        remain_space['number'] += _diff_number

    _pedestrian_type_1 = covered_space['pedestrian_type']
    _pedestrian_type_2 = input_space['pedestrian_type']
    _diff_pedestrian_type, _diff_number = list_compare(_pedestrian_type_1, _pedestrian_type_2)
    remain_space['pedestrian_type'] = _diff_pedestrian_type
    remain_space['number'] += _diff_number

    return remain_space


if __name__ == "__main__":

    directory0 = '/run/user/1001/gvfs/smb-share:server=synology_nas.local,share=zhouyuan/'
    test_rounds = ['ga_3/']  # 'random_2/', 'random_3/', 'random_4/', 'random_5/'
    scenarios = ['intersection1', 'intersection2', 'intersection3', 'intersection4', 'intersection5', 'lanechange1', 'lanechange3', 'overtaking1']
    for test_round in test_rounds:
        direct = directory0 + test_round
        # sub_folders = os.listdir(direct)
        # sub_folders = sorted(sub_folders)
        for sub_folder in scenarios:
            logging_file = direct + '/model_coverage_ga.log'
            file_handler = logging.FileHandler(logging_file, mode='w')
            stdout_handler = logging.StreamHandler(sys.stdout)
            logging.basicConfig(level=logging.INFO, handlers=[stdout_handler, file_handler], format='%(asctime)s, %(levelname)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
            logging.info("Current Scenarios: {}".format(sub_folder))
            # start to compute coverage based on the trace
            sub_direct = direct + sub_folder + '/data/'
            items = os.listdir(sub_direct)
            items = sorted(items)
            file_init = sub_direct + items[0]
            with open(file_init) as f:
                trace = json.load(f)
                input_space = model_space(trace).space
            covered_space = init_model_coverage()
            for i in range(len(items)):
                file = sub_direct + items[i]
                with open(file) as f:
                    trace = json.load(f)
                    current_case = get_testcase(trace)
                    test_case_covered = get_model_coverage(current_case, input_space)
                    flag = coverage_compare(test_case_covered, covered_space)
                    logging.info("TestCase: {}, New Coverage: {}, Current Covered: {}".format(i, flag, test_case_covered['number']))
            logging.info("Total Model Coverage: {}/{}".format(covered_space['number'], input_space['number']))

