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

vehicle_list = get_npc_list()
pedestrian_list = get_pedestrian_list()
weather_list = get_weather_list()
offset_offset = 2.0


# def TestCaseFromMsg(msg) -> Dict[str, Any]:
#     testcase_ = {}
#     testcase_['ScenarioName'] = msg['ScenarioName']
#     testcase_['MapVariable'] = msg['MapVariable']
#     testcase_['map'] = msg['map']
#     testcase_['ego'] = msg['ego']
#     testcase_['npcList'] = msg['npcList']
#     testcase_['pedestrianList'] = msg['pedestrianList']
#     testcase_['obstacleList'] = msg['obstacleList']
#     testcase_['AgentNames'] = msg['AgentNames']
#     # remove the vector positions in ego's start and destination states
#     testcase_['ego']['start'].pop('position', None)
#     testcase_['ego']['destination'].pop('position', None)
#
#     for _i in range(len(testcase_['npcList'])):
#         testcase_['npcList'][_i]['start'].pop('position', None)
#         if testcase_['npcList'][_i]['destination'] != None:
#             testcase_['npcList'][_i]['destination'].pop('position', None)
#         for _j in range(len(testcase_['npcList'][_i]['motion'])):
#             testcase_['npcList'][_i]['motion'][_j].pop('position', None)
#
#     for _i in range(len(testcase_['pedestrianList'])):
#         testcase_['pedestrianList'][_i]['start'].pop('position', None)
#         testcase_['pedestrianList'][_i]['destination'].pop('position', None)
#         for _j in range(len(testcase_['pedestrianList'][_i]['motion'])):
#             testcase_['pedestrianList'][_i]['motion'][_j].pop('position', None)
#
#     for _i in range(len(testcase_['obstacleList'])):
#         testcase_['obstacleList'][_i]['position'].pop('position', None)
#
#     return testcase_


'''
 self.ScenarioName = ""
        self.MapVariable = ""
        self.map = ""
        self.ego = EgoVehicle()
        # self.NPCNumber = lgsvl_filter_testcase.NPCNumber
        self.npcList = []
        # self.PedestrianNumber = lgsvl_filter_testcase.PedestrianNumber
        self.pedestrianList = []
        # self.ObsNumber = lgsvl_filter_testcase.ObsNumber
        self.obstacleList = []
        self.AgentNames = []
'''


# def RandomGeneration(OneTestCase, Number):
#     initial_case = OneTestCase
#     testcases = [initial_case]
#     for i in range(Number):
#         new_case = initial_case
#         ego_start_offset = new_case['ego']['start']['lane_position']['offset']
#         # ego_start_speed = new_case['ego']['start']['speed']
#         delta_offset = gauss(ego_start_offset, 1.0)
#         # delta_speed = gauss(ego_start_speed, 1.0)
#         new_case['ego']['start']['lane_position']['offset'] = delta_offset + ego_start_offset
#         # new_case['ego']['start']['speed'] = delta_speed + ego_start_speed
#         testcases.append(new_case)
#
#     return testcases


class TestCaseRandom:
    def __init__(self, msg):
        testcase_ = {}
        testcase_['ScenarioName'] = msg['ScenarioName']
        testcase_['MapVariable'] = msg['MapVariable']
        testcase_['map'] = msg['map']
        testcase_['time'] = msg['time']
        testcase_['weather'] = msg['weather']
        testcase_['ego'] = msg['ego']
        testcase_['npcList'] = msg['npcList']
        testcase_['pedestrianList'] = msg['pedestrianList']
        testcase_['obstacleList'] = msg['obstacleList']
        testcase_['AgentNames'] = msg['AgentNames']
        # remove the vector positions in ego's start and destination states
        testcase_['ego']['start'].pop('position', None)
        testcase_['ego']['start']['heading'].pop('ref_point', None)
        testcase_['ego']['destination'].pop('position', None)
        testcase_['ego']['destination']['heading'].pop('ref_point', None)

        for _i in range(len(testcase_['npcList'])):
            testcase_['npcList'][_i]['start'].pop('position', None)
            testcase_['npcList'][_i]['start']['heading'].pop('ref_point', None)
            if testcase_['npcList'][_i]['destination'] is not None:
                testcase_['npcList'][_i]['destination'].pop('position', None)
                testcase_['npcList'][_i]['destination']['heading'].pop('ref_point', None)
            for _j in range(len(testcase_['npcList'][_i]['motion'])):
                testcase_['npcList'][_i]['motion'][_j].pop('position', None)
                testcase_['npcList'][_i]['motion'][_j]['heading'].pop('ref_point', None)

        for _i in range(len(testcase_['pedestrianList'])):
            # testcase_['pedestrianList'][_i]['start'].pop('position', None)
            testcase_['pedestrianList'][_i]['start']['heading'].pop('ref_point', None)
            if testcase_['pedestrianList'][_i]['destination'] is not None:
                # testcase_['pedestrianList'][_i]['destination'].pop('position', None)
                testcase_['pedestrianList'][_i]['destination']['heading'].pop('ref_point', None)
            for _j in range(len(testcase_['pedestrianList'][_i]['motion'])):
                # testcase_['pedestrianList'][_i]['motion'][_j].pop('position', None)
                testcase_['pedestrianList'][_i]['motion'][_j]['heading'].pop('ref_point', None)

        for _i in range(len(testcase_['obstacleList'])):
            pass
            # testcase_['obstacleList'][_i]['position'].pop('position', None)
        self.original = testcase_
        self.cases = [testcase_]

    def time_random(self):
        _hour = random.randint(0, 23)
        _minute = random.randint(0, 59)
        return {'hour': _hour, 'minute': _minute}

    def weather_random(self):
        _weather = {}
        for key in weather_list:
            _weather[key] = random.uniform(0, 1)
        return _weather
        # return {'rain': random.uniform(0, 1), 'fog': random.uniform(0, 1), 'wetness': random.uniform(0, 1)}
        # , 'cloudiness': random.uniform(0, 1), 'damage': random.uniform(0, 1)


    def ego_random(self, lane_info_para):
        # todo: set maximal speed and lane offset
        # end todo
        # lane_config = copy.deepcopy(lane_info)
        _ego = copy.deepcopy(self.original['ego'])
        ego_start_offset = _ego['start']['lane_position']['offset']
        delta_offset = gauss(ego_start_offset, 1.0)
        _start_lane_max = lane_info_para[_ego['start']['lane_position']['lane']]
        _ego['start']['lane_position']['offset'] = float(np.clip(delta_offset, offset_offset, _start_lane_max - offset_offset))
        _ego['start']['heading']['ref_lane_point'] = _ego['start']['lane_position']
        _ego['start']['heading']['ref_angle'] = 0.0
        _ego['start']['heading'].pop('ref_position', None)
        # del lane_config
        # gc.collect()

        # ego_destination_offset = _ego['destination']['lane_position']['offset']
        # delta_offset = gauss(ego_destination_offset, 1.0)
        # _destination_lane_max = lane_config[_ego['destination']['lane_position']['lane']]
        # _ego['destination']['lane_position']['offset'] = float(np.clip(delta_offset, offset_offset, _destination_lane_max - offset_offset))
        # _ego['destination']['heading']['ref_lane_point'] = _ego['destination']['lane_position']
        # _ego['destination']['heading']['ref_angle'] = 0.0
        # _ego['destination']['heading'].pop('ref_position', None)
        # _ego['start']['speed'] = float(np.clip(delta_speed + ego_start_speed, 0, _speed_max))
        return _ego

    def npc_random(self, original_npc, lane_info, ego_start):
        # todo: set maximal speed
        lane_config = copy.deepcopy(lane_info)
        _speed_max = 20
        _speed_min = 0.5
        # end todo
        _npc = copy.deepcopy(original_npc)
        _type_index = random.randint(0, len(vehicle_list)-1)
        _npc['name'] = vehicle_list[_type_index]
        _npc_start_offset = _npc['start']['lane_position']['offset']
        _npc_start_speed = _npc['start']['speed']
        delta_start_offset = gauss(_npc_start_offset, 1.0)
        delta_start_speed = gauss(_npc_start_speed, 1.0)
        _start_lane_length = lane_config[_npc['start']['lane_position']['lane']]
        if _npc['start']['lane_position']['lane'] == ego_start['lane']:
            _dis_offset = delta_start_offset - ego_start['offset']
            if 0 > _dis_offset > -8:
                print("fine-tuning\n")
                delta_start_offset = ego_start['offset'] - 8
                print(delta_start_offset)
            elif 8 > _dis_offset > 0:
                print("fine-tuning\n")
                delta_start_offset = ego_start['offset'] + 8
                print(delta_start_offset)
        _npc['start']['lane_position']['offset'] = float(np.clip(delta_start_offset, offset_offset, _start_lane_length - offset_offset))

        if _npc['start']['lane_position']['lane'] == ego_start['lane']:
            if np.abs(_npc['start']['lane_position']['offset'] - ego_start['offset']) < 7.9:
                print("something is wrong.")

        _npc['start']['speed'] = float(np.clip(delta_start_speed, 0, _speed_max))
        _npc['start']['heading']['ref_lane_point'] = _npc['start']['lane_position']
        _npc['start']['heading']['ref_angle'] = 0.

        _current_lane = _npc['start']['lane_position']['lane']
        _current_length = _start_lane_length
        # _end_lane = _npc['destination']['lane_position']['lane']
        for _i in range(len(_npc['motion'])):
            wp_i = _npc['motion'][_i]
            wp_i_lane = wp_i['lane_position']['lane']
            wp_i_offset = wp_i['lane_position']['offset']
            wp_i_speed = wp_i['speed']
            delta_wpi_offset = gauss(wp_i_offset, 1.0)
            delta_wpi_speed = gauss(wp_i_speed, 1.0)

            if _current_lane == wp_i_lane:
                if _i == 0:
                    _min_offset = _npc['start']['lane_position']['offset']
                else:
                    _min_offset = _npc['motion'][_i-1]['lane_position']['offset']
            else:
                _min_offset = offset_offset
                _current_lane = wp_i_lane
                _current_length = lane_config[_current_lane]
            _new_offset = float(np.clip(delta_wpi_offset, _min_offset, _current_length - offset_offset))
            _npc['motion'][_i]['lane_position']['offset'] = float(np.clip(delta_wpi_offset, _min_offset, _current_length - offset_offset))
            _npc['motion'][_i]['speed'] = float(np.clip(delta_wpi_speed, _speed_min, _speed_max))
            _npc['motion'][_i]['heading']['ref_lane_point'] = _npc['motion'][_i]['lane_position']
            _npc['motion'][_i]['heading']['ref_angle'] = 0.

        if _npc['destination'] is not None:
            _npc_destination_lane = _npc['destination']['lane_position']['lane']
            if _npc_destination_lane == _current_lane:
                _npc_destination_min = _npc['motion'][-1]['lane_position']['offset']
                _npc_destination_max = _current_length
            else:
                _npc_destination_min = offset_offset
                _npc_destination_max = lane_config[_npc['destination']['lane_position']['lane']]
            _npc_destination_offset = _npc['destination']['lane_position']['offset']
            _npc_destination_speed = _npc['destination']['speed']
            delta_destination_offset = gauss(_npc_destination_offset, 1.0)
            delta_destination_speed = gauss(_npc_destination_speed, 1.0)
            _npc['destination']['lane_position']['offset'] = float(np.clip(delta_destination_offset, _npc_destination_min, _npc_destination_max - offset_offset))
            _npc['destination']['speed'] = 0.0
            # _npc['destination']['heading']['ref_lane_point'] = _npc['destination']['lane_position']
            # _npc['destination']['heading']['ref_angle'] = 0.

        return _npc

    def pedestrian_random(self, pedestrian, crosswalk_info):
        # todo: set maximal speed
        crosswalk_config = copy.deepcopy(crosswalk_info)
        _speed_max = 5
        _speed_min = 0.05
        # end todo
        _ped = copy.deepcopy(pedestrian)
        _type_index = random.randint(0, len(pedestrian_list)-1)
        _ped['name'] = pedestrian_list[_type_index]
        _ped_start_x = _ped['start']['position']['x']
        _ped_start_y = _ped['start']['position']['y']
        _ped_start_speed = _ped['start']['speed']
        delta_start_x = gauss(_ped_start_x, 1.0)
        delta_start_y = gauss(_ped_start_y, 1.0)
        crosswalk_name, _init_point = nearest((delta_start_x, delta_start_y), crosswalk_config)
        delta_start_speed = gauss(_ped_start_speed, 1.0)
        # _start_lane_length = map_config[_ped['start']['lane_position']['lane']]
        # _ped['start']['lane_position']['offset'] = float(np.clip(delta_start_offset, offset_offset, _start_lane_length - offset_offset))
        _ped['start']['position']['x'] = _init_point[0]
        _ped['start']['position']['y'] = _init_point[1]
        _ped['start']['speed'] = float(np.clip(delta_start_speed, 0, _speed_max))
        # _ped['start']['heading']['ref_lane_point'] = _ped['start']['lane_position']
        # _ped['start']['heading']['ref_angle'] = 0.

        for _i in range(len(_ped['motion'])):
            wp_i_x = _ped['motion'][_i]['position']['x']
            wp_i_y = _ped['motion'][_i]['position']['y']
            wp_i_speed = _ped['motion'][_i]['speed']
            _dx = gauss(wp_i_x, 1)
            _dy = gauss(wp_i_y, 1)
            _, _pd = nearest((_dx, _dy), {crosswalk_name: crosswalk_config[crosswalk_name]})
            _ped['motion'][_i]['position']['x'] = _pd[0]
            _ped['motion'][_i]['position']['y'] = _pd[1]
            _ped['motion'][_i]['speed'] = float(np.clip(wp_i_speed, _speed_min, _speed_max))
        if _ped['destination'] is not None:
            _ped_destination_x = _ped['destination']['position']['x']
            _ped_destination_y = _ped['destination']['position']['y']
            _ped_destination_speed = _ped['destination']['speed']
            _dx = gauss(_ped_destination_x, 1.0)
            _dy = gauss(_ped_destination_y, 1.0)
            _, _pd = nearest((_dx, _dy), {crosswalk_name: crosswalk_config[crosswalk_name]})
            _ped['destination']['position']['x'] = _dx
            _ped['destination']['position']['y'] = _dy
            _ped['destination']['speed'] = 0.0
        return _ped

    def testcase_random(self, num):
        for _i in range(num):
            # print("random test case: {}".format(_i))
            _new_case = copy.deepcopy(self.original)
            # if not _new_case['ego']['groundTruthPerception']:
            map_name = _new_case['map']
            map_info = get_map_info(map_name)
            lane_info = map_info.get_lane_config()
            crosswalk_info = map_info.get_crosswalk_config()
            if True:
                _new_case['time'] = self.time_random()
                _new_case['weather'] = self.weather_random()
            ego_random = self.ego_random(lane_info)
            _new_case['ego'] = copy.deepcopy(ego_random)
            for _j in range(len(_new_case['npcList'])):
                npc_j = _new_case['npcList'][_j]
                _new_npc = self.npc_random(npc_j, lane_info, _new_case['ego']['start']['lane_position'])
                _new_case['npcList'][_j] = copy.deepcopy(_new_npc)
            for _j in range(len(_new_case['pedestrianList'])):
                ped_j = _new_case['pedestrianList'][_j]
                _new_case['pedestrianList'][_j] = copy.deepcopy(self.pedestrian_random(ped_j, crosswalk_info))
            self.cases.append(_new_case)

        for i in range(len(self.cases)-1):
            # print("test case {}".format(i))
            case = self.cases[i+1]
            dis = []
            for j in range(len(case['npcList'])):
                # print("after random: npc {}: {}".format(j, case['npcList'][j]['start']['lane_position']['offset']))
                if case['ego']['start']['lane_position']['lane'] == case['npcList'][j]['start']['lane_position']['lane']:
                    dif_dis = np.abs(case['ego']['start']['lane_position']['offset'] - case['npcList'][j]['start']['lane_position']['offset'])
                    if dif_dis < 7.9:
                        print("checking!")
                    dis.append(dif_dis)
            print(dis)


if __name__ == "__main__":
    file_name = 'result1.json'
    with open(file_name) as f:
        data = json.load(f)
        testcase = TestCaseRandom(data)
        testcase.testcase_random(20)
        # print(testcase.cases[i])
