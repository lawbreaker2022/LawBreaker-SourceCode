import rtamt
import sys
import numpy as np
from TracePreprocess import Trace
import json
import copy
from EXtraction import ExtractAll
from AssertionExtraction import SingleAssertion
from shapely.geometry import Polygon, Point
import exception
from spec_coverage import failure_statement

inf_value = 1000

def polygon2polygon_distance(polygon_list1, polygon_list2):
    distance = []
    n = np.min(len(polygon_list1), len(polygon_list2))
    for i in range(n):
        if polygon_list1[i] == [] or polygon_list2 == []:
            distance.append(inf_value)
        else:
            polygon1 = Polygon(polygon_list1[i])
            polygon2 = Polygon(polygon_list2[i])
            distance.append(polygon1.distance(polygon2))
    return np.array(distance)


def polygon2point_distance(polygon_list, point):
    '''

    Args:
        p: [x, y]
        polygon_list: [p1, p2, p3]
        point: [x, y]
    Returns:

    '''
    distance = []
    p = Point(point)
    for i in range(len(polygon_list)):
        polygon = Polygon(polygon_list[i])
        distance.append(polygon.distance(p))
    return np.array(distance)


def velocitylist_distance(list1, list2):
    n = min(len(list1), len(list2))
    v1 = np.array(list1)[0:n, 0:2]
    v2 = np.array(list2)[0:n, 0:2]
    vel_dis = np.linalg.norm(v1 - v2, axis=1)
    return vel_dis


def velocitylist2point_distance(list1, velocity_point):
    v1 = np.array(list1)[:, 0:2]
    v_point = np.array(velocity_point)[0:2]
    vel_dis = np.linalg.norm(v1 - v_point, axis=1)
    return vel_dis


def acclist_distance(list1, list2):
    n = min(len(list1), len(list2))
    acc1 = np.array(list1)[0:n, 0:2]
    acc2 = np.array(list2)[0:n, 0:2]
    acc_dis = np.linalg.norm(acc1 - acc2, axis=1)
    return acc_dis


def acclist2point_distance(list1, acc_point):
    acc1 = np.array(list1)[:, 0:2]
    acc_point = np.array(acc_point)[0:2]
    acc_dis = np.linalg.norm(acc1 - acc_point, axis=1)
    return acc_dis


def speed_value(velocity_list):
    velocity_array = np.array(velocity_list)[:, 0:2]
    speed_array = np.linalg.norm(velocity_array, axis=1)
    return speed_array


def speedlist_distance(velocity_list1, velocity_list2):
    speed1 = speed_value(velocity_list1)
    speed2 = speed_value(velocity_list2)
    spd_dis = speed1 - speed2
    return spd_dis


def speedlist2point_distance(velocity_list, speed_point):
    speed = speed_value(velocity_list)
    spd_dis = speed - speed_point
    return spd_dis


class Monitor:
    def __init__(self, returned_msg, specification):
        self.specification = copy.deepcopy(specification)
        self.isGroundTruth = returned_msg['groundTruthPerception']
        self.original_data = copy.deepcopy(returned_msg['trace'])
        self.atom_data = dict()
        self.data = dict()
        self.c_data = dict()
        self.robustness_list = {}
        self.preprocessed_data = Trace(returned_msg)
        self.prepare_data()

    def prepare_data(self):
        self.prepare_distance_data()
        self.prepare_speed_data()
        self.prepare_velocity_data()
        self.prepare_acceleration_data()
        self.prepare_perception_data()
        self.final_data()
        self.continuous_data()

    def continuous_data(self):
        state_len = len(self.original_data)
        _data = self.preprocessed_data.trace['time']
        self.c_data['time'] = [[i, _data[i]] for i in range(state_len)]
        for var in self.specification.predicate_variable:
            _var_data = list(eval(self.specification.predicate_statement[var], self.atom_data))
            self.c_data[var] = [[_data[i], _var_data[i]] for i in range(state_len)]

    def final_data(self):
        state_len = len(self.original_data)
        self.data['time'] = [i for i in range(state_len)]
        self.data['t'] = self.preprocessed_data.trace['time']
        for var in self.specification.predicate_variable:
            try:
                self.data[var] = list(eval(self.specification.predicate_statement[var], self.atom_data))
            except TypeError:
                print("debugging")

    def prepare_distance_data(self):
        distance_statement = self.specification.dis_statement
        distance_variable = self.specification.dis_variables
        state_len = len(self.original_data)
        for item in distance_variable:
            self.atom_data[item] = []
            _item_statement = distance_statement[item]
            first_one = _item_statement[0]
            second_one = _item_statement[1]
            filter_first = {k: v for k, v in first_one.items() if v is not None}
            filter_second = {k: v for k, v in second_one.items() if v is not None}
            if len(filter_first) != 1 or len(filter_second) != 1:
                print("Declare proper elements to compute position distance!")
                exit()
            keys = list(filter_first.keys())[0] + "_" + list(filter_second.keys())[0]
            if keys == "ego_ego":
                self.atom_data[item] = np.array([0] * state_len)
            elif keys == "ego_agent":
                try:
                    self.atom_data[item] = np.array(self.preprocessed_data.distance['perception'][second_one['agent']])
                except KeyError:
                    print("check")
            elif keys == "ego_truth":
                self.atom_data[item] = np.array(self.preprocessed_data.distance['truth'][second_one['truth']])
            elif keys == "ego_position":
                ego_polygon_list = self.preprocessed_data.trace['ego']['shape']
                if second_one['position'][0] != "ENU":
                    exception.AssertionPositionError("The position should be translated to the ENU frame.")
                _point_position = second_one['position'][1][0:2]
                self.atom_data[item] = polygon2point_distance(ego_polygon_list, _point_position)
            elif keys == "agent_ego":
                _agent_name = filter_first['agent']
                self.atom_data[item] = np.array(self.preprocessed_data.distance['perception'][_agent_name])
            elif keys == "agent_agent":
                _agent1_polygon_list = self.preprocessed_data.trace['perception'][filter_first['agent']]['shape']
                _agent2_polygon_list = self.preprocessed_data.trace['perception'][filter_second['agent']]['shape']
                self.atom_data[item] = polygon2polygon_distance(_agent1_polygon_list, _agent2_polygon_list)
            elif keys == "agent_truth":
                _agent1_polygon_list = self.preprocessed_data.trace['perception'][filter_first['agent']]['shape']
                _agent2_polygon_list = self.preprocessed_data.trace['truth'][filter_second['agent']]['shape']
                self.atom_data[item] = polygon2polygon_distance(_agent1_polygon_list, _agent2_polygon_list)
            elif keys == "agent_position":
                _agent1_polygon_list = self.preprocessed_data.trace['perception'][filter_first['agent']]['shape']
                _point_position = second_one['position'][1][0:2]
                self.atom_data[item] = polygon2point_distance(_agent1_polygon_list, _point_position)
            elif keys == "truth_ego":
                _agent_name = filter_first['truth']
                self.atom_data[item] = np.array(self.preprocessed_data.distance['truth'][_agent_name])
            elif keys == "truth_agent":
                _agent1_polygon_list = self.preprocessed_data.trace['truth'][filter_first['agent']]['shape']
                _agent2_polygon_list = self.preprocessed_data.trace['perception'][filter_second['agent']]['shape']
                self.atom_data[item] = polygon2polygon_distance(_agent1_polygon_list, _agent2_polygon_list)
            elif keys == "truth_truth":
                _agent1_polygon_list = self.preprocessed_data.trace['truth'][filter_first['agent']]['shape']
                _agent2_polygon_list = self.preprocessed_data.trace['truth'][filter_second['agent']]['shape']
                self.atom_data[item] = polygon2polygon_distance(_agent1_polygon_list, _agent2_polygon_list)
            elif keys == "truth_position":
                _agent1_polygon_list = self.preprocessed_data.trace['truth'][filter_first['agent']]['shape']
                _point_position = second_one['position'][1][0:2]
                self.atom_data[item] = polygon2point_distance(_agent1_polygon_list, _point_position)
            elif keys == "position_ego":
                _point_position = filter_first['position'][1][0:2]
                ego_polygon_list = self.preprocessed_data.trace['ego']['shape']
                self.atom_data[item] = polygon2point_distance(ego_polygon_list, _point_position)
            elif keys == "position_agent":
                _point_position = filter_first['position'][1][0:2]
                _agent1_polygon_list = self.preprocessed_data.trace['truth'][second_one['agent']]['shape']
                self.atom_data[item] = polygon2point_distance(_agent1_polygon_list, _point_position)
            elif keys == "position_truth":
                _point_position = filter_first['position'][1][0:2]
                _agent1_polygon_list = self.preprocessed_data.trace['truth'][second_one['truth']]['shape']
                self.atom_data[item] = polygon2point_distance(_agent1_polygon_list, _point_position)
            elif keys == "position_position":
                _point_position1 = filter_first['position'][1][0:2]
                _point_position2 = filter_second['position'][1][0:2]
                self.atom_data[item] = np.array([np.linalg.norm(np.array(_point_position1) - np.array(_point_position2))]*state_len)
            else:
                print("Wrong distance element.")
                exit()

    def prepare_velocity_data(self):
        velocity_variable = self.specification.vel_variables
        velocity_statement = self.specification.vel_statement
        state_len = len(self.original_data)
        for item in velocity_variable:
            self.atom_data[item] = []
            _item_statement = velocity_statement[item]
            first_one = _item_statement[0]
            second_one = _item_statement[1]
            filter_first = {k: v for k, v in first_one.items() if v is not None}
            filter_second = {k: v for k, v in second_one.items() if v is not None}
            if len(filter_first) != 1 or len(filter_second) != 1:
                print("Declare proper elements to compute velocity distance!")
                exit()
            keys = list(filter_first.keys())[0] + "_" + list(filter_second.keys())[0]
            if keys == "ego_ego":
                self.atom_data[item] = np.array([0] * state_len)
            elif keys == "ego_agent":
                ego_velocity = self.preprocessed_data.trace['ego']['velocity']
                agent_name = second_one['agent']
                agent_velocity = self.preprocessed_data.trace['perception'][agent_name]['velocity']
                self.atom_data[item] = velocitylist_distance(ego_velocity, agent_velocity)
            elif keys == "ego_truth":
                ego_velocity = self.preprocessed_data.trace['ego']['velocity']
                agent_name = second_one['truth']
                agent_velocity = self.preprocessed_data.trace['truth'][agent_name]['velocity']
                self.atom_data[item] = velocitylist_distance(ego_velocity, agent_velocity)
            elif keys == "ego_velocity":
                ego_velocity = self.preprocessed_data.trace['ego']['velocity']
                _point_velocity = second_one['velocity']
                self.atom_data[item] = velocitylist2point_distance(ego_velocity, _point_velocity)
            elif keys == "agent_ego":
                agent_name = filter_first['agent']
                agent_velocity = self.preprocessed_data.trace['perception'][agent_name]['velocity']
                ego_velocity = self.preprocessed_data.trace['ego']['velocity']
                self.atom_data[item] = velocitylist_distance(agent_velocity, ego_velocity)
            elif keys == "agent_agent":
                agent_name1 = filter_first['agent']
                agent_name2 = filter_second['agent']
                agent1_velocity = self.preprocessed_data.trace['perception'][agent_name1]['velocity']
                agent2_velocity = self.preprocessed_data.trace['perception'][agent_name2]['velocity']
                self.atom_data[item] = velocitylist_distance(agent1_velocity, agent2_velocity)
            elif keys == "agent_truth":
                agent_name1 = filter_first['agent']
                agent_name2 = filter_second['agent']
                agent1_velocity = self.preprocessed_data.trace['perception'][agent_name1]['velocity']
                agent2_velocity = self.preprocessed_data.trace['truth'][agent_name2]['velocity']
                self.atom_data[item] = velocitylist_distance(agent1_velocity, agent2_velocity)
            elif keys == "agent_velocity":
                agent_name1 = filter_first['agent']
                agent1_velocity = self.preprocessed_data.trace['perception'][agent_name1]['velocity']
                _point_velocity = second_one['velocity']
                self.atom_data[item] = velocitylist2point_distance(agent1_velocity, _point_velocity)
            elif keys == "truth_ego":
                agent_name1 = filter_first['truth']
                agent1_velocity = self.preprocessed_data.trace['truth'][agent_name1]['velocity']
                ego_velocity = self.preprocessed_data.trace['ego']['velocity']
                self.atom_data[item] = velocitylist_distance(agent1_velocity, ego_velocity)
            elif keys == "truth_agent":
                agent_name1 = filter_first['truth']
                agent1_velocity = self.preprocessed_data.trace['truth'][agent_name1]['velocity']
                agent_name2 = filter_second['agent']
                agent2_velocity = self.preprocessed_data.trace['perception'][agent_name2]['velocity']
                self.atom_data[item] = velocitylist_distance(agent1_velocity, agent2_velocity)
            elif keys == "truth_truth":
                agent_name1 = filter_first['truth']
                agent1_velocity = self.preprocessed_data.trace['truth'][agent_name1]['velocity']
                agent_name2 = filter_second['truth']
                agent2_velocity = self.preprocessed_data.trace['truth'][agent_name2]['velocity']
                self.atom_data[item] = velocitylist_distance(agent1_velocity, agent2_velocity)
            elif keys == "truth_velocity":
                agent_name = filter_first['truth']
                agent_velocity = self.preprocessed_data.trace['truth'][agent_name]['velocity']
                _velocity_point = filter_second['velocity']
                self.atom_data[item] = velocitylist2point_distance(agent_velocity, _velocity_point)
            elif keys == "velocity_ego":
                velocity_point = filter_first['velocity']
                ego_velocity = self.preprocessed_data.trace['ego']['velocity']
                self.atom_data[item] = velocitylist2point_distance(ego_velocity, velocity_point)
            elif keys == "velocity_agent":
                velocity_point = filter_first['velocity']
                agent_name = filter_second['agent']
                agent_velocity = self.preprocessed_data.trace['perception'][agent_name]['velocity']
                self.atom_data[item] = velocitylist2point_distance(agent_velocity, velocity_point)
            elif keys == "velocity_truth":
                velocity_point = filter_first['velocity']
                agent_name = filter_second['truth']
                agent_velocity = self.preprocessed_data.trace['truth'][agent_name]['velocity']
                self.atom_data[item] = velocitylist2point_distance(agent_velocity, velocity_point)
            elif keys == "velocity_velocity":
                velocity_point1 = filter_first['velocity']
                velocity_point2 = filter_second['velocity']
                self.atom_data[item] = np.array([np.linalg.norm(np.array(velocity_point1)[0:2] - np.array(velocity_point2)[0:2])]*state_len)
            else:
                print("Wrong velocity element.")
                exit()

    def prepare_acceleration_data(self):
        acceleration_variable = self.specification.acc_variables
        acceleration_statement = self.specification.acc_statement
        state_len = len(self.original_data)
        for item in acceleration_variable:
            self.atom_data[item] = []
            _item_statement = acceleration_statement[item]
            first_one = _item_statement[0]
            second_one = _item_statement[1]
            filter_first = {k: v for k, v in first_one.items() if v is not None}
            filter_second = {k: v for k, v in second_one.items() if v is not None}
            if len(filter_first) != 1 or len(filter_second) != 1:
                print("Declare proper elements to compute acceleration distance!")
                exit()
            keys = list(filter_first.keys())[0] + "_" + list(filter_second.keys())[0]
            if keys == "ego_ego":
                self.atom_data[item] = np.array([0] * state_len)
            elif keys == "ego_agent":
                ego_acceleration = self.preprocessed_data.trace['ego']['acceleration']
                agent_name = second_one['agent']
                agent_acceleration = self.preprocessed_data.trace['perception'][agent_name]['acceleration']
                self.atom_data[item] = acclist_distance(ego_acceleration, agent_acceleration)
            elif keys == "ego_truth":
                ego_acceleration = self.preprocessed_data.trace['ego']['acceleration']
                agent_name = second_one['truth']
                agent_acceleration = self.preprocessed_data.trace['truth'][agent_name]['acceleration']
                self.atom_data[item] = acclist_distance(ego_acceleration, agent_acceleration)
            elif keys == "ego_acceleration":
                ego_acceleration = self.preprocessed_data.trace['ego']['acceleration']
                _point_acceleration = second_one['acceleration']
                self.atom_data[item] = acclist2point_distance(ego_acceleration, _point_acceleration)
            elif keys == "agent_ego":
                agent_name = filter_first['agent']
                agent_acceleration = self.preprocessed_data.trace['perception'][agent_name]['acceleration']
                ego_acceleration = self.preprocessed_data.trace['ego']['acceleration']
                self.atom_data[item] = acclist_distance(agent_acceleration, ego_acceleration)
            elif keys == "agent_agent":
                agent_name1 = filter_first['agent']
                agent_name2 = filter_second['agent']
                agent1_acceleration = self.preprocessed_data.trace['perception'][agent_name1]['acceleration']
                agent2_acceleration = self.preprocessed_data.trace['perception'][agent_name2]['acceleration']
                self.atom_data[item] = acclist_distance(agent1_acceleration, agent2_acceleration)
            elif keys == "agent_truth":
                agent_name1 = filter_first['agent']
                agent_name2 = filter_second['agent']
                agent1_acceleration = self.preprocessed_data.trace['perception'][agent_name1]['acceleration']
                agent2_acceleration = self.preprocessed_data.trace['truth'][agent_name2]['acceleration']
                self.atom_data[item] = acclist_distance(agent1_acceleration, agent2_acceleration)
            elif keys == "agent_acceleration":
                agent_name1 = filter_first['agent']
                agent1_acceleration = self.preprocessed_data.trace['perception'][agent_name1]['acceleration']
                _point_acceleration = second_one['acceleration']
                self.atom_data[item] = acclist2point_distance(agent1_acceleration, _point_acceleration)
            elif keys == "truth_ego":
                agent_name1 = filter_first['truth']
                agent1_acceleration = self.preprocessed_data.trace['truth'][agent_name1]['acceleration']
                ego_acceleration = self.preprocessed_data.trace['ego']['acceleration']
                self.atom_data[item] = acclist_distance(agent1_acceleration, ego_acceleration)
            elif keys == "truth_agent":
                agent_name1 = filter_first['truth']
                agent1_acceleration = self.preprocessed_data.trace['truth'][agent_name1]['acceleration']
                agent_name2 = filter_second['agent']
                agent2_acceleration = self.preprocessed_data.trace['perception'][agent_name2]['acceleration']
                self.atom_data[item] = acclist_distance(agent1_acceleration, agent2_acceleration)
            elif keys == "truth_truth":
                agent_name1 = filter_first['truth']
                agent1_acceleration = self.preprocessed_data.trace['truth'][agent_name1]['acceleration']
                agent_name2 = filter_second['truth']
                agent2_acceleration = self.preprocessed_data.trace['truth'][agent_name2]['acceleration']
                self.atom_data[item] = acclist_distance(agent1_acceleration, agent2_acceleration)
            elif keys == "truth_acceleration":
                agent_name = filter_first['truth']
                agent_acceleration = self.preprocessed_data.trace['truth'][agent_name]['acceleration']
                acceleration_point = filter_second['acceleration']
                self.atom_data[item] = acclist2point_distance(agent_acceleration, acceleration_point)
            elif keys == "acceleration_ego":
                acceleration_point = filter_first['acceleration']
                ego_acceleration = self.preprocessed_data.trace['ego']['acceleration']
                self.atom_data[item] = acclist2point_distance(ego_acceleration, acceleration_point)
            elif keys == "acceleration_agent":
                acceleration_point = filter_first['acceleration']
                agent_name = filter_second['agent']
                agent_acceleration = self.preprocessed_data.trace['perception'][agent_name]['acceleration']
                self.atom_data[item] = acclist2point_distance(agent_acceleration, acceleration_point)
            elif keys == "acceleration_truth":
                acceleration_point = filter_first['acceleration']
                agent_name = filter_second['truth']
                agent_acceleration = self.preprocessed_data.trace['truth'][agent_name]['acceleration']
                self.atom_data[item] = acclist2point_distance(agent_acceleration, acceleration_point)
            elif keys == "acceleration_acceleration":
                acceleration_point1 = filter_first['acceleration']
                acceleration_point2 = filter_second['acceleration']
                self.atom_data[item] = np.array([np.linalg.norm(np.array(acceleration_point1)[0:2] - np.array(acceleration_point2)[0:2])]*state_len)
            else:
                print("Wrong acceleration element.")
                exit()

    def prepare_speed_data(self):
        speed_variable = self.specification.spd_variables
        speed_statement = self.specification.spd_statement
        state_len = len(self.original_data)
        for item in speed_variable:
            self.atom_data[item] = []
            _item_statement = speed_statement[item]
            first_one = _item_statement[0]
            second_one = _item_statement[1]
            filter_first = {k: v for k, v in first_one.items() if v is not None}
            filter_second = {k: v for k, v in second_one.items() if v is not None}
            if len(filter_first) != 1 or len(filter_second) != 1:
                print("Declare proper elements to compute speed distance!")
                exit()
            keys = list(filter_first.keys())[0] + "_" + list(filter_second.keys())[0]
            if keys == "ego_ego":
                self.atom_data[item] = np.array([0] * state_len)
            elif keys == "ego_agent":
                ego_velocity = self.preprocessed_data.trace['ego']['velocity']
                agent_name = second_one['agent']
                agent_velocity = self.preprocessed_data.trace['perception'][agent_name]['velocity']
                self.atom_data[item] = speedlist_distance(ego_velocity, agent_velocity)
            elif keys == "ego_truth":
                ego_velocity = self.preprocessed_data.trace['ego']['velocity']
                agent_name = second_one['truth']
                agent_velocity = self.preprocessed_data.trace['truth'][agent_name]['velocity']
                self.atom_data[item] = speedlist_distance(ego_velocity, agent_velocity)
            elif keys == "ego_speed":
                ego_velocity = self.preprocessed_data.trace['ego']['velocity']
                point_speed = second_one['speed']
                self.atom_data[item] = speed_value(ego_velocity) - point_speed
            elif keys == "agent_ego":
                agent_name = filter_first['agent']
                agent_velocity = self.preprocessed_data.trace['perception'][agent_name]['velocity']
                ego_velocity = self.preprocessed_data.trace['ego']['velocity']
                self.atom_data[item] = speedlist_distance(agent_velocity, ego_velocity)
            elif keys == "agent_agent":
                agent_name1 = filter_first['agent']
                agent_name2 = filter_second['agent']
                agent1_velocity = self.preprocessed_data.trace['perception'][agent_name1]['velocity']
                agent2_velocity = self.preprocessed_data.trace['perception'][agent_name2]['velocity']
                self.atom_data[item] = speedlist_distance(agent1_velocity, agent2_velocity)
            elif keys == "agent_truth":
                agent_name1 = filter_first['agent']
                agent_name2 = filter_second['agent']
                agent1_velocity = self.preprocessed_data.trace['perception'][agent_name1]['velocity']
                agent2_velocity = self.preprocessed_data.trace['truth'][agent_name2]['velocity']
                self.atom_data[item] = speedlist_distance(agent1_velocity, agent2_velocity)
            elif keys == "agent_speed":
                agent_name1 = filter_first['agent']
                agent1_velocity = self.preprocessed_data.trace['perception'][agent_name1]['velocity']
                point_speed = second_one['speed']
                self.atom_data[item] = speed_value(agent1_velocity) - point_speed
            elif keys == "truth_ego":
                agent_name1 = filter_first['truth']
                agent1_velocity = self.preprocessed_data.trace['truth'][agent_name1]['velocity']
                ego_velocity = self.preprocessed_data.trace['ego']['velocity']
                self.atom_data[item] = speedlist_distance(agent1_velocity, ego_velocity)
            elif keys == "truth_agent":
                agent_name1 = filter_first['truth']
                agent1_velocity = self.preprocessed_data.trace['truth'][agent_name1]['velocity']
                agent_name2 = filter_second['agent']
                agent2_velocity = self.preprocessed_data.trace['perception'][agent_name2]['velocity']
                self.atom_data[item] = speedlist_distance(agent1_velocity, agent2_velocity)
            elif keys == "truth_truth":
                agent_name1 = filter_first['truth']
                agent1_velocity = self.preprocessed_data.trace['truth'][agent_name1]['velocity']
                agent_name2 = filter_second['truth']
                agent2_velocity = self.preprocessed_data.trace['truth'][agent_name2]['velocity']
                self.atom_data[item] = speedlist_distance(agent1_velocity, agent2_velocity)
            elif keys == "truth_speed":
                agent_name = filter_first['truth']
                agent_velocity = self.preprocessed_data.trace['truth'][agent_name]['speed']
                speed_point = filter_second['speed']
                self.atom_data[item] = speed_value(agent_velocity) - speed_point
            elif keys == "speed_ego":
                speed_point = filter_first['speed']
                ego_velocity = self.preprocessed_data.trace['ego']['velocity']
                self.atom_data[item] = speed_point - speed_value(ego_velocity)
            elif keys == "speed_agent":
                speed_point = filter_first['speed']
                agent_name = filter_second['agent']
                agent_velocity = self.preprocessed_data.trace['perception'][agent_name]['velocity']
                self.atom_data[item] = speed_point - speed_value(agent_velocity)
            elif keys == "speed_truth":
                speed_point = filter_first['speed']
                agent_name = filter_second['truth']
                agent_velocity = self.preprocessed_data.trace['truth'][agent_name]['velocity']
                self.atom_data[item] = speed_point - speed_value(agent_velocity)
            elif keys == "speed_speed":
                speed_point1 = filter_first['speed']
                speed_point2 = filter_second['speed']
                self.atom_data[item] = np.array([speed_point1 - speed_point2]*state_len)
            else:
                print("Wrong speed element.")
                exit()

    def prepare_perception_data(self):
        perception_variable = self.specification.diff_variables
        perception_statement = self.specification.diff_statement
        state_len = len(self.original_data)
        with open('config.json') as f:
            _config = json.load(f)
            weight = _config['diff_weight']
            weight_dis = weight['dis_w']
            weight_vel = weight['vel_w']
            weight_heading = weight['heading_w']
            weight_shape = weight['shape_w']

        for item in perception_variable:
            diff_agent = perception_statement[item]
            diff_data = self.preprocessed_data.perception_diff[diff_agent]
            diff_position = np.array(diff_data['position'])
            diff_velocity = np.array(diff_data['velocity'])
            diff_heading = np.array(diff_data['heading'])
            diff_shape = np.array(diff_data['shape'])
            self.atom_data[item] = (diff_velocity*weight_vel + diff_position*weight_dis +
                                    diff_heading*weight_heading + diff_shape*weight_shape)/(weight_dis + weight_vel + weight_heading + weight_shape)

    def discrete_monitor(self):
        spec = rtamt.STLSpecification(semantics=rtamt.Semantics.STANDARD)
        for item in self.specification.predicate_variable:
            spec.declare_var(item, 'float')
        spec.spec = self.specification.translated_statement

        try:
            spec.parse()
        except rtamt.STLParseException as err:
            print('STL Parse Exception: {}'.format(err))
            sys.exit()

        rob = spec.evaluate(self.data)
        return rob[0][1]
        # min_robustness = np.array(rob)[:, 1].min()
        # # print('Standard robustness: ' + str(rob))
        # return min_robustness

    def continuous_monitor(self):
        spec = rtamt.STLDenseTimeSpecification(semantics=rtamt.Semantics.STANDARD)
        for item in self.specification.predicate_variable:
            spec.declare_var(item, 'float')
        spec.spec = self.specification.translated_statement
        try:
            spec.parse()
            # spec.pastify()
        except rtamt.STLParseException as err:
            print('STL Parse Exception: {}'.format(err))
            sys.exit()

        _data = [[var, self.c_data[var]] for var in self.specification.predicate_variable]
        rob = spec.evaluate(*_data)
        return rob[0][1]

    def coverage_monitor(self):
        spec_str = self.specification.translated_statement
        spec_parser = failure_statement(spec_str)
        failure_statement_list = spec_parser.neg_predicate()
        covered_statement_list = []
        for i in range(len(failure_statement_list)):
            spec = rtamt.STLDenseTimeSpecification(semantics=rtamt.Semantics.STANDARD)
            for item in self.specification.predicate_variable:
                spec.declare_var(item, 'float')
            spec.spec = failure_statement_list[i]
            try:
                spec.parse()
                # spec.pastify()
            except rtamt.STLParseException as err:
                print('STL Parse Exception: {}'.format(err))
                sys.exit()

            _data = [[var, self.c_data[var]] for var in self.specification.predicate_variable]
            rob = spec.evaluate(*_data)
            if rob[0][1] > 0:
                covered_statement_list.append(failure_statement_list[i])
        coverage_rate = len(covered_statement_list) / len(failure_statement_list)
        return coverage_rate, covered_statement_list, failure_statement_list


if __name__ == "__main__":
    polygon_list_test = [[[552825.7382552056, 4183199.635237372], [552826.9335539752, 4183201.3129920773], [552830.7614409243, 4183198.585854108], [552829.5661421546, 4183196.9080994027]]]
    point_test = [552824.8724093935, 4183201.008688295]
    point_test1 = [552826.17, 4183200.08]
    dis_test = np.linalg.norm(np.array(point_test1) - np.array(point_test))
    print(dis_test)
    print(polygon2point_distance(polygon_list_test, point_test))

    # input_file = 'test_cases/input-test.txt'
    input_file = 'test_cases/final/intersection2.txt'
    # input_file = 'test_cases/intersection/intersection1.txt'
    isGroundTruth = True
    extracted_script = ExtractAll(input_file,isGroundTruth)
    scenario_spec = extracted_script.Get_Specifications()
    all_agents = extracted_script.Get_AllAgents()
    output_file = 'data/result01.json'
    with open(output_file) as f:
        data = json.load(f)  # read as a msg from apollo via websocket
        scenario_name = data['ScenarioName']
        single_spec = SingleAssertion(scenario_spec[scenario_name][0], "san_francisco")
        monitor = Monitor(data, single_spec)
        value = monitor.discrete_monitor()
        print(value)
        coverage_rate, coverage_predicate, _ = monitor.coverage_monitor()
        for spec_index in range(len(scenario_spec[scenario_name])):
            single_spec = SingleAssertion(scenario_spec[scenario_name][spec_index], "san_francisco")  # the first specification in scenario0
            print(single_spec.translated_statement)
            print(single_spec.atom_statement_variable_mapping)
            monitor = Monitor(data, single_spec)
            min_value = monitor.discrete_monitor()
            print("Specification {}: Minimal robustness: {}".format(spec_index, min_value))
            value2 = monitor.continuous_monitor()
            print(value2)
    #     print(type(data))
    #     scenarioName = data['ScenarioName']
    #     agents = all_agents[scenarioName]
    #     trace_data = Trace(data, agents)
    #     spec = scenario_spec[scenarioName]
    #     monitor = DiscreteMonitor1(trace_data, spec)
    #     monitor.fitness()
    #     print(monitor.robustness_list)
