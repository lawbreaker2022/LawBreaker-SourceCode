DREAMVIEW Frontend - Backend communication API endpoint
---

Communication Protocol: Websocket JSON string
```
FrontEnd (Website)                                                                                  Backend (C++ server)                                                        
                                                                                   listening on localhost:8888/websocket
   
const client = new WebSocket(`ws://localhost:8888/websocket`);
client.binaryType = "arraybuffer";
client.onopen = () => {...}
client.onmessage = () => {...} 
                                                                                                    on connect response:
                                                                                                               HMIStatus 
                                                                                                            VehicleParam 
                                                                                                        PointCloudStatus
                                                                                                        SimControlStatus
                                                                                                            TeleopStatus               

// communication afterwards is request-based. 
// browser sends request and dreamview backend replies with requested data
// below lists down some of the common requests sent by DreamView Browser

{ type: "HMIAction", action: "SETUP_MODE" }                                             Backend turns on all the modules

{ type: "HMIAction", action: "RESET_MODE" }                                            Backend turns off all the modules

{ type: 'HMIAction', action: "START_MODULE", value: "Planning" }                        Backend turns on Planning module

// here's a list of the actions 
enum HMIAction {
  NONE = 0,
  SETUP_MODE = 1,
  RESET_MODE = 2,
  ENTER_AUTO_MODE = 3,
  DISENGAGE = 4,
  CHANGE_MODE = 5,
  CHANGE_MAP = 6,
  CHANGE_VEHICLE = 7,
  START_MODULE = 8,
  STOP_MODULE = 9
};

{ type: "HMIStatus" }                                                                                response: HMIStatus

{ type: "RequestSimulationWorld", planning: true }                                             response: SimulationWorld

{ type: "SendRoutingRequest",                                                    Backend publish a Route Request message 
  start: {                                                                        to CyberRT, which will be receieved by 
    x: start.x,                                                                                       the routing module
    y: start.y,
    z: start.z,
    heading: heading / 180 * Math.PI
  },
  end: {
    x: destination.x,
    y: destination.y,
    z: destination.z
  },
  waypoint: []
}                                                                     

```


Some sample message types:

```protobuf
message HMIStatus {
  optional apollo.common.Header header = 1;

  repeated string modes = 2;
  optional string current_mode = 3;

  repeated string maps = 4;
  optional string current_map = 5;

  repeated string vehicles = 6;
  optional string current_vehicle = 7;

  // {module_name: is_running_or_not}
  map<string, bool> modules = 8;
  // {component_name: status}
  map<string, apollo.monitor.ComponentStatus> monitored_components = 9;

  optional string docker_image = 10;
  optional int32 utm_zone_id = 11;  // FLAGS_local_utm_zone_id

  // Message which will be read aloud to drivers and passengers through
  // Dreamview.
  optional string passenger_msg = 12;
}


// Next-id: 30
message SimulationWorld {
  // Timestamp in milliseconds
  optional double timestamp = 1;

  // Sequence number
  optional uint32 sequence_num = 2;

  // Objects in the world and the associated predictions/decisions
  repeated Object object = 3;

  // Autonomous driving cars
  optional Object auto_driving_car = 4;

  // Planning signal
  optional Object traffic_signal = 5;

  // Routing paths
  repeated RoutePath route_path = 6;
  // Timestamp of latest routing
  optional double routing_time = 7;

  // Planned trajectory
  repeated Object planning_trajectory = 8;

  // Main decision
  optional Object main_stop = 9 [deprecated = true];
  optional Object main_decision = 10;

  // Speed limit
  optional double speed_limit = 11;

  // Module delays
  optional DelaysInMs delay = 12;

  // Notification
  optional apollo.common.monitor.MonitorMessage monitor = 13
      [deprecated = true];
  repeated Notification notification = 14;

  // Engage advice from planning
  optional string engage_advice = 15;

  // Module latency
  map<string, Latency> latency = 16;

  optional MapElementIds map_element_ids = 17;
  optional uint64 map_hash = 18;
  optional double map_radius = 19;

  // Planning data
  optional apollo.planning_internal.PlanningData planning_data = 20;

  // GPS
  optional Object gps = 21;

  // Lane Markers from perception
  optional apollo.perception.LaneMarkers lane_marker = 22;

  // Control data
  optional ControlData control_data = 23;

  // Relative Map
  repeated apollo.common.Path navigation_path = 24;

  // RSS info
  optional bool is_rss_safe = 25 [default = true];

  // Shadow localization
  optional Object shadow_localization = 26;

  // Perception detected signals
  repeated Object perceived_signal = 27;

  // A map from a story name to whether it is on
  map<string, bool> stories = 28;

  // A map from a sensor_id to a group of sensor_measurements
  map<string, SensorMeasurements> sensor_measurements = 29;
}


// Next-id: 36
message Object {
  // ID
  optional string id = 1;  // primary identifier for each object

  // Shape Info
  repeated PolygonPoint polygon_point = 2;  // corners of an object

  // Position Info
  optional double heading = 3;
  optional double latitude = 4;
  optional double longitude = 5;
  optional double position_x = 6;
  optional double position_y = 7;
  optional double length = 8 [default = 2.8];
  optional double width = 9 [default = 1.4];
  optional double height = 10 [default = 1.8];

  // Motion Info
  // For objects with motion info such as ADC.
  optional double speed = 11;               // in m/s, can be negative
  optional double speed_acceleration = 12;  // in m/s^2
  optional double speed_jerk = 13;
  optional double spin = 14;
  optional double spin_acceleration = 15;
  optional double spin_jerk = 16;
  optional double speed_heading = 17;
  optional double kappa = 18;
  optional double dkappa = 35;

  // Signal Info
  // For objects with signals set and current signal such as Traffic Light,
  // Stop Sign, and Vehicle Signal.
  repeated string signal_set = 19;
  optional string current_signal = 20;

  // Time Info
  optional double timestamp_sec = 21;

  // Decision Info
  repeated Decision decision = 22;
  optional bool yielded_obstacle = 32 [default = false];

  // Chassis Info
  // For ADC
  optional double throttle_percentage = 23;
  optional double brake_percentage = 24;
  optional double steering_percentage = 25;
  optional double steering_angle = 26;
  optional double steering_ratio = 27;
  enum DisengageType {
    DISENGAGE_NONE = 0;
    DISENGAGE_UNKNOWN = 1;
    DISENGAGE_MANUAL = 2;
    DISENGAGE_EMERGENCY = 3;
    DISENGAGE_AUTO_STEER_ONLY = 4;
    DISENGAGE_AUTO_SPEED_ONLY = 5;
    DISENGAGE_CHASSIS_ERROR = 6;
  };

  optional DisengageType disengage_type = 28;

  enum Type {
    UNKNOWN = 0;
    UNKNOWN_MOVABLE = 1;
    UNKNOWN_UNMOVABLE = 2;
    PEDESTRIAN = 3;  // pedestrian, usually determined by moving behavior.
    BICYCLE = 4;     // bike, motor bike.
    VEHICLE = 5;     // passenger car or truck.
    VIRTUAL = 6;     // virtual object created by decision module.
    CIPV = 7;        // closest in-path vehicle determined by perception module.
  };

  optional Type type = 29;  // obstacle type
  // obstacle sub-type
  optional apollo.perception.PerceptionObstacle.SubType sub_type = 34;
  repeated Prediction prediction = 30;

  // perception confidence level. Range: [0,1]
  optional double confidence = 31 [default = 1];
  optional apollo.prediction.ObstaclePriority obstacle_priority = 33;
}

```





