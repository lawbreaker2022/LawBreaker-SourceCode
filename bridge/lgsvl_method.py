import socket
import json
import numpy
import math 

import lgsvl
from environs import Env

from shapely.geometry import LineString, Point
from shapely.geometry import Polygon

from modules.control.proto import control_cmd_pb2
from modules.drivers.gnss.proto import imu_pb2
from modules.drivers.gnss.proto import ins_pb2
from modules.drivers.gnss.proto import gnss_best_pose_pb2

from modules.localization.proto import imu_pb2 as corrected_imu
from modules.localization.proto import gps_pb2
from modules.perception.proto import perception_obstacle_pb2
from modules.perception.proto import traffic_light_detection_pb2
from modules.planning.proto import planning_pb2

from modules.routing.proto import routing_pb2

from modules.canbus.proto import chassis_pb2
from modules.perception.proto import perception_lane_pb2
from lgsvl_pkgs.lgsvl_msgs.proto import detection2darray_pb2
from modules.drivers.proto import conti_radar_pb2
from modules.drivers.proto import pointcloud_pb2
from modules.localization.proto import pose_pb2


from map_for_bridge import get_map_info


# obstacle_type = {"UNKNOWN": 0, "UNKNOWN_MOVABLE": 1,"UNKNOWN_UNMOVABLE": 2,"PEDESTRIAN": 3,"BICYCLE": 4,"VEHICLE": 5}


class CyberBridgeInstance:
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connect_status = 'disconnected'
		self.setup = []
		self.trace = []
		self.Ego = {}
		self.Canbus = {}
		# self.ctl = {}
		self.traffic_lights = {}
		self.sim = None
		self.destination = []
		self.ego_position_area = None
		self.testFailures = []
		self.junction_ahead = None
		# self.turn_signal = 0
		self.planning_turn_signal = 0

		self.minEgoObsDist = None
		self.AgentNames = []
		self.Check_The_vehicle_is_stuck_or_not = None 
		self.position_for_check = {}
		self.position_check_num = 0

		self.reach_destinaton = False

		self.map_info = None
		self.is_groundtruth = None
		self.truth = {}

		self.is_overtaking = False 
		self.is_lanechanging = False


		# self.Obstacles = {}


	def connect(self):
		if self.connect_status == 'disconnected':
			HOST = '127.0.0.1'  # The server's hostname or IP address
			PORT = 9090        # The port used by the server

			# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
				
			self.connect_status = 'connecting'

			self.sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)

			SEND_BUF_SIZE = 1024*1024
			RECV_BUF_SIZE = 1024*1024
			self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF,SEND_BUF_SIZE)
			self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,RECV_BUF_SIZE)
			self.sock.settimeout(10)

			try:
				self.sock.connect((HOST, PORT))
				self.connect_status = 'connected'
				print('Connected to Apollo Port 9090 successfully!')
				for i in self.setup:
					self.send(i)

				while True:                  
					response = self.receive()
					if response:
						self.receive_publish(response)
					else:
						self.testFailures.append("Receive message is None")
						print('Error!')
						break
					if self.reach_destinaton == True or self.Check_The_vehicle_is_stuck_or_not == "Stuck!":
						break
			except socket.error as err:
				self.testFailures.append("Couldnt connect with the socket-server: " + str(err))
				print ("Couldnt connect with the socket-server: %s\n terminating program" % err)  
		else:
			print('The status of connection is: ' + str(connect_status))
			pass


	def disconnect(self):
		self.sock.close()
		self.connect_status = 'disconnected'


	def send(self, data):
		if self.connect_status == 'connected':
			try:
				self.sock.sendall(data)
			except socket.error as err:
				self.testFailures.append("Send Error: "+str(err))
				print ("Send Error: %s\n terminating program" % err)
				self.disconnect()
		else:
			ptint('Not Connected! Send Fail!')


	def receive(self):
		if self.connect_status == 'connected':
			try:
				response = self.sock.recv(1024*1024)
				# response = response.decode("ascii") 
				if response[0] != 4:
					# print('Receive Error:  Not from Publish')
					# self.disconnect()
					return response
				else:
					return response
			except socket.error as err:
				self.testFailures.append("Receive Error: "+str(err))
				print ("Receive Error: %s\n terminating program" % err)
				self.disconnect()
		else:
			print('Not Connected! Receive Fail!') 


	def add_heading_to_ego(self,angle,x,y,pointx,pointy):

		angle = -angle
		srx = (x-pointx)*math.cos(angle) + (y-pointy)*math.sin(angle)+pointx

		sry = (y-pointy)*math.cos(angle) - (x-pointx)*math.sin(angle)+pointy

		point = [srx , sry]

		return point


	def get_four_polygon_point_list_of_ego(self,original_point,heading_of_ego,lengthen_of_ego,width_of_ego):
		# zhouju = 2.71
		zhouju = 2.697298

		result = []

		point0 = []
		point0.append(original_point[0] + (lengthen_of_ego - zhouju)/2 + zhouju)
		point0.append(original_point[1] + width_of_ego/2)  
		x = point0[0] 
		y = point0[1]
		point0 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
		result.append(point0)

		point1 = []
		point1.append(original_point[0] + (lengthen_of_ego - zhouju)/2 + zhouju)
		point1.append(original_point[1] - width_of_ego/2)
		x = point1[0] 
		y = point1[1]
		point1 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
		result.append(point1)

		point2 = []
		point2.append(original_point[0] - (lengthen_of_ego - zhouju)/2 )
		point2.append(original_point[1] - width_of_ego/2)
		x = point2[0] 
		y = point2[1]
		point2 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
		result.append(point2)

		point3 = []
		point3.append(original_point[0] - (lengthen_of_ego - zhouju)/2 )
		point3.append(original_point[1] + width_of_ego/2)
		x = point3[0] 
		y = point3[1]
		point3 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
		result.append(point3)

		return result


	def get_the_back_middle_point_of_ego(self,original_point,heading_of_ego,lengthen_of_ego,width_of_ego):
		# zhouju = 2.71
		zhouju = 2.697298
		result = []

		point0 = []
		point0.append(original_point[0] - (lengthen_of_ego - zhouju)/2 )
		point0.append(original_point[1] - width_of_ego/2)  
		x = point0[0] 
		y = point0[1]
		point0 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])

		point1 = []
		point1.append(original_point[0] - (lengthen_of_ego - zhouju)/2 )
		point1.append(original_point[1] + width_of_ego/2)
		x = point1[0] 
		y = point1[1]
		point1 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])

		result.append((point0[0] + point1[0])/2) 
		result.append((point0[1] + point1[1])/2) 
		return result


	def get_the_head_middle_point_of_ego(self,original_point,heading_of_ego,lengthen_of_ego,width_of_ego):
		# zhouju = 2.71
		zhouju = 2.697298
		result = []

		point0 = []
		point0.append(original_point[0] + (lengthen_of_ego - zhouju)/2 + zhouju)
		point0.append(original_point[1] + width_of_ego/2)  
		x = point0[0] 
		y = point0[1]
		point0 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])

		point1 = []
		point1.append(original_point[0] + (lengthen_of_ego - zhouju)/2 + zhouju)
		point1.append(original_point[1] - width_of_ego/2)
		x = point1[0] 
		y = point1[1]
		point1 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])

		result.append((point0[0] + point1[0])/2) 
		result.append((point0[1] + point1[1])/2) 
		return result


	def calculate_distToDEstination(self):
		assert self.Ego != {}
		original_point = []
		original_point.append(self.Ego["pose"]["position"]["x"])
		original_point.append(self.Ego["pose"]["position"]["y"])

		heading_of_ego = self.Ego["pose"]["heading"]

		lengthen_of_ego = self.Ego["size"]["length"]
		width_of_ego = self.Ego["size"]["width"]

		ego_polygonPointList = []

		ego_polygonPointList = self.get_four_polygon_point_list_of_ego(original_point,heading_of_ego,lengthen_of_ego,width_of_ego)
		ego = Polygon(ego_polygonPointList)

		point = Point(self.destination[0],self.destination[1])
		distance = point.distance(ego)

		return distance


	def calculate_distToEgo(self, obstacle):
		assert self.Ego != {}
		original_point = []
		original_point.append(self.Ego["pose"]["position"]["x"])
		original_point.append(self.Ego["pose"]["position"]["y"])
		# original_point.append(self.Ego["pose"]["position"]["z"])

		heading_of_ego = self.Ego["pose"]["heading"]

		lengthen_of_ego = self.Ego["size"]["length"]
		width_of_ego = self.Ego["size"]["width"]

		ego_polygonPointList = []

		ego_polygonPointList = self.get_four_polygon_point_list_of_ego(original_point,heading_of_ego,lengthen_of_ego,width_of_ego)

		obstacles_polygonPointList = []

		for _i in obstacle["polygonPointList"]:
			temp = []
			temp.append(_i["x"])
			temp.append(_i["y"])
			obstacles_polygonPointList.append(temp)

		ego = Polygon(ego_polygonPointList)

		obstacle = Polygon(obstacles_polygonPointList)

		Mindis = ego.distance(obstacle)

		return Mindis


	def parse_message_of_pose(self, pose):
		temp = {}

		position = {}
		position["x"] = pose.localization.position.x
		position["y"] = pose.localization.position.y
		position["z"] = pose.localization.position.z
		temp["position"] = position

		orientation = {}
		orientation["qx"] = pose.localization.orientation.qx
		orientation["qy"] = pose.localization.orientation.qy
		orientation["qz"] = pose.localization.orientation.qz
		orientation["qw"] = pose.localization.orientation.qw
		temp["orientation"] = orientation

		linear_velocity = {}
		linear_velocity["x"] = pose.localization.linear_velocity.x
		linear_velocity["y"] = pose.localization.linear_velocity.y
		linear_velocity["z"] = pose.localization.linear_velocity.z
		temp["linearVelocity"] = linear_velocity

		linear_acceleration = {}
		linear_acceleration["x"] = pose.localization.linear_acceleration.x
		linear_acceleration["y"] = pose.localization.linear_acceleration.y
		linear_acceleration["z"] = pose.localization.linear_acceleration.z
		temp["linearAcceleration"] = linear_acceleration

		angular_velocity = {}
		angular_velocity["x"] = pose.localization.angular_velocity.x
		angular_velocity["y"] = pose.localization.angular_velocity.y
		angular_velocity["z"] = pose.localization.angular_velocity.z
		temp["angularVelocity"] = angular_velocity

		heading = pose.localization.heading
		temp["heading"] = heading


		linear_acceleration_vrf = {}
		linear_acceleration_vrf["x"] = pose.localization.linear_acceleration_vrf.x
		linear_acceleration_vrf["y"] = pose.localization.linear_acceleration_vrf.y
		linear_acceleration_vrf["z"] = pose.localization.linear_acceleration_vrf.z
		temp["linearAccelerationVrf"] = linear_acceleration_vrf


		angular_velocity_vrf = {}
		angular_velocity_vrf["x"] = pose.localization.angular_velocity_vrf.x
		angular_velocity_vrf["y"] = pose.localization.angular_velocity_vrf.y
		angular_velocity_vrf["z"] = pose.localization.angular_velocity_vrf.z
		temp["angularVelocityVrf"] = angular_velocity_vrf

		euler_angles = {}
		euler_angles["x"] = pose.localization.euler_angles.x
		euler_angles["y"] = pose.localization.euler_angles.y
		euler_angles["z"] = pose.localization.euler_angles.z
		temp["eulerAngles"] = euler_angles

		self.Ego = {}
		self.Ego["pose"] = temp
		self.Ego["size"] = { "length": 4.7, "width": 2.06 }

		

		if self.Canbus != {} and self.truth != {}:
			single_trace = {}
			single_trace["timestamp"] = pose.header.sequence_num
			# assert self.Canbus!={}
			self.Ego["Chasis"] = self.Canbus
			# for key in self.ctl:
			# 	self.Ego["Chasis"][key] = self.ctl[key]



					# get the polygon of ego vehicle and then do the processing
			original_point = []
			original_point.append(self.Ego["pose"]["position"]["x"])
			original_point.append(self.Ego["pose"]["position"]["y"])
			heading_of_ego = self.Ego["pose"]["heading"]
			lengthen_of_ego = self.Ego["size"]["length"]
			width_of_ego = self.Ego["size"]["width"]
			ego_polygonPointList = []
			ego_polygonPointList = self.get_four_polygon_point_list_of_ego(original_point,heading_of_ego,lengthen_of_ego,width_of_ego)
			self.ego_position_area = Polygon(ego_polygonPointList)

			head_middle_point = self.get_the_head_middle_point_of_ego(original_point,heading_of_ego,lengthen_of_ego,width_of_ego)
			back_middle_point = self.get_the_back_middle_point_of_ego(original_point,heading_of_ego,lengthen_of_ego,width_of_ego)

			currentLane = self.check_current_lane()  #the currentLane API
			self.Ego["currentLane"] = currentLane
			ahead_area_polygon = self.calculate_area_of_ahead(head_middle_point, self.Ego["pose"]["heading"],width_of_ego)
			back_area_polygon = self.calculate_area_of_ahead(back_middle_point, self.Ego["pose"]["heading"],width_of_ego)
			back_area_polygon2 = self.calculate_area_of_ahead2(back_middle_point, self.Ego["pose"]["heading"])

			ahead_area_polygon_for_opposite = self.calculate_area_of_ahead(head_middle_point, self.Ego["pose"]["heading"],width_of_ego, dist=30)

			left_area_polygon = self.calculate_area_of_ahead_left(back_middle_point, self.Ego["pose"]["heading"])
			right_area_polygon = self.calculate_area_of_ahead_right(back_middle_point, self.Ego["pose"]["heading"])
			backward_area_left = self.calculate_area_of_back_left(back_middle_point, self.Ego["pose"]["heading"],width_of_ego)
			backward_area_right = self.calculate_area_of_back_right(back_middle_point, self.Ego["pose"]["heading"],width_of_ego)

			crosswalkAhead = self.calculate_distance_to_crosswalk_ahead(ahead_area_polygon) #the crosswalkAhead API
			self.Ego["crosswalkAhead"] = crosswalkAhead
			# print("crosswalkAhead: "+ str(crosswalkAhead))
			junctionAhead = self.calculate_distance_to_junction_ahead(ahead_area_polygon) #the junctionAhead API
			self.Ego["junctionAhead"] = junctionAhead
			# print("junctionAhead: "+ str(junctionAhead))
			stopSignAhead = self.calculate_distance_to_stopline_of_sign_ahead(ahead_area_polygon) #the stopSignAhead API
			self.Ego["stopSignAhead"] = stopSignAhead
			# print("stopSignAhead: "+ str(stopSignAhead))
			stoplineAhead = self.calculate_distance_to_stopline_of_ahead(back_area_polygon) #the stoplineAhead API
			self.Ego["stoplineAhead"] = stoplineAhead
			# print("stoplineAhead: "+ str(stoplineAhead))

			self.Ego["planning_of_turn"] = self.planning_turn_signal



			# self.deal_with_traffic_signs()
			# print(self.classify_oblist(oblist))
			self.truth["NPCAhead"] = self.find_npc_ahead(self.truth["obsList"], ahead_area_polygon)

			self.truth["PedAhead"] = self.find_ped_ahead(self.truth["obsList"], ahead_area_polygon)

			self.truth["NPCOpposite"] = self.find_npc_opposite(self.truth["obsList"], ahead_area_polygon_for_opposite)


			# print(truth["NPCAhead"])
			# print(truth["PedAhead"])

			self.truth["npcClassification"] =  self.classify_oblist(self.truth["obsList"])
			
			# truth["trafficLight"] = self.traffic_lights


			self.Ego["isTrafficJam"] = self.check_is_traffic_jam(self.truth["obsList"])

			single_trace["ego"] = self.Ego
			if self.is_groundtruth:
				single_trace["truth"] = self.truth
			else:
				single_trace["perception"] = self.truth

			single_trace["traffic_lights"] = self.traffic_lights


			distance = self.calculate_distToDEstination()

			# print(distance)

			threshold = 0.01
			if distance < 2:
				self.reach_destinaton = True
				print("Destination Reached!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
			else: #Check whether the ego vehicle is stuck at on place, this may happen.
				self.reach_destinaton = False
				if self.position_for_check == {}:
					self.position_for_check = self.Ego["pose"]["position"]
					self.position_check_num = 0
				elif abs(self.position_for_check["x"]- self.Ego["pose"]["position"]["x"]) <= threshold and abs(self.position_for_check["y"]- self.Ego["pose"]["position"]["y"]) <= threshold and abs(self.position_for_check["z"]- self.Ego["pose"]["position"]["z"]) <= threshold:
					self.position_check_num += 1
					# print(self.position_check_num)
					# print(self.position_for_check )
					if self.position_check_num >= 150:
						self.Check_The_vehicle_is_stuck_or_not = "Stuck!"
						self.testFailures.append(self.Check_The_vehicle_is_stuck_or_not)
						print('Stuck!')
					else:
						self.Check_The_vehicle_is_stuck_or_not = None 
				else:
					self.position_check_num = 0
					self.position_for_check = self.Ego["pose"]["position"]  


			
			# self.Ego = {}
			# self.traffic_lights = {}
			self.trace.append(single_trace)  

			self.check_is_lane_changing()
			self.check_is_overtaking()
			self.check_is_TurningAround()
			self.Find_Priority_NPCs_and_Peds(back_area_polygon2, left_area_polygon, right_area_polygon, backward_area_left, backward_area_right)
		

	def check_current_lane(self):
		value = {}
		assert self.ego_position_area is not None
		ego = self.ego_position_area

		result = self.map_info.find_which_area_the_ego_is_in(ego)

		# print(result)
		if result != None:
			if result[0].__contains__("lane_id"):
				ego_lane_id = result[0]["lane_id"]
				value["currentLaneId"] = ego_lane_id
				forward = 0
				left = 0
				right = 0
				U = 0
				number = 0
				for _i in result:
					number += _i["laneNumber"] 
					if _i["turn"] == 1:
						forward = 1
					elif _i["turn"] == 2:
						left = 1
					elif _i["turn"] == 3:
						right = 1
					elif _i["turn"] == 4:
						U = 1
				if forward == 1:
					if left == 1:
						if right == 1:
							# value["turn"] = "forwardOrLeftOrRight"
							value["turn"] = 6
						else:
							# value["turn"] = "forwardOrLeft"
							value["turn"] = 4
					else:
						if right == 1:
							# value["turn"] = "forwardOrRight"
							value["turn"] = 5
						else:
							# value["turn"] = "forward"
							value["turn"] = 0
				else:
					if left == 1:
						if right == 1:
							# value["turn"] = "LeftOrRight"
							value["turn"] = 7
						else:
							# value["turn"] = "Left"
							value["turn"] = 1
					else:
						if right == 1:
							# value["turn"] = "Right"
							value["turn"] = 2
						else:
							if U == 1:
								# value["turn"] = "UTurn"
								value["turn"] = 3
							else:
								print("Unexpected!!!")
				value["number"] = number
			if result[0].__contains__("junction_id"):
				ego_lane_id = result[0]["junction_id"]
				value["currentLaneId"] = None
				value["number"] = 0 
		else:
			ego_lane_id = None

		# print(value)

		return value


	def calculate_area_of_ahead(self, original_point, heading_of_ego,width_of_ego, dist=200):
		 # calculate the Ahead area
		ahead_area = []
		point0 = []
		point0.append(original_point[0] + dist)
		point0.append(original_point[1] + dist)  
		x = point0[0] 
		y = point0[1]
		point0 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
		ahead_area.append(point0)

		point1 = []
		point1.append(original_point[0] + dist)
		point1.append(original_point[1] - dist)
		x = point1[0] 
		y = point1[1]
		point1 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
		ahead_area.append(point1)

		point2 = []
		point2.append(original_point[0] - 0 )
		point2.append(original_point[1] - width_of_ego/2)
		x = point2[0] 
		y = point2[1]
		point2 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
		ahead_area.append(point2)

		point3 = []
		point3.append(original_point[0] - 0 )
		point3.append(original_point[1] + width_of_ego/2)
		x = point3[0] 
		y = point3[1]
		point3 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
		ahead_area.append(point3)

		ahead_area_polygon = Polygon(ahead_area)
		return ahead_area_polygon


	def calculate_area_of_back_left(self, original_point, heading_of_ego, width_of_ego):
		 # calculate the Ahead area
		ahead_area = []
		point0 = []
		point0.append(original_point[0] + 0)
		point0.append(original_point[1] - width_of_ego/2-0.3)  
		x = point0[0] 
		y = point0[1]
		point0 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
		ahead_area.append(point0)

		point1 = []
		point1.append(original_point[0] + 0)
		point1.append(original_point[1] - width_of_ego/2-0.3-3)
		x = point1[0] 
		y = point1[1]
		point1 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
		ahead_area.append(point1)

		point2 = []
		point2.append(original_point[0] - 30 )
		point2.append(original_point[1] - width_of_ego/2-0.3-3)
		x = point2[0] 
		y = point2[1]
		point2 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
		ahead_area.append(point2)

		point3 = []
		point3.append(original_point[0] - 30 )
		point3.append(original_point[1] - width_of_ego/2-0.3)
		x = point3[0] 
		y = point3[1]
		point3 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
		ahead_area.append(point3)

		ahead_area_polygon = Polygon(ahead_area)
		return ahead_area_polygon


	def calculate_area_of_back_right(self, original_point, heading_of_ego,width_of_ego):
		 # calculate the Ahead area
		ahead_area = []
		point0 = []
		point0.append(original_point[0] + 0)
		point0.append(original_point[1] + width_of_ego/2+0.3+3)  
		x = point0[0] 
		y = point0[1]
		point0 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
		ahead_area.append(point0)

		point1 = []
		point1.append(original_point[0] + 0)
		point1.append(original_point[1] + width_of_ego/2+0.3)
		x = point1[0] 
		y = point1[1]
		point1 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
		ahead_area.append(point1)

		point2 = []
		point2.append(original_point[0] - 30 )
		point2.append(original_point[1] + width_of_ego/2+0.3)
		x = point2[0] 
		y = point2[1]
		point2 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
		ahead_area.append(point2)

		point3 = []
		point3.append(original_point[0] - 30 )
		point3.append(original_point[1] + width_of_ego/2+0.3+3)
		x = point3[0] 
		y = point3[1]
		point3 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
		ahead_area.append(point3)

		ahead_area_polygon = Polygon(ahead_area)
		return ahead_area_polygon


	def calculate_area_of_ahead2(self, original_point, heading_of_ego):
		 # calculate the Ahead area
		ahead_area = []
		point0 = []
		point0.append(original_point[0] + 200)
		point0.append(original_point[1] + 200)  
		x = point0[0] 
		y = point0[1]
		point0 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
		ahead_area.append(point0)

		point1 = []
		point1.append(original_point[0] + 200)
		point1.append(original_point[1] - 200)
		x = point1[0] 
		y = point1[1]
		point1 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
		ahead_area.append(point1)

		point2 = []
		point2.append(original_point[0] - 0 )
		point2.append(original_point[1] - 200)
		x = point2[0] 
		y = point2[1]
		point2 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
		ahead_area.append(point2)

		point3 = []
		point3.append(original_point[0] - 0 )
		point3.append(original_point[1] + 200)
		x = point3[0] 
		y = point3[1]
		point3 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
		ahead_area.append(point3)

		ahead_area_polygon = Polygon(ahead_area)
		return ahead_area_polygon


	def calculate_area_of_ahead_left(self, original_point, heading_of_ego):
		 # calculate the Ahead area
		ahead_area = []
		point0 = []
		point0.append(original_point[0] + 30)
		point0.append(original_point[1] + 0)  
		x = point0[0] 
		y = point0[1]
		point0 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
		ahead_area.append(point0)

		point1 = []
		point1.append(original_point[0] + 30)
		point1.append(original_point[1] - 30)
		x = point1[0] 
		y = point1[1]
		point1 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
		ahead_area.append(point1)

		point2 = []
		point2.append(original_point[0] - 0 )
		point2.append(original_point[1] - 30)
		x = point2[0] 
		y = point2[1]
		point2 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
		ahead_area.append(point2)

		point3 = []
		point3.append(original_point[0] - 0 )
		point3.append(original_point[1] + 0)
		x = point3[0] 
		y = point3[1]
		point3 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
		ahead_area.append(point3)

		ahead_area_polygon = Polygon(ahead_area)
		return ahead_area_polygon


	def calculate_area_of_ahead_right(self, original_point, heading_of_ego):
		 # calculate the Ahead area
		ahead_area = []
		point0 = []
		point0.append(original_point[0] + 30)
		point0.append(original_point[1] + 30)  
		x = point0[0] 
		y = point0[1]
		point0 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
		ahead_area.append(point0)

		point1 = []
		point1.append(original_point[0] + 30)
		point1.append(original_point[1] - 0)
		x = point1[0] 
		y = point1[1]
		point1 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
		ahead_area.append(point1)

		point2 = []
		point2.append(original_point[0] - 0 )
		point2.append(original_point[1] - 0)
		x = point2[0] 
		y = point2[1]
		point2 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
		ahead_area.append(point2)

		point3 = []
		point3.append(original_point[0] - 0 )
		point3.append(original_point[1] + 30)
		x = point3[0] 
		y = point3[1]
		point3 = self.add_heading_to_ego(heading_of_ego,x,y,original_point[0],original_point[1])
		ahead_area.append(point3)

		ahead_area_polygon = Polygon(ahead_area)
		return ahead_area_polygon


	def calculate_distance_to_stopline_of_sign_ahead(self, ahead_area_polygon):
		result = []
		traffic_sign_list = self.map_info.get_traffic_sign()
	  
		assert self.ego_position_area is not None
		ego = self.ego_position_area

		for _i in traffic_sign_list:
			# single_result = {}
			# single_result["id"] = _i["id"]
			# single_result["type"] = _i["type"]
			points = []
			for _j in _i["stop_line_points"]:
				temp = []
				temp.append(_j["x"])
				temp.append(_j["y"])
				points.append(temp)
			the_line = LineString(points)
			if ahead_area_polygon.distance(the_line) == 0:              
				result.append(ego.distance(the_line))


		if result != []:
			_min = result[0]
		else:
			_min = 200
		for _i in result:
			if _min > _i:
				_min = _i
		return _min


	def calculate_distance_to_crosswalk_ahead(self, ahead_area_polygon):
		result = []
		crosswalk_list = self.map_info.get_crosswalk_config()
		assert self.ego_position_area is not None
		ego = self.ego_position_area

		for key in crosswalk_list:
			points = []
			points = crosswalk_list[key]
			the_area = Polygon(points)  
			if ahead_area_polygon.distance(the_area) == 0:     
				result.append(ego.distance(the_area))

		if result != []:
			_min = result[0]
		else:
			_min = 200
		for _i in result:
			if _min > _i:
				_min = _i
		return _min


	def calculate_distance_to_junction_ahead(self, ahead_area_polygon):
		result = {}
		junction_list = self.map_info.areas["junction_areas"]
		assert self.ego_position_area is not None
		ego = self.ego_position_area


		for key in junction_list:
			points = []
			points = junction_list[key]
			the_area = Polygon(points)   
			if ahead_area_polygon.distance(the_area) == 0:          
				dist = ego.distance(the_area)
				result[key] = dist

		if result!= {}:
			_min = 200
		else:
			self.junction_ahead = None
			_min = 200
		for key in result:
			if _min > result[key]:
				_min = result[key]
				self.junction_ahead = key
		return _min


	def calculate_distance_to_stopline_of_ahead(self, ahead_area_polygon):
		min1 = self.calculate_distance_to_stopline_of_sign_ahead(ahead_area_polygon)

		result = []
		traffic_signal_list = self.map_info.get_traffic_signals()
		assert self.ego_position_area is not None
		ego = self.ego_position_area

		for _i in traffic_signal_list:
			points = []
			for _j in _i["stop_line_points"]:
				temp = []
				temp.append(_j["x"])
				temp.append(_j["y"])
				points.append(temp)
			the_line = LineString(points)
			if ahead_area_polygon.distance(the_line) == 0:              
				result.append(ego.distance(the_line))


		if result != []:
			_min = result[0]
		else:
			_min = 200
		for _i in result:
			if _min > _i:
				_min = _i

		if _min < min1:
			return _min
		else:
			return min1


	def deal_with_traffic_signs(self):
		pass
		# result = {}
		# distance_to_signs = self.calculate_distance_to_stopline_of_sign_ahead()
		# _min = distance_to_signs[0]["distance"]
		# _id =  distance_to_signs[0]["id"]
		# for _i in distance_to_signs:
		#     if _min > _i["distance"]:
		#         _min = _i["distance"]
		#         _id = _i["id"]
		# # print('distance_to_signs: '+str(_min))
		# result["id"] = _id
		# result["distanceToTrafficSign"] = _min

		# distance_to_crosswalk  = self.calculate_distance_to_crosswalk_ahead()

		# _min = distance_to_crosswalk[0]
		# for _i in distance_to_crosswalk:
		#     if _min > _i:
		#         _min = _i

		# return result
		# print('distance_to_crosswalk: '+str(_min))

	# we should know which lane the obstacle is in and classify it.
	def classify_oblist(self, oblist):
		assert self.Ego != {}
		x = self.Ego["pose"]["position"]["x"]
		y = self.Ego["pose"]["position"]["y"]
		point = (x,y)
		the_result_after_classification = dict()

		result = self.map_info.find_which_area_the_point_is_in(point)
		if result != None:
			if result[0].__contains__("lane_id"):
				ego_lane_id = result[0]["lane_id"]
			else:
				ego_lane_id = result[0]["junction_id"]
		else:
			ego_lane_id = None

		same_list = []
		different_list = []
		junction_list = []

		fourth_list = []
		fivth_list = []
		unknown_list = []
		for ob in oblist:
			temp = dict()
			x = ob["position"]["x"]
			y = ob["position"]["y"]
			point = (x,y)
			result = self.map_info.find_which_area_the_point_is_in(point)
			if result != None:
				if result[0].__contains__("lane_id"):
					oblist_lane_id = result[0]["lane_id"]
				else:
					oblist_lane_id = result[0]["junction_id"]
			else:
				oblist_lane_id = None
			if ego_lane_id != None and oblist_lane_id!= None:
				if "lane" in ego_lane_id:
					# print('???')
					if "lane" in oblist_lane_id:
						if self.map_info.check_whether_two_lanes_are_in_the_same_road(ego_lane_id, oblist_lane_id):
							# print("ego and "+ob["name"] +" on the same Road")
							temp["name"] = ob["name"]
							temp["laneId"] = oblist_lane_id
							temp["turn"] = result[0]["turn"]
							same_list.append(temp)
						else:
							# print("ego and "+ob["name"] +" on the different Road")
							temp["name"] = ob["name"]
							temp["laneId"] = oblist_lane_id
							temp["turn"] = result[0]["turn"]
							different_list.append(temp)
					elif "J_" in oblist_lane_id or "junction" in oblist_lane_id:
						# print("ego on lane and "+ob["name"] +" on the junction")
						temp["name"] = ob["name"]
						temp["junctionId"] = oblist_lane_id
						junction_list.append(temp)
				elif "J_" in ego_lane_id or "junction" in oblist_lane_id:
					# print('!!!!')
					if "lane" in oblist_lane_id:
						temp["name"] = ob["name"]
						temp["laneId"] = oblist_lane_id
						temp["turn"] = result[0]["turn"]
						fourth_list.append(temp)
					elif "J_" in ego_lane_id or "junction" in oblist_lane_id:
						temp["name"] = ob["name"]
						temp["junctionId"] = oblist_lane_id
						fivth_list.append(temp)
			else:
				temp["name"] = ob["name"]
				unknown_list.append(temp)

		#When ego on lane
		the_result_after_classification["NextToEgo"] = same_list
		the_result_after_classification["OntheDifferentRoad"] = different_list
		the_result_after_classification["IntheJunction"] = junction_list

		#when ego on junction
		the_result_after_classification["EgoInjunction_Lane"] = fourth_list
		the_result_after_classification["EgoInjunction_junction"] = fivth_list


		return the_result_after_classification
		# print(oblist_lane_position)


	def convert_velocity_to_speed(self, velocity):
		x = velocity["x"]
		y = velocity["y"]
		z = velocity["z"]

		return math.sqrt(x*x+y*y+z*z)


	def find_npc_ahead(self, oblist, ahead_area_polygon):
		assert self.ego_position_area is not None
		ego = self.ego_position_area

		return_value = None
	
		result = self.map_info.find_which_area_the_ego_is_in(ego)
		if result != None:
			if result[0].__contains__("lane_id"): #If in lane area, get the name of the lane.
				ego_lane_id = result[0]["lane_id"]
				_temp = {}
				for _i in oblist:
					points = []
					for _p in _i["polygonPointList"]:
						x = _p["x"]
						y = _p["y"]
						points.append((x,y))
					the_area = Polygon(points)
					result1 = self.map_info.find_which_area_the_ego_is_in(the_area)
					if ahead_area_polygon.distance(the_area) == 0 and _i["type"] == 5 and result1 == result:
						_temp[_i["name"]] = ego.distance(the_area)
						return_value = _i["name"]
				for key in _temp:
					if _temp[key] < _temp[return_value]:
						return_value = key 
				return return_value
			else:
				ego_lane_id = result[0]["junction_id"] #If in junction area, get the name of the lane.
				_temp = {}
				for _i in oblist:
					points = []
					for _p in _i["polygonPointList"]:
						x = _p["x"]
						y = _p["y"]
						points.append((x,y))
					the_area = Polygon(points) 
					if ahead_area_polygon.distance(the_area) == 0 and _i["type"] == 5:
						_temp[_i["name"]] = ego.distance(the_area)
						return_value = _i["name"]
				for key in _temp:
					if _temp[key] < _temp[return_value]:
						return_value = key 
				return return_value
		else:
			print("!bug of localization of ego")
			return return_value


	def find_ped_ahead(self, oblist, ahead_area_polygon):
		assert self.ego_position_area is not None
		ego = self.ego_position_area

		return_value = None
		_temp = {}
		for _i in oblist:
			points = []
			for _p in _i["polygonPointList"]:
				x = _p["x"]
				y = _p["y"]
				points.append((x,y))
			the_area = Polygon(points) 
			if ahead_area_polygon.distance(the_area) == 0 and _i["type"] == 3:
				_temp[_i["name"]] = ego.distance(the_area)
				return_value = _i["name"]             
		for key in _temp:
			if _temp[key] < _temp[return_value]:
				return_value = key 
		return return_value


	def find_npc_opposite(self, oblist, ahead_area_polygon):
		assert self.ego_position_area is not None
		ego = self.ego_position_area

		heading_of_ego = self.Ego["pose"]["heading"]

		return_value = None
		_temp = {}
		for _i in oblist:
			points = []
			for _p in _i["polygonPointList"]:
				x = _p["x"]
				y = _p["y"]
				points.append((x,y))
			the_area = Polygon(points) 
			if ahead_area_polygon.distance(the_area) == 0 and _i["type"] == 5:
				heading_of_npc = _i["theta"]
				heading_of_npc = self.process_with_angle_pi(heading_of_npc)
				if abs(heading_of_npc- heading_of_ego)> 3*math.pi/4 and abs(heading_of_npc- heading_of_ego)< 5*math.pi/4:					
					_temp[_i["name"]] = ego.distance(the_area)
					return_value = _i["name"]             
		for key in _temp:
			if _temp[key] < _temp[return_value]:
				return_value = key 
		return return_value


	def check_is_traffic_jam(self, oblist):
		number = 0
		for _i in oblist:
			points = []
			if _i["speed"] < 1 and _i["type"] == 5:
				for _p in _i["polygonPointList"]:
					x = _p["x"]
					y = _p["y"]
					points.append((x,y))
				the_area = Polygon(points)
				junction = self.map_info.check_whether_in_junction_area(the_area)
				if junction != []:
					# print(junction)
					# print(self.junction_ahead)
					if junction[0]["junction_id"] == self.junction_ahead:
						number = number + 1

		if number >=3:
			return True
		else:
			return False


	def check_is_lane_changing(self):
		num_of_track = -10 	#check the value of 5 states before
		if len(self.trace) >= -num_of_track: 
			if self.trace[num_of_track]["ego"]["isLaneChanging"] == False:
				previous_trace = self.trace[num_of_track]
				orig = previous_trace["ego"]["currentLane"]["currentLaneId"]
				if previous_trace["ego"]["planning_of_turn"] != 0:
					#print("is turning")
					for num in range(num_of_track+1,0):
						dest = self.trace[num]["ego"]["currentLane"]["currentLaneId"]
						In_the_same_road = self.map_info.check_whether_two_lanes_are_in_the_same_road(orig, dest)
						if dest != orig and dest != None and In_the_same_road == True:
							self.trace[num_of_track]["ego"]["isLaneChanging"] = True
							# print("dectect lane change previous!!")

		# if self.reach_destinaton or self.Check_The_vehicle_is_stuck_or_not == "Stuck!":
		# 	if len(self.trace) >= -num_of_track: 
		# 		for num in range(num_of_track+1,0):
		# 			self.trace[num]["ego"]["isLaneChanging"] = False
		# 	else:
		# 		for num in range(-len(self.trace),0):
		# 			self.trace[num]["ego"]["isLaneChanging"] = False


	def check_is_overtaking(self):	
		self.trace[-1]["ego"]["isOverTaking"] = self.is_overtaking
		if self.is_overtaking:
			self.trace[-1]["ego"]["isLaneChanging"] = True		
		else:
			self.trace[-1]["ego"]["isLaneChanging"] = False		

		# print(self.trace[-1]["ego"]["isOverTaking"])
		# num_of_track = -10 	#check the value of 20 states before
		# if len(self.trace) >= -num_of_track: 
		# 	self.trace[num_of_track]["ego"]["isOverTaking"] = False
		# 	previous_trace = self.trace[num_of_track]
		# 	orig = previous_trace["ego"]["currentLane"]["currentLaneId"]

		# 	if self.is_groundtruth:
		# 		npc_ahead = previous_trace["truth"]["NPCAhead"]
		# 		obstacles = previous_trace["truth"]["obsList"]
		# 	else:
		# 		npc_ahead = previous_trace["perception"]["NPCAhead"]
		# 		obstacles = previous_trace["perception"]["obsList"]

		# 	# when the car is lanechanging, check whether it's overtaking on wthether there is a npc ahead
		# 	if previous_trace["ego"]["isLaneChanging"] == True and npc_ahead!= None:
		# 		previous_trace["ego"]["isOverTaking"] = True
		# 		print("dectect overtake previous!!")
		# 		# print(npc_ahead)
		# 		# for obstacle in obstacles:
		# 		# 	if obstacle["name"] == npc_ahead:
		# 		# 		print(obstacle["distToEgo"])
		# 		# 		if obstacle["distToEgo"] <= 15:
		# 	# if 	
		# 		# for num in range(num_of_track+1,0):
		# 		# 	dest = self.trace[num]["ego"]["currentLane"]["currentLaneId"]
		# 		# 	if dest != orig and dest != None:
		# 		# 		# when lane change has finshed, the car move to another lane
		# 		# 		# , then check whether the car return to original lane
		# 		# 		for num2 in range(num+1,0):
		# 		# 			dest2 = self.trace[num2]["ego"]["currentLane"]["currentLaneId"]
		# 		# 			if dest2 == orig:
				

		# if self.reach_destinaton or self.Check_The_vehicle_is_stuck_or_not == "Stuck!":
		# 	if len(self.trace) >= -num_of_track: 
		# 		for num in range(num_of_track+1,0):
		# 			self.trace[num]["ego"]["isOverTaking"] = False
		# 	else:
		# 		for num in range(-len(self.trace),0):
		# 			self.trace[num]["ego"]["isOverTaking"] = False


	def process_with_angle_pi(self, angle_pi):
		if angle_pi<0:
			return angle_pi + 2*math.pi
		else:
			return angle_pi


	def check_is_TurningAround(self):
		num_of_track = -20 	#check the value of 5 states before
		if len(self.trace) >= -num_of_track: 
			self.trace[num_of_track]["ego"]["isTurningAround"] = False
			previous_trace = self.trace[num_of_track]
			# orig = previous_trace["ego"]["currentLane"]["currentLaneId"]
			orig = previous_trace["ego"]["pose"]["heading"]
			orig = self.process_with_angle_pi(orig)
			if previous_trace["ego"]["planning_of_turn"] != 0:
				#print("is turning")
				for num in range(num_of_track+1,0):
					# dest = self.trace[num]["ego"]["currentLane"]["currentLaneId"]
					dest = self.trace[num]["ego"]["pose"]["heading"]
					dest = self.process_with_angle_pi(dest)
					# print(str(dest) +"-" + str(orig) +"= "+str(abs(dest - orig)))
					if abs(dest - orig) > 3*math.pi/4:
						self.trace[num_of_track]["ego"]["isTurningAround"] = True
						# print("dectect Turning Around previous!!")

		if self.reach_destinaton or self.Check_The_vehicle_is_stuck_or_not == "Stuck!":
			if len(self.trace) >= -num_of_track: 
				for num in range(num_of_track+1,0):
					self.trace[num]["ego"]["isTurningAround"] = False
			else:
				for num in range(-len(self.trace),0):
					self.trace[num]["ego"]["isTurningAround"] = False


	def _sub_Find_Priority_NPCs_and_Peds(self, ahead_square_area , left_area_polygon, right_area_polygon, num_of_track, backward_area_left, backward_area_right):
		previous_trace = self.trace[num_of_track]
		previous_trace["ego"]["PriorityNPCAhead"] = False 
		previous_trace["ego"]["PriorityPedsAhead"] = False 		

		if self.is_groundtruth:
			obstacles = previous_trace["truth"]["obsList"]
			_road =  previous_trace["truth"]
		else:
			obstacles = previous_trace["perception"]["obsList"]
			_road =  previous_trace["perception"]

		heading_of_ego = previous_trace["ego"]["pose"]["heading"]
		heading_of_ego = self.process_with_angle_pi(heading_of_ego)

		# if we are turning, we should give way to the cars in the direct way
		for obstacle in obstacles:
			points = []
			for _p in obstacle["polygonPointList"]:
				x = _p["x"]
				y = _p["y"]
				points.append((x,y))
			the_area = Polygon(points)
			# Find priority NPC of ahead
			if _road['NPCAhead'] == obstacle['name'] and obstacle['distToEgo'] < 3:
				previous_trace["ego"]["PriorityNPCAhead"] = True
			if obstacle["type"] == 5:
				# Find priority NPC when turning
				heading_of_npc = obstacle["theta"]
				heading_of_npc = self.process_with_angle_pi(heading_of_npc)
				if previous_trace["ego"]["planning_of_turn"] != 0 and previous_trace["ego"]["isLaneChanging"] == False:
					points = []
					if abs(heading_of_npc- heading_of_ego)>math.pi/4 and abs(heading_of_npc- heading_of_ego)< 3*math.pi/4:
						if obstacle["distToEgo"] < 30 and ahead_square_area.distance(the_area) == 0:
							previous_trace["ego"]["PriorityNPCAhead"] = True
							# print("Find priority NPC for turing!")
				# Find priority NPC when lane changing
				if previous_trace["ego"]["isLaneChanging"] == True:
					if abs(heading_of_npc- heading_of_ego)<math.pi/4 :
						ego_speed = self.convert_velocity_to_speed(previous_trace["ego"]["pose"]["linearVelocity"])
						if previous_trace["ego"]["planning_of_turn"] == 1 and backward_area_left.distance(the_area) == 0: #left lane changing
							if obstacle["distToEgo"] < 10 and obstacle["speed"] > ego_speed:
								previous_trace["ego"]["PriorityNPCAhead"] = True
								print("Find priority NPC for left lane changing!")
						if previous_trace["ego"]["planning_of_turn"] == 2 and backward_area_right.distance(the_area) == 0: #right lane changing
							if obstacle["distToEgo"] < 10 and obstacle["speed"] > ego_speed:
								previous_trace["ego"]["PriorityNPCAhead"] = True
								print("Find priority NPC for right lane changing!")

			elif obstacle["type"] == 3:
				if previous_trace["ego"]["planning_of_turn"] == 0:						
					if obstacle["distToEgo"] < 3 and ahead_square_area.distance(the_area) == 0: 
						previous_trace["ego"]["PriorityPedsAhead"] = True
						print("Find priority Ped for direct!")
				if previous_trace["ego"]["planning_of_turn"] == 1:						
					if obstacle["distToEgo"] < 10 and left_area_polygon.distance(the_area) == 0: 
						previous_trace["ego"]["PriorityPedsAhead"] = True
						print("Find priority Ped for turning left!")
				if previous_trace["ego"]["planning_of_turn"] == 2:						
					if obstacle["distToEgo"] < 10 and right_area_polygon.distance(the_area) == 0: 
						previous_trace["ego"]["PriorityPedsAhead"] = True
						print("Find priority Ped for turning right!")

  # enum SubType {
  #   ST_UNKNOWN = 0;
  #   ST_UNKNOWN_MOVABLE = 1;
  #   ST_UNKNOWN_UNMOVABLE = 2;
  #   ST_CAR = 3;
  #   ST_VAN = 4;
  #   ST_TRUCK = 5;
  #   ST_BUS = 6;
  #   ST_CYCLIST = 7;
  #   ST_MOTORCYCLIST = 8;
  #   ST_TRICYCLIST = 9;
  #   ST_PEDESTRIAN = 10;
  #   ST_TRAFFICCONE = 11;
  # };

  # enum Type {
  #   UNKNOWN = 0;
  #   UNKNOWN_MOVABLE = 1;
  #   UNKNOWN_UNMOVABLE = 2;
  #   PEDESTRIAN = 3;  // Pedestrian, usually determined by moving behavior.
  #   BICYCLE = 4;     // bike, motor bike
  #   VEHICLE = 5;     // Passenger car or truck.
  # };

	def Find_Priority_NPCs_and_Peds(self, ahead_square_area , left_area_polygon, right_area_polygon, backward_area_left, backward_area_right):
		num_of_track = -20
		if len(self.trace) >= -num_of_track: 
			self._sub_Find_Priority_NPCs_and_Peds(ahead_square_area , left_area_polygon, right_area_polygon, num_of_track, backward_area_left, backward_area_right)

			# previous_trace = self.trace[num_of_track]
			# previous_trace["ego"]["PriorityNPCAhead"] = False 
			# previous_trace["ego"]["PriorityPedsAhead"] = False 		

			# if self.is_groundtruth:
			# 	obstacles = previous_trace["truth"]["obsList"]
			# 	_road =  previous_trace["truth"]
			# else:
			# 	obstacles = previous_trace["perception"]["obsList"]
			# 	_road =  previous_trace["perception"]

			# heading_of_ego = previous_trace["ego"]["pose"]["heading"]
			# heading_of_ego = self.process_with_angle_pi(heading_of_ego)

			# # if we are turning, we should give way to the cars in the direct way
			# for obstacle in obstacles:
			# 	points = []
			# 	for _p in obstacle["polygonPointList"]:
			# 		x = _p["x"]
			# 		y = _p["y"]
			# 		points.append((x,y))
			# 	the_area = Polygon(points)
			# 	if _road['NPCAhead'] == obstacle['name'] and obstacle['distToEgo'] < 3:
			# 		previous_trace["ego"]["PriorityNPCAhead"] = True
			# 	if obstacle["type"] == 5:
			# 		if previous_trace["ego"]["planning_of_turn"] != 0 and previous_trace["ego"]["isLaneChanging"] == False:
			# 			heading_of_npc = obstacle["theta"]
			# 			heading_of_npc = self.process_with_angle_pi(heading_of_npc)
			# 			points = []
			# 			if abs(heading_of_npc- heading_of_ego)>math.pi/4 and abs(heading_of_npc- heading_of_ego)< 3*math.pi/4:
			# 				if obstacle["distToEgo"] < 30 and ahead_square_area.distance(the_area) == 0:
			# 					previous_trace["ego"]["PriorityNPCAhead"] = True
			# 					print("Find priority NPC for turing!")
			# 	elif obstacle["type"] == 3:
			# 		if previous_trace["ego"]["planning_of_turn"] == 0:						
			# 			if obstacle["distToEgo"] < 3 and ahead_square_area.distance(the_area) == 0: 
			# 				previous_trace["ego"]["PriorityPedsAhead"] = True
			# 				print("Find priority NPC for direct!")
			# 		if previous_trace["ego"]["planning_of_turn"] == 1:						
			# 			if obstacle["distToEgo"] < 10 and left_area_polygon.distance(the_area) == 0: 
			# 				previous_trace["ego"]["PriorityPedsAhead"] = True
			# 				print("Find priority NPC for turning left!")
			# 		if previous_trace["ego"]["planning_of_turn"] == 2:						
			# 			if obstacle["distToEgo"] < 10 and right_area_polygon.distance(the_area) == 0: 
			# 				previous_trace["ego"]["PriorityPedsAhead"] = True
			# 				print("Find priority NPC for turning right!")

			

			

		if self.reach_destinaton or self.Check_The_vehicle_is_stuck_or_not == "Stuck!":
			if len(self.trace) >= -num_of_track: 
				for num in range(num_of_track+1,0):
					self._sub_Find_Priority_NPCs_and_Peds(ahead_square_area , left_area_polygon, right_area_polygon, num, backward_area_left, backward_area_right)
					# previous_trace = self.trace[num]
					# previous_trace["ego"]["PriorityNPCAhead"] = False 
					# previous_trace["ego"]["PriorityPedsAhead"] = False 

					# if self.is_groundtruth:
					# 	obstacles = previous_trace["truth"]["obsList"]
					# else:
					# 	obstacles = previous_trace["perception"]["obsList"]

					# heading_of_ego = previous_trace["ego"]["pose"]["heading"]
					# heading_of_ego = self.process_with_angle_pi(heading_of_ego)

					# for obstacle in obstacles:
					# 	points = []
					# 	for _p in obstacle["polygonPointList"]:
					# 		x = _p["x"]
					# 		y = _p["y"]
					# 		points.append((x,y))
					# 	the_area = Polygon(points)
					# 	if _road['NPCAhead'] == obstacle['name'] and obstacle['distToEgo'] < 3:
					# 		previous_trace["ego"]["PriorityNPCAhead"] = True
					# 	if obstacle["type"] == 5:							
					# 		# if we are turning, we should give way to the cars in the direct way
					# 		if previous_trace["ego"]["planning_of_turn"] != 0 and previous_trace["ego"]["isLaneChanging"] == False:
					# 			heading_of_npc = obstacle["theta"]
					# 			heading_of_npc = self.process_with_angle_pi(heading_of_npc)
					# 			if abs(heading_of_npc- heading_of_ego)>math.pi/4 and abs(heading_of_npc- heading_of_ego)< 3*math.pi/4:
					# 				if obstacle["distToEgo"] < 30 and ahead_square_area.distance(the_area) == 0:
					# 					previous_trace["ego"]["PriorityNPCAhead"] = True
					# 					print("Find priority NPC for turing!")
					# 	elif obstacle["type"] == 3:
					# 		if previous_trace["ego"]["planning_of_turn"] == 0:						
					# 			if obstacle["distToEgo"] < 3 and ahead_square_area.distance(the_area) == 0: 
					# 				previous_trace["ego"]["PriorityPedsAhead"] = True
					# 				print("Find priority NPC for direct!")
					# 		if previous_trace["ego"]["planning_of_turn"] == 1:						
					# 			if obstacle["distToEgo"] < 10 and left_area_polygon.distance(the_area) == 0: 
					# 				previous_trace["ego"]["PriorityPedsAhead"] = True
					# 				print("Find priority NPC for turning left!")
					# 		if previous_trace["ego"]["planning_of_turn"] == 2:						
					# 			if obstacle["distToEgo"] < 10 and right_area_polygon.distance(the_area) == 0: 
					# 				previous_trace["ego"]["PriorityPedsAhead"] = True
					# 				print("Find priority NPC for turning right!")
			else:				
				for num in range(-len(self.trace),0):
					self._sub_Find_Priority_NPCs_and_Peds(ahead_square_area , left_area_polygon, right_area_polygon, num, backward_area_left, backward_area_right)
					# previous_trace = self.trace[num]
					# previous_trace["ego"]["PriorityNPCAhead"] = False 
					# previous_trace["ego"]["PriorityPedsAhead"] = False 

					# if self.is_groundtruth:
					# 	obstacles = previous_trace["truth"]["obsList"]
					# else:
					# 	obstacles = previous_trace["perception"]["obsList"]

					# heading_of_ego = previous_trace["ego"]["pose"]["heading"]
					# heading_of_ego = self.process_with_angle_pi(heading_of_ego)

					# for obstacle in obstacles:
					# 	points = []
					# 	for _p in obstacle["polygonPointList"]:
					# 		x = _p["x"]
					# 		y = _p["y"]
					# 		points.append((x,y))
					# 	the_area = Polygon(points)
					# 	if _road['NPCAhead'] == obstacle['name'] and obstacle['distToEgo'] < 3:
					# 		previous_trace["ego"]["PriorityNPCAhead"] = True
					# 	if obstacle["type"] == 5:
					# 		# if we are turning, we should give way to the cars in the direct way
					# 		if previous_trace["ego"]["planning_of_turn"] != 0 and previous_trace["ego"]["isLaneChanging"] == False:
					# 			heading_of_npc = obstacle["theta"]
					# 			heading_of_npc = self.process_with_angle_pi(heading_of_npc)
					# 			if abs(heading_of_npc- heading_of_ego)>math.pi/4 and abs(heading_of_npc- heading_of_ego)< 3*math.pi/4:
					# 				if obstacle["distToEgo"] < 30 and ahead_square_area.distance(the_area) == 0:
					# 					previous_trace["ego"]["PriorityNPCAhead"] = True
					# 					print("Find priority NPC for turing!")
					# 	elif obstacle["type"] == 3:
					# 		if previous_trace["ego"]["planning_of_turn"] == 0:						
					# 			if obstacle["distToEgo"] < 3 and ahead_square_area.distance(the_area) == 0: 
					# 				previous_trace["ego"]["PriorityPedsAhead"] = True
					# 				print("Find priority NPC for direct!")
					# 		if previous_trace["ego"]["planning_of_turn"] == 1:						
					# 			if obstacle["distToEgo"] < 10 and left_area_polygon.distance(the_area) == 0: 
					# 				previous_trace["ego"]["PriorityPedsAhead"] = True
					# 				print("Find priority NPC for turning left!")
					# 		if previous_trace["ego"]["planning_of_turn"] == 2:						
					# 			if obstacle["distToEgo"] < 10 and right_area_polygon.distance(the_area) == 0: 
					# 				previous_trace["ego"]["PriorityPedsAhead"] = True
					# 				print("Find priority NPC for turning right!")


	def parse_message_of_obstacles(self, obstacles):
		oblist = []
		# print("!!!!!!!")
		# print(hasattr(obstacles.perception_obstacle[0],'position'))
		self.truth ={}
		truth = {}
		if self.Ego != {}:
			# print(self.Ego["pose"]["heading"])
			for _i in obstacles.perception_obstacle:
				oblist.append({})
				if hasattr(_i,'id'):
					theta = _i.id
					oblist[-1]["id"] = theta

				if hasattr(_i,'position'):
					position = {}
					position["x"] = _i.position.x
					position["y"] = _i.position.y
					position["z"] = _i.position.z
					oblist[-1]["position"] = position

				if hasattr(_i,'theta'):
					theta = _i.theta
					oblist[-1]["theta"] = theta



				if hasattr(_i,'velocity'):
					velocity = {}
					velocity["x"] = _i.velocity.x
					velocity["y"] = _i.velocity.y
					velocity["z"] = _i.velocity.z
					oblist[-1]["velocity"] = velocity

				speed = self.convert_velocity_to_speed(velocity)
				oblist[-1]["speed"] = speed

				if hasattr(_i,'length'):
					length = _i.length
					oblist[-1]["length"] = length   

				if hasattr(_i,'width'):
					width = _i.width
					oblist[-1]["width"] = width

				if hasattr(_i,'height'):
					height = _i.height
					oblist[-1]["height"] = height    

				if hasattr(_i,"polygon_point"):
					temp0 = []        
					for _j in _i.polygon_point:
						temp = {}
						temp["x"] = _j.x
						temp["y"] = _j.y
						temp["z"] = _j.z
						temp0.append(temp)
					oblist[-1]["polygonPointList"] = temp0   

				if hasattr(_i,"tracking_time"):
					trackingTime = _i.tracking_time
					oblist[-1]["trackingTime"] = trackingTime  

				if hasattr(_i,"type"):
					type0 = _i.type
					oblist[-1]["type"] = type0

				if hasattr(_i,"timestamp"):
					timestamp = _i.timestamp
					oblist[-1]["timestamp"] = timestamp

				if hasattr(_i,"pointCloudList"):
					temp0 = []
					temp = {}
					for _j in _i.pointCloudList:
						temp["x"] = _j.x
						temp["y"] = _j.y
						temp["z"] = _j.z
						temp0.append(temp)
					oblist[-1]["pointCloudList"] = temp0  
				else:
					oblist[-1]["pointCloudList"] = []   

				if hasattr(_i,"dropsList"):
					temp0 = []
					temp = {}
					for _j in _i.dropsList:
						temp["x"] = _j.x
						temp["y"] = _j.y
						temp["z"] = _j.z
						temp0.append(temp)
					oblist[-1]["dropsList"] = temp0  
				else:
					oblist[-1]["dropsList"] = [] 

				if hasattr(_i,"acceleration"):
					acceleration = {}
					acceleration["x"] = _i.acceleration.x
					acceleration["y"] = _i.acceleration.y
					acceleration["z"] = _i.acceleration.z
					oblist[-1]["acceleration"] = acceleration   

				if hasattr(_i,"anchor_point"):
					anchorPoint = {}
					anchorPoint["x"] = _i.anchor_point.x
					anchorPoint["y"] = _i.anchor_point.y
					anchorPoint["z"] = _i.anchor_point.z
					oblist[-1]["anchorPoint"] = anchorPoint

				if hasattr(_i,"bbox2d"):
					bbox2d = {}
					bbox2d["xmin"] = _i.bbox2d.xmin
					bbox2d["ymin"] = _i.bbox2d.ymin
					bbox2d["xmax"] = _i.bbox2d.xmax
					bbox2d["ymax"] = _i.bbox2d.ymax
					oblist[-1]["bbox2d"] = bbox2d

				if hasattr(_i,"sub_type"):
					subType = _i.sub_type
					oblist[-1]["subType"] = subType

				if hasattr(_i,"measurements"):
					temp0 = []
					for _j in _i.measurements:
						temp = {}
						temp["sensorId"] = _j.sensor_id
						temp["id"] = _j.id

						temp1 = {}
						temp1["x"] = _j.position.x
						temp1["y"] = _j.position.y
						temp1["z"] = _j.position.z

						temp["position"] = temp1
						temp["theta"] = _j.theta
						temp["length"] = _j.length
						temp["width"] = _j.width
						temp["height"] = _j.height

						temp1 = {}
						temp1["x"] = _j.velocity.x
						temp1["y"] = _j.velocity.y
						temp1["z"] = _j.velocity.z
						temp["velocity"] = temp1

						temp["type"] = _j.type

						if hasattr(_j,"sub_type"):
							subType = _j.sub_type
							temp["subType"] = subType

						temp["timestamp"] = _j.timestamp

						temp0.append(temp)
					oblist[-1]["measurementsList"] = temp0  

				if hasattr(_i,"height_above_ground"):
					height_above_ground = _i.height_above_ground
					oblist[-1]["heightAboveGround"] = height_above_ground


				if hasattr(_i,"position_covariance"):
					temp0 = []
					for _j in _i.position_covariance:
						temp0.append(_j)
					oblist[-1]["positionCovarianceList"] = temp0

				if hasattr(_i,"velocity_covariance"):
					temp0 = []
					for _j in _i.velocity_covariance:
						temp0.append(_j)
					oblist[-1]["velocityCovarianceList"] = temp0

				if hasattr(_i,"acceleration_covariance"):
					temp0 = []
					for _j in _i.acceleration_covariance:
						temp0.append(_j)
					oblist[-1]["accelerationCovarianceList"] = temp0

				if hasattr(_i,"type_name"):
					type_name = _i.type_name
					oblist[-1]["typeName"] = type_name   

				if hasattr(_i,"sub_type_name"):
					sub_type_name = _i.sub_type_name
					oblist[-1]["subTypeName"] = sub_type_name 

				# if hasattr(_i,"name"):
				#     name = _i.name
				#     oblist[-1]["name"] = name 
				# else:
				num = oblist[-1]["id"]
				oblist[-1]["name"] = self.AgentNames[num-2]

				# print(str(self.AgentNames[num-2])+ "  " +str(theta))

				if self.Ego != {}:
					distToEgo = self.calculate_distToEgo(oblist[-1])
					oblist[-1]["distToEgo"] = distToEgo
					# print(distToEgo)
		
			if len(oblist) > 0:
				nearestGtObs = oblist[0]["name"]
				minDistToEgo = oblist[0]["distToEgo"]

				NearestNPC = None

				for _ii in oblist:
					if _ii["distToEgo"] <= minDistToEgo:
						minDistToEgo = _ii["distToEgo"]
						nearestGtObs = _ii["name"]
						if _ii['type'] == 5:
							NearestNPC = _ii["name"]

				truth["minDistToEgo"] = minDistToEgo
				truth["nearestGtObs"] = nearestGtObs
				truth["NearestNPC"] = NearestNPC
				truth["obsList"] = oblist
				# single_trace = {}
				# # single_trace["timestamp"] = obstacles.header.lidar_timestamp
			else:
				truth["obsList"] = oblist
				# single_trace["timestamp"] = obstacles.header.lidar_timestamp
				truth["NearestNPC"] = None
				truth["minDistToEgo"] = 200
				truth["nearestGtObs"] = None

			self.truth = truth

			# # get the polygon of ego vehicle and then do the processing
			# original_point = []
			# original_point.append(self.Ego["pose"]["position"]["x"])
			# original_point.append(self.Ego["pose"]["position"]["y"])
			# heading_of_ego = self.Ego["pose"]["heading"]
			# lengthen_of_ego = self.Ego["size"]["length"]
			# width_of_ego = self.Ego["size"]["width"]
			# ego_polygonPointList = []
			# ego_polygonPointList = self.get_four_polygon_point_list_of_ego(original_point,heading_of_ego,lengthen_of_ego,width_of_ego)
			# self.ego_position_area = Polygon(ego_polygonPointList)

			# head_middle_point = self.get_the_head_middle_point_of_ego(original_point,heading_of_ego,lengthen_of_ego,width_of_ego)
			# back_middle_point = self.get_the_back_middle_point_of_ego(original_point,heading_of_ego,lengthen_of_ego,width_of_ego)

			# currentLane = self.check_current_lane()  #the currentLane API
			# self.Ego["currentLane"] = currentLane
			# ahead_area_polygon = self.calculate_area_of_ahead(head_middle_point, self.Ego["pose"]["heading"],width_of_ego)
			# back_area_polygon = self.calculate_area_of_ahead(back_middle_point, self.Ego["pose"]["heading"],width_of_ego)
			# back_area_polygon2 = self.calculate_area_of_ahead2(back_middle_point, self.Ego["pose"]["heading"])

			# left_area_polygon = self.calculate_area_of_ahead_left(back_middle_point, self.Ego["pose"]["heading"])
			# right_area_polygon = self.calculate_area_of_ahead_right(back_middle_point, self.Ego["pose"]["heading"])

			# crosswalkAhead = self.calculate_distance_to_crosswalk_ahead(ahead_area_polygon) #the crosswalkAhead API
			# self.Ego["crosswalkAhead"] = crosswalkAhead
			# # print("crosswalkAhead: "+ str(crosswalkAhead))
			# junctionAhead = self.calculate_distance_to_junction_ahead(ahead_area_polygon) #the junctionAhead API
			# self.Ego["junctionAhead"] = junctionAhead
			# # print("junctionAhead: "+ str(junctionAhead))
			# stopSignAhead = self.calculate_distance_to_stopline_of_sign_ahead(ahead_area_polygon) #the stopSignAhead API
			# self.Ego["stopSignAhead"] = stopSignAhead
			# # print("stopSignAhead: "+ str(stopSignAhead))
			# stoplineAhead = self.calculate_distance_to_stopline_of_ahead(back_area_polygon) #the stoplineAhead API
			# self.Ego["stoplineAhead"] = stoplineAhead
			# # print("stoplineAhead: "+ str(stoplineAhead))

			# self.Ego["planning_of_turn"] = self.turn_signal

			

		


			# # self.deal_with_traffic_signs()
			# # print(self.classify_oblist(oblist))
			# truth["NPCAhead"] = self.find_npc_ahead(oblist, ahead_area_polygon)

			# truth["PedAhead"] = self.find_ped_ahead(oblist, ahead_area_polygon)


			# # print(truth["NPCAhead"])
			# # print(truth["PedAhead"])

			# truth["npcClassification"] =  self.classify_oblist(oblist)
			
			# # truth["trafficLight"] = self.traffic_lights


			# self.Ego["isTrafficJam"] = self.check_is_traffic_jam(oblist)

			# single_trace["ego"] = self.Ego
			# if self.is_groundtruth:
			# 	single_trace["truth"] = truth
			# else:
			# 	single_trace["perception"] = truth

			# single_trace["traffic_lights"] = self.traffic_lights


			# distance = self.calculate_distToDEstination()

			# threshold = 0.01
			# if distance < 2:
			# 	self.reach_destinaton = True
			# 	print("Destination Reached!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
			# else: #Check whether the ego vehicle is stuck at on place, this may happen.
			# 	self.reach_destinaton = False
			# 	if self.position_for_check == {}:
			# 		self.position_for_check = self.Ego["pose"]["position"]
			# 		self.position_check_num = 0
			# 	elif abs(self.position_for_check["x"]- self.Ego["pose"]["position"]["x"]) <= threshold and abs(self.position_for_check["y"]- self.Ego["pose"]["position"]["y"]) <= threshold and abs(self.position_for_check["z"]- self.Ego["pose"]["position"]["z"]) <= threshold:
			# 		self.position_check_num += 1
			# 		# print(self.position_check_num)
			# 		# print(self.position_for_check )
			# 		if self.position_check_num >= 50:
			# 			self.Check_The_vehicle_is_stuck_or_not = "Stuck!"
			# 			self.testFailures.append(self.Check_The_vehicle_is_stuck_or_not)
			# 			print('Stuck!')
			# 		else:
			# 			self.Check_The_vehicle_is_stuck_or_not = None 
			# 	else:
			# 		self.position_check_num = 0
			# 		self.position_for_check = self.Ego["pose"]["position"]  


			
			# # self.Ego = {}
			# # self.traffic_lights = {}
			# self.trace.append(single_trace)  

			# self.check_is_lane_changing()
			# self.check_is_overtaking()
			# self.check_is_TurningAround()
			# self.Find_Priority_NPCs_and_Peds(back_area_polygon2, left_area_polygon, right_area_polygon)
   

		else:
			pass


	def calculate_distance_to_traffic_light_stop_line(self, ID):
		# result = []
		traffic_signal_list = self.map_info.get_traffic_signals()

		assert self.Ego != {}
		original_point = []
		original_point.append(self.Ego["pose"]["position"]["x"])
		original_point.append(self.Ego["pose"]["position"]["y"])
		heading_of_ego = self.Ego["pose"]["heading"]
		lengthen_of_ego = self.Ego["size"]["length"]
		width_of_ego = self.Ego["size"]["width"]
		ego_polygonPointList = []
		ego_polygonPointList = self.get_four_polygon_point_list_of_ego(original_point,heading_of_ego,lengthen_of_ego,width_of_ego)
		ego = Polygon(ego_polygonPointList)
		# point = Point(position["x"], position["y"])

		_distance = 10000000
		single_result = {}
		for _i in traffic_signal_list:
			if _i["id"] == ID:             
				single_result["id"] = _i["id"]
				single_result["types"] = _i["sub_signal_type_list"]

				points = []
				for _j in _i["stop_line_points"]:
					temp = []
					temp.append(_j["x"])
					temp.append(_j["y"])
					points.append(temp)
				the_line = LineString(points)

				single_result["distance"] = ego.distance(the_line)
			else:
				# single_result = {}
				# single_result["id"] = _i["id"]
				# single_result["types"] = _i["sub_signal_type_list"]

				points = []
				for _j in _i["stop_line_points"]:
					temp = []
					temp.append(_j["x"])
					temp.append(_j["y"])
					points.append(temp)
				the_line = LineString(points)

				distance_of_temp = ego.distance(the_line)
				if distance_of_temp < _distance:
					_distance = distance_of_temp

				if hasattr(single_result, 'distance'):
					if single_result['distance'] > _distance:
						print('Traffic Light Error: wrong traffic light perception!')
						self.testFailures.append("Traffic Light Error: wrong traffic light perception! ")
					else:
						pass
				# pass
			# result.append(single_result)
		return single_result["distance"]      


	def parse_message_of_traffic_light(self, TrafficLight):
		if self.Ego!={}:
			result = {}
			if hasattr(TrafficLight, "header"):
				pass
				# print("TrafficLight" + str(TrafficLight.header.sequence_num))

			if hasattr(TrafficLight, "contain_lights"):
				result["containLights"] = TrafficLight.contain_lights
				if TrafficLight.contain_lights:
					if hasattr(TrafficLight, "traffic_light"):
						traffic_light = []
						for _i in TrafficLight.traffic_light:
							temp = {}
							if hasattr(_i,"color"):
								temp["color"] = _i.color
							if hasattr(_i,"id"):
								temp["id"] = _i.id
							# if hasattr(_i,"confidence"):
							#     temp["confidence"] = _i.confidence
							# if hasattr(_i,"tracking_time"):
							#     temp["tracking_time"] = _i.tracking_time
							if hasattr(_i,"blink"):
								temp["blink"] = _i.blink
							# if hasattr(_i,"remaining_time"):
							#     temp["remaining_time"] = _i.remaining_time
							traffic_light.append(temp)
						result["trafficLightList"] = traffic_light                   
						result["trafficLightStopLine"] = self.calculate_distance_to_traffic_light_stop_line(temp["id"])
					else:
						print("No information for traffic lights found!")

			self.traffic_lights = result
			# print(self.traffic_lights)
		else:
			pass


	# def parse_message_of_ctl(self, chassis):
	# 	# print(chassis)
	# 	# optional bool left_turn = 13 [deprecated = true];
	# 	# optional bool right_turn = 14 [deprecated = true];
	# 	# optional bool high_beam = 11 [deprecated = true];
	# 	# optional bool low_beam = 12 [deprecated = true];
	# 	# optional bool horn = 15 [deprecated = true];
	# 	# optional TurnSignal turnsignal = 21 [deprecated = true];

	# 	# optional TurnSignal turn_signal = 1;
	# 	# // lights enable command
	# 	# optional bool high_beam = 2;
	# 	# optional bool low_beam = 3;
	# 	# optional bool horn = 4;
	# 	# optional bool emergency_light = 5;

	# 	result = {}
	# 	# result["lowBeamOn"] = chassis.signal.low_beam
	# 	# result["highBeamOn"] = chassis.signal.high_beam
	# 	# result["turnSignal"] = chassis.signal.turn_signal

	# 	# if chassis.left_turn:
	# 	# 	result["turnSignal"] = 1 #means left
	# 	# elif chassis.right_turn:
	# 	# 	result["turnSignal"] = 2 #means right
	# 	# else:
	# 	# 	result["turnSignal"] = 0 #means forward


	# 	# print(result["turnSignal"])

	# 	# result["speed"] = chassis.speed


	# 	# result["hornOn"] = chassis.signal.horn
	# 	# result["engineOn"] = chassis.engine_on_off
	# 	# result["gear"] = chassis.gear_location
	# 	# result["brake"] = chassis.brake

	# 	self.ctl = result





	def parse_message_of_canbus(self, chassis):
		result = {}
		
		result["lowBeamOn"] = chassis.signal.low_beam
		result["highBeamOn"] = chassis.signal.high_beam
		result["turnSignal"] = chassis.signal.turn_signal

		# print("turn_signal:"+ str(result["turnSignal"]))

		result["hornOn"] = chassis.signal.horn
		result["speed"] = chassis.speed_mps

		result["engineOn"] = chassis.engine_started
		result["gear"] = chassis.gear_location
		result["brake"] = chassis.brake_percentage

		result["day"] = chassis.chassis_gps.day
		result["hours"] = chassis.chassis_gps.hours
		result["minutes"] = chassis.chassis_gps.minutes
		result["seconds"] = chassis.chassis_gps.seconds

		result["error_code"] = chassis.error_code

		# result["direction"] = self.turn_signal #result["turnSignal"]

		self.Canbus = result


	def parse_message_of_planning(self, Planning):
		decisions = Planning.decision.object_decision
		self.is_overtaking = False
		for item in decisions.decision:
			item0 = item.object_decision[0]
			if item0.overtake.distance_s != 0:
				self.is_overtaking = True
				# print("Overtake!!!!!!!!!!!!!!!!!!")
			if item0.nudge.distance_l != 0:
				self.is_overtaking = True
				# print("nudge!!!!!!!!!!!!!!!!!!")				
			if item0.stop.distance_s != 0:
				pass
				# print("stop!!!!!!!!!!!!!!!!!!")
# [nudge {
#   type: RIGHT_NUDGE
#   distance_l: -0.3
# }
# ]

# message ObjectDecisionType {
#   oneof object_tag {
#     ObjectIgnore ignore = 1;
#     ObjectStop stop = 2;
#     ObjectFollow follow = 3;
#     ObjectYield yield = 4;
#     ObjectOvertake overtake = 5;
#     ObjectNudge nudge = 6;
#     ObjectAvoid avoid = 7;
#     ObjectSidePass side_pass = 8;
#   }


		# print(decisions.decision)

		# for item in decisions.__dict__:
		# 	if hasattr(item, "overtake"):
		# 		print(item.object_decision.overtake)

		# print(Planning.decision.object_decision)
		# main_decision = Planning.decision.main_decision
		# if hasattr(main_decision, "stop"):
		# 	if hasattr(main_decision, "change_lane_type"):
		# 		change_lane_type0 = main_decision.stop.change_lane_type
		# 		print("Change_lane0:"+str(change_lane_type0))
		# if hasattr(main_decision, "cruise"):
		# 	if hasattr(main_decision, "change_lane_type"):
		# 		change_lane_type0 = main_decision.cruise.change_lane_type
		# 		print("Change_lane0:"+str(change_lane_type0))
		# if hasattr(main_decision, "change_lane"):
		# 	change_lane_type1 = main_decision.change_lane.type
		# 	print("Change_lane1:"+str(change_lane_type1))

		
		# result = {}


		# decision = Planning.decision.main_decision

		# print(decision)
		# if getattr(decision, 'change_lane', False):
		#     print("is_change_lane!")
		#     print(decision.change_lane.type)
		# else:
		#     print("else!")
			# Planning.main_decision.stop.
		pass





	def parse_message_of_routing(self, Routing):
		# print("Routing.road.passage.change_lane_type")
		# print(Routing.road.passage.change_lane_type)
		pass

	def Get32le(self, offset, response):
		ret = response[offset + 0] | response[offset + 1]<<8 | response[offset + 2]<<16 | response[offset + 3]<<24
		return ret

	def receive_publish(self, response:bytes):
		if len(response) < 1+2*4:
			return False

		offset = 1
		channelsize = self.Get32le(offset,response)
		offset = offset + 4
		if len(response) < offset + channelsize:
			return False

		channeloffset = offset
		offset = channelsize + offset

		if len(response) < offset + 4:
			return False

		messagesize = self.Get32le(offset,response)
		offset = offset + 4

		if len(response) < offset + messagesize:
			return False

		messageoffset = offset
		offset = messagesize + offset

		# print('Responsesize: '+ str(len(response)))

		# print('Channelsize: '+ str(channelsize))

		# print('Messagesize: '+ str(messagesize))
		legal_flag = True
		for _iii in response[channeloffset:channeloffset+channelsize]:
			if _iii >= 128:
				legal_flag = False 

		if legal_flag!= False:
			channel = response[channeloffset:channeloffset+channelsize].decode("ascii") 
		else:
			return False 
			print('!!!!!!!!!!!!!')
		# print("From Channel: "+channel)

		message = response[messageoffset:messageoffset+messagesize]

		if channel == '/apollo/localization/pose':
			# Pose = pose_pb2.Pose()
			Pose = gps_pb2.Gps()
			Pose.ParseFromString(message)
			self.parse_message_of_pose(Pose)
		elif channel == '/apollo/perception/obstacles':
			PerceptionObstacles = perception_obstacle_pb2.PerceptionObstacles()
			PerceptionObstacles.ParseFromString(message)
			self.parse_message_of_obstacles(PerceptionObstacles)
		elif channel == "/apollo/perception/traffic_light":
			TrafficLightDetection = traffic_light_detection_pb2.TrafficLightDetection()
			TrafficLightDetection.ParseFromString(message)
			self.parse_message_of_traffic_light(TrafficLightDetection)
			# print(TrafficLightDetection)
		elif channel == "/apollo/planning":
			Planning = planning_pb2.ADCTrajectory()
			Planning.ParseFromString(message)
			self.parse_message_of_planning(Planning)
			self.planning_turn_signal = Planning.decision.vehicle_signal.turn_signal
			# print(Planning.decision.vehicle_signal.turn_signal) #the direction

		elif channel == "/apollo/routing":
			Routing = routing_pb2.RoutingResponse()
			Routing.ParseFromString(message)
			self.parse_message_of_routing(Routing)

		elif channel == '/apollo/control':
			ctl = control_cmd_pb2.ControlCommand()
			ctl.ParseFromString(message)
			# print(ctl)
			# print(ctl.gear_location) #Gear is ready
			# print(ctl.brake) #brake is ready [0, 100]
			# self.parse_message_of_ctl(ctl)
			
			# print("ctl: "+str(ctl.signal.turn_signal))

			# self.turn_signal = ctl.signal.turn_signal#This one is better for use
			# self.turn_signal = ctl.turnsignal

  			# optional bool left_turn = 13 [deprecated = true];
  			# optional bool right_turn = 14 [deprecated = true];
  			# optional bool high_beam = 11 [deprecated = true];
  			# optional bool low_beam = 12 [deprecated = true];
  			# optional bool horn = 15 [deprecated = true];
  			# optional TurnSignal turnsignal = 21 [deprecated = true];

			# print("turn_signal:" + str(self.turn_signal))

			# self.

			# enum TurnSignal {
			#   TURN_NONE = 0;
			#   TURN_LEFT = 1;
			#   TURN_RIGHT = 2;
			# }
		elif channel == '/apollo/canbus/chassis':
			chassis = chassis_pb2.Chassis()
			chassis.ParseFromString(message)
			self.parse_message_of_canbus(chassis)
			# print(chassis.low_beam_signal) 
			# print(chassis.high_beam_signal)
			# print("left"+str(chassis.left_turn_signal))
			# print("right"+str(chassis.right_turn_signal))
			# # print(chassis.horn)
			# print(chassis.engine_started)
			# print(chassis.gear_location)
			# print(chassis.brake_percentage)
			

			

		# elif channel == "/simulator/ground_truth/signals":
		#     TrafficLightDetection = traffic_light_detection_pb2.TrafficLightDetection()
		#     TrafficLightDetection.ParseFromString(message)
		#     self.parse_message_of_traffic_light(TrafficLightDetection)
		#     print(TrafficLightDetection)

		elif channel == '/apollo/sensor/gnss/imu':
			imu = imu_pb2.Imu()
			imu.ParseFromString(message)
			# print('Imu')
			# print(imu)
		elif channel == '/apollo/sensor/gnss/corrected_imu':
			corrected_imu1 = corrected_imu.CorrectedImu()
			corrected_imu1.ParseFromString(message)
			# print('corrected_Imu')
			# print(corrected_imu1)
		elif channel == '/apollo/sensor/gnss/odometry':
			odometry = gps_pb2.Gps()
			odometry.ParseFromString(message)
			# print('Odometry')
			# print(odometry)
		elif channel == '/apollo/sensor/gnss/ins_stat':
			ins_stat = ins_pb2.InsStat()
			ins_stat.ParseFromString(message)
			# print('Ins_stat')
			# print(ins_stat)
		elif channel == '/simulator/ground_truth/2d_detections':
			Detection2DArray = detection2darray_pb2.Detection2DArray()
			Detection2DArray.ParseFromString(message)
			print('Detection2DArray')
			print(Detection2DArray)       
		elif channel == 'Lane_lane':
			PerceptionLanes = perception_lane_pb2.PerceptionLanes() 
			PerceptionLanes.ParseFromString(message)
			print('PerceptionLanes') 
			# print(PerceptionLanes) 
		elif channel == '/apollo/sensor/gnss/best_pose':
			GnssBestPose = gnss_best_pose_pb2.GnssBestPose()
			GnssBestPose.ParseFromString(message)
			print('GnssBestPose') 
			print(GnssBestPose) 
		elif channel == '/apollo/sensor/conti_radar':
			ContiRadar = conti_radar_pb2.ContiRadar()
			ContiRadar.ParseFromString(message)
			print('ContiRadar') 
			print(ContiRadar)
		elif channel == '/apollo/sensor/lidar128/compensator/PointCloud2':
			PointCloud = pointcloud_pb2.PointCloud() 
			PointCloud.ParseFromString(message)
			print('PointCloud') 
			print(PointCloud)
		else:
			pass
			# print('Can not process message from channel: '+ str(channel))

		
	def AddSubscriber(self, BridgeType, Topic: str):
		channelBytes = Topic.encode('ascii')
		typeBytes = (str(BridgeType)).encode('ascii')
		bytes_for_set = []
		bytes_for_set.append('2'.encode('ascii'))
		bytes_for_set.append(str(len(channelBytes)>>0).encode('ascii'))
		bytes_for_set.append(str(len(channelBytes)>>8).encode('ascii'))
		bytes_for_set.append(str(len(channelBytes)>>16).encode('ascii'))
		bytes_for_set.append(str(len(channelBytes)>>24).encode('ascii'))
		for i in channelBytes:
			bytes_for_set.append(str(i).encode('ascii'))
		bytes_for_set.append(str(len(typeBytes)>>0).encode('ascii'))
		bytes_for_set.append(str(len(typeBytes)>>8).encode('ascii'))
		bytes_for_set.append(str(len(typeBytes)>>16).encode('ascii'))
		bytes_for_set.append(str(len(typeBytes)>>24).encode('ascii'))
		for i in typeBytes:
			bytes_for_set.append(str(i).encode('ascii'))
			# bytes_for_set.append(i)

		# print(len(bytes([len(channelBytes)>>0])))

		data = bytes([2]) + \
				bytes([len(channelBytes)>>0]) +\
				bytes([len(channelBytes)>>8]) + \
				bytes([len(channelBytes)>>16]) + \
				bytes([len(channelBytes)>>24]) + \
				channelBytes + \
				bytes([len(typeBytes)>>0]) +\
				bytes([len(typeBytes)>>8]) + \
				bytes([len(typeBytes)>>16]) + \
				bytes([len(typeBytes)>>24]) + \
				typeBytes


		self.setup.append(data)                


	def register(self, sim, destination, AgentNames, mapname, groundtruth):
		# #The speed and acceleration -useless
		# self.AddSubscriber("apollo.drivers.gnss.Imu","/apollo/sensor/gnss/imu")
		# self.AddSubscriber("apollo.localization.CorrectedImu","/apollo/sensor/gnss/corrected_imu")
		self.AgentNames = AgentNames

		# #The location -useless
		# self.AddSubscriber("apollo.localization.Gps","/apollo/sensor/gnss/odometry")
		# # self.AddSubscriber("apollo.drivers.gnss.InsStat","/apollo/sensor/gnss/ins_stat")


		#ladar -uesless
		# self.AddSubscriber("apollo.drivers.ContiRadar","/apollo/sensor/conti_radar")

		#pointcloud -useless
		# self.AddSubscriber("apollo.drivers.PointCloud","/apollo/sensor/lidar128/compensator/PointCloud2")

		#GnssBestPose -useless
		# self.AddSubscriber("apollo.drivers.gnss.GnssBestPose","/apollo/sensor/gnss/best_pose")

		# The control -useful!
		self.AddSubscriber("apollo.control.ControlCommand","/apollo/control")

		# Canbus -useful!
		self.AddSubscriber("apollo.canbus.Chassis","/apollo/canbus/chassis")

		# Pose -Key!
		self.AddSubscriber("apollo.localization.Pose","/apollo/localization/pose")

		#The PerceptionObstacles -Key!
		self.AddSubscriber("apollo.perception.PerceptionObstacles","/apollo/perception/obstacles")

		#The Traffic lights -Key!
		self.AddSubscriber("apollo.perception.TrafficLightDetection","/apollo/perception/traffic_light")

		#The planning -Key!
		self.AddSubscriber("apollo.planning.Planning","/apollo/planning")

		self.AddSubscriber("apollo.routing.Routing","/apollo/routing")

		

		# self.AddSubscriber("apollo.perception.TrafficLightDetection","/simulator/ground_truth/signals")

		 

		#Lane -Key!
		# self.AddSubscriber("apollo.perception.PerceptionLanes","Lane_lane")    
		self.is_groundtruth = groundtruth    
		self.sim = sim
		self.destination = destination
		# print('destination:  '+ str(self.destination) )
		self.map_info = get_map_info(mapname)
		self.connect()

		

		for _ii in self.trace:
			truth = _ii["truth"] 
			if truth.__contains__("minDistToEgo"):
				if self.minEgoObsDist == None:
					self.minEgoObsDist = truth["minDistToEgo"]
				elif self.minEgoObsDist > truth["minDistToEgo"]:
					self.minEgoObsDist = truth["minDistToEgo"]
			else:
				self.minEgoObsDist = 200


		if self.minEgoObsDist <=0:
			self.testFailures.append('Accident!')



		trace_for_process = {}
		trace_for_process["testFailures"] = self.testFailures
		trace_for_process["trace"] = self.trace

		trace_for_process["minEgoObsDist"] = self.minEgoObsDist
		
		if self.reach_destinaton:
			trace_for_process["completed"] = True
			trace_for_process["destinationReached"] = self.reach_destinaton
			return trace_for_process
		else:
			trace_for_process["completed"] = False
			trace_for_process["destinationReached"] = self.reach_destinaton
			return trace_for_process
		# print(self.trace)
