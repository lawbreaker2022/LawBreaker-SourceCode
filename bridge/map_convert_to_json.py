from modules.map.proto import map_pb2
import json


def Parse_Projection(projection):
	proj = {}
	if hasattr(projection,"proj"):
		proj["proj"] = projection.proj
	return proj
# message Projection {
#   optional string proj = 1;
# }

def Parse_header(map_header):
	header = {}
	if hasattr(map_header, "version"):
		header["version"] = map_header.version.decode("utf-8") 
	if hasattr(map_header, "date"):
		header["date"] = map_header.date.decode("utf-8") 
	if hasattr(map_header, "projection"):
		proj = Parse_Projection(map_header.projection)
		header["Projection"] = proj 
	if hasattr(map_header, "district"):
		header["district"] = map_header.district.decode("utf-8")
	if hasattr(map_header, "generation"):
		header["generation"] = map_header.generation.decode("utf-8")
	if hasattr(map_header, "rev_major"):
		header["rev_major"] = map_header.rev_major.decode("utf-8")
	if hasattr(map_header, "rev_minor"):
		header["rev_minor"] = map_header.rev_minor.decode("utf-8")
	if hasattr(map_header, "left"):
		header["left"] = map_header.left
	if hasattr(map_header, "top"):
		header["top"] = map_header.top
	if hasattr(map_header, "right"):
		header["right"] = map_header.right
	if hasattr(map_header, "bottom"):
		header["bottom"] = map_header.bottom
	if hasattr(map_header, "vendor"):
		header["vendor"] = map_header.vendor.decode("utf-8")
	return header
# message Header {
#   optional bytes version = 1;
#   optional bytes date = 2;
#   optional Projection projection = 3;
#   optional bytes district = 4;
#   optional bytes generation = 5;
#   optional bytes rev_major = 6;
#   optional bytes rev_minor = 7;
#   optional double left = 8;
#   optional double top = 9;
#   optional double right = 10;
#   optional double bottom = 11;
#   optional bytes vendor = 12;
# }


def Parse_id(id):
	ID = {}
	if hasattr(id,"id"):
		ID["id"] = id.id
	return ID
# message Id {
#   optional string id = 1;
# }

def Parse_polygon(polygon):
	return_polygon = {}
	pointList = []
	if hasattr(polygon,"point"):
		for _i in polygon.point:
			single_point = {}
			if hasattr(_i,"x"):
				single_point["x"] = _i.x
			if hasattr(_i,"y"):
				single_point["y"] = _i.y
			if hasattr(_i,"z"):
				single_point["z"] = _i.z
			else:
				single_point["z"] = 0
			pointList.append(single_point)
	return_polygon["pointList"] = pointList
	return return_polygon
# message Polygon {
#   repeated apollo.common.PointENU point = 1;
# }


def Parse_crosswalk(map_crosswalk):
	crosswalk = []
	for _i in map_crosswalk:
		single_crosswalk = {}
		if hasattr(_i, "id"):
			single_crosswalk["id"] = Parse_id(_i.id)
		if hasattr(_i, "polygon"):
			single_crosswalk["polygon"] = Parse_polygon(_i.polygon)
		if hasattr(_i, "overlap_id"):
			overlap_id = []
			for _ii in _i.overlap_id:
				temp = None
				temp = Parse_id(_ii)
				overlap_id.append(temp)
			single_crosswalk["overlapIdList"] = overlap_id

		crosswalk.append(single_crosswalk)
	return crosswalk
# message Crosswalk {
#   optional Id id = 1;
#   optional Polygon polygon = 2;
#   repeated Id overlap_id = 3;
# }
def Parse_junction(map_junction):
	junction = []
	for _i in map_junction:
		single_junction = {}
		if hasattr(_i, "id"):
			single_junction["id"] = Parse_id(_i.id)
		if hasattr(_i, "polygon"):
			single_junction["polygon"] = Parse_polygon(_i.polygon)
		if hasattr(_i, "overlap_id"):
			overlap_id = []
			for _ii in _i.overlap_id:
				temp = None
				temp = Parse_id(_ii)
				overlap_id.append(temp)
			single_junction["overlapIdList"] = overlap_id

		junction.append(single_junction)
	return junction 
# message Junction {
#   optional Id id = 1;
#   optional Polygon polygon = 2;
#   repeated Id overlap_id = 3;
# }

def Parse_curve(curve):
	centralCurve = {}
	segmentList = []
	for _i in curve.segment:
		single_segment = {}

		if hasattr(_i,"line_segment"):
			lineSegment = {}
			pointList = []
			for _ii in _i.line_segment.point:
				single_point = {}
				if hasattr(_ii,"x"):
					single_point["x"] = _ii.x
				if hasattr(_ii,"y"):
					single_point["y"] = _ii.y
				if hasattr(_ii,"z"):
					single_point["z"] = _ii.z
				pointList.append(single_point)
			lineSegment["pointList"] = pointList
			single_segment["lineSegment"] = lineSegment

		if hasattr(_i,"s"):
			single_segment["s"] = _i.s

		if hasattr(_i,"start_position"):
			start_position = {}
			start_position["x"] = _i.start_position.x
			start_position["y"] = _i.start_position.y
			start_position["z"] = _i.start_position.z
			single_segment["startPosition"] = start_position

		if hasattr(_i,"heading"):
			single_segment["heading"] = _i.heading

		if hasattr(_i,"length"):
			single_segment["length"] = _i.length


		segmentList.append(single_segment)

	centralCurve["segmentList"] = segmentList
	return centralCurve

def Parse_LaneBoundaryType(LaneBoundaryType):
	result = {}
	if hasattr(LaneBoundaryType,"s"):
		result["s"] = LaneBoundaryType.s
	if hasattr(LaneBoundaryType,"types"):
		for _i in LaneBoundaryType.types:
			single_types = []
			single_type = _i
			single_types.append(single_type)
		result["typesList"] = single_types
	return result

def Parse_boundary(boundary):
	_boundary = {}
	if hasattr(boundary, "curve"):
		_boundary["curve"] = Parse_curve(boundary.curve)
	if hasattr(boundary, "length"):
		_boundary["length"] = boundary.length
	if hasattr(boundary, "virtual"):
		_boundary["virtual"] = boundary.virtual
	if hasattr(boundary, "boundary_type"):
		boundaryTypeList = []
		for _i in boundary.boundary_type:
			single_boundary_type = {}
			single_boundary_type = Parse_LaneBoundaryType(_i)
			boundaryTypeList.append(single_boundary_type)
		_boundary["boundaryTypeList"] = boundaryTypeList
	return _boundary

def Parse_lane(map_lane):
	lane = []
	for _i in map_lane:
		single_lane = {}
		if hasattr(_i, "id"):
			single_lane["id"] = Parse_id(_i.id)
		if hasattr(_i, "central_curve"):
			single_lane["centralCurve"] = Parse_curve(_i.central_curve)

		if hasattr(_i, "left_boundary"):
			single_lane["leftBoundary"] = Parse_boundary(_i.left_boundary)
		if hasattr(_i, "right_boundary"):
			single_lane["rightBoundary"] = Parse_boundary(_i.right_boundary)

		if hasattr(_i, "length"):
			single_lane["length"] = _i.length
		if hasattr(_i, "speed_limit"):
			single_lane["speedLimit"] = _i.speed_limit
		if hasattr(_i, "overlap_id"):
			overlap_id = []
			for _ii in _i.overlap_id:
				temp = None
				temp = Parse_id(_ii)
				overlap_id.append(temp)
			single_lane["overlapIdList"] = overlap_id
		if hasattr(_i, "predecessor_id"):
			predecessor_id = []
			for _ii in _i.predecessor_id:
				temp = None
				temp = Parse_id(_ii)
				predecessor_id.append(temp)
			single_lane["predecessorIdList"] = predecessor_id
		if hasattr(_i, "successor_id"):
			successor_id = []
			for _ii in _i.successor_id:
				temp = None
				temp = Parse_id(_ii)
				successor_id.append(temp)
			single_lane["successorIdList"] = successor_id
		if hasattr(_i, "left_neighbor_forward_lane_id"):
			left_neighbor_forward_lane_id = []
			for _ii in _i.left_neighbor_forward_lane_id:
				temp = None
				temp = Parse_id(_ii)
				left_neighbor_forward_lane_id.append(temp)
			single_lane["leftNeighborForwardLaneIdList"] = left_neighbor_forward_lane_id
		if hasattr(_i, "right_neighbor_forward_lane_id"):
			right_neighbor_forward_lane_id = []
			for _ii in _i.right_neighbor_forward_lane_id:
				temp = None
				temp = Parse_id(_ii)
				right_neighbor_forward_lane_id.append(temp)
			single_lane["rightNeighborForwardLaneIdList"] = right_neighbor_forward_lane_id
		if hasattr(_i, "type"):
			single_lane["type"] = _i.type
		if hasattr(_i, "turn"):
			single_lane["turn"] = _i.turn
		if hasattr(_i, "left_neighbor_reverse_lane_id"):
			left_neighbor_reverse_lane_id = []
			for _ii in _i.left_neighbor_reverse_lane_id:
				temp = None
				temp = Parse_id(_ii)
				left_neighbor_reverse_lane_id.append(temp)
			single_lane["leftNeighborReverseLaneIdList"] = left_neighbor_reverse_lane_id
		if hasattr(_i, "right_neighbor_reverse_lane_id"):
			right_neighbor_reverse_lane_id = []
			for _ii in _i.right_neighbor_reverse_lane_id:
				temp = None
				temp = Parse_id(_ii)
				right_neighbor_reverse_lane_id.append(temp)
			single_lane["rightNeighborReverseLaneIdList"] = right_neighbor_reverse_lane_id
		if hasattr(_i, "junction_id"):
			single_lane["junction_id"] = Parse_id(_i.junction_id)
		if hasattr(_i, "left_sample"):
			left_sample = []
			for _ii in _i.left_sample:
				single_sample = {}
				if hasattr(_ii, "s"):
					single_sample["s"]=_ii.s 
				if hasattr(_ii, "width"):
					single_sample["width"]=_ii.width
				left_sample.append(single_sample)	
			single_lane["leftSampleList"] = left_sample
		if hasattr(_i, "right_sample"):
			right_sample = []
			for _ii in _i.right_sample:
				single_sample = {}
				if hasattr(_ii, "s"):
					single_sample["s"]=_ii.s 
				if hasattr(_ii, "width"):
					single_sample["width"]=_ii.width
				right_sample.append(single_sample)	
			single_lane["rightSampleList"] = right_sample
		if hasattr(_i, "direction"):
			single_lane["direction"] = _i.direction
		if hasattr(_i, "left_road_sample"):
			left_road_sample = []
			for _ii in _i.left_road_sample:
				single_sample = {}
				if hasattr(_ii, "s"):
					single_sample["s"]=_ii.s 
				if hasattr(_ii, "width"):
					single_sample["width"]=_ii.width
				left_road_sample.append(single_sample)	
			single_lane["leftRoadSampleList"] = left_road_sample
		if hasattr(_i, "right_road_sample"):
			right_road_sample = []
			for _ii in _i.right_road_sample:
				single_sample = {}
				if hasattr(_ii, "s"):
					single_sample["s"]=_ii.s 
				if hasattr(_ii, "width"):
					single_sample["width"]=_ii.width
				right_road_sample.append(single_sample)	
			single_lane["rightRoadSampleList"] = right_road_sample
		if hasattr(_i, "self_reverse_lane_id"):
			self_reverse_lane_id = []
			for _ii in _i.self_reverse_lane_id:
				temp = None
				temp = Parse_id(_ii)
				self_reverse_lane_id.append(temp)
			single_lane["selfReverseLaneIdList"] = self_reverse_lane_id

		lane.append(single_lane)
	return lane


def Parse_stop_sign(map_stop_sign):
	stop_sign = []
	for _i in map_stop_sign:
		single_stop_sign = {}
		if hasattr(_i,"id"):
			single_stop_sign["id"] = Parse_id(_i.id)
		if hasattr(_i,"stop_line"):
			curveList = []
			for _ii in _i.stop_line:
				curve = Parse_curve(_ii)
				curveList.append(curve)
			single_stop_sign["stopLineList"] = curveList
		if hasattr(_i, "overlap_id"):
			overlap_id = []
			for _ii in _i.overlap_id:
				temp = None
				temp = Parse_id(_ii)
				overlap_id.append(temp)
			single_stop_sign["overlapIdList"] = overlap_id
		if hasattr(_i, "type"):
			single_stop_sign["type"] = _i.type
		stop_sign.append(single_stop_sign)
	return stop_sign

def Parse_point(point):
	_point = {}
	if hasattr(point,"x"):
		_point["x"] = point.x
	if hasattr(point,"y"):
		_point["y"] = point.y
	if hasattr(point,"z"):
		_point["z"] = point.z
	else:
		_point["z"] = 0
	return _point


def Parse_Subsignal(subsignal):
	_subsignal = {}
	if hasattr(subsignal, "id"):
		_subsignal["id"] = Parse_id(subsignal.id)
	if hasattr(subsignal, "type"):
		_subsignal["type"] = subsignal.type
	if hasattr(subsignal, "location"):
		_subsignal["location"] = Parse_point(subsignal.location)

	return _subsignal

def Parse_overlapIdList(overlap_id_list):
	overlapIdList = []
	for _ii in overlap_id_list:
		single_overlap_id = {}
		single_overlap_id = Parse_id(_ii)
		overlapIdList.append(single_overlap_id)
	return overlapIdList

def Parse_sign_info(sign_info):
	signInfo = {}
	if hasattr(sign_info, "type"):
		signInfo["type"] = sign_info.type
	return signInfo

def Parse_signal(map_signal):
	signal = []
	for _i in map_signal:
		single_signal = {}
		if hasattr(_i,"id"):
			single_signal["id"] = Parse_id(_i.id)
		if hasattr(_i, "boundary"):
			single_signal["boundary"] = Parse_polygon(_i.boundary)
		if hasattr(_i, "subsignal"):
			subsignalList = []
			for _ii in _i.subsignal:
				single_subsignal = {}
				single_subsignal = Parse_Subsignal(_ii)
				subsignalList.append(single_subsignal)
			single_signal["subsignalList"] = subsignalList
		if hasattr(_i, "overlap_id"):
			single_signal["overlapIdList"] = Parse_overlapIdList(_i.overlap_id)
		if hasattr(_i, "type"):
			single_signal["type"] = _i.type
		if hasattr(_i, "stop_line"):
			curveList = []
			for _ii in _i.stop_line:
				curve = Parse_curve(_ii)
				curveList.append(curve)
			single_signal["stopLineList"] = curveList
		if hasattr(_i, "sign_info"):
			signInfoList = []
			for _ii in _i.sign_info:
				sign_info = Parse_sign_info(_ii)
				signInfoList.append(sign_info)
			single_signal["signInfoList"] = signInfoList
		signal.append(single_signal)
	return signal


def Parse_ObjectOverlapInfo(item):
	_object = {}
	# print('!!!')
	# print(item.lane_overlap_info)
	# print(item.signal_overlap_info)
	# print( hasattr(item, "lane_overlap_info"))
	# print( hasattr(item, "signal_overlap_info"))
	# print( hasattr(item, "stop_sign_overlap_info"))
	# print( hasattr(item, "crosswalk_overlap_info"))
	if hasattr(item, "id"):
		_object["id"] = Parse_id(item.id)
	if hasattr(item, "lane_overlap_info"):
		lane_overlap_info = {}
		if hasattr(item.lane_overlap_info, "start_s"):
			lane_overlap_info["startS"] = item.lane_overlap_info.start_s
		if hasattr(item.lane_overlap_info, "end_s"):
			lane_overlap_info["endS"] = item.lane_overlap_info.end_s
		if hasattr(item.lane_overlap_info, "is_merge"):
			lane_overlap_info["isMerge"] = item.lane_overlap_info.is_merge
		if hasattr(item.lane_overlap_info, "region_overlap_id"):
			lane_overlap_info["regionOverlapId"] = Parse_id(item.lane_overlap_info.region_overlap_id) 
		_object["laneOverlapInfo"] = lane_overlap_info
	if hasattr(item, "signal_overlap_info"):
		_object["signalOverlapInfo"] = {}
	if hasattr(item, "stop_sign_overlap_info"):
		_object["stopSignOverlapInfo"] = {}
	if hasattr(item, "crosswalk_overlap_info"):
		item1 = {}
		if hasattr(item.crosswalk_overlap_info, "region_overlap_id"):
			item1["regionOverlapId"] =Parse_id(item.crosswalk_overlap_info.region_overlap_id) 
		_object["crosswalkOverlapInfo"] = item1
	if hasattr(item, "junction_overlap_info"):
		_object["junctionOverlapInfo"] = {}	
	if hasattr(item, "yield_sign_overlap_info"):
		_object["yieldSignOverlapInfo"] = {}
	if hasattr(item, "clear_area_overlap_info"):
		_object["clearAreaOverlapInfo"] = {}
	if hasattr(item, "speed_bump_overlap_info"):
		_object["speedBumpOverlapInfo"] = {}	
	if hasattr(item, "parking_space_overlap_info"):
		_object["parkingSpaceOverlapInfo"] = {}
	if hasattr(item, "pnc_junction_overlap_info"):
		_object["pncJunctionOverlapInfo"] = {}

	return _object


def Parse_region_overlap(item):
	_object = {}
	if hasattr(item, "id"):
		_object["id"] = Parse_id(item.id)
	if hasattr(item, "polygon"):
		polygon_list = []
		for _i in item.polygon:
			single_polygon = {}
			single_polygon = Parse_polygon(_i)
			polygon_list.append(single_polygon)
		_object["polygonList"] = polygon_list
	return _object

def Parse_overlap(map_overlap):
	overlap = []
	for _i in map_overlap:
		single_overlap = {}
		if hasattr(_i,"id"):
			single_overlap["id"] = Parse_id(_i.id)
		if hasattr(_i,"object"):
			curveList = []
			for _ii in _i.object:
				curve = {}
				curve = Parse_ObjectOverlapInfo(_ii)
				curveList.append(curve)
			single_overlap["objectList"] = curveList
		if hasattr(_i,"region_overlap"):
			curveList = []
			for _ii in _i.region_overlap:
				curve = {}
				curve = Parse_region_overlap(_ii)
				curveList.append(curve)
			single_overlap["regionOverlapList"] = curveList

		overlap.append(single_overlap)
	return overlap

def Parse_clear_area(item):
	result = []
	for _i in item:
		single_one = {}
		if hasattr(_i,"id"):
			single_one["id"] = Parse_id(_i.id)
		if hasattr(_i,"overlap_id"):
			single_one["overlapIdList"] = Parse_overlapIdList(_i.overlap_id)
		if hasattr(_i,"polygon"):
			single_one["polygon"] = Parse_polygon(_i.polygon)
		result.append(single_one)
	return result
# message ClearArea {
#   optional Id id = 1;
#   repeated Id overlap_id = 2;
#   optional Polygon polygon = 3;
# }
def Parse_speed_bump(item):
	result = []
	for _i in item:
		single_one = {}
		if hasattr(_i,"id"):
			single_one["id"] = Parse_id(_i.id)
		if hasattr(_i,"overlap_id"):
			single_one["overlapIdList"] = Parse_overlapIdList(_i.overlap_id)
		if hasattr(_i,"position"):
			List = []
			for _ii in _i.position:
				single = {}
				single = Parse_curve(_ii)
				List.append(single)
			single_one["positionList"] = List

		result.append(single_one)
	return result
# message SpeedBump {
#   optional Id id = 1;
#   repeated Id overlap_id = 2;
#   repeated Curve position = 3;
# }
def Parse_BoundaryEdge(item):
	result = {}
	if hasattr(item,"curve"):
		result["curve"] = Parse_curve(item.curve)
	if hasattr(item,"type"):
		result["type"] = item.type
	return result

def Parse_BoundaryPolygon(item):
	result = {}
	if hasattr(item, "edge"):
		List = []
		for _ii in item.edge:
			single = []
			single = Parse_BoundaryEdge(_ii)
			List.append(single)
		result["edgeList"] = List
	return result


def Parse_RoadBoundary(item):
	result = {}
	if hasattr(item,"outer_polygon"):
		result["outerPolygon"] = Parse_BoundaryPolygon(item.outer_polygon)
	if hasattr(item,"hole"):
		List = []
		for _ii in item.hole:
			single = []
			single = Parse_BoundaryPolygon(_ii)
			List.append(single)
		result["holeList"] = List

	return result

def Parse_RoadSection(item):
	result = {}
	if hasattr(item,"id"):
		result["id"] = Parse_id(item.id)
	if hasattr(item,"lane_id"):
		result["laneIdList"] = Parse_overlapIdList(item.lane_id)
	if hasattr(item,"boundary"):
		result["boundary"] = Parse_RoadBoundary(item.boundary)


	return result


def Parse_road(item):
	result = []
	for _i in item:
		single_one = {}
		if hasattr(_i,"id"):
			single_one["id"] = Parse_id(_i.id)
		if hasattr(_i,"section"):
			List = []
			for _ii in _i.section:
				single = {}
				single = Parse_RoadSection(_ii)
				List.append(single)
			single_one["sectionList"] = List
		result.append(single_one)
	return result



def Parse_parking_space(item):
	result = []
	for _i in item:
		single_one = {}
		if hasattr(_i,"id"):
			single_one["id"] = Parse_id(_i.id)
		if hasattr(_i,"polygon"):
			single_one["polygon"] = Parse_polygon(_i.polygon)
		if hasattr(_i,"overlap_id"):
			single_one["overlapIdList"] = Parse_overlapIdList(_i.overlap_id)
		if hasattr(_i,"heading"):
			single_one["heading"] = _i.heading
		result.append(single_one)
	return result
# message ParkingSpace {
#   optional Id id = 1;
#   optional Polygon polygon = 2;
#   repeated Id overlap_id = 3;
#   optional double heading = 4;
# }
def Parse_Passage(item):
	result = {}
	if hasattr(item,"id"):
		result["id"] = Parse_id(item.id)
	if hasattr(item,"signal_id"):
		result["signalIdList"] = Parse_overlapIdList(item.signal_id)
	if hasattr(item,"yield_id"):
		result["yieldIdList"] = Parse_overlapIdList(item.yield_id)
	if hasattr(item,"stop_sign_id"):
		result["stopSignIdList"] = Parse_overlapIdList(item.stop_sign_id)
	if hasattr(item,"lane_id"):
		result["laneIdList"] = Parse_overlapIdList(item.lane_id)
	if hasattr(item,"type"):
		result["type"] = item.type
	return result

def Parse_PassageGroup(item):
	result = {}
	if hasattr(item,"id"):
		result["id"] = Parse_id(item.id)
	if hasattr(item,"passage"):
		List = []
		for _ii in _i.passage:
			single = {}
			single = Parse_Passage(_ii)
			List.append(single)
		result["passageList"] = List
	return result

# message Passage {
#   optional Id id = 1;

#   repeated Id signal_id = 2;
#   repeated Id yield_id = 3;
#   repeated Id stop_sign_id = 4;
#   repeated Id lane_id = 5;

#   enum Type {
#     UNKNOWN = 0;
#     ENTRANCE = 1;
#     EXIT = 2;
#   };
#   optional Type type = 6;

# };

# message PassageGroup {
#   optional Id id = 1;

#   repeated Passage passage = 2;
# };


def Parse_pnc_junction(item):
	result = []
	for _i in item:
		single_one = {}
		if hasattr(_i,"id"):
			single_one["id"] = Parse_id(_i.id)
		if hasattr(_i,"polygon"):
			single_one["polygon"] = Parse_polygon(_i.polygon)
		if hasattr(_i,"overlap_id"):
			single_one["overlapIdList"] = Parse_overlapIdList(_i.overlap_id)
		if hasattr(_i,"passage_group"):
			single_one["passage_group"] = Parse_PassageGroup(_i.passage_group)
		result.append(single_one)
	return result


# message PNCJunction {
#   optional Id id = 1;
#   optional Polygon polygon = 2;
#   repeated Id overlap_id = 3;
#   repeated PassageGroup passage_group = 4;
# }



def for_map_convert_bin_to_json(_map):
	_map_after_parser = {}
	if hasattr(_map, "header"):
		map_header = _map.header
		header = Parse_header(map_header)
		_map_after_parser["header"] = header
	if hasattr(_map, "crosswalk"):
		map_crosswalk = _map.crosswalk
		crosswalk = Parse_crosswalk(map_crosswalk)
		_map_after_parser["crosswalkList"] = crosswalk
	if hasattr(_map, "junction"):
		map_junction = _map.junction
		junction = Parse_crosswalk(map_junction)
		_map_after_parser["junctionList"] = junction
	if hasattr(_map, "lane"):
		map_lane = _map.lane
		lane = Parse_lane(map_lane)
		_map_after_parser["laneList"] = lane
	if hasattr(_map, "stop_sign"):
		map_stop_sign = _map.stop_sign
		stop_sign = Parse_stop_sign(map_stop_sign)
		_map_after_parser["stopSignList"] = stop_sign	
	if hasattr(_map, "signal"):
		map_signal = _map.signal
		signal = Parse_signal(map_signal)
		_map_after_parser["signalList"] = signal
	if hasattr(_map, "yield"): #can't use yield:a reserved word
		_map_after_parser["yieldList"] = []
	if hasattr(_map, "overlap"):
		map_overlap = _map.overlap
		overlap = Parse_overlap(map_overlap)
		_map_after_parser["overlapList"] = overlap
	if hasattr(_map, "clear_area"):
		map_clear_area = _map.clear_area
		clear_area = Parse_clear_area(map_clear_area)
		_map_after_parser["clearAreaList"] = clear_area
	if hasattr(_map, "speed_bump"):
		map_speed_bump = _map.speed_bump
		speed_bump = Parse_speed_bump(map_speed_bump)
		_map_after_parser["speedBumpList"] = speed_bump
	if hasattr(_map, "road"):
		map_road = _map.road
		road = Parse_road(map_road)
		_map_after_parser["roadList"] = road
	if hasattr(_map, "parking_space"):
		map_parking_space = _map.parking_space
		parking_space = Parse_parking_space(map_parking_space)
		_map_after_parser["parkingSpaceList"] = parking_space
	if hasattr(_map, "pnc_junction"):
		map_pnc_junction = _map.pnc_junction
		pnc_junction = Parse_pnc_junction(map_pnc_junction)
		_map_after_parser["pncJunctionList"] = pnc_junction
	# print(_map_after_parser)

	return _map_after_parser

# message Map {
#   optional Header header = 1;
#   repeated Crosswalk crosswalk = 2;
#   repeated Junction junction = 3;
#   repeated Lane lane = 4;
#   repeated StopSign stop_sign = 5;
#   repeated Signal signal = 6;
#   repeated YieldSign yield = 7;
#   repeated Overlap overlap = 8;
#   repeated ClearArea clear_area = 9;
#   repeated SpeedBump speed_bump = 10;
#   repeated Road road = 11;
#   repeated ParkingSpace parking_space = 12;
#   repeated PNCJunction pnc_junction = 13;
# }



if __name__ == '__main__':

	map_name = "borregas_ave"
	f = open("original_map/"+map_name+"/base_map.bin", "rb")
	# header = map_pb2.Header()
	# header.ParseFromString(f.read())
	# print(header)
	_map = map_pb2.Map()
	_map.ParseFromString(f.read())
	f.close()
	# print(_map)

	_map_after_parser = for_map_convert_bin_to_json(_map)

	file = 'map_after_process/' + map_name + '.json'

	with open(file, 'w') as outfile:
		json.dump(_map_after_parser, outfile)









