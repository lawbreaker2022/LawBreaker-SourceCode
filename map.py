import copy
import json
import warnings

import numpy as np
from shapely.geometry import Point, LineString

directory = 'map/'



class get_map_info:
    def __init__(self, map_name):
        self.file = directory + map_name + ".json"
        self.lane_config = dict()
        self.lane_waypoints = dict()
        self.crosswalk_config = dict()
        self.lane_predecessor = dict()
        self.lane_successor = dict()

        with open(self.file) as f:
            map_config = json.load(f)
            lane = map_config['laneList']
            crosswalk = map_config['crosswalkList']
            for i in range(len(lane)):
                lane_id = lane[i]['id']['id']
                lane_length = lane[i]['length']
                self.lane_config[lane_id] = lane_length
                self.lane_waypoints[lane_id] = []
                for _i in range(len(lane[i]['centralCurve']['segmentList'])):
                    lane_segment_point = lane[i]['centralCurve']['segmentList'][_i]['lineSegment']['pointList']
                    for k in range(len(lane_segment_point)):
                        _wp_k = lane_segment_point[k]
                        self.lane_waypoints[lane_id].append(np.array([_wp_k['x'], _wp_k['y']]))
                predecessor = lane[i]['predecessorIdList']
                self.lane_predecessor[lane_id] = []
                for j in range(len(predecessor)):
                    self.lane_predecessor[lane_id].append(predecessor[j]['id'])
                successor = lane[i]['successorIdList']
                self.lane_successor[lane_id] = []
                for k in range(len(successor)):
                    self.lane_successor[lane_id].append(successor[k]['id'])

            for j in range(len(crosswalk)):
                crosswalk_polygon = crosswalk[j]['polygon']['pointList']
                if len(crosswalk_polygon) != 4:
                    print('Needs four points to describe a crosswalk!')
                    exit()
                crosswalk_points = [(crosswalk_polygon[0]['x'], crosswalk_polygon[0]['y']),
                                    (crosswalk_polygon[1]['x'], crosswalk_polygon[1]['y']),
                                    (crosswalk_polygon[2]['x'], crosswalk_polygon[2]['y']),
                                    (crosswalk_polygon[3]['x'], crosswalk_polygon[3]['y'])
                                    ]
                self.crosswalk_config['crosswalk'+str(j+1)] = crosswalk_points


    def get_lane_config(self):
        return self.lane_config

    def get_successor_lanes(self, lane_name):
        return self.lane_successor[lane_name]

    def get_predecessor_lanes(self, lane_name):
        return self.lane_predecessor[lane_name]

    def get_crosswalk_config(self):
        return self.crosswalk_config

    def get_position(self, lane_position):
        ## lane_position = [lane_id, offset]
        lane_id = lane_position[0]
        offset = lane_position[1]
        waypoint = self.lane_waypoints[lane_id]
        _distance = 0
        for i in range(len(waypoint)-1):
            wp1 = waypoint[i]
            wp2 = waypoint[i+1]
            _dis_wp1_2 = np.linalg.norm(wp1 - wp2)
            if _distance + _dis_wp1_2 > offset:
                current_dis = offset - _distance
                k = current_dis / _dis_wp1_2
                x = wp1[0] + (wp2[0] - wp1[0])*k
                y = wp1[1] + (wp2[1] - wp1[1])*k
                return (x, y, 0)
            _distance += _dis_wp1_2
        if i == len(waypoint)-2:
            warnings.warn("The predefined position is out of the given lane, set to the end of the lane.")
            return (wp2[0], wp2[1], 0)

    def position2lane(self, position):
        _dis = float('inf')
        _point = Point(position)
        for item in self.lane_waypoints.keys():
            _line = LineString(self.lane_waypoints[item])
            _current_dis = _point.distance(_line)
            if _current_dis < _dis:
                _dis = _current_dis
                _lane_name = item
        return _lane_name




    def get_global_position(self, position, local_position):
        '''

        Args:
            position: (x, y)
            local_position: position in the vehicle frame

        Returns:

        '''
        # _dis = float('inf')
        _point = Point(position)
        # for item in self.lane_waypoints.keys():
        #     _line = LineString(self.lane_waypoints[item])
        #     _current_dis = _point.distance(_line)
        #     if _current_dis < _dis:
        #         _dis = _current_dis
        #         _lane_name = item
        _lane_name = self.position2lane(position)
        _lane_waypoint = self.lane_waypoints[_lane_name]
        _in_lane_dis = float('inf')
        _waypoint_index = 0
        for i in range(len(_lane_waypoint)-1):
            _segment_line = LineString([_lane_waypoint[i], _lane_waypoint[i+1]])
            _current_dis = _point.distance(_segment_line)
            if _current_dis < _in_lane_dis:
                _in_lane_dis = _current_dis
                _waypoint_index = i

        direction = _lane_waypoint[_waypoint_index+1] - _lane_waypoint[_waypoint_index]
        cos_theta = direction[0] / np.linalg.norm(direction)
        sin_theta = direction[1] / np.linalg.norm(direction)
        x1 = local_position[0] * cos_theta - local_position[1] * sin_theta
        y1 = local_position[0] * sin_theta + local_position[1] * cos_theta
        return (x1 + position[0], y1 + position[1])








if __name__ == "__main__":
    map = "san_francisco"
    map_info = get_map_info(map)
    map_info.get_lane_config()
    lane_point = ["lane_231", 100]
    p = map_info.get_position(lane_point)
    print(p)
