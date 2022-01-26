import copy
import random
import sys
from typing import List
import numpy as np
from parser.ast import AST, ASTDumper, Parse
import json
from json import JSONEncoder
import warnings
import math
from config import get_npc_list, get_pedestrian_list, get_ego_list, get_map_list, get_weather_list
from map import get_map_info
from pedestrian_motion_checking import nearest
import exception

npc_list = get_npc_list()
pedestrian_list = get_pedestrian_list()
map_list = get_map_list()
ego_list = get_ego_list()
weather_list = get_weather_list()

offset_offset = 2.0

class Vector3D:
    def __init__(self, x, y, z=10.124655723571777):
        self.x = x
        self.y = y
        self.z = z


class Vector4D:
    def __init__(self, qx=0.0, qy=0.0, qz=0.0, qw=1.0):
        self.qx = qx
        self.qy = qy
        self.qz = qz
        self.qw = qw


class Heading:
    def __init__(self, reference_position=None, reference_angle=0.0):
        self.ref_point = reference_position
        self.ref_angle = reference_angle  # unit: deg


class Heading_Lane:
    def __init__(self, ref_lane_position=None, ref_angle=0.0):
        self.ref_lane_point = ref_lane_position
        self.ref_angle = ref_angle


class PositionState:
    def __init__(self, position, heading=0.0, speed=0.0):
        self.position = position
        self.heading = heading
        self.speed = speed


class LaneState:
    def __init__(self, position, heading=None, speed=0.0):
        self.lane_position = position
        self.heading = heading
        self.speed = speed


class LanePosition:
    def __init__(self, laneID, distance=0, roadID=None):
        self.lane = laneID
        self.offset = distance
        self.roadID = roadID


class EgoVehicle:
    def __init__(self, identifier=None, name=None, start=None, destination=None, color=None, useGroundTruth=True):
        self.ID = identifier
        self.name = name
        self.groundTruthPerception = useGroundTruth
        self.color = color
        self.start = start
        self.destination = destination


class NPCVehicle:
    def __init__(self, identifier, name, start_state, motion=[], end_position=None, color=None):
        self.ID = identifier
        self.name = name
        self.color = color
        self.start = start_state
        self.motion = motion
        self.destination = end_position


class Pedestrian:
    def __init__(self, identifier=None, name=None, start_state=None, motion=[], end_position=None, height=None,
                 color=None, is_randomwalk=True):
        self.ID = identifier
        self.name = name
        self.start = start_state
        self.motion = motion
        self.destination = end_position
        self.height = height
        self.color = color
        self.random_walk = is_randomwalk

class Obstacle:
    def __init__(self, identifer=None, position=None, shape=None):
        self.ID = identifer
        self.position = position
        self.shape = shape


class ScenarioElements:
    def __init__(self, scenario, isGroundTruth):
        self.scenario = scenario
        self.ScenarioName = None
        self.MapVariable = None
        self.MapName = None
        self.EgoVariable = None
        self.EgoType = None
        self.EgoColor = None
        self.EgoInitialState = None
        self.EgoTargetState = None  # State(Vector3D(553093.05225720361, 4182687.8989561526), 0.0, 0.0)
        self.ego = EgoVehicle(identifier=self.EgoVariable, name=self.EgoType, start=self.EgoInitialState,
                              destination=self.EgoTargetState, color=self.EgoColor, useGroundTruth=isGroundTruth)
        self.NPCNumber = 0
        self.NPCs = []
        self.PedestrianNumber = 0
        self.pedestrians = []
        self.ObsNumber = 0
        self.obstacles = []
        self.AgentName = []
        self.time = {}
        self.weather = {}
        self.extraction()

    def _state_extract(self, state):
        # Get position
        map_info = get_map_info(self.MapName)
        position_type = '3D'
        raw_position = state.get_position()
        _ref_position = (0, 0, 0)
        if raw_position.has_frame():
            _cf_value = str(raw_position.get_frame())
            if "IMU" in _cf_value:
                if self.EgoInitialState is None:
                    exception.FrameError("For IMU frame, please define the initial position of the ego vehicle.")
                _frame = "IMU"
                if type(self.EgoInitialState) == LaneState:
                    ego_position = self.EgoInitialState.lane_position
                    _ref_position = map_info.get_position([ego_position.lane, ego_position.offset])
                else:
                    ego_position = self.EgoInitialState.position
                    _ref_position = (ego_position.x, ego_position.y, ego_position.z)
                if raw_position.is_normal_coordinate():
                    _local_coordinate = raw_position.get_coordinate()
                    _new_position = map_info.get_global_position((_ref_position[0], _ref_position[1]), (_local_coordinate.get_x(), _local_coordinate.get_y()))
                    if _local_coordinate.has_z():
                        # position = Vector3D(_local_coordinate.get_x()+_ref_position[0], _local_coordinate.get_y()+_ref_position[1], _local_coordinate.get_z()+_ref_position[2])
                        position = Vector3D(_new_position[0], _new_position[1], _local_coordinate.get_z()+_ref_position[2])
                    else:
                        # position = Vector3D(_local_coordinate.get_x()+_ref_position[0], _local_coordinate.get_y()+_ref_position[1], +_ref_position[2])
                        position = Vector3D(_new_position[0], _new_position[1], +_ref_position[2])
            elif "WGS84" in _cf_value:
                _frame = "WGS84"
                exception.Error("The current version does not suppose WGS84 frame.")
            else:
                _local_coordinate = raw_position.get_coordinate()
                if _local_coordinate.has_z():
                    position = Vector3D(_local_coordinate.get_x(), _local_coordinate.get_y(), _local_coordinate.get_z())
                else:
                    position = Vector3D(_local_coordinate.get_x(), _local_coordinate.get_y(), 0)
        else:
            if raw_position.is_normal_coordinate():
                _local_coordinate = raw_position.get_coordinate()
                if _local_coordinate.has_z():
                    position = Vector3D(_local_coordinate.get_x(), _local_coordinate.get_y(), _local_coordinate.get_z())
                else:
                    position = Vector3D(_local_coordinate.get_x(), _local_coordinate.get_y(), 0)
            elif raw_position.is_relative_coordinate():
                position_type = 'lane'
                distance2start = raw_position.get_coordinate().get_distance()
                laneID_str = raw_position.get_coordinate().get_lane().get_lane_id()
                if "." in laneID_str:
                    roadID = None
                    if laneID_str.split(".")[0] != "":
                        roadID = laneID_str.split(".")[0]
                    laneID = laneID_str.split(".")[1]
                    position = LanePosition(laneID, distance2start, roadID)
                else:
                    laneID = laneID_str
                    position = LanePosition(laneID, distance2start)

        # Get heading values with respect to the lane direction at ego vehicle's initial position
        # heading = Heading()
        if state.has_heading():
            raw_heading = state.get_heading()
            # retrieve the relative degree in the given statement
            _ref_angle = 0.0
            if raw_heading.is_heading_DEG():
                if raw_heading.is_pi_value():
                    key = input("PI value is used, do you really mean to set the unit as \"degree\"? (y/n)")
                    if key == 'y' or 'Y' or 'yes' or 'YES':
                        _ref_angle = raw_heading.get_raw_heading_angle() * math.pi
                    else:
                        _ref_angle = raw_heading.get_raw_heading_angle() *180.0
                else:
                    _ref_angle = raw_heading.get_raw_heading_angle()
            elif raw_heading.is_heading_RAD():
                if raw_heading.is_pi_value():
                    _ref_angle = raw_heading.get_raw_heading_angle() * 180.0
                else:
                    _ref_angle = raw_heading.get_raw_heading_angle() * 180.0 / math.pi

            if raw_heading.has_direction():
                direction = raw_heading.get_direction()
                if direction.is_default_ego():
                    ego_angle = self.EgoInitialState.heading.ref_angle
                    _ref_angle += ego_angle
                    _ref_point = self.ego.start.heading.ref_point
                elif direction.is_lane_reference():
                    _reference_point = direction.get_lane_reference()
                    _ref_point = LanePosition(laneID=_reference_point[0].get_lane_id(), distance=_reference_point[1])
                else:
                    relative_object = direction.get_reference().get_name()
                    if relative_object == self.EgoVariable:
                        ego_angle = self.EgoInitialState.heading.ref_angle
                        _ref_angle += ego_angle
                        _ref_point = self.ego.start.heading.ref_point
                    elif direction.is_lane_reference():
                        lane_reference = direction.get_lane_reference()
                        lane_id = lane_reference[0].get_lane_id()
                        lane_distance = lane_reference[1]
                        _ref_point = LanePosition(lane_id, lane_distance)
                    else:
                        if relative_object in self.AgentName:
                            for _index in range(len(self.NPCs)):
                                if relative_object == self.NPCs[_index].ID:
                                    _ref_point = self.NPCs[_index].start.heading.ref_point
                                    # if relative_position is None:
                                    #     try:
                                    #         relative_position = self.NPCs[_index].start.position
                                    #     except AttributeError:
                                    #         relative_position = self.NPCs[_index].start.lane_position
                                    _ref_angle += self.NPCs[_index].start.heading.ref_angle
                                    break
            else:
                _ref_point = position
        else:
            _ref_angle = 0.0
            _ref_point = position
        if type(_ref_point).__name__ == 'Vector3D':
            heading = Heading(_ref_point, _ref_angle)
        elif type(_ref_point).__name__ == 'LanePosition':
            heading = Heading_Lane(_ref_point, _ref_angle)
        else:
            raise Exception("The reference point must be in a type of 3D vector or lane position!")

        # retrieve speed
        if state.has_speed():
            raw_speed = state.get_speed()
            speed = raw_speed.get_speed_value()
        else:
            speed = 0.0  # default value

        if position_type == '3D':
            return PositionState(position, heading, speed)
        elif position_type == 'lane':
            return LaneState(position, heading, speed)

    def _motion_extract(self, motion_object):
        _motion = []
        if motion_object.is_waypoint_motion():
            waypoint_motion_object = motion_object.get_motion()
            state_list_obj = waypoint_motion_object.get_state_list()
            for _i in range(state_list_obj.get_size()):
                state_list = state_list_obj.get_states()
                waypoint_element = self._state_extract(state_list[_i])
                _motion.append(waypoint_element)
            return 'waypoint', _motion
        else:
            uniform_motion_object = motion_object.get_motion()
            _state = uniform_motion_object.get_state()
            _state_ref = self._state_extract(_state)
            return 'uniform', _state_ref

    def _type_extract(self, type_object):
        type_str = None
        color = None
        _type = type_object.get_type()
        if type_object.is_specific_type():
            type_str = type_object.get_type().get_value()
        elif type_object.is_general_type():
            # todo
            type_str = type_object.get_type().get_kind()
        if type_object.is_rgb_color():
            color = type_object.get_color().get_value()
        elif type_object.is_color_list():
            rgb_list = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0), (255, 255, 255)]
            color = rgb_list[type_object.get_color().get_kind()]
        return type_str, color

    def get_map(self):
        _map = self.scenario.get_map()
        self.MapVariable = _map.get_name()
        self.MapName = _map.get_map_name()

    def _get_weather_kind(self, weather):
        weather_kind = str(weather.get_weather_kind())
        # if 'SUNNY' in weather_kind:
        #     weather_kind = 'sunny'
        if 'RAIN' in weather_kind:
            weather_kind = 'rain'
        # elif 'SNOW' in weather_kind:
        #     weather_kind = 'snow'
        elif 'FOG' in weather_kind:
            weather_kind = 'fog'
        elif 'WETNESS' in weather_kind:
            weather_kind = 'wetness'
        else:
            warnings.warn("The weather kind is not defined or not in the predefined kind list, set to default sunny weather.")
            weather_kind = 'sunny'
        return weather_kind

    def _get_weather_value(self, weather):
        if weather.is_weather_continuous_index():
            value = weather.get_weather_kind_value().get_index()
        elif weather.is_weather_discrete_level():
            value = str(weather.get_weather_kind_value().get_level())
            if 'LIGHT' in value:
                value = 0.1
            elif 'MIDDLE' in value:
                value = 0.5
            elif 'HEAVY' in value:
                value = 0.8
            else:
                warnings.warn("The discrete level is not in the predefined levels, set to default value 0.")
                value = 0.0
        else:
            warnings.warn("The discrete level is not in the predefined levels, set to default value 0.")
            value = 0.0
        return value

    def get_environment(self):
        if self.scenario.has_environment():
            env = self.scenario.get_environment()
            time_obj = env.get_time()
            self.time = {'hour': time_obj.get_hour(), 'minute': time_obj.get_minute()}
            weather_obj = env.get_weathers()
            for i in range(weather_obj.get_size()):
                weather = weather_obj.get_weathers()[i]
                weather_kind = self._get_weather_kind(weather)
                value = self._get_weather_value(weather)
                self.weather[weather_kind] = value

    def get_ego(self):
        _ego = self.scenario.get_ego_vehicle()
        self.EgoVariable = _ego.get_name()
        if _ego.has_vehicle_type():
            _type = _ego.get_vehicle_type()
            self.EgoType, self.EgoColor = self._type_extract(_type)
        _init_state = _ego.get_first_state()
        self.EgoInitialState = self._state_extract(_init_state)
        _ego_target_state = _ego.get_second_state()
        self.EgoTargetState = self._state_extract(_ego_target_state)
        self.ego.ID = self.EgoVariable
        self.ego.name = self.EgoType
        self.ego.start = self.EgoInitialState
        self.ego.destination = self.EgoTargetState
        self.ego.color = self.EgoColor

    def single_npc_extract(self, npc_object):
        _identifier = npc_object.get_name()
        if npc_object.has_vehicle_type():
            type_object = npc_object.get_vehicle_type()
            _name, _color = self._type_extract(type_object)
        else:
            _name, _color = None, None
        first_state_object = npc_object.get_first_state()
        _start_state = self._state_extract(first_state_object)
        if npc_object.has_second_state():
            end_state_object = npc_object.get_second_state()
            _destination_state = self._state_extract(end_state_object)
        else:
            _destination_state = None
        _motion = []
        if npc_object.has_vehicle_motion():
            _motion_obj = npc_object.get_vehicle_motion()
            _motion_type, _motion = self._motion_extract(_motion_obj)
            if _motion_type == 'uniform':
                warnings.warn("reset initial speed to {}".format(_motion.speed))
                _start_state.speed = _motion.speed
                _motion = []
        return NPCVehicle(_identifier, _name, _start_state, _motion, _destination_state, color=_color)

    def get_npcs(self):
        if self.scenario.has_npc_vehicles():
            npcs_object = self.scenario.get_npc_vehicles()
            self.NPCNumber = npcs_object.get_size()
            npclist_object = npcs_object.get_npc_vehicles()
            for i in range(npcs_object.get_size()):
                npc_i = self.single_npc_extract(npclist_object[i])
                self.NPCs.append(npc_i)
                self.AgentName.append(npc_i.ID)

    def single_ped_extraction(self, pedestrian_obj):
        _ped_obj = pedestrian_obj
        single_pedestrian = Pedestrian()
        single_pedestrian.ID = _ped_obj.get_name()
        _first_state = _ped_obj.get_first_state()
        single_pedestrian.start = self._state_extract(_first_state)
        if _ped_obj.has_second_state():
            single_pedestrian.random_walk = False
            _end_state = _ped_obj.get_second_state()
            single_pedestrian.destination = self._state_extract(_end_state)
        if _ped_obj.has_pedestrian_motion():
            single_pedestrian.random_walk = False
            _motion_obj = _ped_obj.get_pedestrian_motion()
            _motion_type, _motion = self._motion_extract(_motion_obj)
            if _motion_type == 'uniform':
                warnings.warn("reset initial speed to {}".format(_motion.speed))
                single_pedestrian.start.speed = _motion.speed
            elif _motion_type == 'waypoint':
                single_pedestrian.motion = _motion
        if _ped_obj.has_pedestrian_type():
            # todo: will add specific type
            _ped_type = _ped_obj.get_pedestrian_type()
            _height = _ped_type.get_height()
            single_pedestrian.height = _height.get_value()
            if _ped_type.is_rgb_color():
                _color = _ped_type.get_color().get_value()
                single_pedestrian.color = _color
            if _ped_type.is_color_list():
                rgb_list = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0), (255, 255, 255)]
                _color = rgb_list[_ped_type.get_color().get_kind()]
                single_pedestrian.color = _color
        return single_pedestrian

    def get_peds(self):
        if self.scenario.has_pedestrians():
            peds_obj = self.scenario.get_pedestrians()
            self.PedestrianNumber = peds_obj.get_size()
            ped_obj_list = peds_obj.get_pedestrians()
            for _i in range(peds_obj.get_size()):
                ped_i = self.single_ped_extraction(ped_obj_list[_i])
                self.pedestrians.append(ped_i)
                self.AgentName.append(ped_i.ID)

    def single_obs_extraction(self, obs_obj):
        _obs_obj = obs_obj
        name = _obs_obj.get_name()
        position = _obs_obj.get_position()
        if _obs_obj.has_shape():
            shape = _obs_obj.get_shape()
        else:
            shape = None
        return Obstacle(identifer=name, position=position, shape=shape)


    def get_obss(self):
        if self.scenario.has_obstacles():
            obss_obj = self.scenario.get_obstacles().get_obstacles()
            for _i in range(len(obss_obj)):
                obs_obj = obss_obj[_i]
                _obs_i = self.single_obs_extraction(obs_obj)
                self.obstacles.append(_obs_i)
                self.AgentName.append(_obs_i.ID)

    def extraction(self):
        self.ScenarioName = self.scenario.get_name()
        self.get_map()
        self.get_environment()
        self.get_ego()
        self.get_npcs()
        self.get_peds()
        self.get_obss()



def custom_formatwarning(msg, *args, **kwargs):
    # ignore everything except the message
    return "Warning: " + str(msg) + '\n'


warnings.formatwarning = custom_formatwarning


class LGSVLAdapter:
    def __init__(self, scenario_object):
        self.ScenarioName = scenario_object.ScenarioName
        self.MapVariable = scenario_object.MapVariable
        self.MapName = scenario_object.MapName
        self.time = scenario_object.time
        self.weather = scenario_object.weather
        self.ego = scenario_object.ego
        self.NPCNumber = scenario_object.NPCNumber
        self.NPCs = scenario_object.NPCs
        self.PedestrianNumber = scenario_object.PedestrianNumber
        self.pedestrians = scenario_object.pedestrians
        self.ObsNumber = scenario_object.ObsNumber
        self.obstacles = scenario_object.obstacles
        self.AgentName = scenario_object.AgentName
        self.check()

    def check_map(self):
        if self.MapName is None:
            self.MapName = "san_francisco_roadonly"
            warnings.warn("There is no map or wrong map specified, set to \"san_francisco_roadonly\"")
        elif self.MapName not in map_list:
            self.MapName = map_list[0]
            warnings.warn("The current supported maps are {}, "
                          "set to {}.".format(map_list, map_list[0]))

    def check_time(self):
        _time = self.time
        self.time = {'hour': 12, 'minute': 0}
        if _time != {}:
            self.time['hour'] = int(np.clip(_time['hour'], 0, 23))
            self.time['minute'] = int(np.clip(_time['minute'], 0, 59))

    def check_weather(self):
        _weather = self.weather
        for key in weather_list:
            self.weather[key] = 0.0
        # self.weather = {'rain': 0.0, 'fog': 0.0, 'wetness': 0.0} #'cloudiness': 0.0, 'damage': 0.0
        if self.weather != {}:
            for item in _weather.keys():
                if item in weather_list:
                    self.weather[item] = float(np.clip(_weather[item], 0, 1))
                elif item == "sunny":
                    pass
                else:
                    warnings.warn("LGSVL cannot support the weather: {}".format(item))

    def check_ego(self):
        # check vehicle type
        if self.ego.groundTruthPerception:
            if self.ego.name != "gt_sensors":
                self.ego.name = "gt_sensors"
                warnings.warn("Perform test bypassing perception, need to set the ego to \"gt_sensors\"")
            # if self.ego.name is None:
            #     self.ego.name = "gt_sensors"
            #     warnings.warn("There is no type of the ego vehicle, set to \"gt_sensors\" ")
            # elif self.ego.name not in self.ego_pre_list:
            #     self.ego.name = self.ego_pre_list[0]
            #     warnings.warn("The current version only supports the types in {}, "
            #                   "set to \"{}\".".format(self.ego_pre_list, self.ego_pre_list[0]))
        else:
            if self.ego.name != "lidar_only":
                self.ego.name = "lidar_only"
                warnings.warn("Perform test with perception, need to set the ego to \"lidar_only\"")
            # if self.ego.name is None:
            #     self.ego.name = "lidar_only"
            #     warnings.warn("There is no type of the ego vehicle, set to \"lidar_only\"")
            # elif self.ego.name not in self.ego_pre_list:
            #     self.ego.name = self.ego_pre_list[1]
            #     warnings.warn("The current version only supports the types in {}, "
            #                   "set to \"{}\".".format(self.ego_pre_list, self.ego_pre_list[1]))

    def check_npcs(self):
        for i in range(self.NPCNumber):
            if self.NPCs[i].name is None:
                self.NPCs[i].name = npc_list[0]
                warnings.warn("No type is specified for Vehicle \"{}\", "
                              "set to \"{}\".".format(self.NPCs[i].ID, npc_list[0]))
            elif self.NPCs[i].name not in npc_list:
                self.NPCs[i].name = npc_list[0]
                warnings.warn("The NPC vehicles supported in the current version are {}, "
                              "set to \"{}\"".format(npc_list, npc_list[0]))
            if self.NPCs[i].color is not None:
                self.NPCs[i].color = None
                warnings.warn("The current version does not support customized color! "
                              "Set Vehicle \"{}\" to its default color.".format(self.NPCs[i].ID))

    def check_ped(self):
        for _i in range(self.PedestrianNumber):
            if self.pedestrians[_i].name is None:
                self.pedestrians[_i].name = pedestrian_list[0]
                warnings.warn("No pedestrian type is specified for Pedestrian \"{}\", "
                              "set to \"{}\".".format(self.pedestrians[_i].ID, pedestrian_list[0]))
            elif self.pedestrians[_i].name not in pedestrian_list:
                self.pedestrians[_i].name = pedestrian_list[0]
                warnings.warn("The pedestrian types supported in this version are {},"
                              "set to \"{}\".".format(pedestrian_list, pedestrian_list[0]))
            if self.pedestrians[_i].height is not None or self.pedestrians[_i].color is not None:
                warnings.warn("The current version does not support customized pedestrian!"
                              "Set  \"{}\" to the default.".format(self.pedestrians[_i]))

    def check(self):
        self.check_map()
        self.check_time()
        self.check_weather()
        self.check_ego()
        self.check_npcs()
        self.check_ped()


class TestCase:
    def __init__(self):
        self.ScenarioName = ""
        self.MapVariable = ""
        self.map = ""
        self.time = None
        self.weather = None
        self.ego = EgoVehicle()
        # self.NPCNumber = lgsvl_filter_testcase.NPCNumber
        self.npcList = []
        # self.PedestrianNumber = lgsvl_filter_testcase.PedestrianNumber
        self.pedestrianList = []
        # self.ObsNumber = lgsvl_filter_testcase.ObsNumber
        self.obstacleList = []
        self.AgentNames = []

    def GetFromLGSVL(self, lgsvl_filter_testcase):
        self.ScenarioName = lgsvl_filter_testcase.ScenarioName
        self.MapVariable = lgsvl_filter_testcase.MapVariable
        self.map = lgsvl_filter_testcase.MapName
        self.time = lgsvl_filter_testcase.time
        self.weather = lgsvl_filter_testcase.weather
        self.ego = lgsvl_filter_testcase.ego
        # self.NPCNumber = lgsvl_filter_testcase.NPCNumber
        self.npcList = lgsvl_filter_testcase.NPCs
        # self.PedestrianNumber = lgsvl_filter_testcase.PedestrianNumber
        self.pedestrianList = lgsvl_filter_testcase.pedestrians
        # self.ObsNumber = lgsvl_filter_testcase.ObsNumber
        # self.obstacleList = lgsvl_filter_testcase.obstacles
        self.AgentNames = lgsvl_filter_testcase.AgentName

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)


class AllTestCase:
    def __init__(self, scenariolist, isGroundTruth):
        self.scenarios = scenariolist
        self.AgentNames = {}
        self.TestCases = self.test_cases_json(isGroundTruth)

    def test_cases_json(self, isGroundTruth) -> List[str]:
        CaseList = []
        for _i in range(len(self.scenarios)):
            raw_scenario_i = ScenarioElements(self.scenarios[_i], isGroundTruth)
            lgsvl_scenario_i = LGSVLAdapter(raw_scenario_i)
            test_case = TestCase()
            test_case.GetFromLGSVL(lgsvl_scenario_i)
            self.AgentNames[test_case.ScenarioName] = test_case.AgentNames
            test_case_json = test_case.toJSON()
            new_test_case = self.evaluate_test(json.loads(test_case_json))
            CaseList.append(new_test_case)
        # self.TestCases = CaseList
        return CaseList

    def evaluate_test(self, test_case_dict):
        map_name = test_case_dict['map']
        map_info = get_map_info(map_name)
        lane_config = map_info.get_lane_config()
        crosswalk_config = map_info.get_crosswalk_config()
        new_test_case = copy.deepcopy(test_case_dict)
        _ego_start = test_case_dict['ego']['start']
        if "lane_position" in _ego_start.keys():
            _lane_position = _ego_start['lane_position']
            _lane_name = _lane_position['lane']
            if _lane_name in lane_config.keys():
                lane_offset = np.clip(_lane_position['offset'], offset_offset, lane_config[_lane_name] - offset_offset)
                new_test_case['ego']['start']['lane_position']['offset'] = lane_offset
                if 'ref_lane_point' in new_test_case['ego']['start']['heading'].keys() and new_test_case['ego']['start']['heading']['ref_lane_point'] == test_case_dict['ego']['start']['lane_position']:
                    new_test_case['ego']['start']['heading']['ref_lane_point']['offset'] = lane_offset
            else:
                raise exception.LaneError("The defined lane ID in the ego's initial position is not in the map!")

        _ego_destination = test_case_dict['ego']['destination']
        if "lane_position" in _ego_destination.keys():
            _lane_position = _ego_destination['lane_position']
            _lane_name = _lane_position['lane']
            if _lane_name in lane_config.keys():
                lane_offset = np.clip(_lane_position['offset'], offset_offset, lane_config[_lane_name] - offset_offset)
                new_test_case['ego']['destination']['lane_position']['offset'] = lane_offset
                if 'ref_lane_point' in new_test_case['ego']['destination']['heading'].keys() and new_test_case['ego']['destination']['heading']['ref_lane_point'] == test_case_dict['ego']['destination']['lane_position']:
                    new_test_case['ego']['destination']['heading']['ref_lane_point']['offset'] = lane_offset
            else:
                raise exception.LaneError("The defined lane ID in the ego's destination is not in the map!")

        for i in range(len(test_case_dict['npcList'])):
            _npc = test_case_dict['npcList'][i]
            # if len(_npc['motion']):
            #     new_test_case['npcList'][i]['start']['speed'] = _npc['motion'][0]['speed']
            if "lane_position" in _npc['start'].keys():
                _lane_position = _npc['start']['lane_position']
                _lane_name = _npc['start']['lane_position']['lane']
                try:
                    if _lane_name in lane_config.keys():
                        _offset = np.clip(_npc['start']['lane_position']['offset'], offset_offset, lane_config[_lane_name] -offset_offset)
                        new_test_case['npcList'][i]['start']['lane_position']['offset'] = _offset
                        if 'ref_lane_point' in new_test_case['npcList'][i]['start']['heading'].keys() and new_test_case['npcList'][i]['start']['heading']['ref_lane_point'] == test_case_dict['npcList'][i]['start']['lane_position']:
                            new_test_case['npcList'][i]['start']['heading']['ref_lane_point']['offset'] = _offset
                    else:
                        raise exception.LaneError("The defined lane ID in {}'s initial position is not in the map!".format(_npc['ID']))
                except KeyError:
                    print("checking for key error.")


            for j in range(len(_npc['motion'])):
                _motion_state = _npc['motion'][j]
                if "lane_position" in _motion_state.keys():
                    _lane_position = _motion_state['lane_position']
                    _lane_name = _motion_state['lane_position']['lane']
                    if _lane_name in lane_config.keys():
                        _offset = np.clip(_motion_state['lane_position']['offset'], offset_offset, lane_config[_lane_name] -offset_offset)
                        new_test_case['npcList'][i]['motion'][j]['lane_position']['offset'] = _offset
                        if 'ref_lane_point' in new_test_case['npcList'][i]['motion'][j]['heading'].keys() and new_test_case['npcList'][i]['motion'][j]['heading']['ref_lane_point'] == test_case_dict['npcList'][i]['motion'][j]['lane_position']:
                            new_test_case['npcList'][i]['motion'][j]['heading']['ref_lane_point']['offset'] = _offset
                    else:
                        raise exception.LaneError("The defined lane ID in {}'s waypoints is not in the map!".format(_npc['ID']))

            if len(_npc['motion']):
                new_test_case['npcList'][i]['motion'].insert(0, copy.deepcopy(new_test_case['npcList'][i]['start']))

            if _npc['destination'] is not None:
                _npc_destination = copy.deepcopy(_npc['destination'])
                _npc['motion'].append(_npc_destination)
                new_test_case['npcList'][i]['motion'].append(_npc_destination)
                if "lane_position" in _npc['destination'].keys():
                    _lane_position = _npc['destination']['lane_position']
                    _lane_name = _npc['destination']['lane_position']['lane']
                    if _lane_name in lane_config.keys():
                        _offset = np.clip(_npc['destination']['lane_position']['offset'], offset_offset, lane_config[_lane_name] -offset_offset)
                        new_test_case['npcList'][i]['destination']['lane_position']['offset'] = _offset
                        if 'ref_lane_point' in new_test_case['npcList'][i]['destination']['heading'].keys() and new_test_case['npcList'][i]['destination']['heading']['ref_lane_point'] == test_case_dict['npcList'][i]['destination']['lane_position']:
                            new_test_case['npcList'][i]['destination']['heading']['ref_lane_point']['offset'] = _offset
                    else:
                        raise exception.LaneError("The defined lane ID in {}'s destination position is not in the map!".format(_npc['ID']))
            elif len(_npc['motion']):
                _last_state = copy.deepcopy(_npc['motion'][j])
                if "lane_position" in _motion_state.keys():
                    _lane_name = _motion_state['lane_position']['lane']
                    for next_index in range(3):
                        successor1 = map_info.get_successor_lanes(_lane_name)
                        random1 = random.randint(0, len(successor1)-1)
                        _lane_name = successor1[random1]
                    new_end_state = {"lane_position": {"lane": _lane_name, "offset": lane_config[_lane_name], "roadID": None},
                                     "heading": {"ref_lane_point": {"lane": _lane_name, "offset": lane_config[_lane_name], "roadID": None},
                                                 "ref_angle": 0},
                                     "speed": 0.0
                                     }
                    new_test_case['npcList'][i]['motion'].append(new_end_state)
                else:
                    point = (_last_state['position']['x'], _last_state['position']['y'], _last_state['position']['z'])
                    _lane_name = map_info.position2lane(point)
                    for next_index in range(3):
                        successor1 = map_info.get_successor_lanes(_lane_name)
                        random1 = random.randint(0, len(successor1)-1)
                        _lane_name = successor1[random1]
                    new_end_state = {"lane_position": {"lane": _lane_name, "offset": lane_config[_lane_name], "roadID": None},
                                     "heading": {"ref_lane_point": {"lane": _lane_name, "offset": lane_config[_lane_name], "roadID": None},
                                                 "ref_angle": 0},
                                     "speed": 0.0
                                     }
                    new_test_case['npcList'][i]['motion'].append(new_end_state)

        for k in range(len(test_case_dict['pedestrianList'])):
            ped_k = test_case_dict['pedestrianList'][k]
            start_x = ped_k['start']['position']['x']
            start_y = ped_k['start']['position']['y']
            crosswalk_name, _init_point = nearest((start_x, start_y), crosswalk_config)
            new_test_case['pedestrianList'][k]['start']['position']['x'] = _init_point[0]
            new_test_case['pedestrianList'][k]['start']['position']['y'] = _init_point[1]
            if ped_k['destination'] is not None:
                end_x = ped_k['destination']['position']['x']
                end_y = ped_k['destination']['position']['y']
                _, _end_point = nearest((end_x, end_y), {crosswalk_name: crosswalk_config[crosswalk_name]})
                new_test_case['pedestrianList'][k]['destination']['position']['x'] = _end_point[0]
                new_test_case['pedestrianList'][k]['destination']['position']['y'] = _end_point[1]
            for j in range(len(ped_k['motion'])):
                _motion_state = ped_k['motion'][j]
                state_x = _motion_state['position']['x']
                state_y = _motion_state['position']['y']
                _, _point = nearest((state_x, state_y), {crosswalk_name: crosswalk_config[crosswalk_name]})
                new_test_case['pedestrianList'][k]['motion'][j]['position']['x'] = _point[0]
                new_test_case['pedestrianList'][k]['motion'][j]['position']['y'] = _point[1]
        return new_test_case


if __name__ == "__main__":
    # input_file = 'changing.txt'
    input_file = 'test_cases/input-test.txt'
    isGroundTruth = True
    ast = Parse(input_file)
    scenario_list = ast.get_scenarios()
    test_cases = AllTestCase(scenario_list, isGroundTruth)
    formated_test_cases = test_cases.TestCases
    print(formated_test_cases)


    # ast = Parse(input_file)
    # scenario_list = ast.get_scenarios()
    # first_scenario = scenario_list[0]
    # scenario_map = first_scenario.get_map()
    # map_name = scenario_map.get_map_name()
    # ego_vehicle = first_scenario.get_ego_vehicle()
    # ego_init_state = ego_vehicle.get_first_state()
    # ego_target_state = ego_vehicle.get_second_state()
    # print(ego_init_state.get_position().get_coordinate().get)
