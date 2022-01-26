import copy
import warnings

from map import get_map_info
from shapely.geometry import Point, LinearRing
from shapely.geometry.polygon import Polygon
from shapely.ops import nearest_points


def point_in_crosswalk(point, crosswalk_config):
    _point = Point(point)
    contained_key = None
    for key in crosswalk_config:
        polygon = Polygon(crosswalk_config[key])
        if polygon.contains(_point):
            contained_key = key
            break
    return contained_key


def pedestrian_in_crosswalk(position_list, crosswalk_config):
    new_points = copy.deepcopy(position_list)
    crosswalk_name = point_in_crosswalk(position_list[0], crosswalk_config)

    if crosswalk_name is None:
        crosswalk_name, new_points[0] = nearest(position_list[0], crosswalk_config)
    polygon = Polygon(crosswalk_config[crosswalk_name])
    for i in range(len(position_list) - 1):
        _wp = position_list[i + 1]
        _point = Point(_wp)
        if not polygon.contains(_point):
            warnings.warn("Currently, each time a pedestrian is required to move along one crosswalk. Set to the nearest point in the crosswalk")
            _, new_points[i + 1] = nearest(_wp, {crosswalk_name: crosswalk_config[crosswalk_name]})
    return crosswalk_name, new_points


def nearest(point, crosswalk_config):
    _distance = 1000
    crosswalk_name = None
    for key in crosswalk_config:
        _dis = Point(point).distance(Polygon(crosswalk_config[key]))
        if _dis < _distance:
            _distance = _dis
            crosswalk_name = key
    polygon = Polygon(crosswalk_config[crosswalk_name])
    pol_ext = LinearRing(polygon.exterior.coords)
    d = pol_ext.project(Point(point))
    p = pol_ext.interpolate(d)
    closest_point_coords = list(p.coords)[0]
    return crosswalk_name, closest_point_coords




if __name__ == "__main__":
    poly = Polygon([(0, 0), (2,8), (14, 10), (6, 1)])
    point = Point(6, 2)
    print(point.distance(poly))
    # np  = nearest_points(poly, point)
    # print(np[0])
    # pol_ext = LinearRing(poly.exterior.coords)
    # d = pol_ext.project(point)
    # p = pol_ext.interpolate(d)
    # closest_point_coords = list(p.coords)[0]
    # print(closest_point_coords)
    points = [(553020.54, 4182690.69), (553020.54,4182690.69), (553023.26, 4182671.82)]
    name, new_points = pedestrian_in_crosswalk(points, crosswalk_config)
    print(name)
    print(new_points)

# point = (552820.0, 4182680.0)
# a = point_in_crosswalk(point[0], point[1], crosswalk_config)
# print(a)
#
#

#


