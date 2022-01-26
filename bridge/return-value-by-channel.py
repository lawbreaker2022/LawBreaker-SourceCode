

From Channel:/apollo/control
header {
  timestamp_sec: 1623230844.3421998
  module_name: "control"
  sequence_num: 818752
  lidar_timestamp: 0
  camera_timestamp: 0
  radar_timestamp: 0
  status {
    error_code: OK
  }
}
throttle: 0.0
brake: 57.594106176559066
steering_rate: 100.0
steering_target: 0.0054523438578755554
acceleration: -0.2745233671157263
gear_location: GEAR_DRIVE
debug {
  simple_lon_debug {
    station_reference: 0.0
    station_error: 0.00045719271830684297
    station_error_limited: 0.00045719271830684297
    preview_station_error: 0.00045719271830684297
    speed_reference: 0.0
    speed_error: -0.000150894415651802
    speed_controller_input_limited: -5.945587199043341e-05
    preview_speed_reference: 0.0
    preview_speed_error: -0.000150894415651802
    preview_acceleration_reference: 0.0
    acceleration_cmd_closeloop: -0.2745233671157263
    acceleration_cmd: -0.2745233671157263
    acceleration_lookup: -0.2745233671157263
    speed_lookup: 0.00015089444059412926
    calibration_value: -57.594106176559066
    throttle_cmd: 0.0
    brake_cmd: 57.594106176559066
    is_full_stop: false
    slope_offset_compensation: 0.3211464782573347
    current_station: -0.00045719271830684297
    path_remain: 0.00045719271830684297
    pid_saturation_status: 0
    speed_offset: 9.14385436613686e-05
    current_speed: 0.000150894415651802
    acceleration_reference: 0.0
    current_acceleration: 0.0
    acceleration_error: 0.0
    jerk_reference: 0.0
    current_jerk: 0.0
    jerk_error: 0.0
    current_matched_point {
      path_point {
        x: 587094.0302282763
        y: 4141562.7903892873
      }
    }
    current_reference_point {
      path_point {
        x: 587094.6443699514
        y: 4141562.636505048
      }
    }
    preview_reference_point {
      path_point {
        x: 587094.6449527717
        y: 4141562.636358094
      }
    }
  }
  simple_lat_debug {
    lateral_error: -0.10046760169313437
    ref_heading: -0.38774143295574737
    heading: -0.3870719906780984
    heading_error: 0.0006694422776489795
    heading_error_rate: 0.0
    lateral_error_rate: 1.0101511045086529e-07
    curvature: -8.324257256397148e-19
    steer_angle: 0.0054523438578755554
    steer_angle_feedforward: -4.483582328904523e-16
    steer_angle_lateral_contribution: 0.07752077579125276
    steer_angle_lateral_rate_contribution: -5.267427054580901e-11
    steer_angle_heading_contribution: -0.006956418799169312
    steer_angle_heading_rate_contribution: -0.0
    steer_angle_feedback: 0.07056435693940918
    steering_position: 0.005452343728393316
    ref_speed: 0.00015089444059412926
    steer_angle_limited: 0.07056435693940874
    lateral_acceleration: 0.0
    lateral_jerk: 0.0
    ref_heading_rate: -0.0
    heading_rate: 0.0
    ref_heading_acceleration: 0.0
    heading_acceleration: 0.0
    heading_error_acceleration: 0.0
    ref_heading_jerk: 0.0
    heading_jerk: 0.0
    heading_error_jerk: 0.0
    lateral_error_feedback: -0.10046760169313437
    heading_error_feedback: 0.0006694422776489795
    current_target_point {
      path_point {
        x: 587094.6449527717
        y: 4141562.636358094
      }
    }
    steer_angle_feedback_augment: 0.0
  }
  input_debug {
    localization_header {
      timestamp_sec: 1623230844.257459
      module_name: "localization"
      sequence_num: 229931
    }
    canbus_header {
      timestamp_sec: 1623230694.8638933
      module_name: "chassis"
      sequence_num: 180450
    }
    trajectory_header {
      timestamp_sec: 1623230844.2889528
      module_name: "planning"
      sequence_num: 1553
      lidar_timestamp: 0
      camera_timestamp: 0
      radar_timestamp: 0
    }
    latest_replan_trajectory_header {
      timestamp_sec: 1623230720.717531
      module_name: "planning"
      sequence_num: 321
      lidar_timestamp: 0
      camera_timestamp: 0
      radar_timestamp: 0
    }
  }
}
signal {
  turn_signal: TURN_NONE
}
latency_stats {
  total_time_ms: 11.647111
  controller_time_ms: 6.7901611328125
  controller_time_ms: 0.4456043243408203
  total_time_exceeded: true
}
engage_advice {
  advice: READY_TO_ENGAGE
}


From Channel: /apollo/sensor/gnss/imu
Imu
header {
  timestamp_sec: 1623742420.7891867
  sequence_num: 244640
}
measurement_time: 1307777638.789
measurement_span: 0.009999999776482582
linear_acceleration {
  x: -0.2617420256137848
  y: 0.10205671936273575
  z: 9.805932998657227
}
angular_velocity {
  x: -2.096639946103096e-07
  y: -1.2271630112081766e-07
  z: 6.073300028219819e-06
}

Imu
header {
  timestamp_sec: 1623230694.8938932
  sequence_num: 1843266
}
measurement_time: 1307265912.893
measurement_span: 0.009999999776482582
linear_acceleration {
  x: -0.1112317219376564
  y: 0.301820307970047
  z: 9.80490493774414
}
angular_velocity {
  x: -9.032082743942738e-07
  y: 8.598144631832838e-07
  z: 5.693058483302593e-06
}



From Channel: /apollo/sensor/gnss/corrected_imu
corrected_Imu
header {
  timestamp_sec: 1623738410.6156125
}
imu {
  linear_acceleration {
    x: 0.0
    y: 0.0
    z: 0.0
  }
  angular_velocity {
    x: 0.0
    y: 0.0
    z: 0.0
  }
  heading: 257.1951904296875
  euler_angles {
    x: 0.025517745657791524
    y: 6.2822861753306825
    z: 4.488902858519168
  }
}


From Channel: "/apollo/perception/traffic_light"
traffic_light {
  color: RED
  id: "signal_13"
  confidence: 1.0
  blink: false
}
header {
  timestamp_sec: 1633171663.2235441
  sequence_num: 284
  camera_timestamp: 1633171663223544064
}
contain_lights: true



From Channel: /apollo/sensor/gnss/ins_stat
Ins_stat
header {
  timestamp_sec: 1623738593.565438
  sequence_num: 4267
  frame_id: "gps"
}
ins_status: 3
pos_type: 56



From Channel: /apollo/sensor/gnss/odometry
Odometry
header {
  timestamp_sec: 1623738593.555438
  sequence_num: 34332
}
localization {
  position {
    x: 587098.7370033264
    y: 4141563.6697130203
    z: -1.7459309101104736
  }
  orientation {
    qx: 0.00830988772213459
    qy: 0.009692161343991756
    qz: -0.7813951373100281
    qw: 0.6239061951637268
  }
  linear_velocity {
    x: 0.00010313536040484905
    y: -1.7384241800755262e-05
    z: -3.014891262864694e-06
  }
  heading: 257.210693359375
}


From Channel: /apollo/canbus/chassis
Canbus
engine_started: true
engine_rpm: 799.9998779296875
speed_mps: 4.7962810640456155e-05
odometer_m: 0.0
fuel_range_m: 0
throttle_percentage: 0.0
brake_percentage: 62.82792663574219
steering_percentage: 0.0003023436001967639
parking_brake: false
wiper: false
driving_mode: COMPLETE_AUTO_DRIVE
gear_location: GEAR_DRIVE
header {
  timestamp_sec: 1623746175.263506
  module_name: "chassis"
  sequence_num: 3746
}
chassis_gps {
  latitude: 37.41737248598786
  longitude: -122.0161285322553
  gps_valid: true
  year: 2011
  month: 6
  day: 11
  hours: 16
  minutes: 36
  seconds: 33
  compass_direction: 180.0
  pdop: 0.1
  is_gps_fault: false
  is_inferred: false
  altitude: -0.7383725643157959
  heading: 165.15663146972656
  hdop: 0.1
  vdop: 0.1
  quality: FIX_3D
  num_satellites: 15
  gps_speed: 4.7962810640456155e-05
}




From Channel: /apollo/sensor/gnss/best_pose
GnssBestPose
header {
  timestamp_sec: 1623759764.8159823
  sequence_num: 11355
  frame_id: "gps"
}
measurement_time: 1307794982.815
sol_status: SOL_COMPUTED
sol_type: NARROW_INT
latitude: 37.416762965445784
longitude: -122.01635047723568
height_msl: 0.0
undulation: 0.0
datum_id: WGS84
latitude_std_dev: 0.009999999776482582
longitude_std_dev: 0.009999999776482582
height_std_dev: 0.009999999776482582
base_station_id: "0"
differential_age: 2.0
solution_age: 0.0
num_sats_tracked: 15
num_sats_in_solution: 15
num_sats_l1: 15
num_sats_multi: 12
extended_solution_status: 33
galileo_beidou_used_mask: 0
gps_glonass_used_mask: 51











From Channel: /apollo/sensor/conti_radar
ContiRadar
header {
  timestamp_sec: 1623761195.3046181
  module_name: "conti_radar"
  sequence_num: 19187
  frame_id: ""
}
contiobs {
  header {
    timestamp_sec: 1623761195.3046181
    module_name: "conti_radar"
    sequence_num: 19187
    frame_id: ""
  }
  clusterortrack: false
  obstacle_id: -3116
  longitude_dist: 2.2900474071502686
  lateral_dist: 0.0008592447265982628
  longitude_vel: 0.0
  lateral_vel: 0.0
  rcs: 11.0
  dynprop: 1
  longitude_dist_rms: 0.0
  lateral_dist_rms: 0.0
  longitude_vel_rms: 0.0
  lateral_vel_rms: 0.0
  probexist: 1.0
  meas_state: 2
  longitude_accel: 0.0
  lateral_accel: 0.0
  oritation_angle: -0.0
  longitude_accel_rms: 0.0
  lateral_accel_rms: 0.0
  oritation_angle_rms: 0.0
  length: 2.801422119140625
  width: 4.986095428466797
  obstacle_class: 1
}
contiobs {
  header {
    timestamp_sec: 1623761195.3046181
    module_name: "conti_radar"
    sequence_num: 19187
    frame_id: ""
  }
  clusterortrack: false
  obstacle_id: -11894
  longitude_dist: 37.48213195800781
  lateral_dist: -13.739904403686523
  longitude_vel: -0.34185412526130676
  lateral_vel: 0.007613399066030979
  rcs: 11.0
  dynprop: 1
  longitude_dist_rms: 0.0
  lateral_dist_rms: 0.0
  longitude_vel_rms: 0.0
  lateral_vel_rms: 0.0
  probexist: 1.0
  meas_state: 2
  longitude_accel: 0.0
  lateral_accel: 0.0
  oritation_angle: 11.839407920837402
  longitude_accel_rms: 0.0
  lateral_accel_rms: 0.0
  oritation_angle_rms: 0.0
  length: 0.5
  width: 0.5
  obstacle_class: 1
}
contiobs {
  header {
    timestamp_sec: 1623761195.3046181
    module_name: "conti_radar"
    sequence_num: 19187
    frame_id: ""
  }
  clusterortrack: false
  obstacle_id: -9212
  longitude_dist: 37.915916442871094
  lateral_dist: -13.988276481628418
  longitude_vel: -0.04319736361503601
  lateral_vel: -0.018976422026753426
  rcs: 11.0
  dynprop: 1
  longitude_dist_rms: 0.0
  lateral_dist_rms: 0.0
  longitude_vel_rms: 0.0
  lateral_vel_rms: 0.0
  probexist: 1.0
  meas_state: 2
  longitude_accel: 0.0
  lateral_accel: 0.0
  oritation_angle: 36.885005950927734
  longitude_accel_rms: 0.0
  lateral_accel_rms: 0.0
  oritation_angle_rms: 0.0
  length: 0.5
  width: 0.5
  obstacle_class: 1
}
contiobs {
  header {
    timestamp_sec: 1623761195.3046181
    module_name: "conti_radar"
    sequence_num: 19187
    frame_id: ""
  }
  clusterortrack: false
  obstacle_id: -10678
  longitude_dist: 38.6185417175293
  lateral_dist: -14.586426734924316
  longitude_vel: 3.170700802002102e-05
  lateral_vel: -0.00014242505130823702
  rcs: 11.0
  dynprop: 1
  longitude_dist_rms: 0.0
  lateral_dist_rms: 0.0
  longitude_vel_rms: 0.0
  lateral_vel_rms: 0.0
  probexist: 1.0
  meas_state: 2
  longitude_accel: 0.0
  lateral_accel: 0.0
  oritation_angle: 13.35601806640625
  longitude_accel_rms: 0.0
  lateral_accel_rms: 0.0
  oritation_angle_rms: 0.0
  length: 0.5
  width: 0.5
  obstacle_class: 1
}
contiobs {
  header {
    timestamp_sec: 1623761195.3046181
    module_name: "conti_radar"
    sequence_num: 19187
    frame_id: ""
  }
  clusterortrack: false
  obstacle_id: -9516
  longitude_dist: 49.37957000732422
  lateral_dist: -14.482278823852539
  longitude_vel: -2.770956234598998e-05
  lateral_vel: -4.768300641444512e-05
  rcs: 11.0
  dynprop: 1
  longitude_dist_rms: 0.0
  lateral_dist_rms: 0.0
  longitude_vel_rms: 0.0
  lateral_vel_rms: 0.0
  probexist: 1.0
  meas_state: 2
  longitude_accel: 0.0
  lateral_accel: 0.0
  oritation_angle: -59.1609001159668
  longitude_accel_rms: 0.0
  lateral_accel_rms: 0.0
  oritation_angle_rms: 0.0
  length: 0.5
  width: 0.5
  obstacle_class: 1
}
contiobs {
  header {
    timestamp_sec: 1623761195.3046181
    module_name: "conti_radar"
    sequence_num: 19187
    frame_id: ""
  }
  clusterortrack: false
  obstacle_id: -11286
  longitude_dist: 13.533171653747559
  lateral_dist: -18.091445922851562
  longitude_vel: -0.03316420316696167
  lateral_vel: -0.33053767681121826
  rcs: 11.0
  dynprop: 1
  longitude_dist_rms: 0.0
  lateral_dist_rms: 0.0
  longitude_vel_rms: 0.0
  lateral_vel_rms: 0.0
  probexist: 1.0
  meas_state: 2
  longitude_accel: 0.0
  lateral_accel: 0.0
  oritation_angle: 9.190902709960938
  longitude_accel_rms: 0.0
  lateral_accel_rms: 0.0
  oritation_angle_rms: 0.0
  length: 0.5
  width: 0.5
  obstacle_class: 1
}
contiobs {
  header {
    timestamp_sec: 1623761195.3046181
    module_name: "conti_radar"
    sequence_num: 19187
    frame_id: ""
  }
  clusterortrack: false
  obstacle_id: -10070
  longitude_dist: 30.169448852539062
  lateral_dist: -14.239145278930664
  longitude_vel: -2.593028148112353e-05
  lateral_vel: -2.2994820028543472e-05
  rcs: 11.0
  dynprop: 1
  longitude_dist_rms: 0.0
  lateral_dist_rms: 0.0
  longitude_vel_rms: 0.0
  lateral_vel_rms: 0.0
  probexist: 1.0
  meas_state: 2
  longitude_accel: 0.0
  lateral_accel: 0.0
  oritation_angle: -5.387070178985596
  longitude_accel_rms: 0.0
  lateral_accel_rms: 0.0
  oritation_angle_rms: 0.0
  length: 0.5
  width: 0.5
  obstacle_class: 1
}
contiobs {
  header {
    timestamp_sec: 1623761195.3046181
    module_name: "conti_radar"
    sequence_num: 19187
    frame_id: ""
  }
  clusterortrack: false
  obstacle_id: -10982
  longitude_dist: 34.76570510864258
  lateral_dist: -13.927248001098633
  longitude_vel: -0.001160077634267509
  lateral_vel: -0.003509830217808485
  rcs: 11.0
  dynprop: 1
  longitude_dist_rms: 0.0
  lateral_dist_rms: 0.0
  longitude_vel_rms: 0.0
  lateral_vel_rms: 0.0
  probexist: 1.0
  meas_state: 2
  longitude_accel: 0.0
  lateral_accel: 0.0
  oritation_angle: 14.193526268005371
  longitude_accel_rms: 0.0
  lateral_accel_rms: 0.0
  oritation_angle_rms: 0.0
  length: 0.5
  width: 0.5
  obstacle_class: 1
}
contiobs {
  header {
    timestamp_sec: 1623761195.3046181
    module_name: "conti_radar"
    sequence_num: 19187
    frame_id: ""
  }
  clusterortrack: false
  obstacle_id: -10374
  longitude_dist: 13.66903305053711
  lateral_dist: -18.572097778320312
  longitude_vel: 0.258335143327713
  lateral_vel: 0.16522687673568726
  rcs: 11.0
  dynprop: 1
  longitude_dist_rms: 0.0
  lateral_dist_rms: 0.0
  longitude_vel_rms: 0.0
  lateral_vel_rms: 0.0
  probexist: 1.0
  meas_state: 2
  longitude_accel: 0.0
  lateral_accel: 0.0
  oritation_angle: -14.1925048828125
  longitude_accel_rms: 0.0
  lateral_accel_rms: 0.0
  oritation_angle_rms: 0.0
  length: 0.5
  width: 0.5
  obstacle_class: 1
}
object_list_status {
  nof_objects: 9
  meas_counter: 22800
  interface_version: 0
}







From Channel: /apollo/perception/obstacles
PerceptionObstacles
perception_obstacle {
  id: 4509
  position {
    x: 587040.3681370254
    y: 4141575.3995795655
    z: -2.351690305688747
  }
  theta: -0.17801684141159058
  velocity {
    x: 1.3466945886611938
    y: -0.24200965464115143
    z: 0.0
  }
  length: 4.830799579620361
  width: 2.209441661834717
  height: 2.0205557346343994
  polygon_point {
    x: 587037.7799876059
    y: 4141574.895931123
    z: -2.351690400002104
  }
  polygon_point {
    x: 587042.4398922051
    y: 4141573.802717088
    z: -2.351690400002104
  }
  polygon_point {
    x: 587042.472712549
    y: 4141573.83621013
    z: -2.351690400002104
  }
  polygon_point {
    x: 587042.9570931519
    y: 4141575.9033850413
    z: -2.351690400002104
  }
  polygon_point {
    x: 587038.2971885527
    y: 4141576.9965990763
    z: -2.351690400002104
  }
  polygon_point {
    x: 587038.2643683279
    y: 4141576.9631060343
    z: -2.351690400002104
  }
  tracking_time: 26.409974813461304
  type: VEHICLE
  timestamp: 1623764283.2516732
  acceleration {
    x: 3.441345691680908
    y: -0.6099125742912292
    z: 0.0
  }
  anchor_point {
    x: 587040.368539923
    y: 4141575.399658253
    z: -1.3414124830901728
  }
  bbox2d {
    xmin: 0.0
    ymin: 0.0
    xmax: 0.0
    ymax: 0.0
  }
  sub_type: ST_UNKNOWN
  measurements {
    sensor_id: "velodyne128"
    id: 4045
    position {
      x: 587040.3681370254
      y: 4141575.3995795655
      z: -2.351690305688747
    }
    theta: -0.17801684141159058
    length: 4.830799579620361
    width: 2.209441661834717
    height: 2.0205557346343994
    velocity {
      x: 1.3476632833480835
      y: -0.2424735128879547
      z: 0.0
    }
    type: VEHICLE
    timestamp: 1623764283.2516732
    box {
      xmin: 0.0
      ymin: 0.0
      xmax: 0.0
      ymax: 0.0
    }
  }
  height_above_ground: nan
  position_covariance: 0.0
  position_covariance: 0.0
  position_covariance: 0.0
  position_covariance: 0.0
  position_covariance: 0.0
  position_covariance: 0.0
  position_covariance: 0.0
  position_covariance: 0.0
  position_covariance: 0.0
  velocity_covariance: 1.1407160758972168
  velocity_covariance: -0.33387696743011475
  velocity_covariance: 0.0
  velocity_covariance: -0.33387696743011475
  velocity_covariance: 0.13680648803710938
  velocity_covariance: 0.0
  velocity_covariance: 0.0
  velocity_covariance: 0.0
  velocity_covariance: 0.009999999776482582
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  light_status {
    brake_visible: 0.0
    brake_switch_on: 0.0
    left_turn_visible: 0.0
    left_turn_switch_on: 0.0
    right_turn_visible: 0.0
    right_turn_switch_on: 0.0
  }
}
perception_obstacle {
  id: 4518
  position {
    x: 587044.1923580633
    y: 4141567.2704636115
    z: -2.6656075430195774
  }
  theta: -1.867294192314148
  velocity {
    x: 0.0
    y: -0.0
    z: 0.0
  }
  length: 4.811776161193848
  width: 2.2134957313537598
  height: 2.005388021469116
  polygon_point {
    x: 587042.4333588207
    y: 4141565.2927798014
    z: -2.6656075600362836
  }
  polygon_point {
    x: 587044.5286677206
    y: 4141564.653087018
    z: -2.6656075600362836
  }
  polygon_point {
    x: 587044.5608306254
    y: 4141564.68590915
    z: -2.6656075600362836
  }
  polygon_point {
    x: 587045.9530186976
    y: 4141569.2500151377
    z: -2.6656075600362836
  }
  polygon_point {
    x: 587043.8577099169
    y: 4141569.889708398
    z: -2.6656075600362836
  }
  polygon_point {
    x: 587043.8255470122
    y: 4141569.8568867426
    z: -2.6656075600362836
  }
  tracking_time: 17.309983491897583
  type: VEHICLE
  timestamp: 1623764283.2516732
  acceleration {
    x: -3.4971478157785896e-08
    y: 8.013428498543362e-08
    z: 0.0
  }
  anchor_point {
    x: 587044.1931887375
    y: 4141567.271397628
    z: -1.6629134699700414
  }
  bbox2d {
    xmin: 0.0
    ymin: 0.0
    xmax: 0.0
    ymax: 0.0
  }
  sub_type: ST_UNKNOWN
  measurements {
    sensor_id: "velodyne128"
    id: 4030
    position {
      x: 587044.1923580633
      y: 4141567.2704636115
      z: -2.6656075430195774
    }
    theta: -1.867294192314148
    length: 4.811776161193848
    width: 2.2134957313537598
    height: 2.005388021469116
    velocity {
      x: 0.0
      y: 0.0
      z: 0.0
    }
    type: VEHICLE
    timestamp: 1623764283.2516732
    box {
      xmin: 0.0
      ymin: 0.0
      xmax: 0.0
      ymax: 0.0
    }
  }
  height_above_ground: nan
  position_covariance: 0.0
  position_covariance: 0.0
  position_covariance: 0.0
  position_covariance: 0.0
  position_covariance: 0.0
  position_covariance: 0.0
  position_covariance: 0.0
  position_covariance: 0.0
  position_covariance: 0.0
  velocity_covariance: 0.010117744095623493
  velocity_covariance: 0.00016996757767628878
  velocity_covariance: 0.0
  velocity_covariance: 0.00016996757767628878
  velocity_covariance: 0.01073944941163063
  velocity_covariance: 0.0
  velocity_covariance: 0.0
  velocity_covariance: 0.0
  velocity_covariance: 0.009999999776482582
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  light_status {
    brake_visible: 0.0
    brake_switch_on: 0.0
    left_turn_visible: 0.0
    left_turn_switch_on: 0.0
    right_turn_visible: 0.0
    right_turn_switch_on: 0.0
  }
}
perception_obstacle {
  id: 4522
  position {
    x: 587055.2218126493
    y: 4141578.269597576
    z: -1.826757791711517
  }
  theta: -2.8458425998687744
  velocity {
    x: -1.1276214122772217
    y: -0.3435702621936798
    z: 0.0
  }
  length: 4.67047643661499
  width: 2.1208009719848633
  height: 1.8834004402160645
  polygon_point {
    x: 587052.6846762026
    y: 4141578.476091264
    z: -1.826757777092558
  }
  polygon_point {
    x: 587053.3658314074
    y: 4141576.516151307
    z: -1.826757777092558
  }
  polygon_point {
    x: 587057.7312527025
    y: 4141578.032136796
    z: -1.826757777092558
  }
  polygon_point {
    x: 587057.7614021624
    y: 4141578.062904237
    z: -1.826757777092558
  }
  polygon_point {
    x: 587057.0802469576
    y: 4141580.0228441935
    z: -1.826757777092558
  }
  polygon_point {
    x: 587052.7148256624
    y: 4141578.5068587046
    z: -1.826757777092558
  }
  tracking_time: 15.209985494613647
  type: VEHICLE
  timestamp: 1623764283.2516732
  acceleration {
    x: -1.9131757020950317
    y: -0.5829173922538757
    z: 0.0
  }
  anchor_point {
    x: 587055.2230388843
    y: 4141578.2694977485
    z: -0.885057515476261
  }
  bbox2d {
    xmin: 0.0
    ymin: 0.0
    xmax: 0.0
    ymax: 0.0
  }
  sub_type: ST_UNKNOWN
  measurements {
    sensor_id: "velodyne128"
    id: 4057
    position {
      x: 587055.2218126493
      y: 4141578.269597576
      z: -1.826757791711517
    }
    theta: -2.8458425998687744
    length: 4.67047643661499
    width: 2.1208009719848633
    height: 1.8834004402160645
    velocity {
      x: -1.1477301120758057
      y: -0.349697083234787
      z: 0.0
    }
    type: VEHICLE
    timestamp: 1623764283.2516732
    box {
      xmin: 0.0
      ymin: 0.0
      xmax: 0.0
      ymax: 0.0
    }
  }
  height_above_ground: nan
  position_covariance: 0.0
  position_covariance: 0.0
  position_covariance: 0.0
  position_covariance: 0.0
  position_covariance: 0.0
  position_covariance: 0.0
  position_covariance: 0.0
  position_covariance: 0.0
  position_covariance: 0.0
  velocity_covariance: 1.7527786493301392
  velocity_covariance: 0.45409125089645386
  velocity_covariance: 0.0
  velocity_covariance: 0.45409125089645386
  velocity_covariance: 0.13385918736457825
  velocity_covariance: 0.0
  velocity_covariance: 0.0
  velocity_covariance: 0.0
  velocity_covariance: 0.009999999776482582
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  light_status {
    brake_visible: 0.0
    brake_switch_on: 0.0
    left_turn_visible: 0.0
    left_turn_switch_on: 0.0
    right_turn_visible: 0.0
    right_turn_switch_on: 0.0
  }
}

perception_obstacle {
  id: 4524
  position {
    x: 587048.935653297
    y: 4141574.127929984
    z: -2.1727301118971156
  }
  theta: 0.7202008962631226
  velocity {
    x: -0.0
    y: -0.0
    z: 0.0
  }
  length: 4.800119400024414
  width: 2.241948366165161
  height: 1.8667330741882324
  polygon_point {
    x: 587046.4333277071
    y: 4141573.341901658
    z: -2.1727300766683637
  }
  polygon_point {
    x: 587047.8922210062
    y: 4141571.7198084574
    z: -2.1727300766683637
  }
  polygon_point {
    x: 587051.4110145891
    y: 4141574.8843334895
    z: -2.1727300766683637
  }
  polygon_point {
    x: 587051.44096187
    y: 4141574.9148949366
    z: -2.1727300766683637
  }
  polygon_point {
    x: 587049.9820690477
    y: 4141576.536989091
    z: -2.1727300766683637
  }
  polygon_point {
    x: 587046.4632754648
    y: 4141573.3724631052
    z: -2.1727300766683637
  }
  tracking_time: 11.509989023208618
  type: VEHICLE
  timestamp: 1623764283.2516732
  acceleration {
    x: -1.9060952354266192e-06
    y: -1.0993703654094134e-06
    z: 0.0
  }
  anchor_point {
    x: 587048.9371447688
    y: 4141574.128398835
    z: -1.239363632330723
  }
  bbox2d {
    xmin: 0.0
    ymin: 0.0
    xmax: 0.0
    ymax: 0.0
  }
  sub_type: ST_UNKNOWN
  measurements {
    sensor_id: "velodyne128"
    id: 4059
    position {
      x: 587048.935653297
      y: 4141574.127929984
      z: -2.1727301118971156
    }
    theta: 0.7202008962631226
    length: 4.800119400024414
    width: 2.241948366165161
    height: 1.8667330741882324
    velocity {
      x: 0.0
      y: 0.0
      z: 0.0
    }
    type: VEHICLE
    timestamp: 1623764283.2516732
    box {
      xmin: 0.0
      ymin: 0.0
      xmax: 0.0
      ymax: 0.0
    }
  }
  height_above_ground: nan
  position_covariance: 0.0
  position_covariance: 0.0
  position_covariance: 0.0
  position_covariance: 0.0
  position_covariance: 0.0
  position_covariance: 0.0
  position_covariance: 0.0
  position_covariance: 0.0
  position_covariance: 0.0
  velocity_covariance: 90.03731536865234
  velocity_covariance: -21.646425247192383
  velocity_covariance: 0.0
  velocity_covariance: -21.646425247192383
  velocity_covariance: 5.802471160888672
  velocity_covariance: 0.0
  velocity_covariance: 0.0
  velocity_covariance: 0.0
  velocity_covariance: 0.009999999776482582
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  light_status {
    brake_visible: 0.0
    brake_switch_on: 0.0
    left_turn_visible: 0.0
    left_turn_switch_on: 0.0
    right_turn_visible: 0.0
    right_turn_switch_on: 0.0
  }
}

perception_obstacle {
  id: 4527
  position {
    x: 587031.2292501448
    y: 4141578.2264314825
    z: -2.1167787112217895
  }
  theta: -0.3359089493751526
  velocity {
    x: 1.1029198169708252
    y: -0.38507404923439026
    z: 0.0
  }
  length: 4.578289031982422
  width: 2.1571853160858154
  height: 1.9104602336883545
  polygon_point {
    x: 587028.7539320315
    y: 4141577.896961091
    z: -2.1167787197805463
  }
  polygon_point {
    x: 587033.0793514574
    y: 4141576.5756834727
    z: -2.1167787197805463
  }
  polygon_point {
    x: 587033.1104555452
    y: 4141576.6074255686
    z: -2.1167787197805463
  }
  polygon_point {
    x: 587033.7051534975
    y: 4141578.5559805613
    z: -2.1167787197805463
  }
  polygon_point {
    x: 587029.3797350252
    y: 4141579.8772581797
    z: -2.1167787197805463
  }
  polygon_point {
    x: 587029.3486318911
    y: 4141579.8455160838
    z: -2.1167787197805463
  }
  tracking_time: 0.5099995136260986
  type: VEHICLE
  timestamp: 1623764283.2516732
  acceleration {
    x: 0.028172489255666733
    y: -0.009844474494457245
    z: 0.0
  }
  anchor_point {
    x: 587031.2295432121
    y: 4141578.226471609
    z: -1.1615485850532095
  }
  bbox2d {
    xmin: 0.0
    ymin: 0.0
    xmax: 0.0
    ymax: 0.0
  }
  sub_type: ST_UNKNOWN
  measurements {
    sensor_id: "velodyne128"
    id: 4061
    position {
      x: 587031.2292501448
      y: 4141578.2264314825
      z: -2.1167787112217895
    }
    theta: -0.3359089493751526
    length: 4.578289031982422
    width: 2.1571853160858154
    height: 1.9104602336883545
    velocity {
      x: 1.1244314908981323
      y: -0.3925846219062805
      z: 0.0
    }
    type: VEHICLE
    timestamp: 1623764283.2516732
    box {
      xmin: 0.0
      ymin: 0.0
      xmax: 0.0
      ymax: 0.0
    }
  }
  height_above_ground: nan
  position_covariance: 0.0
  position_covariance: 0.0
  position_covariance: 0.0
  position_covariance: 0.0
  position_covariance: 0.0
  position_covariance: 0.0
  position_covariance: 0.0
  position_covariance: 0.0
  position_covariance: 0.0
  velocity_covariance: 1.448632001876831
  velocity_covariance: -0.5453196167945862
  velocity_covariance: 0.0
  velocity_covariance: -0.5453196167945862
  velocity_covariance: 0.2733396887779236
  velocity_covariance: 0.0
  velocity_covariance: 0.0
  velocity_covariance: 0.0
  velocity_covariance: 0.009999999776482582
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  acceleration_covariance: 0.0
  light_status {
    brake_visible: 0.0
    brake_switch_on: 0.0
    left_turn_visible: 0.0
    left_turn_switch_on: 0.0
    right_turn_visible: 0.0
    right_turn_switch_on: 0.0
  }
}
header {
  timestamp_sec: 1623764286.3026705
  module_name: "perception_obstacle"
  sequence_num: 46291
  lidar_timestamp: 1623764283251673344
  camera_timestamp: 0
  radar_timestamp: 0
}
error_code: OK



From Channel: /apollo/localization/pose
Pose
header {
  timestamp_sec: 1623766798.8114822
  module_name: "localization"
  sequence_num: 2910
}
localization {
  position {
    x: 587035.480178833
    y: 4141521.4636306763
    z: -2.735304117202759
  }
  orientation {
    qx: -1.095324205380166e-05
    qy: 0.00847282912582159
    qz: -0.9960733652114868
    qw: -0.08812598884105682
  }
  linear_velocity {
    x: 2.9571237973868847e-05
    y: 5.4270203690975904e-06
    z: -1.6893100109882653e-06
  }
  linear_acceleration {
    x: -0.0
    y: 0.0
    z: 0.0
  }
  angular_velocity {
    x: -0.0
    y: 0.0
    z: 0.0
  }
  heading: -1.747296391176853
  linear_acceleration_vrf {
    x: 0.0
    y: 0.0
    z: 0.0
  }
  angular_velocity_vrf {
    x: 0.0
    y: 0.0
    z: 0.0
  }
  euler_angles {
    x: 0.016881849799753046
    y: 6.281713595700751
    z: 2.965092960956639
  }
}




From Channel: Lane_lane
PerceptionLanes
header {
  timestamp_sec: 1623828298.4508007
  sequence_num: 1549
  frame_id: "Lane"
}
camera_laneline {
  type: YELLOW_SOLID
  pos_type: EGO_LEFT
  curve_camera_coord {
    longitude_min: 2.3326916694641113
    longitude_max: 23.872610092163086
    a: -2.383181571960449
    b: -0.004792015999555588
    c: -9.4414299383061e-06
    d: 2.3054059283822426e-07
  }
}
camera_laneline {
  type: WHITE_DASHED
  pos_type: EGO_RIGHT
  curve_camera_coord {
    longitude_min: 2.247539520263672
    longitude_max: 23.11398696899414
    a: 2.330697774887085
    b: -0.010599522851407528
    c: -2.874049869205919e-07
    d: 7.428406334497595e-09
  }
}




From Channel: /apollo/planning
The decision part
main_decision {
  stop {
    reason_code: STOP_REASON_SIGNAL
    reason: "stop by TL_signal_13"
    stop_point {
      x: 552864.1751095449
      y: 4182683.960536364
    }
    stop_heading: 3.1357639601399594
    change_lane_type: LEFT
  }
}
object_decision {
  decision {
    id: "2_0"
    perception_id: 2
    object_decision {
      overtake {
        distance_s: 11.997346100531068
        fence_point {
          x: 552944.8023779017
          y: 4182683.788196684
          z: 0.0
        }
        fence_heading: -3.141122153920231
        time_buffer: 2.0
      }
    }
  }
  decision {
    id: "TL_signal_13"
    perception_id: -589675150
    object_decision {
      stop {
        reason_code: STOP_REASON_SIGNAL
        distance_s: -1.0
        stop_point {
          x: 552864.1751095449
          y: 4182683.960536364
          z: 0.0
        }
        stop_heading: 3.1357639601399594
      }
    }
  }
}
vehicle_signal {
  turn_signal: TURN_LEFT
}




 [{'timestamp': 1623915380633518336, 

 'Ego': 
 {'size': {'length': 4.7, 'width': 2.06}, 'pose': {'position': {'x': 587049.5892372131, 'y': 4141586.311776161, 'z': -1.5999374389648438}, 'orientation': {'qx': -0.0011840370716527104, 'qy': 0.002963780192658305, 'qz': -0.9903981685638428, 'qw': -0.1382073163986206}, 'linear_velocity': {'x': 1.2232863809913397e-05, 'y': 1.2005810276605189e-05, 'z': -2.875602604035521e-06}, 'linear_acceleration': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'angular_velocity': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'heading': -1.8481087789109827, 'linear_acceleration_vrf': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'angular_velocity_vrf': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'euler_angles': {'x': 0.006197964874105344, 'y': 0.0015261349838580768, 'z': 2.8642936460585133}}}, 

 'truth': 
 {'minDistToEgo': 1.1735254095650558, 
 'nearestGtObs': 8800, 
 'obsList': 
 [{'id': 8805, 'position': {'x': 587064.1953940392, 'y': 4141581.815495014, 'z': -1.277207374572754}, 'theta': 2.8564556967150168, 'velocity': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'length': 4.566516876220703, 'width': 2.0909385681152344, 'height': 1.3560072183609009, 'polygonPointList': [{'x': 587066.0923828777, 'y': 4141580.169983378, 'z': -1.277207374572754}, {'x': 587066.6805405463, 'y': 4141582.17649645, 'z': -1.277207374572754}, {'x': 587062.2984052006, 'y': 4141583.4610066502, 'z': -1.277207374572754}, {'x': 587061.710247532, 'y': 4141581.4544935785, 'z': -1.277207374572754}], 'trackingTime': 37.63999915868044, 'type': 5, 'timestamp': 1623915380.6335185, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'anchorPoint': {'x': 587064.1953940392, 'y': 4141581.815495014, 'z': -1.277207374572754}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 8805, 'position': {'x': 587064.1953940392, 'y': 4141581.815495014, 'z': -1.277207374572754}, 'theta': 2.8564556967150168, 'length': 4.566516876220703, 'width': 2.0909385681152344, 'height': 1.3560072183609009, 'velocity': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'type': 5, 'subType': 3, 'timestamp': 1623915380.6335185}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 11.666138694333505}, 
 {'id': 8813, 'position': {'x': 587072.407394886, 'y': 4141579.528820753, 'z': -1.2396973371505737}, 'theta': 2.873612046640517, 'velocity': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'length': 4.566516876220703, 'width': 2.0909385681152344, 'height': 1.3560072183609009, 'polygonPointList': [{'x': 587074.3323339646, 'y': 4141577.9160949467, 'z': -1.2396973371505737}, {'x': 587074.8859824929, 'y': 4141579.9324027873, 'z': -1.2396973371505737}, {'x': 587070.4824558074, 'y': 4141581.1415465595, 'z': -1.2396973371505737}, {'x': 587069.9288072791, 'y': 4141579.125238719, 'z': -1.2396973371505737}], 'trackingTime': 3.969999911263585, 'type': 5, 'timestamp': 1623915380.6335185, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'anchorPoint': {'x': 587072.407394886, 'y': 4141579.528820753, 'z': -1.2396973371505737}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 8813, 'position': {'x': 587072.407394886, 'y': 4141579.528820753, 'z': -1.2396973371505737}, 'theta': 2.873612046640517, 'length': 4.566516876220703, 'width': 2.0909385681152344, 'height': 1.3560072183609009, 'velocity': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'type': 5, 'subType': 3, 'timestamp': 1623915380.6335185}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 20.191405333746395}, 
 {'id': 17, 'position': {'x': 587053.7144203186, 'y': 4141553.0074157715, 'z': -1.417405366897583}, 'theta': 5.568488701266006, 'velocity': {'x': 0.0, 'y': -0.0, 'z': -2.384185791015625e-05}, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'polygonPointList': [{'x': 587053.6894443631, 'y': 4141553.360085875, 'z': -1.417405366897583}, {'x': 587053.3617502153, 'y': 4141552.982439816, 'z': -1.417405366897583}, {'x': 587053.7393962741, 'y': 4141552.654745668, 'z': -1.417405366897583}, {'x': 587054.0670904219, 'y': 4141553.032391727, 'z': -1.417405366897583}], 'trackingTime': 2950.7399340458214, 'type': 3, 'timestamp': 1623915380.6335185, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.0, 'y': -0.0, 'z': -0.00476837158203125}, 'anchorPoint': {'x': 587053.7144203186, 'y': 4141553.0074157715, 'z': -1.417405366897583}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 10, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 17, 'position': {'x': 587053.7144203186, 'y': 4141553.0074157715, 'z': -1.417405366897583}, 'theta': 5.568488701266006, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'velocity': {'x': 0.0, 'y': -0.0, 'z': -2.384185791015625e-05}, 'type': 3, 'subType': 10, 'timestamp': 1623915380.6335185}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 31.81196494023312}, 
 {'id': 18, 'position': {'x': 587016.5036354065, 'y': 4141546.4150829315, 'z': -0.9020534157752991}, 'theta': 0.9436415901635087, 'velocity': {'x': 0.0, 'y': -0.0, 'z': -4.76837158203125e-05}, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'polygonPointList': [{'x': 587016.1544994414, 'y': 4141546.3593686223, 'z': -0.9020534157752991}, {'x': 587016.5593497157, 'y': 4141546.0659469664, 'z': -0.9020534157752991}, {'x': 587016.8527713716, 'y': 4141546.4707972407, 'z': -0.9020534157752991}, {'x': 587016.4479210973, 'y': 4141546.7642188966, 'z': -0.9020534157752991}], 'trackingTime': 2941.04993426241, 'type': 3, 'timestamp': 1623915380.6335185, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.0, 'y': 0.0, 'z': -0.002384185791015625}, 'anchorPoint': {'x': 587016.5036354065, 'y': 4141546.4150829315, 'z': -0.9020534157752991}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 10, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 18, 'position': {'x': 587016.5036354065, 'y': 4141546.4150829315, 'z': -0.9020534157752991}, 'theta': 0.9436415901635087, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'velocity': {'x': 0.0, 'y': -0.0, 'z': -4.76837158203125e-05}, 'type': 3, 'subType': 10, 'timestamp': 1623915380.6335185}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 47.89309998560779}, 
 {'id': 8810, 'position': {'x': 587055.882853508, 'y': 4141608.720384598, 'z': -0.8181061744689941}, 'theta': 4.450673713999436, 'velocity': {'x': -9.536744619254023e-05, 'y': 1.1368683772161603e-11, 'z': 1.1920928955078125e-05}, 'length': 3.9509117603302, 'width': 1.8471839427947998, 'height': 1.6631338596343994, 'polygonPointList': [{'x': 587057.2861200992, 'y': 4141610.389603217, 'z': -0.8181061744689941}, {'x': 587055.5018372613, 'y': 4141610.8675395865, 'z': -0.8181061744689941}, {'x': 587054.4795869167, 'y': 4141607.0511659784, 'z': -0.8181061744689941}, {'x': 587056.2638697547, 'y': 4141606.573229609, 'z': -0.8181061744689941}], 'trackingTime': 9.649999784305692, 'type': 5, 'timestamp': 1623915380.6335185, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.00953674502670765, 'y': -1.1368683772161603e-09, 'z': 0.0011920928955078125}, 'anchorPoint': {'x': 587055.882853508, 'y': 4141608.720384598, 'z': -0.8181061744689941}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 8810, 'position': {'x': 587055.882853508, 'y': 4141608.720384598, 'z': -0.8181061744689941}, 'theta': 4.450673713999436, 'length': 3.9509117603302, 'width': 1.8471839427947998, 'height': 1.6631338596343994, 'velocity': {'x': -9.536744619254023e-05, 'y': 1.1368683772161603e-11, 'z': 1.1920928955078125e-05}, 'type': 5, 'subType': 3, 'timestamp': 1623915380.6335185}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 19.93972335982196}, 
 {'id': 30, 'position': {'x': 587016.2228279114, 'y': 4141545.3629436493, 'z': -0.9703857898712158}, 'theta': 2.9042514484284254, 'velocity': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'polygonPointList': [{'x': 587016.4070397429, 'y': 4141545.0611721985, 'z': -0.9703857898712158}, {'x': 587016.5245993622, 'y': 4141545.547155481, 'z': -0.9703857898712158}, {'x': 587016.0386160798, 'y': 4141545.6647151, 'z': -0.9703857898712158}, {'x': 587015.9210564606, 'y': 4141545.1787318178, 'z': -0.9703857898712158}], 'trackingTime': 2939.539934296161, 'type': 3, 'timestamp': 1623915380.6335185, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.0, 'y': 0.0, 'z': 0.002384185791015625}, 'anchorPoint': {'x': 587016.2228279114, 'y': 4141545.3629436493, 'z': -0.9703857898712158}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 10, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 30, 'position': {'x': 587016.2228279114, 'y': 4141545.3629436493, 'z': -0.9703857898712158}, 'theta': 2.9042514484284254, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'velocity': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'type': 3, 'subType': 10, 'timestamp': 1623915380.6335185}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 48.824754903411446}, 
 {'id': 8797, 'position': {'x': 587056.2340812683, 'y': 4141584.1342425346, 'z': -1.263519525527954}, 'theta': 2.854335287871521, 'velocity': {'x': 0.0, 'y': -0.0, 'z': -4.76837158203125e-05}, 'length': 4.061402797698975, 'width': 1.8944153785705566, 'height': 1.4395885467529297, 'polygonPointList': [{'x': 587057.9132079894, 'y': 4141582.650502595, 'z': -1.263519525527954}, {'x': 587058.4499395316, 'y': 4141584.4672934483, 'z': -1.263519525527954}, {'x': 587054.5549545472, 'y': 4141585.617982474, 'z': -1.263519525527954}, {'x': 587054.018223005, 'y': 4141583.801191621, 'z': -1.263519525527954}], 'trackingTime': 58.769998686388135, 'type': 5, 'timestamp': 1623915380.6335185, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.0, 'y': 0.0, 'z': -0.002384185791015625}, 'anchorPoint': {'x': 587056.2340812683, 'y': 4141584.1342425346, 'z': -1.263519525527954}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 8797, 'position': {'x': 587056.2340812683, 'y': 4141584.1342425346, 'z': -1.263519525527954}, 'theta': 2.854335287871521, 'length': 4.061402797698975, 'width': 1.8944153785705566, 'height': 1.4395885467529297, 'velocity': {'x': 0.0, 'y': -0.0, 'z': -4.76837158203125e-05}, 'type': 5, 'subType': 3, 'timestamp': 1623915380.6335185}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 3.626251031534762}, 

 {'id': 8816, 'position': {'x': 587057.7088165283, 'y': 4141615.591403961, 'z': -0.63883376121521}, 'theta': 4.451746967910424, 'velocity': {'x': -0.002288819756358862, 'y': -0.008773804642260075, 'z': 0.0007033348083496094}, 'length': 3.9509117603302, 'width': 1.8471839427947998, 'height': 1.6631338596343994, 'polygonPointList': [{'x': 587059.1102906707, 'y': 4141617.2621278125, 'z': -0.63883376121521}, {'x': 587057.3254958641, 'y': 4141617.738148759, 'z': -0.63883376121521}, {'x': 587056.307342386, 'y': 4141613.92068011, 'z': -0.63883376121521}, {'x': 587058.0921371925, 'y': 4141613.4446591632, 'z': -0.63883376121521}], 'trackingTime': 3.9099999126046896, 'type': 5, 'timestamp': 1623915380.6335185, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.0286102294921875, 'y': 0.03814697265625, 'z': -0.0059604644775390625}, 'anchorPoint': {'x': 587057.7088165283, 'y': 4141615.591403961, 'z': -0.63883376121521}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 8816, 'position': {'x': 587057.7088165283, 'y': 4141615.591403961, 'z': -0.63883376121521}, 'theta': 4.451746967910424, 'length': 3.9509117603302, 'width': 1.8471839427947998, 'height': 1.6631338596343994, 'velocity': {'x': -0.002288819756358862, 'y': -0.008773804642260075, 'z': 0.0007033348083496094}, 'type': 5, 'subType': 3, 'timestamp': 1623915380.6335185}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 27.049194537741513}, 

 {'id': 8814, 'position': {'x': 587040.3999500275, 'y': 4141553.8074245453, 'z': -1.8741106986999512}, 'theta': 4.572600418293717, 'velocity': {'x': -1.34811532497406, 'y': -9.955216407775879, 'z': -0.18694400787353516}, 'length': 4.061402797698975, 'width': 1.8944153785705566, 'height': 1.4395885467529297, 'polygonPointList': [{'x': 587041.6208633331, 'y': 4141555.6863394133, 'z': -1.8741106986999512}, {'x': 587039.7449271024, 'y': 4141555.950295365, 'z': -1.8741106986999512}, {'x': 587039.1790367218, 'y': 4141551.9285096773, 'z': -1.8741106986999512}, {'x': 587041.0549729526, 'y': 4141551.6645537256, 'z': -1.8741106986999512}], 'trackingTime': 4.689999895170331, 'type': 5, 'timestamp': 1623915380.6335185, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': -3.47137451171875, 'y': -8.525848388671875, 'z': 0.09298324584960938}, 'anchorPoint': {'x': 587040.3999500275, 'y': 4141553.8074245453, 'z': -1.8741106986999512}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 8814, 'position': {'x': 587040.3999500275, 'y': 4141553.8074245453, 'z': -1.8741106986999512}, 'theta': 4.572600418293717, 'length': 4.061402797698975, 'width': 1.8944153785705566, 'height': 1.4395885467529297, 'velocity': {'x': -1.34811532497406, 'y': -9.955216407775879, 'z': -0.18694400787353516}, 'type': 5, 'subType': 3, 'timestamp': 1623915380.6335185}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 28.97196756380873}, 
 {'id': 81, 'position': {'x': 587066.7363066673, 'y': 4141559.7622909546, 'z': -1.2982889413833618}, 'theta': 5.879625809009781, 'velocity': {'x': 0.0008821492665447295, 'y': 0.0036239626351743937, 'z': -7.152557373046875e-05}, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'polygonPointList': [{'x': 587066.6045630574, 'y': 4141560.090381831, 'z': -1.2982889413833618}, {'x': 587066.408215791, 'y': 4141559.6305473447, 'z': -1.2982889413833618}, {'x': 587066.8680502772, 'y': 4141559.4342000782, 'z': -1.2982889413833618}, {'x': 587067.0643975437, 'y': 4141559.8940345645, 'z': -1.2982889413833618}], 'trackingTime': 2964.1099337469786, 'type': 3, 'timestamp': 1623915380.6335185, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': -0.021457690745592117, 'y': -0.1525879204273224, 'z': 0.019073486328125}, 'anchorPoint': {'x': 587066.7363066673, 'y': 4141559.7622909546, 'z': -1.2982889413833618}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 10, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 81, 'position': {'x': 587066.7363066673, 'y': 4141559.7622909546, 'z': -1.2982889413833618}, 'theta': 5.879625809009781, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'velocity': {'x': 0.0008821492665447295, 'y': 0.0036239626351743937, 'z': -7.152557373046875e-05}, 'type': 3, 'subType': 10, 'timestamp': 1623915380.6335185}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 30.00759400953133}, 
 {'id': 26, 'position': {'x': 587018.3042755127, 'y': 4141547.7686748505, 'z': -0.48381471633911133}, 'theta': 1.1533000106203417, 'velocity': {'x': 0.0003814696683548391, 'y': -0.0009536744910292327, 'z': -0.014221668243408203}, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'polygonPointList': [{'x': 587017.9743805006, 'y': 4141547.64151638, 'z': -0.48381471633911133}, {'x': 587018.4314339831, 'y': 4141547.4387798384, 'z': -0.48381471633911133}, {'x': 587018.6341705248, 'y': 4141547.895833321, 'z': -0.48381471633911133}, {'x': 587018.1771170422, 'y': 4141548.0985698625, 'z': -0.48381471633911133}], 'trackingTime': 2942.279934234917, 'type': 3, 'timestamp': 1623915380.6335185, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': -0.0381469801068306, 'y': 5.820766091346741e-09, 'z': -0.0667572021484375}, 'anchorPoint': {'x': 587018.3042755127, 'y': 4141547.7686748505, 'z': -0.48381471633911133}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 10, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 26, 'position': {'x': 587018.3042755127, 'y': 4141547.7686748505, 'z': -0.48381471633911133}, 'theta': 1.1533000106203417, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'velocity': {'x': 0.0003814696683548391, 'y': -0.0009536744910292327, 'z': -0.014221668243408203}, 'type': 3, 'subType': 10, 'timestamp': 1623915380.6335185}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 45.67789451015159}, 
 {'id': 109, 'position': {'x': 587002.6622314453, 'y': 4141571.889111042, 'z': -0.869399905204773}, 'theta': 2.9668312061866686, 'velocity': {'x': -0.9841920137405396, 'y': 0.1745225340127945, 'z': 0.0263214111328125}, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'polygonPointList': [{'x': 587002.8649551384, 'y': 4141571.5994507186, 'z': -0.869399905204773}, {'x': 587002.9518917687, 'y': 4141572.091834735, 'z': -0.869399905204773}, {'x': 587002.4595077522, 'y': 4141572.1787713654, 'z': -0.869399905204773}, {'x': 587002.3725711219, 'y': 4141571.686387349, 'z': -0.869399905204773}], 'trackingTime': 58.36999869532883, 'type': 3, 'timestamp': 1623915380.6335185, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.0, 'y': 0.01430511474609375, 'z': 0.002384185791015625}, 'anchorPoint': {'x': 587002.6622314453, 'y': 4141571.889111042, 'z': -0.869399905204773}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 10, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 109, 'position': {'x': 587002.6622314453, 'y': 4141571.889111042, 'z': -0.869399905204773}, 'theta': 2.9668312061866686, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'velocity': {'x': -0.9841920137405396, 'y': 0.1745225340127945, 'z': 0.0263214111328125}, 'type': 3, 'subType': 10, 'timestamp': 1623915380.6335185}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 44.973733198108384}, 

 {'id': 8815, 'position': {'x': 587029.1103897095, 'y': 4141586.190881729, 'z': -1.0561153888702393}, 'theta': 5.986194063416548, 'velocity': {'x': -1.1368683772161603e-11, 'y': -9.536744619254023e-05, 'z': 0.0}, 'length': 4.705558776855469, 'width': 2.080930471420288, 'height': 1.771530270576477, 'polygonPointList': [{'x': 587027.1650985078, 'y': 4141587.874324891, 'z': -1.0561153888702393}, {'x': 587026.5561254629, 'y': 4141585.8844948867, 'z': -1.0561153888702393}, {'x': 587031.0556809112, 'y': 4141584.5074385675, 'z': -1.0561153888702393}, {'x': 587031.6646539561, 'y': 4141586.4972685715, 'z': -1.0561153888702393}], 'trackingTime': 4.619999896734953, 'type': 5, 'timestamp': 1623915380.6335185, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'anchorPoint': {'x': 587029.1103897095, 'y': 4141586.190881729, 'z': -1.0561153888702393}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 8815, 'position': {'x': 587029.1103897095, 'y': 4141586.190881729, 'z': -1.0561153888702393}, 'theta': 5.986194063416548, 'length': 4.705558776855469, 'width': 2.080930471420288, 'height': 1.771530270576477, 'velocity': {'x': -1.1368683772161603e-11, 'y': -9.536744619254023e-05, 'z': 0.0}, 'type': 5, 'subType': 3, 'timestamp': 1623915380.6335185}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 14.01368368734794}, 

 {'id': 8800, 'position': {'x': 587040.1297416687, 'y': 4141582.9542455673, 'z': 0.11438179016113281}, 'theta': 6.0487088400446964, 'velocity': {'x': -5.6843418860808015e-12, 'y': -4.7683723096270114e-05, 'z': -2.384185791015625e-05}, 'length': 10.51540470123291, 'width': 3.209941864013672, 'height': 4.441589832305908, 'polygonPointList': [{'x': 587035.388799694, 'y': 4141585.7368407254, 'z': 0.11438179016113281}, {'x': 587034.6430213867, 'y': 4141582.614735378, 'z': 0.11438179016113281}, {'x': 587044.8706836434, 'y': 4141580.171650409, 'z': 0.11438179016113281}, {'x': 587045.6164619507, 'y': 4141583.2937557567, 'z': 0.11438179016113281}], 'trackingTime': 50.76999886520207, 'type': 5, 'timestamp': 1623915380.6335185, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': -5.684341886080801e-10, 'y': -0.004768372513353825, 'z': -0.002384185791015625}, 'anchorPoint': {'x': 587040.1297416687, 'y': 4141582.9542455673, 'z': 0.11438179016113281}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 5, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 8800, 'position': {'x': 587040.1297416687, 'y': 4141582.9542455673, 'z': 0.11438179016113281}, 'theta': 6.0487088400446964, 'length': 10.51540470123291, 'width': 3.209941864013672, 'height': 4.441589832305908, 'velocity': {'x': -5.6843418860808015e-12, 'y': -4.7683723096270114e-05, 'z': -2.384185791015625e-05}, 'type': 5, 'subType': 5, 'timestamp': 1623915380.6335185}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 1.1735254095650558}, 

 {'id': 38, 'position': {'x': 587019.1614112854, 'y': 4141547.73928833, 'z': -0.830270528793335}, 'theta': 2.5797583216052544, 'velocity': {'x': 0.0, 'y': -0.0, 'z': -4.76837158203125e-05}, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'polygonPointList': [{'x': 587019.239796266, 'y': 4141547.394533649, 'z': -0.830270528793335}, {'x': 587019.5061659664, 'y': 4141547.8176733106, 'z': -0.830270528793335}, {'x': 587019.0830263048, 'y': 4141548.084043011, 'z': -0.830270528793335}, {'x': 587018.8166566044, 'y': 4141547.6609033495, 'z': -0.830270528793335}], 'trackingTime': 2942.419934231788, 'type': 3, 'timestamp': 1623915380.6335185, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.0, 'y': -0.0, 'z': -0.00476837158203125}, 'anchorPoint': {'x': 587019.1614112854, 'y': 4141547.73928833, 'z': -0.830270528793335}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 10, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 38, 'position': {'x': 587019.1614112854, 'y': 4141547.73928833, 'z': -0.830270528793335}, 'theta': 2.5797583216052544, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'velocity': {'x': 0.0, 'y': -0.0, 'z': -4.76837158203125e-05}, 'type': 3, 'subType': 10, 'timestamp': 1623915380.6335185}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 45.21924595701151}, 

 {'id': 8817, 'position': {'x': 587056.7055511475, 'y': 4141627.1496124268, 'z': -0.4174642860889435}, 'theta': 4.454087087542149, 'velocity': {'x': -1.597691535949707, 'y': -6.049347400665283, 'z': -0.17908811569213867}, 'length': 3.9509117603302, 'width': 1.8471839427947998, 'height': 1.6631338596343994, 'polygonPointList': [{'x': 587058.1031118092, 'y': 4141628.823611278, 'z': -0.4174642860889435}, {'x': 587056.3172079581, 'y': 4141629.295454342, 'z': -0.4174642860889435}, {'x': 587055.3079904857, 'y': 4141625.4756135754, 'z': -0.4174642860889435}, {'x': 587057.0938943368, 'y': 4141625.0037705116, 'z': -0.4174642860889435}], 'trackingTime': 0.9299999792128801, 'type': 5, 'timestamp': 1623915380.6335185, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': -0.5245208740234375, 'y': -0.80108642578125, 'z': 0.05364418029785156}, 'anchorPoint': {'x': 587056.7055511475, 'y': 4141627.1496124268, 'z': -0.4174642860889435}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 8817, 'position': {'x': 587056.7055511475, 'y': 4141627.1496124268, 'z': -0.4174642860889435}, 'theta': 4.454087087542149, 'length': 3.9509117603302, 'width': 1.8471839427947998, 'height': 1.6631338596343994, 'velocity': {'x': -1.597691535949707, 'y': -6.049347400665283, 'z': -0.17908811569213867}, 'type': 5, 'subType': 3, 'timestamp': 1623915380.6335185}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 38.07793420445525}, 

 {'id': 82, 'position': {'x': 587019.743522644, 'y': 4141548.482105255, 'z': -0.797447681427002}, 'theta': 1.8595439609437392, 'velocity': {'x': 0.00038146975566633046, 'y': -0.00019073493604082614, 'z': 0.0024080276489257812}, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'polygonPointList': [{'x': 587019.5750603154, 'y': 4141548.1712669656, 'z': -0.797447681427002}, {'x': 587020.0543609336, 'y': 4141548.3136429265, 'z': -0.797447681427002}, {'x': 587019.9119849727, 'y': 4141548.7929435447, 'z': -0.797447681427002}, {'x': 587019.4326843545, 'y': 4141548.6505675837, 'z': -0.797447681427002}], 'trackingTime': 2942.919934220612, 'type': 3, 'timestamp': 1623915380.6335185, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.45776376128196716, 'y': 0.2098083347082138, 'z': -0.03337860107421875}, 'anchorPoint': {'x': 587019.743522644, 'y': 4141548.482105255, 'z': -0.797447681427002}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 10, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 82, 'position': {'x': 587019.743522644, 'y': 4141548.482105255, 'z': -0.797447681427002}, 'theta': 1.8595439609437392, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'velocity': {'x': 0.00038146975566633046, 'y': -0.00019073493604082614, 'z': 0.0024080276489257812}, 'type': 3, 'subType': 10, 'timestamp': 1623915380.6335185}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 44.19345361922708}]}}, 














 {'timestamp': 1623915380733518336, 
 'Ego': {
 'size': {'length': 4.7, 'width': 2.06}, 
 'pose': {'position': {'x': 587049.5892372131, 'y': 4141586.311776161, 'z': -1.5999374389648438}, 
 'orientation': {'qx': -0.0011840370716527104, 'qy': 0.002963780192658305, 'qz': -0.9903981685638428, 'qw': -0.1382073163986206}, 
 'linear_velocity': {'x': 1.2232863809913397e-05, 'y': 1.2005810276605189e-05, 'z': -2.875602604035521e-06}, 
 'linear_acceleration': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'angular_velocity': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 
 'heading': -1.8481087789109827, 'linear_acceleration_vrf': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 
 'angular_velocity_vrf': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 
 'euler_angles': {'x': 0.006197964874105344, 'y': 0.0015261349838580768, 'z': 2.8642936460585133}}}, 

 'truth': {
 'minDistToEgo': 1.1735388531725728, 
 'nearestGtObs': 8800, 
 'obsList': 
 [{'id': 8805, 
 'position': {'x': 587064.1953940392, 'y': 4141581.815495014, 'z': -1.277207612991333}, 
 'theta': 2.85645543039891, 'velocity': {'x': 0.0, 'y': -0.0, 'z': -1.1920928955078125e-05}, 
 'length': 4.566516876220703, 'width': 2.0909385681152344,  'height': 1.3560072183609009, 
 'polygonPointList': [{'x': 587066.0923822628, 'y': 4141580.169982754, 'z': -1.277207612991333}, {'x': 587066.6805406169, 'y': 4141582.1764955767, 'z': -1.277207612991333}, {'x': 587062.2984058155, 'y': 4141583.461007274, 'z': -1.277207612991333}, {'x': 587061.7102474615, 'y': 4141581.4544944516, 'z': -1.277207612991333}], 
 'trackingTime': 37.739999156445265, 'type': 5, 'timestamp': 1623915380.7335184, 
 'pointCloudList': [], 
 'dropsList': [], 
 'acceleration': {'x': 0.0, 'y': -0.0, 'z': -0.0011920928955078125}, 
 'anchorPoint': {'x': 587064.1953940392, 'y': 4141581.815495014, 'z': -1.277207612991333}, 
 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 
 'measurementsList': [{'sensorId': 'velodyne128', 'id': 8805, 'position': {'x': 587064.1953940392, 'y': 4141581.815495014, 'z': -1.277207612991333}, 
 'theta': 2.85645543039891, 'length': 4.566516876220703, 'width': 2.0909385681152344, 'height': 1.3560072183609009, 
 'velocity': {'x': 0.0, 'y': -0.0, 'z': -1.1920928955078125e-05}, 'type': 5, 'subType': 3, 'timestamp': 1623915380.7335184}], 
 'heightAboveGround': nan, 
 'positionCovarianceList': [], 
 'velocityCovarianceList': [], 
 'accelerationCovarianceList': [], 
 'distToEgo': 11.666138685001327}, 

 {'id': 8813, 'position': {'x': 587072.4073958397, 'y': 4141579.528820753, 'z': -1.2396970987319946}, 
 'theta': 2.873612046640517, 
 'velocity': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'length': 4.566516876220703, 'width': 2.0909385681152344, 'height': 1.3560072183609009, 
 'polygonPointList': [{'x': 587074.3323349183, 'y': 4141577.9160949467, 'z': -1.2396970987319946}, {'x': 587074.8859834466, 'y': 4141579.9324027873, 'z': -1.2396970987319946}, {'x': 587070.4824567611, 'y': 4141581.1415465595, 'z': -1.2396970987319946}, {'x': 587069.9288082328, 'y': 4141579.125238719, 'z': -1.2396970987319946}], 
 'trackingTime': 4.069999909028411, 'type': 5, 'timestamp': 1623915380.7335184, 
 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 
 'anchorPoint': {'x': 587072.4073958397, 'y': 4141579.528820753, 'z': -1.2396970987319946}, 
 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 
 'measurementsList': [{'sensorId': 'velodyne128', 'id': 8813, 'position': {'x': 587072.4073958397, 'y': 4141579.528820753, 'z': -1.2396970987319946}, 'theta': 2.873612046640517, 'length': 4.566516876220703, 'width': 2.0909385681152344, 'height': 1.3560072183609009, 'velocity': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'type': 5, 'subType': 3, 'timestamp': 1623915380.7335184}], 
 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 20.191406253258446}, 

 {'id': 17, 'position': {'x': 587053.7144203186, 'y': 4141553.0074157715, 'z': -1.4174052476882935}, 'theta': 5.568488701266006, 'velocity': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'polygonPointList': [{'x': 587053.6894443631, 'y': 4141553.360085875, 'z': -1.4174052476882935}, {'x': 587053.3617502153, 'y': 4141552.982439816, 'z': -1.4174052476882935}, {'x': 587053.7393962741, 'y': 4141552.654745668, 'z': -1.4174052476882935}, {'x': 587054.0670904219, 'y': 4141553.032391727, 'z': -1.4174052476882935}], 'trackingTime': 2950.8399340435863, 'type': 3, 'timestamp': 1623915380.7335184, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'anchorPoint': {'x': 587053.7144203186, 'y': 4141553.0074157715, 'z': -1.4174052476882935}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 10, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 17, 'position': {'x': 587053.7144203186, 'y': 4141553.0074157715, 'z': -1.4174052476882935}, 'theta': 5.568488701266006, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'velocity': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'type': 3, 'subType': 10, 'timestamp': 1623915380.7335184}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 31.81196494023312}, 
 {'id': 18, 'position': {'x': 587016.5036354065, 'y': 4141546.4150829315, 'z': -0.9020533561706543}, 'theta': 0.9436415901635087, 'velocity': {'x': 0.0, 'y': -0.0, 'z': -2.384185791015625e-05}, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'polygonPointList': [{'x': 587016.1544994414, 'y': 4141546.3593686223, 'z': -0.9020533561706543}, {'x': 587016.5593497157, 'y': 4141546.0659469664, 'z': -0.9020533561706543}, {'x': 587016.8527713716, 'y': 4141546.4707972407, 'z': -0.9020533561706543}, {'x': 587016.4479210973, 'y': 4141546.7642188966, 'z': -0.9020533561706543}], 'trackingTime': 2941.1499342601746, 'type': 3, 'timestamp': 1623915380.7335184, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'anchorPoint': {'x': 587016.5036354065, 'y': 4141546.4150829315, 'z': -0.9020533561706543}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 10, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 18, 'position': {'x': 587016.5036354065, 'y': 4141546.4150829315, 'z': -0.9020533561706543}, 'theta': 0.9436415901635087, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'velocity': {'x': 0.0, 'y': -0.0, 'z': -2.384185791015625e-05}, 'type': 3, 'subType': 10, 'timestamp': 1623915380.7335184}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 47.89309998560779}, 
 {'id': 8810, 'position': {'x': 587055.8828439713, 'y': 4141608.720384598, 'z': -0.818105936050415}, 'theta': 4.450677975057147, 'velocity': {'x': -9.536744619254023e-05, 'y': 1.1368683772161603e-11, 'z': -3.5762786865234375e-05}, 'length': 3.9509117603302, 'width': 1.8471839427947998, 'height': 1.6631338596343994, 'polygonPointList': [{'x': 587057.2861034251, 'y': 4141610.3896092805, 'z': -0.818105936050415}, {'x': 587055.5018184952, 'y': 4141610.8675379977, 'z': -0.818105936050415}, {'x': 587054.4795845174, 'y': 4141607.051159915, 'z': -0.818105936050415}, {'x': 587056.2638694473, 'y': 4141606.573231198, 'z': -0.818105936050415}], 'trackingTime': 9.749999782070518, 'type': 5, 'timestamp': 1623915380.7335184, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': -0.00953674502670765, 'y': 1.1368683772161603e-09, 'z': -0.007152557373046875}, 'anchorPoint': {'x': 587055.8828439713, 'y': 4141608.720384598, 'z': -0.818105936050415}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 8810, 'position': {'x': 587055.8828439713, 'y': 4141608.720384598, 'z': -0.818105936050415}, 'theta': 4.450677975057147, 'length': 3.9509117603302, 'width': 1.8471839427947998, 'height': 1.6631338596343994, 'velocity': {'x': -9.536744619254023e-05, 'y': 1.1368683772161603e-11, 'z': -3.5762786865234375e-05}, 'type': 5, 'subType': 3, 'timestamp': 1623915380.7335184}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 19.939720778781588},
{'id': 30, 'position': {'x': 587016.2228279114, 'y': 4141545.3629436493, 'z': -0.9703857898712158}, 'theta': 2.9042503831639976, 'velocity': {'x': 0.0, 'y': 0.0, 'z': 2.384185791015625e-05}, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'polygonPointList': [{'x': 587016.4070394076, 'y': 4141545.0611720122, 'z': -0.9703857898712158}, {'x': 587016.5245995484, 'y': 4141545.5471551456, 'z': -0.9703857898712158}, {'x': 587016.0386164151, 'y': 4141545.6647152863, 'z': -0.9703857898712158}, {'x': 587015.9210562743, 'y': 4141545.178732153, 'z': -0.9703857898712158}], 'trackingTime': 2939.6399342939258, 'type': 3, 'timestamp': 1623915380.7335184, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.0, 'y': 0.0, 'z': 0.00476837158203125}, 'anchorPoint': {'x': 587016.2228279114, 'y': 4141545.3629436493, 'z': -0.9703857898712158}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 10, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 30, 'position': {'x': 587016.2228279114, 'y': 4141545.3629436493, 'z': -0.9703857898712158}, 'theta': 2.9042503831639976, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'velocity': {'x': 0.0, 'y': 0.0, 'z': 2.384185791015625e-05}, 'type': 3, 'subType': 10, 'timestamp': 1623915380.7335184}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 48.824755056074814}, 
{'id': 8797, 'position': {'x': 587056.234079361, 'y': 4141584.134243965, 'z': -1.263520359992981}, 'theta': 2.854336353135949, 'velocity': {'x': 0.0, 'y': -0.0, 'z': -2.384185791015625e-05}, 'length': 4.061402797698975, 'width': 1.8944153785705566, 'height': 1.4395885467529297, 'polygonPointList': [{'x': 587057.913207647, 'y': 4141582.6505058007, 'z': -1.263520359992981}, {'x': 587058.4499372697, 'y': 4141584.4672972187, 'z': -1.263520359992981}, {'x': 587054.5549510749, 'y': 4141585.6179821296, 'z': -1.263520359992981}, {'x': 587054.0182214523, 'y': 4141583.8011907116, 'z': -1.263520359992981}], 'trackingTime': 58.86999868415296, 'type': 5, 'timestamp': 1623915380.7335184, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.0, 'y': -0.0, 'z': -0.002384185791015625}, 'anchorPoint': {'x': 587056.234079361, 'y': 4141584.134243965, 'z': -1.263520359992981}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 8797, 'position': {'x': 587056.234079361, 'y': 4141584.134243965, 'z': -1.263520359992981}, 'theta': 2.854336353135949, 'length': 4.061402797698975, 'width': 1.8944153785705566, 'height': 1.4395885467529297, 'velocity': {'x': 0.0, 'y': -0.0, 'z': -2.384185791015625e-05}, 'type': 5, 'subType': 3, 'timestamp': 1623915380.7335184}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 3.626248978570386}, 
{'id': 8816, 'position': {'x': 587057.7086687088, 'y': 4141615.5908432007, 'z': -0.6387834548950195}, 'theta': 4.4517485658070655, 'velocity': {'x': -0.001239777309820056, 'y': -0.004577637184411287, 'z': 0.0003933906555175781}, 'length': 3.9509117603302, 'width': 1.8471839427947998, 'height': 1.6631338596343994, 'polygonPointList': [{'x': 587059.1101400573, 'y': 4141617.2615693626, 'z': -0.6387834548950195}, {'x': 587057.3253444801, 'y': 4141617.7375873365, 'z': -0.6387834548950195}, {'x': 587056.3071973603, 'y': 4141613.920117039, 'z': -0.6387834548950195}, {'x': 587058.0919929375, 'y': 4141613.444099065, 'z': -0.6387834548950195}], 'trackingTime': 4.009999910369515, 'type': 5, 'timestamp': 1623915380.7335184, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.0, 'y': 0.03814697265625, 'z': -0.0011920928955078125}, 'anchorPoint': {'x': 587057.7086687088, 'y': 4141615.5908432007, 'z': -0.6387834548950195}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 8816, 'position': {'x': 587057.7086687088, 'y': 4141615.5908432007, 'z': -0.6387834548950195}, 'theta': 4.4517485658070655, 'length': 3.9509117603302, 'width': 1.8471839427947998, 'height': 1.6631338596343994, 'velocity': {'x': -0.001239777309820056, 'y': -0.004577637184411287, 'z': 0.0003933906555175781}, 'type': 5, 'subType': 3, 'timestamp': 1623915380.7335184}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 27.048614591254967}, 
{'id': 8814, 'position': {'x': 587040.2409629822, 'y': 4141552.7592487335, 'z': -1.893194317817688}, 'theta': 4.547603722179758, 'velocity': {'x': -1.7288223505020142, 'y': -10.788346290588379, 'z': -0.18379688262939453}, 'length': 4.061402797698975, 'width': 1.8944153785705566, 'height': 1.4395885467529297, 'polygonPointList': [{'x': 587041.5084567557, 'y': 4141554.6070609675, 'z': -1.893194317817688}, {'x': 587039.6397038993, 'y': 4141554.917821881, 'z': -1.893194317817688}, {'x': 587038.9734692087, 'y': 4141550.9114364996, 'z': -1.893194317817688}, {'x': 587040.8422220651, 'y': 4141550.600675586, 'z': -1.893194317817688}], 'trackingTime': 4.789999892935157, 'type': 5, 'timestamp': 1623915380.7335184, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': -4.043591022491455, 'y': -8.087158203125, 'z': -0.3075599670410156}, 'anchorPoint': {'x': 587040.2409629822, 'y': 4141552.7592487335, 'z': -1.893194317817688}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 8814, 'position': {'x': 587040.2409629822, 'y': 4141552.7592487335, 'z': -1.893194317817688}, 'theta': 4.547603722179758, 'length': 4.061402797698975, 'width': 1.8944153785705566, 'height': 1.4395885467529297, 'velocity': {'x': -1.7288223505020142, 'y': -10.788346290588379, 'z': -0.18379688262939453}, 'type': 5, 'subType': 3, 'timestamp': 1623915380.7335184}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 30.054751458804592}, 
{'id': 81, 'position': {'x': 587066.7363734245, 'y': 4141559.7626075745, 'z': -1.2983036041259766}, 'theta': 5.879693719617052, 'velocity': {'x': 0.0012397771934047341, 'y': 0.0034332277718931437, 'z': -0.00016689300537109375}, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'polygonPointList': [{'x': 587066.604607448, 'y': 4141560.0906894654, 'z': -1.2983036041259766}, {'x': 587066.4082915336, 'y': 4141559.630841598, 'z': -1.2983036041259766}, {'x': 587066.8681394011, 'y': 4141559.4345256835, 'z': -1.2983036041259766}, {'x': 587067.0644553155, 'y': 4141559.894373551, 'z': -1.2983036041259766}], 'trackingTime': 2964.2099337447435, 'type': 3, 'timestamp': 1623915380.7335184, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.07867814600467682, 'y': -2.3283064365386963e-08, 'z': -0.002384185791015625}, 'anchorPoint': {'x': 587066.7363734245, 'y': 4141559.7626075745, 'z': -1.2983036041259766}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 10, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 81, 'position': {'x': 587066.7363734245, 'y': 4141559.7626075745, 'z': -1.2983036041259766}, 'theta': 5.879693719617052, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'velocity': {'x': 0.0012397771934047341, 'y': 0.0034332277718931437, 'z': -0.00016689300537109375}, 'type': 3, 'subType': 10, 'timestamp': 1623915380.7335184}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 30.00735618859227}, 
{'id': 26, 'position': {'x': 587018.3043251038, 'y': 4141547.7685775757, 'z': -0.4852027893066406}, 'theta': 1.1533064022069084, 'velocity': {'x': 0.0003814696683548391, 'y': -0.0009536744910292327, 'z': -0.014197826385498047}, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'polygonPointList': [{'x': 587017.9744308963, 'y': 4141547.6414169893, 'z': -0.4852027893066406}, {'x': 587018.4314856902, 'y': 4141547.4386833683, 'z': -0.4852027893066406}, {'x': 587018.6342193112, 'y': 4141547.895738162, 'z': -0.4852027893066406}, {'x': 587018.1771645173, 'y': 4141548.098471783, 'z': -0.4852027893066406}], 'trackingTime': 2942.379934232682, 'type': 3, 'timestamp': 1623915380.7335184, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': -0.0381469801068306, 'y': 5.820766091346741e-09, 'z': -0.057220458984375}, 'anchorPoint': {'x': 587018.3043251038, 'y': 4141547.7685775757, 'z': -0.4852027893066406}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 10, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 26, 'position': {'x': 587018.3043251038, 'y': 4141547.7685775757, 'z': -0.4852027893066406}, 'theta': 1.1533064022069084, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'velocity': {'x': 0.0003814696683548391, 'y': -0.0009536744910292327, 'z': -0.014197826385498047}, 'type': 3, 'subType': 10, 'timestamp': 1623915380.7335184}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 45.67794083879479}, 
{'id': 109, 'position': {'x': 587002.5638122559, 'y': 4141571.9065361023, 'z': -0.8667694330215454}, 'theta': 2.966843190411481, 'velocity': {'x': -0.9841920137405396, 'y': 0.17437948286533356, 'z': 0.026297569274902344}, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'polygonPointList': [{'x': 587002.7665394321, 'y': 4141571.616878219, 'z': -0.8667694330215454}, {'x': 587002.8534701392, 'y': 4141572.1092632785, 'z': -0.8667694330215454}, {'x': 587002.3610850796, 'y': 4141572.1961939856, 'z': -0.8667694330215454}, {'x': 587002.2741543725, 'y': 4141571.703808926, 'z': -0.8667694330215454}], 'trackingTime': 58.46999869309366, 'type': 3, 'timestamp': 1623915380.7335184, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.0, 'y': 0.0095367431640625, 'z': -0.0035762786865234375}, 'anchorPoint': {'x': 587002.5638122559, 'y': 4141571.9065361023, 'z': -0.8667694330215454}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 10, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 109, 'position': {'x': 587002.5638122559, 'y': 4141571.9065361023, 'z': -0.8667694330215454}, 'theta': 2.966843190411481, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'velocity': {'x': -0.9841920137405396, 'y': 0.17437948286533356, 'z': 0.026297569274902344}, 'type': 3, 'subType': 10, 'timestamp': 1623915380.7335184}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 45.06376169895936}, 
{'id': 8815, 'position': {'x': 587029.1103897095, 'y': 4141586.1908750534, 'z': -1.056114673614502}, 'theta': 5.986192199203799, 'velocity': {'x': 0.0, 'y': 0.0, 'z': 1.1920928955078125e-05}, 'length': 4.705558776855469, 'width': 2.080930471420288, 'height': 1.771530270576477, 'polygonPointList': [{'x': 587027.1651016613, 'y': 4141587.8743219343, 'z': -1.056114673614502}, {'x': 587026.5561248334, 'y': 4141585.8844930464, 'z': -1.056114673614502}, {'x': 587031.0556777576, 'y': 4141584.5074281725, 'z': -1.056114673614502}, {'x': 587031.6646545855, 'y': 4141586.4972570604, 'z': -1.056114673614502}], 'trackingTime': 4.719999894499779, 'type': 5, 'timestamp': 1623915380.7335184, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 1.1368683772161603e-09, 'y': 0.00953674502670765, 'z': -0.0011920928955078125}, 'anchorPoint': {'x': 587029.1103897095, 'y': 4141586.1908750534, 'z': -1.056114673614502}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 8815, 'position': {'x': 587029.1103897095, 'y': 4141586.1908750534, 'z': -1.056114673614502}, 'theta': 5.986192199203799, 'length': 4.705558776855469, 'width': 2.080930471420288, 'height': 1.771530270576477, 'velocity': {'x': 0.0, 'y': 0.0, 'z': 1.1920928955078125e-05}, 'type': 5, 'subType': 3, 'timestamp': 1623915380.7335184}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 14.013682870421398}, 
{'id': 8800, 'position': {'x': 587040.1297245026, 'y': 4141582.9542455673, 'z': 0.1143796443939209}, 'theta': 6.048707774780269, 'velocity': {'x': -0.00019073489238508046, 'y': -4.7683697630418465e-05, 'z': -4.76837158203125e-05}, 'length': 10.51540470123291, 'width': 3.209941864013672, 'height': 4.441589832305908, 'polygonPointList': [{'x': 587035.3887852642, 'y': 4141585.7368452004, 'z': 0.1143796443939209}, {'x': 587034.6430039912, 'y': 4141582.614740618, 'z': 0.1143796443939209}, {'x': 587044.8706637409, 'y': 4141580.171645934, 'z': 0.1143796443939209}, {'x': 587045.6164450139, 'y': 4141583.2937505166, 'z': 0.1143796443939209}], 'trackingTime': 50.869998862966895, 'type': 5, 'timestamp': 1623915380.7335184, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.0, 'y': -0.004768372047692537, 'z': 0.0}, 'anchorPoint': {'x': 587040.1297245026, 'y': 4141582.9542455673, 'z': 0.1143796443939209}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 5, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 8800, 'position': {'x': 587040.1297245026, 'y': 4141582.9542455673, 'z': 0.1143796443939209}, 'theta': 6.048707774780269, 'length': 10.51540470123291, 'width': 3.209941864013672, 'height': 4.441589832305908, 'velocity': {'x': -0.00019073489238508046, 'y': -4.7683697630418465e-05, 'z': -4.76837158203125e-05}, 'type': 5, 'subType': 5, 'timestamp': 1623915380.7335184}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 1.1735388531725728}, 
{'id': 38, 'position': {'x': 587019.1614112854, 'y': 4141547.73928833, 'z': -0.8302704095840454}, 'theta': 2.579760185818003, 'velocity': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'polygonPointList': [{'x': 587019.2397968769, 'y': 4141547.394533783, 'z': -0.8302704095840454}, {'x': 587019.5061658323, 'y': 4141547.8176739216, 'z': -0.8302704095840454}, {'x': 587019.0830256939, 'y': 4141548.084042877, 'z': -0.8302704095840454}, {'x': 587018.8166567385, 'y': 4141547.6609027386, 'z': -0.8302704095840454}], 'trackingTime': 2942.5199342295527, 'type': 3, 'timestamp': 1623915380.7335184, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.0, 'y': 0.0, 'z': 0.0011920928955078125}, 'anchorPoint': {'x': 587019.1614112854, 'y': 4141547.73928833, 'z': -0.8302704095840454}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 10, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 38, 'position': {'x': 587019.1614112854, 'y': 4141547.73928833, 'z': -0.8302704095840454}, 'theta': 2.579760185818003, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'velocity': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'type': 3, 'subType': 10, 'timestamp': 1623915380.7335184}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 45.21924554356163}, 
{'id': 8817, 'position': {'x': 587056.5444469452, 'y': 4141626.5396347046, 'z': -0.4352281987667084}, 'theta': 4.454052200132139, 'velocity': {'x': -1.613713264465332, 'y': -6.120300769805908, 'z': -0.17697811126708984}, 'length': 3.9509117603302, 'width': 1.8471839427947998, 'height': 1.6631338596343994, 'polygonPointList': [{'x': 587057.9420659312, 'y': 4141628.2135849083, 'z': -0.4352281987667084}, {'x': 587056.156178485, 'y': 4141628.6854901793, 'z': -0.4352281987667084}, {'x': 587055.1468279592, 'y': 4141624.865684501, 'z': -0.4352281987667084}, {'x': 587056.9327154054, 'y': 4141624.39377923, 'z': -0.4352281987667084}], 'trackingTime': 1.029999976977706, 'type': 5, 'timestamp': 1623915380.7335184, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': -0.5245208740234375, 'y': -0.49591064453125, 'z': 0.0035762786865234375}, 'anchorPoint': {'x': 587056.5444469452, 'y': 4141626.5396347046, 'z': -0.4352281987667084}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 8817, 'position': {'x': 587056.5444469452, 'y': 4141626.5396347046, 'z': -0.4352281987667084}, 'theta': 4.454052200132139, 'length': 3.9509117603302, 'width': 1.8471839427947998, 'height': 1.6631338596343994, 'velocity': {'x': -1.613713264465332, 'y': -6.120300769805908, 'z': -0.17697811126708984}, 'type': 5, 'subType': 3, 'timestamp': 1623915380.7335184}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 37.44886924094707}, 
{'id': 82, 'position': {'x': 587019.7435302734, 'y': 4141548.482110977, 'z': -0.79804527759552}, 'theta': 1.8601277258501625, 'velocity': {'x': 0.0030517582781612873, 'y': 0.0017166136531159282, 'z': 0.0028133392333984375}, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'polygonPointList': [{'x': 587019.575249441, 'y': 4141548.1711743996, 'z': -0.79804527759552}, {'x': 587020.054466851, 'y': 4141548.3138301447, 'z': -0.79804527759552}, {'x': 587019.9118111059, 'y': 4141548.793047555, 'z': -0.79804527759552}, {'x': 587019.4325936958, 'y': 4141548.6503918096, 'z': -0.79804527759552}], 'trackingTime': 2943.019934218377, 'type': 3, 'timestamp': 1623915380.7335184, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.9918214678764343, 'y': 0.5722045302391052, 'z': 0.4291534423828125}, 'anchorPoint': {'x': 587019.7435302734, 'y': 4141548.482110977, 'z': -0.79804527759552}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 10, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 82, 'position': {'x': 587019.7435302734, 'y': 4141548.482110977, 'z': -0.79804527759552}, 'theta': 1.8601277258501625, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'velocity': {'x': 0.0030517582781612873, 'y': 0.0017166136531159282, 'z': 0.0028133392333984375}, 'type': 3, 'subType': 10, 'timestamp': 1623915380.7335184}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 44.193473664219084}]}}, 


{'timestamp': 1623915380833518336, 
'Ego': {'size': {'length': 4.7, 'width': 2.06}, 
'pose': {'position': {'x': 587049.5892372131, 'y': 4141586.311776161, 'z': -1.5999374389648438}, 'orientation': {'qx': -0.0011840370716527104, 'qy': 0.002963780192658305, 'qz': -0.9903981685638428, 'qw': -0.1382073163986206}, 'linear_velocity': {'x': 1.2232863809913397e-05, 'y': 1.2005810276605189e-05, 'z': -2.875602604035521e-06}, 'linear_acceleration': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'angular_velocity': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'heading': -1.8481087789109827, 'linear_acceleration_vrf': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'angular_velocity_vrf': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'euler_angles': {'x': 0.006197964874105344, 'y': 0.0015261349838580768, 'z': 2.8642936460585133}}}, 
'truth': {
'minDistToEgo': 1.173548764686743, 
'nearestGtObs': 8800, 
'obsList': [
{'id': 8805, 'position': {'x': 587064.1953935623, 'y': 4141581.8154935837, 'z': -1.2772085666656494}, 'theta': 2.856454897766696, 'velocity': {'x': 0.0, 'y': -0.0, 'z': -5.9604644775390625e-05}, 'length': 4.566516876220703, 'width': 2.0909385681152344, 'height': 1.3560072183609009, 'polygonPointList': [{'x': 587066.0923810465, 'y': 4141580.1699804277, 'z': -1.2772085666656494}, {'x': 587066.6805403351, 'y': 4141582.176493001, 'z': -1.2772085666656494}, {'x': 587062.2984060781, 'y': 4141583.4610067396, 'z': -1.2772085666656494}, {'x': 587061.7102467895, 'y': 4141581.454494166, 'z': -1.2772085666656494}], 'trackingTime': 37.83999915421009, 'type': 5, 'timestamp': 1623915380.8335183, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 5.684341886080801e-10, 'y': 0.004768372513353825, 'z': -0.008344650268554688}, 'anchorPoint': {'x': 587064.1953935623, 'y': 4141581.8154935837, 'z': -1.2772085666656494}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 8805, 'position': {'x': 587064.1953935623, 'y': 4141581.8154935837, 'z': -1.2772085666656494}, 'theta': 2.856454897766696, 'length': 4.566516876220703, 'width': 2.0909385681152344, 'height': 1.3560072183609009, 'velocity': {'x': 0.0, 'y': -0.0, 'z': -5.9604644775390625e-05}, 'type': 5, 'subType': 3, 'timestamp': 1623915380.8335183}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 11.666138524584616}, 
{'id': 8813, 'position': {'x': 587072.4073958397, 'y': 4141579.5288209915, 'z': -1.2396970987319946}, 'theta': 2.873612046640517, 'velocity': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'length': 4.566516876220703, 'width': 2.0909385681152344, 'height': 1.3560072183609009, 'polygonPointList': [{'x': 587074.3323349183, 'y': 4141577.916095185, 'z': -1.2396970987319946}, {'x': 587074.8859834466, 'y': 4141579.9324030257, 'z': -1.2396970987319946}, {'x': 587070.4824567611, 'y': 4141581.141546798, 'z': -1.2396970987319946}, {'x': 587069.9288082328, 'y': 4141579.1252389573, 'z': -1.2396970987319946}], 'trackingTime': 4.169999906793237, 'type': 5, 'timestamp': 1623915380.8335183, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'anchorPoint': {'x': 587072.4073958397, 'y': 4141579.5288209915, 'z': -1.2396970987319946}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 8813, 'position': {'x': 587072.4073958397, 'y': 4141579.5288209915, 'z': -1.2396970987319946}, 'theta': 2.873612046640517, 'length': 4.566516876220703, 'width': 2.0909385681152344, 'height': 1.3560072183609009, 'velocity': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'type': 5, 'subType': 3, 'timestamp': 1623915380.8335183}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 20.191406190252156}, 
{'id': 17, 'position': {'x': 587053.7144203186, 'y': 4141553.0074157715, 'z': -1.417405366897583}, 'theta': 5.568488434949899, 'velocity': {'x': 0.0, 'y': -0.0, 'z': -2.384185791015625e-05}, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'polygonPointList': [{'x': 587053.6894444525, 'y': 4141553.360085875, 'z': -1.417405366897583}, {'x': 587053.3617502153, 'y': 4141552.9824399054, 'z': -1.417405366897583}, {'x': 587053.7393961847, 'y': 4141552.654745668, 'z': -1.417405366897583}, {'x': 587054.0670904219, 'y': 4141553.0323916376, 'z': -1.417405366897583}], 'trackingTime': 2950.939934041351, 'type': 3, 'timestamp': 1623915380.8335183, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.0, 'y': -0.0, 'z': -0.00476837158203125}, 'anchorPoint': {'x': 587053.7144203186, 'y': 4141553.0074157715, 'z': -1.417405366897583}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 10, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 17, 'position': {'x': 587053.7144203186, 'y': 4141553.0074157715, 'z': -1.417405366897583}, 'theta': 5.568488434949899, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'velocity': {'x': 0.0, 'y': -0.0, 'z': -2.384185791015625e-05}, 'type': 3, 'subType': 10, 'timestamp': 1623915380.8335183}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 31.811964961168393}, 
{'id': 18, 'position': {'x': 587016.5036354065, 'y': 4141546.4150829315, 'z': -0.9020534157752991}, 'theta': 0.9436415901635087, 'velocity': {'x': 0.0, 'y': -0.0, 'z': -4.76837158203125e-05}, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'polygonPointList': [{'x': 587016.1544994414, 'y': 4141546.3593686223, 'z': -0.9020534157752991}, {'x': 587016.5593497157, 'y': 4141546.0659469664, 'z': -0.9020534157752991}, {'x': 587016.8527713716, 'y': 4141546.4707972407, 'z': -0.9020534157752991}, {'x': 587016.4479210973, 'y': 4141546.7642188966, 'z': -0.9020534157752991}], 'trackingTime': 2941.2499342579395, 'type': 3, 'timestamp': 1623915380.8335183, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.0, 'y': 0.0, 'z': -0.002384185791015625}, 'anchorPoint': {'x': 587016.5036354065, 'y': 4141546.4150829315, 'z': -0.9020534157752991}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 10, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 18, 'position': {'x': 587016.5036354065, 'y': 4141546.4150829315, 'z': -0.9020534157752991}, 'theta': 0.9436415901635087, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'velocity': {'x': 0.0, 'y': -0.0, 'z': -4.76837158203125e-05}, 'type': 3, 'subType': 10, 'timestamp': 1623915380.8335183}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 47.89309998560779}, 
{'id': 8810, 'position': {'x': 587055.8828353882, 'y': 4141608.720396042, 'z': -0.8181064128875732}, 'theta': 4.450683301379286, 'velocity': {'x': -9.536741708870977e-05, 'y': 0.00019073489238508046, 'z': 2.384185791015625e-05}, 'length': 3.9509117603302, 'width': 1.8471839427947998, 'height': 1.6631338596343994, 'polygonPointList': [{'x': 587057.2860857426, 'y': 4141610.3896284224, 'z': -0.8181064128875732}, {'x': 587055.5017981704, 'y': 4141610.8675473956, 'z': -0.8181064128875732}, {'x': 587054.4795850337, 'y': 4141607.0511636613, 'z': -0.8181064128875732}, {'x': 587056.263872606, 'y': 4141606.573244688, 'z': -0.8181064128875732}], 'trackingTime': 9.849999779835343, 'type': 5, 'timestamp': 1623915380.8335183, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': -2.1827872842550278e-09, 'y': -0.0190734900534153, 'z': 0.0}, 'anchorPoint': {'x': 587055.8828353882, 'y': 4141608.720396042, 'z': -0.8181064128875732}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 8810, 'position': {'x': 587055.8828353882, 'y': 4141608.720396042, 'z': -0.8181064128875732}, 'theta': 4.450683301379286, 'length': 3.9509117603302, 'width': 1.8471839427947998, 'height': 1.6631338596343994, 'velocity': {'x': -9.536741708870977e-05, 'y': 0.00019073489238508046, 'z': 2.384185791015625e-05}, 'type': 5, 'subType': 3, 'timestamp': 1623915380.8335183}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 19.93972948962988}, 
{'id': 30, 'position': {'x': 587016.2228279114, 'y': 4141545.3629436493, 'z': -0.9703857898712158}, 'theta': 2.9042511821123185, 'velocity': {'x': 0.0, 'y': -0.0, 'z': -2.384185791015625e-05}, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'polygonPointList': [{'x': 587016.4070396721, 'y': 4141545.0611721575, 'z': -0.9703857898712158}, {'x': 587016.5245994031, 'y': 4141545.54715541, 'z': -0.9703857898712158}, {'x': 587016.0386161506, 'y': 4141545.664715141, 'z': -0.9703857898712158}, {'x': 587015.9210564196, 'y': 4141545.1787318885, 'z': -0.9703857898712158}], 'trackingTime': 2939.7399342916906, 'type': 3, 'timestamp': 1623915380.8335183, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.0, 'y': -0.0, 'z': -0.00476837158203125}, 'anchorPoint': {'x': 587016.2228279114, 'y': 4141545.3629436493, 'z': -0.9703857898712158}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 10, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 30, 'position': {'x': 587016.2228279114, 'y': 4141545.3629436493, 'z': -0.9703857898712158}, 'theta': 2.9042511821123185, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'velocity': {'x': 0.0, 'y': -0.0, 'z': -2.384185791015625e-05}, 'type': 3, 'subType': 10, 'timestamp': 1623915380.8335183}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 48.824754934632686}, 
{'id': 8797, 'position': {'x': 587056.234079361, 'y': 4141584.134243965, 'z': -1.2635185718536377}, 'theta': 2.8543371520842697, 'velocity': {'x': 0.0, 'y': 0.0, 'z': 1.1920928955078125e-05}, 'length': 4.061402797698975, 'width': 1.8944153785705566, 'height': 1.4395885467529297, 'polygonPointList': [{'x': 587057.9132088934, 'y': 4141582.650507209, 'z': -1.2635185718536377}, {'x': 587058.4499369917, 'y': 4141584.4672990786, 'z': -1.2635185718536377}, {'x': 587054.5549498285, 'y': 4141585.6179807214, 'z': -1.2635185718536377}, {'x': 587054.0182217302, 'y': 4141583.8011888517, 'z': -1.2635185718536377}], 'trackingTime': 58.96999868191779, 'type': 5, 'timestamp': 1623915380.8335183, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.0, 'y': 0.0, 'z': -0.0011920928955078125}, 'anchorPoint': {'x': 587056.234079361, 'y': 4141584.134243965, 'z': -1.2635185718536377}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 8797, 'position': {'x': 587056.234079361, 'y': 4141584.134243965, 'z': -1.2635185718536377}, 'theta': 2.8543371520842697, 'length': 4.061402797698975, 'width': 1.8944153785705566, 'height': 1.4395885467529297, 'velocity': {'x': 0.0, 'y': 0.0, 'z': 1.1920928955078125e-05}, 'type': 5, 'subType': 3, 'timestamp': 1623915380.8335183}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 3.6262491196207955}, 
{'id': 8816, 'position': {'x': 587057.7085886002, 'y': 4141615.590538025, 'z': -0.6387572288513184}, 'theta': 4.451750696335921, 'velocity': {'x': -0.0006675723707303405, 'y': -0.0022888185922056437, 'z': 0.00016689300537109375}, 'length': 3.9509117603302, 'width': 1.8471839427947998, 'height': 1.6631338596343994, 'polygonPointList': [{'x': 587059.1100567939, 'y': 4141617.261266953, 'z': -0.6387572288513184}, {'x': 587057.3252602259, 'y': 4141617.737281514, 'z': -0.6387572288513184}, {'x': 587056.3071204064, 'y': 4141613.919809097, 'z': -0.6387572288513184}, {'x': 587058.0919169744, 'y': 4141613.443794536, 'z': -0.6387572288513184}], 'trackingTime': 4.109999908134341, 'type': 5, 'timestamp': 1623915380.8335183, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 5.820766091346741e-09, 'y': 0.03814697265625, 'z': -0.00476837158203125}, 'anchorPoint': {'x': 587057.7085886002, 'y': 4141615.590538025, 'z': -0.6387572288513184}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 8816, 'position': {'x': 587057.7085886002, 'y': 4141615.590538025, 'z': -0.6387572288513184}, 'theta': 4.451750696335921, 'length': 3.9509117603302, 'width': 1.8471839427947998, 'height': 1.6631338596343994, 'velocity': {'x': -0.0006675723707303405, 'y': -0.0022888185922056437, 'z': 0.00016689300537109375}, 'type': 5, 'subType': 3, 'timestamp': 1623915380.8335183}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 27.048298931303574}, 
{'id': 8814, 'position': {'x': 587040.0379047394, 'y': 4141551.632894516, 'z': -1.9117226600646973}, 'theta': 4.513788767132638, 'velocity': {'x': -2.223588705062866, 'y': -11.547089576721191, 'z': -0.18668174743652344}, 'length': 4.061402797698975, 'width': 1.8944153785705566, 'height': 1.4395885467529297, 'polygonPointList': [{'x': 587041.3671456216, 'y': 4141553.43679837, 'z': -1.9117226600646973}, {'x': 587039.5099674411, 'y': 4141553.810561306, 'z': -1.9117226600646973}, {'x': 587038.7086638572, 'y': 4141549.828990662, 'z': -1.9117226600646973}, {'x': 587040.5658420377, 'y': 4141549.455227726, 'z': -1.9117226600646973}], 'trackingTime': 4.889999890699983, 'type': 5, 'timestamp': 1623915380.8335183, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': -5.7220458984375, 'y': -7.171630859375, 'z': -0.35762786865234375}, 'anchorPoint': {'x': 587040.0379047394, 'y': 4141551.632894516, 'z': -1.9117226600646973}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 8814, 'position': {'x': 587040.0379047394, 'y': 4141551.632894516, 'z': -1.9117226600646973}, 'theta': 4.513788767132638, 'length': 4.061402797698975, 'width': 1.8944153785705566, 'height': 1.4395885467529297, 'velocity': {'x': -2.223588705062866, 'y': -11.547089576721191, 'z': -0.18668174743652344}, 'type': 5, 'subType': 3, 'timestamp': 1623915380.8335183}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 31.205916841960196}, 
{'id': 81, 'position': {'x': 587066.7364778519, 'y': 4141559.762872696, 'z': -1.2983139753341675}, 'theta': 5.879769886023638, 'velocity': {'x': 0.0002384188846917823, 'y': 0.0022888185922056437, 'z': -4.76837158203125e-05}, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'polygonPointList': [{'x': 587066.6046868414, 'y': 4141560.0909445435, 'z': -1.2983139753341675}, {'x': 587066.4084060043, 'y': 4141559.6310816854, 'z': -1.2983139753341675}, {'x': 587066.8682688624, 'y': 4141559.4348008484, 'z': -1.2983139753341675}, {'x': 587067.0645496994, 'y': 4141559.8946637064, 'z': -1.2983139753341675}], 'trackingTime': 2964.3099337425083, 'type': 3, 'timestamp': 1623915380.8335183, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': -0.08583071827888489, 'y': -0.11444091796875, 'z': 0.0095367431640625}, 'anchorPoint': {'x': 587066.7364778519, 'y': 4141559.762872696, 'z': -1.2983139753341675}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 10, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 81, 'position': {'x': 587066.7364778519, 'y': 4141559.762872696, 'z': -1.2983139753341675}, 'theta': 5.879769886023638, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'velocity': {'x': 0.0002384188846917823, 'y': 0.0022888185922056437, 'z': -4.76837158203125e-05}, 'type': 3, 'subType': 10, 'timestamp': 1623915380.8335183}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 30.00718148449578}, 
{'id': 26, 'position': {'x': 587018.305721283, 'y': 4141547.7659950256, 'z': -0.4813191890716553}, 'theta': 1.1514336673428716, 'velocity': {'x': 0.004577636253088713, 'y': -0.00991821475327015, 'z': 0.03873109817504883}, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'polygonPointList': [{'x': 587017.9755895138, 'y': 4141547.6394524574, 'z': -0.4813191890716553}, {'x': 587018.4322638512, 'y': 4141547.4358632565, 'z': -0.4813191890716553}, {'x': 587018.6358530521, 'y': 4141547.892537594, 'z': -0.4813191890716553}, {'x': 587018.1791787148, 'y': 4141548.096126795, 'z': -0.4813191890716553}], 'trackingTime': 2942.479934230447, 'type': 3, 'timestamp': 1623915380.8335183, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': -0.19073481857776642, 'y': 0.36239632964134216, 'z': -0.2002716064453125}, 'anchorPoint': {'x': 587018.305721283, 'y': 4141547.7659950256, 'z': -0.4813191890716553}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 10, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 26, 'position': {'x': 587018.305721283, 'y': 4141547.7659950256, 'z': -0.4813191890716553}, 'theta': 1.1514336673428716, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'velocity': {'x': 0.004577636253088713, 'y': -0.00991821475327015, 'z': 0.03873109817504883}, 'type': 3, 'subType': 10, 'timestamp': 1623915380.8335183}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 45.679503487464295}, 
{'id': 109, 'position': {'x': 587002.4653930664, 'y': 4141571.923985958, 'z': -0.8641386032104492}, 'theta': 2.966853044107438, 'velocity': {'x': -0.9841920137405396, 'y': 0.17409338057041168, 'z': 0.0263214111328125}, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'polygonPointList': [{'x': 587002.6681231111, 'y': 4141571.634330079, 'z': -0.8641386032104492}, {'x': 587002.7550489455, 'y': 4141572.126716003, 'z': -0.8641386032104492}, {'x': 587002.2626630217, 'y': 4141572.2136418372, 'z': -0.8641386032104492}, {'x': 587002.1757371873, 'y': 4141571.7212559134, 'z': -0.8641386032104492}], 'trackingTime': 58.56999869085848, 'type': 3, 'timestamp': 1623915380.8335183, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.0, 'y': -0.04291534423828125, 'z': 0.0011920928955078125}, 'anchorPoint': {'x': 587002.4653930664, 'y': 4141571.923985958, 'z': -0.8641386032104492}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 10, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 109, 'position': {'x': 587002.4653930664, 'y': 4141571.923985958, 'z': -0.8641386032104492}, 'theta': 2.966853044107438, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'velocity': {'x': -0.9841920137405396, 'y': 0.17409338057041168, 'z': 0.0263214111328125}, 'type': 3, 'subType': 10, 'timestamp': 1623915380.8335183}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 45.153825023561296}, 
{'id': 8815, 'position': {'x': 587029.1103858948, 'y': 4141586.190867424, 'z': -1.0561153888702393}, 'theta': 5.986190068674944, 'velocity': {'x': -1.1368683772161603e-11, 'y': -9.536744619254023e-05, 'z': 0.0}, 'length': 4.705558776855469, 'width': 2.080930471420288, 'height': 1.771530270576477, 'polygonPointList': [{'x': 587027.1651011405, 'y': 4141587.874317962, 'z': -1.0561153888702393}, {'x': 587026.5561205297, 'y': 4141585.8844903144, 'z': -1.0561153888702393}, {'x': 587031.055670649, 'y': 4141584.507416886, 'z': -1.0561153888702393}, {'x': 587031.6646512599, 'y': 4141586.4972445336, 'z': -1.0561153888702393}], 'trackingTime': 4.819999892264605, 'type': 5, 'timestamp': 1623915380.8335183, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'anchorPoint': {'x': 587029.1103858948, 'y': 4141586.190867424, 'z': -1.0561153888702393}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 8815, 'position': {'x': 587029.1103858948, 'y': 4141586.190867424, 'z': -1.0561153888702393}, 'theta': 5.986190068674944, 'length': 4.705558776855469, 'width': 2.080930471420288, 'height': 1.771530270576477, 'velocity': {'x': -1.1368683772161603e-11, 'y': -9.536744619254023e-05, 'z': 0.0}, 'type': 5, 'subType': 3, 'timestamp': 1623915380.8335183}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 14.013685991527396}, 
{'id': 8800, 'position': {'x': 587040.1297225952, 'y': 4141582.9542427063, 'z': 0.1143796443939209}, 'theta': 6.048706176883627, 'velocity': {'x': -5.6843418860808015e-12, 'y': -4.7683723096270114e-05, 'z': -4.76837158203125e-05}, 'length': 10.51540470123291, 'width': 3.209941864013672, 'height': 4.441589832305908, 'polygonPointList': [{'x': 587035.3887874613, 'y': 4141585.7368490514, 'z': 0.1143796443939209}, {'x': 587034.6430017401, 'y': 4141582.6147456174, 'z': 0.1143796443939209}, {'x': 587044.8706577291, 'y': 4141580.171636361, 'z': 0.1143796443939209}, {'x': 587045.6164434503, 'y': 4141583.293739795, 'z': 0.1143796443939209}], 'trackingTime': 50.96999886073172, 'type': 5, 'timestamp': 1623915380.8335183, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': -5.684341886080801e-10, 'y': -0.004768372513353825, 'z': -0.002384185791015625}, 'anchorPoint': {'x': 587040.1297225952, 'y': 4141582.9542427063, 'z': 0.1143796443939209}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 5, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 8800, 'position': {'x': 587040.1297225952, 'y': 4141582.9542427063, 'z': 0.1143796443939209}, 'theta': 6.048706176883627, 'length': 10.51540470123291, 'width': 3.209941864013672, 'height': 4.441589832305908, 'velocity': {'x': -5.6843418860808015e-12, 'y': -4.7683723096270114e-05, 'z': -4.76837158203125e-05}, 'type': 5, 'subType': 5, 'timestamp': 1623915380.8335183}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 1.173548764686743}, 
{'id': 38, 'position': {'x': 587019.1614112854, 'y': 4141547.73928833, 'z': -0.8302702903747559}, 'theta': 2.579759653185789, 'velocity': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'polygonPointList': [{'x': 587019.239796713, 'y': 4141547.3945337385, 'z': -0.8302702903747559}, {'x': 587019.506165877, 'y': 4141547.8176737577, 'z': -0.8302702903747559}, {'x': 587019.0830258578, 'y': 4141548.0840429217, 'z': -0.8302702903747559}, {'x': 587018.8166566938, 'y': 4141547.6609029025, 'z': -0.8302702903747559}], 'trackingTime': 2942.6199342273176, 'type': 3, 'timestamp': 1623915380.8335183, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'anchorPoint': {'x': 587019.1614112854, 'y': 4141547.73928833, 'z': -0.8302702903747559}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 10, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 38, 'position': {'x': 587019.1614112854, 'y': 4141547.73928833, 'z': -0.8302702903747559}, 'theta': 2.579759653185789, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'velocity': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'type': 3, 'subType': 10, 'timestamp': 1623915380.8335183}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 45.21924564933026}, 
{'id': 8817, 'position': {'x': 587056.3821697235, 'y': 4141625.923839569, 'z': -0.45296797156333923}, 'theta': 4.454005328497317, 'velocity': {'x': -1.6275415420532227, 'y': -6.167984485626221, 'z': -0.17720460891723633}, 'length': 3.9509117603302, 'width': 1.8471839427947998, 'height': 1.6631338596343994, 'polygonPointList': [{'x': 587057.7798673082, 'y': 4141627.597724185, 'z': -0.45296797156333923}, {'x': 587055.9940019923, 'y': 4141628.0697132973, 'z': -0.45296797156333923}, {'x': 587054.9844721388, 'y': 4141624.2499549533, 'z': -0.45296797156333923}, {'x': 587056.7703374547, 'y': 4141623.777965841, 'z': -0.45296797156333923}], 'trackingTime': 1.1299999747425318, 'type': 5, 'timestamp': 1623915380.8335183, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': -0.5245208740234375, 'y': -0.2288818359375, 'z': -0.0011920928955078125}, 'anchorPoint': {'x': 587056.3821697235, 'y': 4141625.923839569, 'z': -0.45296797156333923}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 8817, 'position': {'x': 587056.3821697235, 'y': 4141625.923839569, 'z': -0.45296797156333923}, 'theta': 4.454005328497317, 'length': 3.9509117603302, 'width': 1.8471839427947998, 'height': 1.6631338596343994, 'velocity': {'x': -1.6275415420532227, 'y': -6.167984485626221, 'z': -0.17720460891723633}, 'type': 5, 'subType': 3, 'timestamp': 1623915380.8335183}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 36.813925336520676}, 
{'id': 82, 'position': {'x': 587019.7435340881, 'y': 4141548.482110977, 'z': -0.7976394295692444}, 'theta': 1.8576336755086231, 'velocity': {'x': 0.0019073489820584655, 'y': 0.0009536741999909282, 'z': 0.0027418136596679688}, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'polygonPointList': [{'x': 587019.5744782835, 'y': 4141548.171595052, 'z': -0.7976394295692444}, {'x': 587020.0540500134, 'y': 4141548.3130551726, 'z': -0.7976394295692444}, {'x': 587019.9125898927, 'y': 4141548.7926269025, 'z': -0.7976394295692444}, {'x': 587019.4330181628, 'y': 4141548.651166782, 'z': -0.7976394295692444}], 'trackingTime': 2943.1199342161417, 'type': 3, 'timestamp': 1623915380.8335183, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.6866456866264343, 'y': 0.4196166694164276, 'z': 0.0286102294921875}, 'anchorPoint': {'x': 587019.7435340881, 'y': 4141548.482110977, 'z': -0.7976394295692444}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 10, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 82, 'position': {'x': 587019.7435340881, 'y': 4141548.482110977, 'z': -0.7976394295692444}, 'theta': 1.8576336755086231, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'velocity': {'x': 0.0019073489820584655, 'y': 0.0009536741999909282, 'z': 0.0027418136596679688}, 'type': 3, 'subType': 10, 'timestamp': 1623915380.8335183}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 44.193347556711814}]}}, 


{'timestamp': 1623915380933518080, 'Ego': {'size': {'length': 4.7, 'width': 2.06}, 'pose': {'position': {'x': 587049.5892372131, 'y': 4141586.311776161, 'z': -1.5999374389648438}, 'orientation': {'qx': -0.0011840370716527104, 'qy': 0.002963780192658305, 'qz': -0.9903981685638428, 'qw': -0.1382073163986206}, 'linear_velocity': {'x': 1.2232863809913397e-05, 'y': 1.2005810276605189e-05, 'z': -2.875602604035521e-06}, 'linear_acceleration': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'angular_velocity': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'heading': -1.8481087789109827, 'linear_acceleration_vrf': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'angular_velocity_vrf': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'euler_angles': {'x': 0.006197964874105344, 'y': 0.0015261349838580768, 'z': 2.8642936460585133}}}, 'truth': {'minDistToEgo': 1.1735566599201281, 'nearestGtObs': 8800, 'obsList': [{'id': 8805, 'position': {'x': 587064.1953935623, 'y': 4141581.8154935837, 'z': -1.2772083282470703}, 'theta': 2.856454631450589, 'velocity': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'length': 4.566516876220703, 'width': 2.0909385681152344, 'height': 1.3560072183609009, 'polygonPointList': [{'x': 587066.0923806612, 'y': 4141580.1699799458, 'z': -1.2772083282470703}, {'x': 587066.6805404483, 'y': 4141582.1764923944, 'z': -1.2772083282470703}, {'x': 587062.2984064635, 'y': 4141583.4610072216, 'z': -1.2772083282470703}, {'x': 587061.7102466763, 'y': 4141581.454494773, 'z': -1.2772083282470703}], 'trackingTime': 37.93999915197492, 'type': 5, 'timestamp': 1623915380.9335182, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'anchorPoint': {'x': 587064.1953935623, 'y': 4141581.8154935837, 'z': -1.2772083282470703}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 8805, 'position': {'x': 587064.1953935623, 'y': 4141581.8154935837, 'z': -1.2772083282470703}, 'theta': 2.856454631450589, 'length': 4.566516876220703, 'width': 2.0909385681152344, 'height': 1.3560072183609009, 'velocity': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'type': 5, 'subType': 3, 'timestamp': 1623915380.9335182}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 11.666138459715405}, {'id': 8813, 'position': {'x': 587072.4073967934, 'y': 4141579.5288209915, 'z': -1.2396972179412842}, 'theta': 2.873612046640517, 'velocity': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'length': 4.566516876220703, 'width': 2.0909385681152344, 'height': 1.3560072183609009, 'polygonPointList': [{'x': 587074.332335872, 'y': 4141577.916095185, 'z': -1.2396972179412842}, {'x': 587074.8859844003, 'y': 4141579.9324030257, 'z': -1.2396972179412842}, {'x': 587070.4824577147, 'y': 4141581.141546798, 'z': -1.2396972179412842}, {'x': 587069.9288091864, 'y': 4141579.1252389573, 'z': -1.2396972179412842}], 'trackingTime': 4.2699999045580626, 'type': 5, 'timestamp': 1623915380.9335182, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'anchorPoint': {'x': 587072.4073967934, 'y': 4141579.5288209915, 'z': -1.2396972179412842}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 8813, 'position': {'x': 587072.4073967934, 'y': 4141579.5288209915, 'z': -1.2396972179412842}, 'theta': 2.873612046640517, 'length': 4.566516876220703, 'width': 2.0909385681152344, 'height': 1.3560072183609009, 'velocity': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'type': 5, 'subType': 3, 'timestamp': 1623915380.9335182}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 20.191407109764206}, {'id': 17, 'position': {'x': 587053.7125301361, 'y': 4141553.0090198517, 'z': -1.4174046516418457}, 'theta': 5.56862079405505, 'velocity': {'x': -0.00057220458984375, 'y': 0.0003814698429778218, 'z': -9.5367431640625e-05}, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'polygonPointList': [{'x': 587053.6875076145, 'y': 4141553.361686662, 'z': -1.4174046516418457}, {'x': 587053.359863326, 'y': 4141552.98399733, 'z': -1.4174046516418457}, {'x': 587053.7375526577, 'y': 4141552.6563530415, 'z': -1.4174046516418457}, {'x': 587054.0651969463, 'y': 4141553.0340423733, 'z': -1.4174046516418457}], 'trackingTime': 2951.039934039116, 'type': 3, 'timestamp': 1623915380.9335182, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'anchorPoint': {'x': 587053.7125301361, 'y': 4141553.0090198517, 'z': -1.4174046516418457}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 10, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 17, 'position': {'x': 587053.7125301361, 'y': 4141553.0090198517, 'z': -1.4174046516418457}, 'theta': 5.56862079405505, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'velocity': {'x': -0.00057220458984375, 'y': 0.0003814698429778218, 'z': -9.5367431640625e-05}, 'type': 3, 'subType': 10, 'timestamp': 1623915380.9335182}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 31.809955189355772}, {'id': 18, 'position': {'x': 587016.5036354065, 'y': 4141546.4150829315, 'z': -0.9020533561706543}, 'theta': 0.9436415901635087, 'velocity': {'x': 0.0, 'y': -0.0, 'z': -2.384185791015625e-05}, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'polygonPointList': [{'x': 587016.1544994414, 'y': 4141546.3593686223, 'z': -0.9020533561706543}, {'x': 587016.5593497157, 'y': 4141546.0659469664, 'z': -0.9020533561706543}, {'x': 587016.8527713716, 'y': 4141546.4707972407, 'z': -0.9020533561706543}, {'x': 587016.4479210973, 'y': 4141546.7642188966, 'z': -0.9020533561706543}], 'trackingTime': 2941.3499342557043, 'type': 3, 'timestamp': 1623915380.9335182, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'anchorPoint': {'x': 587016.5036354065, 'y': 4141546.4150829315, 'z': -0.9020533561706543}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 10, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 18, 'position': {'x': 587016.5036354065, 'y': 4141546.4150829315, 'z': -0.9020533561706543}, 'theta': 0.9436415901635087, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'velocity': {'x': 0.0, 'y': -0.0, 'z': -2.384185791015625e-05}, 'type': 3, 'subType': 10, 'timestamp': 1623915380.9335182}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 47.89309998560779}, {'id': 8810, 'position': {'x': 587055.8828258514, 'y': 4141608.720397949, 'z': -0.8181060552597046}, 'theta': 4.450688627701425, 'velocity': {'x': -9.536744619254023e-05, 'y': 1.1368683772161603e-11, 'z': 0.0}, 'length': 3.9509117603302, 'width': 1.8471839427947998, 'height': 1.6631338596343994, 'polygonPointList': [{'x': 587057.2860674086, 'y': 4141610.3896375992, 'z': -0.8181060552597046}, {'x': 587055.5017774141, 'y': 4141610.867547214, 'z': -0.8181060552597046}, {'x': 587054.4795842943, 'y': 4141607.051158299, 'z': -0.8181060552597046}, {'x': 587056.2638742888, 'y': 4141606.5732486844, 'z': -0.8181060552597046}], 'trackingTime': 9.94999977760017, 'type': 5, 'timestamp': 1623915380.9335182, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'anchorPoint': {'x': 587055.8828258514, 'y': 4141608.720397949, 'z': -0.8181060552597046}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 8810, 'position': {'x': 587055.8828258514, 'y': 4141608.720397949, 'z': -0.8181060552597046}, 'theta': 4.450688627701425, 'length': 3.9509117603302, 'width': 1.8471839427947998, 'height': 1.6631338596343994, 'velocity': {'x': -9.536744619254023e-05, 'y': 1.1368683772161603e-11, 'z': 0.0}, 'type': 5, 'subType': 3, 'timestamp': 1623915380.9335182}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 19.939728865920145}, {'id': 30, 'position': {'x': 587016.2228279114, 'y': 4141545.3629436493, 'z': -0.9703857898712158}, 'theta': 2.9042517147445324, 'velocity': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'polygonPointList': [{'x': 587016.4070398472, 'y': 4141545.061172273, 'z': -0.9703857898712158}, {'x': 587016.5245992877, 'y': 4141545.547155585, 'z': -0.9703857898712158}, {'x': 587016.0386159755, 'y': 4141545.6647150256, 'z': -0.9703857898712158}, {'x': 587015.9210565351, 'y': 4141545.1787317134, 'z': -0.9703857898712158}], 'trackingTime': 2939.8399342894554, 'type': 3, 'timestamp': 1623915380.9335182, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.0, 'y': 0.0, 'z': -0.0011920928955078125}, 'anchorPoint': {'x': 587016.2228279114, 'y': 4141545.3629436493, 'z': -0.9703857898712158}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 10, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 30, 'position': {'x': 587016.2228279114, 'y': 4141545.3629436493, 'z': -0.9703857898712158}, 'theta': 2.9042517147445324, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'velocity': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'type': 3, 'subType': 10, 'timestamp': 1623915380.9335182}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 48.82475486599304}, {'id': 8797, 'position': {'x': 587056.2340803146, 'y': 4141584.134243965, 'z': -1.2635183334350586}, 'theta': 2.8543379510325906, 'velocity': {'x': 0.0, 'y': -0.0, 'z': -2.384185791015625e-05}, 'length': 4.061402797698975, 'width': 1.8944153785705566, 'height': 1.4395885467529297, 'polygonPointList': [{'x': 587057.9132110934, 'y': 4141582.6505086175, 'z': -1.2635183334350586}, {'x': 587058.4499376673, 'y': 4141584.4673009384, 'z': -1.2635183334350586}, {'x': 587054.5549495359, 'y': 4141585.617979313, 'z': -1.2635183334350586}, {'x': 587054.0182229619, 'y': 4141583.801186992, 'z': -1.2635183334350586}], 'trackingTime': 59.06999867968261, 'type': 5, 'timestamp': 1623915380.9335182, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.0, 'y': -0.0, 'z': -0.002384185791015625}, 'anchorPoint': {'x': 587056.2340803146, 'y': 4141584.134243965, 'z': -1.2635183334350586}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 8797, 'position': {'x': 587056.2340803146, 'y': 4141584.134243965, 'z': -1.2635183334350586}, 'theta': 2.8543379510325906, 'length': 4.061402797698975, 'width': 1.8944153785705566, 'height': 1.4395885467529297, 'velocity': {'x': 0.0, 'y': -0.0, 'z': -2.384185791015625e-05}, 'type': 5, 'subType': 3, 'timestamp': 1623915380.9335182}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 3.626250175053889}, {'id': 8816, 'position': {'x': 587057.7085351944, 'y': 4141615.5903778076, 'z': -0.6387442350387573}, 'theta': 4.451753892129204, 'velocity': {'x': -0.0004768373619299382, 'y': -0.0011444092961028218, 'z': 0.00011920928955078125}, 'length': 3.9509117603302, 'width': 1.8471839427947998, 'height': 1.6631338596343994, 'polygonPointList': [{'x': 587059.1099978006, 'y': 4141617.261111357, 'z': -0.6387442350387573}, {'x': 587057.3251996911, 'y': 4141617.7371199722, 'z': -0.6387442350387573}, {'x': 587056.3070725882, 'y': 4141613.9196442585, 'z': -0.6387442350387573}, {'x': 587058.0918706977, 'y': 4141613.443635643, 'z': -0.6387442350387573}], 'trackingTime': 4.209999905899167, 'type': 5, 'timestamp': 1623915380.9335182, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.0, 'y': 0.0, 'z': 0.002384185791015625}, 'anchorPoint': {'x': 587057.7085351944, 'y': 4141615.5903778076, 'z': -0.6387442350387573}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 8816, 'position': {'x': 587057.7085351944, 'y': 4141615.5903778076, 'z': -0.6387442350387573}, 'theta': 4.451753892129204, 'length': 3.9509117603302, 'width': 1.8471839427947998, 'height': 1.6631338596343994, 'velocity': {'x': -0.0004768373619299382, 'y': -0.0011444092961028218, 'z': 0.00011920928955078125}, 'type': 5, 'subType': 3, 'timestamp': 1623915380.9335182}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 27.048130297087372}, {'id': 8814, 'position': {'x': 587039.7749156952, 'y': 4141550.43702507, 'z': -1.9306771755218506}, 'theta': 4.48327133812171, 'velocity': {'x': -2.8102893829345703, 'y': -12.206269264221191, 'z': -0.17702579498291016}, 'length': 4.061402797698975, 'width': 1.8944153785705566, 'height': 1.4395885467529297, 'polygonPointList': [{'x': 587041.1585794695, 'y': 4141552.1995303826, 'z': -1.9306771755218506}, {'x': 587039.3136705109, 'y': 4141552.629786639, 'z': -1.9306771755218506}, {'x': 587038.3912519208, 'y': 4141548.6745197577, 'z': -1.9306771755218506}, {'x': 587040.2361608795, 'y': 4141548.2442635014, 'z': -1.9306771755218506}], 'trackingTime': 4.9899998884648085, 'type': 5, 'timestamp': 1623915380.9335182, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': -2.384209632873535, 'y': -6.90460205078125, 'z': 0.7653236389160156}, 'anchorPoint': {'x': 587039.7749156952, 'y': 4141550.43702507, 'z': -1.9306771755218506}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 8814, 'position': {'x': 587039.7749156952, 'y': 4141550.43702507, 'z': -1.9306771755218506}, 'theta': 4.48327133812171, 'length': 4.061402797698975, 'width': 1.8944153785705566, 'height': 1.4395885467529297, 'velocity': {'x': -2.8102893829345703, 'y': -12.206269264221191, 'z': -0.17702579498291016}, 'type': 5, 'subType': 3, 'timestamp': 1623915380.9335182}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 32.40678731359856}, {'id': 81, 'position': {'x': 587066.7365779877, 'y': 4141559.7631549835, 'z': -1.2983262538909912}, 'theta': 5.879846318746331, 'velocity': {'x': 0.0008583072922192514, 'y': 0.0024795534554868937, 'z': -0.00019073486328125}, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'polygonPointList': [{'x': 587066.6047619507, 'y': 4141560.0912167653, 'z': -1.2983262538909912}, {'x': 587066.4085162058, 'y': 4141559.6313389465, 'z': -1.2983262538909912}, {'x': 587066.8683940247, 'y': 4141559.4350932017, 'z': -1.2983262538909912}, {'x': 587067.0646397695, 'y': 4141559.8949710205, 'z': -1.2983262538909912}], 'trackingTime': 2964.409933740273, 'type': 3, 'timestamp': 1623915380.9335182, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.03337859734892845, 'y': -0.0762939453125, 'z': -0.016689300537109375}, 'anchorPoint': {'x': 587066.7365779877, 'y': 4141559.7631549835, 'z': -1.2983262538909912}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 10, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 81, 'position': {'x': 587066.7365779877, 'y': 4141559.7631549835, 'z': -1.2983262538909912}, 'theta': 5.879846318746331, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'velocity': {'x': 0.0008583072922192514, 'y': 0.0024795534554868937, 'z': -0.00019073486328125}, 'type': 3, 'subType': 10, 'timestamp': 1623915380.9335182}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 30.0069899597493}, {'id': 26, 'position': {'x': 587018.3056755066, 'y': 4141547.766056061, 'z': -0.47786033153533936}, 'theta': 1.158992251090183, 'velocity': {'x': -0.0026702880859375, 'y': 0.003433228237554431, 'z': 0.034427642822265625}, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'polygonPointList': [{'x': 587017.976509653, 'y': 4141547.6370218173, 'z': -0.47786033153533936}, {'x': 587018.4347097501, 'y': 4141547.436890207, 'z': -0.47786033153533936}, {'x': 587018.6348413602, 'y': 4141547.8950903043, 'z': -0.47786033153533936}, {'x': 587018.1766412631, 'y': 4141548.0952219144, 'z': -0.47786033153533936}], 'trackingTime': 2942.5799342282116, 'type': 3, 'timestamp': 1623915380.9335182, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': -0.0762939602136612, 'y': 0.03814697265625, 'z': 0.022649765014648438}, 'anchorPoint': {'x': 587018.3056755066, 'y': 4141547.766056061, 'z': -0.47786033153533936}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 10, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 26, 'position': {'x': 587018.3056755066, 'y': 4141547.766056061, 'z': -0.47786033153533936}, 'theta': 1.158992251090183, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'velocity': {'x': -0.0026702880859375, 'y': 0.003433228237554431, 'z': 0.034427642822265625}, 'type': 3, 'subType': 10, 'timestamp': 1623915380.9335182}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 45.6780810540509}, {'id': 109, 'position': {'x': 587002.366973877, 'y': 4141571.94140625, 'z': -0.8615081310272217}, 'theta': 2.966868756757748, 'velocity': {'x': -0.9841920137405396, 'y': 0.17390264570713043, 'z': 0.026345252990722656}, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'polygonPointList': [{'x': 587002.5697084516, 'y': 4141571.65175353, 'z': -0.8615081310272217}, {'x': 587002.656626597, 'y': 4141572.1441408247, 'z': -0.8615081310272217}, {'x': 587002.1642393023, 'y': 4141572.23105897, 'z': -0.8615081310272217}, {'x': 587002.0773211569, 'y': 4141571.7386716753, 'z': -0.8615081310272217}], 'trackingTime': 58.66999868862331, 'type': 3, 'timestamp': 1623915380.9335182, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.0, 'y': -0.05245208740234375, 'z': 0.0035762786865234375}, 'anchorPoint': {'x': 587002.366973877, 'y': 4141571.94140625, 'z': -0.8615081310272217}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 10, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 109, 'position': {'x': 587002.366973877, 'y': 4141571.94140625, 'z': -0.8615081310272217}, 'theta': 2.966868756757748, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'velocity': {'x': -0.9841920137405396, 'y': 0.17390264570713043, 'z': 0.026345252990722656}, 'type': 3, 'subType': 10, 'timestamp': 1623915380.9335182}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 45.24393850057778}, {'id': 8815, 'position': {'x': 587029.1103820801, 'y': 4141586.1908607483, 'z': -1.0561156272888184}, 'theta': 5.986187938146088, 'velocity': {'x': 1.1368683772161603e-11, 'y': 9.536744619254023e-05, 'z': 1.1920928955078125e-05}, 'length': 4.705558776855469, 'width': 2.080930471420288, 'height': 1.771530270576477, 'polygonPointList': [{'x': 587027.1651012561, 'y': 4141587.874316003, 'z': -1.0561156272888184}, {'x': 587026.5561158699, 'y': 4141585.88448972, 'z': -1.0561156272888184}, {'x': 587031.055662904, 'y': 4141584.5074054934, 'z': -1.0561156272888184}, {'x': 587031.6646482903, 'y': 4141586.4972317764, 'z': -1.0561156272888184}], 'trackingTime': 4.91999989002943, 'type': 5, 'timestamp': 1623915380.9335182, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 2.2737367544323206e-09, 'y': 0.0190734900534153, 'z': 0.002384185791015625}, 'anchorPoint': {'x': 587029.1103820801, 'y': 4141586.1908607483, 'z': -1.0561156272888184}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 8815, 'position': {'x': 587029.1103820801, 'y': 4141586.1908607483, 'z': -1.0561156272888184}, 'theta': 5.986187938146088, 'length': 4.705558776855469, 'width': 2.080930471420288, 'height': 1.771530270576477, 'velocity': {'x': 1.1368683772161603e-11, 'y': 9.536744619254023e-05, 'z': 1.1920928955078125e-05}, 'type': 5, 'subType': 3, 'timestamp': 1623915380.9335182}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 14.013688752938782}, {'id': 8800, 'position': {'x': 587040.1297225952, 'y': 4141582.954240799, 'z': 0.11438226699829102}, 'theta': 6.048705111619199, 'velocity': {'x': 0.0, 'y': 0.0, 'z': 4.76837158203125e-05}, 'length': 10.51540470123291, 'width': 3.209941864013672, 'height': 4.441589832305908, 'polygonPointList': [{'x': 587035.3887912764, 'y': 4141585.7368540303, 'z': 0.11438226699829102}, {'x': 587034.6430010588, 'y': 4141582.6147515527, 'z': 0.11438226699829102}, {'x': 587044.870653914, 'y': 4141580.1716275676, 'z': 0.11438226699829102}, {'x': 587045.6164441316, 'y': 4141583.293730045, 'z': 0.11438226699829102}], 'trackingTime': 51.06999885849655, 'type': 5, 'timestamp': 1623915380.9335182, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 5.684341886080801e-10, 'y': 0.004768372513353825, 'z': -0.002384185791015625}, 'anchorPoint': {'x': 587040.1297225952, 'y': 4141582.954240799, 'z': 0.11438226699829102}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 5, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 8800, 'position': {'x': 587040.1297225952, 'y': 4141582.954240799, 'z': 0.11438226699829102}, 'theta': 6.048705111619199, 'length': 10.51540470123291, 'width': 3.209941864013672, 'height': 4.441589832305908, 'velocity': {'x': 0.0, 'y': 0.0, 'z': 4.76837158203125e-05}, 'type': 5, 'subType': 5, 'timestamp': 1623915380.9335182}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 1.1735566599201281}, {'id': 38, 'position': {'x': 587019.1614112854, 'y': 4141547.73928833, 'z': -0.8302702903747559}, 'theta': 2.579760718450217, 'velocity': {'x': 0.0, 'y': 0.0, 'z': 2.384185791015625e-05}, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'polygonPointList': [{'x': 587019.2397971004, 'y': 4141547.394533828, 'z': -0.8302702903747559}, {'x': 587019.5061657876, 'y': 4141547.817674145, 'z': -0.8302702903747559}, {'x': 587019.0830254704, 'y': 4141548.0840428323, 'z': -0.8302702903747559}, {'x': 587018.8166567832, 'y': 4141547.660902515, 'z': -0.8302702903747559}], 'trackingTime': 2942.7199342250824, 'type': 3, 'timestamp': 1623915380.9335182, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'anchorPoint': {'x': 587019.1614112854, 'y': 4141547.73928833, 'z': -0.8302702903747559}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 10, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 38, 'position': {'x': 587019.1614112854, 'y': 4141547.73928833, 'z': -0.8302702903747559}, 'theta': 2.579760718450217, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'velocity': {'x': 0.0, 'y': 0.0, 'z': 2.384185791015625e-05}, 'type': 3, 'subType': 10, 'timestamp': 1623915380.9335182}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 45.219245389721}, {'id': 8817, 'position': {'x': 587056.2189874649, 'y': 4141625.3042678833, 'z': -0.47098907828330994}, 'theta': 4.453931026303479, 'velocity': {'x': -1.636887550354004, 'y': -6.201553821563721, 'z': -0.1832723617553711}, 'length': 3.9509117603302, 'width': 1.8471839427947998, 'height': 1.6631338596343994, 'polygonPointList': [{'x': 587057.6168095495, 'y': 4141626.9780485197, 'z': -0.47098907828330994}, {'x': 587055.8309793557, 'y': 4141627.450170469, 'z': -0.47098907828330994}, {'x': 587054.8211653803, 'y': 4141623.630487247, 'z': -0.47098907828330994}, {'x': 587056.6069955741, 'y': 4141623.1583652976, 'z': -0.47098907828330994}], 'trackingTime': 1.2299999725073576, 'type': 5, 'timestamp': 1623915380.9335182, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': -0.57220458984375, 'y': -0.11444091796875, 'z': -0.08940696716308594}, 'anchorPoint': {'x': 587056.2189874649, 'y': 4141625.3042678833, 'z': -0.47098907828330994}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 8817, 'position': {'x': 587056.2189874649, 'y': 4141625.3042678833, 'z': -0.47098907828330994}, 'theta': 4.453931026303479, 'length': 3.9509117603302, 'width': 1.8471839427947998, 'height': 1.6631338596343994, 'velocity': {'x': -1.636887550354004, 'y': -6.201553821563721, 'z': -0.1832723617553711}, 'type': 5, 'subType': 3, 'timestamp': 1623915380.9335182}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 36.17515081559017}, {'id': 82, 'position': {'x': 587019.7434768677, 'y': 4141548.4820747375, 'z': -0.7975622415542603}, 'theta': 1.8569495094298816, 'velocity': {'x': -0.0015258792554959655, 'y': -0.0009536742581985891, 'z': -0.0014066696166992188}, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'polygonPointList': [{'x': 587019.5742086619, 'y': 4141548.1716745645, 'z': -0.7975622415542603}, {'x': 587020.0538770407, 'y': 4141548.312806532, 'z': -0.7975622415542603}, {'x': 587019.9127450734, 'y': 4141548.7924749106, 'z': -0.7975622415542603}, {'x': 587019.4330766946, 'y': 4141548.6513429433, 'z': -0.7975622415542603}], 'trackingTime': 2943.2199342139065, 'type': 3, 'timestamp': 1623915380.9335182, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': -0.07629396766424179, 'y': -0.0381469689309597, 'z': -0.2980232238769531}, 'anchorPoint': {'x': 587019.7434768677, 'y': 4141548.4820747375, 'z': -0.7975622415542603}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 10, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 82, 'position': {'x': 587019.7434768677, 'y': 4141548.4820747375, 'z': -0.7975622415542603}, 'theta': 1.8569495094298816, 'length': 0.5, 'width': 0.5, 'height': 2.0, 'velocity': {'x': -0.0015258792554959655, 'y': -0.0009536742581985891, 'z': -0.0014066696166992188}, 'type': 3, 'subType': 10, 'timestamp': 1623915380.9335182}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 44.193377185614565}]}}


[
{'timestamp': 1624003956218707712, 
'Ego': {'size': {'length': 4.7, 'width': 2.06}, 
'pose': {'position': {'x': 587061.3109407425, 'y': 4141628.6425094604, 'z': -0.7402487993240356}, 'orientation': {'qx': 0.006273551844060421, 'qy': 0.012600654736161232, 'qz': -0.9915356040000916, 'qw': -0.12907052040100098}, 'linear_velocity': {'x': 3.2406067475676537e-05, 'y': -3.518688026815653e-05, 'z': -2.3416796466335654e-06}, 'linear_acceleration': {'x': -0.0, 'y': 0.0, 'z': 0.0}, 'angular_velocity': {'x': -0.0, 'y': 0.0, 'z': 0.0}, 'heading': -1.8295630439635833, 'linear_acceleration_vrf': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'angular_velocity_vrf': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'euler_angles': {'x': 0.02337066151111511, 'y': 6.267486456635538, 'z': 2.882520320417825}}}, 
'truth': {'minDistToEgo': 32.25458562869664, 'nearestGtObs': 85, 'obsList': 
[
{'id': 85, 'position': {'x': 587057.60064888, 'y': 4141592.1928424835, 'z': -1.1964449882507324}, 'theta': 1.1946897946972967, 'velocity': {'x': 4.03089714050293, 'y': 10.116101264953613, 'z': 0.15358924865722656}, 'length': 4.061402797698975, 'width': 1.8944153785705566, 'height': 1.4395885467529297, 'polygonPointList': [{'x': 587055.9737687832, 'y': 4141590.651994777, 'z': -1.1964449882507324}, {'x': 587057.7357678463, 'y': 4141589.9561723312, 'z': -1.1964449882507324}, {'x': 587059.2275289769, 'y': 4141593.73369019, 'z': -1.1964449882507324}, {'x': 587057.4655299137, 'y': 4141594.429512636, 'z': -1.1964449882507324}], 'trackingTime': 7.89999982342124, 'type': 5, 'timestamp': 1624003956.2187078, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': -1.506805419921875, 'y': 0.8106231689453125, 'z': 0.03814697265625}, 'anchorPoint': {'x': 587057.60064888, 'y': 4141592.1928424835, 'z': -1.1964449882507324}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 85, 'position': {'x': 587057.60064888, 'y': 4141592.1928424835, 'z': -1.1964449882507324}, 'theta': 1.1946897946972967, 'length': 4.061402797698975, 'width': 1.8944153785705566, 'height': 1.4395885467529297, 'velocity': {'x': 4.03089714050293, 'y': 10.116101264953613, 'z': 0.15358924865722656}, 'type': 5, 'subType': 3, 'timestamp': 1624003956.2187078}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 32.25458562869664}, 
{'id': 93, 'position': {'x': 587100.2845478058, 'y': 4141575.6948885918, 'z': -1.3464329242706299}, 'theta': 2.883536848998034, 'velocity': {'x': -16.591073989868164, 'y': 4.361870288848877, 'z': 0.03895759582519531}, 'length': 4.566516876220703, 'width': 2.0909385681152344, 'height': 1.3560072183609009, 'polygonPointList': [{'x': 587102.2253979034, 'y': 4141574.101346734, 'z': -1.3464329242706299}, {'x': 587102.7590078533, 'y': 4141576.1230500415, 'z': -1.3464329242706299}, {'x': 587098.3436977082, 'y': 4141577.2884304496, 'z': -1.3464329242706299}, {'x': 587097.8100877582, 'y': 4141575.266727142, 'z': -1.3464329242706299}], 'trackingTime': 0.05999999865889549, 'type': 5, 'timestamp': 1624003956.2187078, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': -4.024505615234375, 'y': -0.10251998901367188, 'z': 0.0095367431640625}, 'anchorPoint': {'x': 587100.2845478058, 'y': 4141575.6948885918, 'z': -1.3464329242706299}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 93, 'position': {'x': 587100.2845478058, 'y': 4141575.6948885918, 'z': -1.3464329242706299}, 'theta': 2.883536848998034, 'length': 4.566516876220703, 'width': 2.0909385681152344, 'height': 1.3560072183609009, 'velocity': {'x': -16.591073989868164, 'y': 4.361870288848877, 'z': 0.03895759582519531}, 'type': 5, 'subType': 3, 'timestamp': 1624003956.2187078}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 62.023187153192104}, 
{'id': 89, 'position': {'x': 587058.8593549728, 'y': 4141586.772409439, 'z': -1.2548772096633911}, 'theta': 2.8420344132078412, 'velocity': {'x': -3.2013895511627197, 'y': 0.9882931709289551, 'z': 0.004100799560546875}, 'length': 4.061402797698975, 'width': 1.8944153785705566, 'height': 1.4395885467529297, 'polygonPointList': [{'x': 587060.520103754, 'y': 4141585.268127582, 'z': -1.2548772096633911}, {'x': 587061.0791422385, 'y': 4141587.0781788207, 'z': -1.2548772096633911}, {'x': 587057.1986061917, 'y': 4141588.276691296, 'z': -1.2548772096633911}, {'x': 587056.6395677072, 'y': 4141586.4666400575, 'z': -1.2548772096633911}], 'trackingTime': 2.4999999441206455, 'type': 5, 'timestamp': 1624003956.2187078, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': -22.830963134765625, 'y': 8.602142333984375, 'z': 0.045299530029296875}, 'anchorPoint': {'x': 587058.8593549728, 'y': 4141586.772409439, 'z': -1.2548772096633911}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 89, 'position': {'x': 587058.8593549728, 'y': 4141586.772409439, 'z': -1.2548772096633911}, 'theta': 2.8420344132078412, 'length': 4.061402797698975, 'width': 1.8944153785705566, 'height': 1.4395885467529297, 'velocity': {'x': -3.2013895511627197, 'y': 0.9882931709289551, 'z': 0.004100799560546875}, 'type': 5, 'subType': 3, 'timestamp': 1624003956.2187078}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 38.411004148950724}, 
{'id': 92, 'position': {'x': 587078.05809021, 'y': 4141585.144648552, 'z': -1.210308313369751}, 'theta': 2.8844527100898176, 'velocity': {'x': -18.776704788208008, 'y': 4.934218406677246, 'z': 0.032019615173339844}, 'length': 4.705558776855469, 'width': 2.080930471420288, 'height': 1.771530270576477, 'polygonPointList': [{'x': 587080.068906815, 'y': 4141583.540044131, 'z': -1.210308313369751}, {'x': 587080.598119741, 'y': 4141585.5525563206, 'z': -1.210308313369751}, {'x': 587076.0472736049, 'y': 4141586.7492529727, 'z': -1.210308313369751}, {'x': 587075.518060679, 'y': 4141584.7367407833, 'z': -1.210308313369751}], 'trackingTime': 1.339999970048666, 'type': 5, 'timestamp': 1624003956.2187078, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': -0.476837158203125, 'y': -0.7343292236328125, 'z': 1.1682510375976562}, 'anchorPoint': {'x': 587078.05809021, 'y': 4141585.144648552, 'z': -1.210308313369751}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 92, 'position': {'x': 587078.05809021, 'y': 4141585.144648552, 'z': -1.210308313369751}, 'theta': 2.8844527100898176, 'length': 4.705558776855469, 'width': 2.080930471420288, 'height': 1.771530270576477, 'velocity': {'x': -18.776704788208008, 'y': 4.934218406677246, 'z': 0.032019615173339844}, 'type': 5, 'subType': 3, 'timestamp': 1624003956.2187078}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 43.31747447392053}]}}, 

{'timestamp': 1624003956318707712, 
'Ego': {'size': {'length': 4.7, 'width': 2.06}, 
'pose': {'position': {'x': 587061.3109407425, 'y': 4141628.6425094604, 'z': -0.7402487993240356}, 'orientation': {'qx': 0.006273551844060421, 'qy': 0.012600654736161232, 'qz': -0.9915356040000916, 'qw': -0.12907052040100098}, 'linear_velocity': {'x': 3.240164369344711e-05, 'y': -3.518257290124893e-05, 'z': -2.4012115318328142e-06}, 'linear_acceleration': {'x': -0.0, 'y': 0.0, 'z': 0.0}, 'angular_velocity': {'x': -0.0, 'y': 0.0, 'z': 0.0}, 'heading': -1.8295630439635833, 'linear_acceleration_vrf': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'angular_velocity_vrf': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'euler_angles': {'x': 0.02337066151111511, 'y': 6.267486456635538, 'z': 2.882520320417825}}}, 
'truth': {'minDistToEgo': 31.237481875842473, 'nearestGtObs': 85, 'obsList': 
[
{'id': 85, 'position': {'x': 587057.9945430756, 'y': 4141593.209115982, 'z': -1.181052803993225}, 'theta': 1.209741448429611, 'velocity': {'x': 3.8833634853363037, 'y': 10.191727638244629, 'z': 0.15370845794677734}, 'length': 4.061402797698975, 'width': 1.8944153785705566, 'height': 1.4395885467529297, 'polygonPointList': [{'x': 587056.3910386844, 'y': 4141591.643956473, 'z': -1.181052803993225}, {'x': 587058.1633110672, 'y': 4141590.974732849, 'z': -1.181052803993225}, {'x': 587059.5980474667, 'y': 4141594.774275491, 'z': -1.181052803993225}, {'x': 587057.825775084, 'y': 4141595.4434991153, 'z': -1.181052803993225}], 'trackingTime': 7.999999821186066, 'type': 5, 'timestamp': 1624003956.3187077, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': -1.4495849609375, 'y': 0.72479248046875, 'z': -0.015497207641601562}, 'anchorPoint': {'x': 587057.9945430756, 'y': 4141593.209115982, 'z': -1.181052803993225}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 85, 'position': {'x': 587057.9945430756, 'y': 4141593.209115982, 'z': -1.181052803993225}, 'theta': 1.209741448429611, 'length': 4.061402797698975, 'width': 1.8944153785705566, 'height': 1.4395885467529297, 'velocity': {'x': 3.8833634853363037, 'y': 10.191727638244629, 'z': 0.15370845794677734}, 'type': 5, 'subType': 3, 'timestamp': 1624003956.3187077}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 31.237481875842473}, 
{'id': 93, 'position': {'x': 587098.6045455933, 'y': 4141576.137986481, 'z': -1.3420014381408691}, 'theta': 2.8846575071760583, 'velocity': {'x': -16.908647537231445, 'y': 4.466160774230957, 'z': 0.04849433898925781}, 'length': 4.566516876220703, 'width': 2.0909385681152344, 'height': 1.3560072183609009, 'polygonPointList': [{'x': 587100.5471804475, 'y': 4141574.546620637, 'z': -1.3420014381408691}, {'x': 587101.0785243812, 'y': 4141576.5689207963, 'z': -1.3420014381408691}, {'x': 587096.661910739, 'y': 4141577.729352325, 'z': -1.3420014381408691}, {'x': 587096.1305668054, 'y': 4141575.707052166, 'z': -1.3420014381408691}], 'trackingTime': 0.1599999964237213, 'type': 5, 'timestamp': 1624003956.3187077, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': -2.47955322265625, 'y': 2.276897430419922, 'z': 0.095367431640625}, 'anchorPoint': {'x': 587098.6045455933, 'y': 4141576.137986481, 'z': -1.3420014381408691}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 93, 'position': {'x': 587098.6045455933, 'y': 4141576.137986481, 'z': -1.3420014381408691}, 'theta': 2.8846575071760583, 'length': 4.566516876220703, 'width': 2.0909385681152344, 'height': 1.3560072183609009, 'velocity': {'x': -16.908647537231445, 'y': 4.466160774230957, 'z': 0.04849433898925781}, 'type': 5, 'subType': 3, 'timestamp': 1624003956.3187077}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 60.701016820116244}, 
{'id': 89, 'position': {'x': 587058.3881540298, 'y': 4141586.9166145325, 'z': -1.2541425228118896}, 'theta': 2.841695925435914, 'velocity': {'x': -5.51328706741333, 'y': 1.7042168378829956, 'z': 0.0091552734375}, 'length': 4.061402797698975, 'width': 1.8944153785705566, 'height': 1.4395885467529297, 'polygonPointList': [{'x': 587060.0483936929, 'y': 4141585.411770722, 'z': -1.2541425228118896}, {'x': 587060.60804469, 'y': 4141587.221632713, 'z': -1.2541425228118896}, {'x': 587056.7279143668, 'y': 4141588.421458343, 'z': -1.2541425228118896}, {'x': 587056.1682633697, 'y': 4141586.611596352, 'z': -1.2541425228118896}], 'trackingTime': 2.5999999418854713, 'type': 5, 'timestamp': 1624003956.3187077, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': -22.020339965820312, 'y': 9.9945068359375, 'z': 0.050067901611328125}, 'anchorPoint': {'x': 587058.3881540298, 'y': 4141586.9166145325, 'z': -1.2541425228118896}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 89, 'position': {'x': 587058.3881540298, 'y': 4141586.9166145325, 'z': -1.2541425228118896}, 'theta': 2.841695925435914, 'length': 4.061402797698975, 'width': 1.8944153785705566, 'height': 1.4395885467529297, 'velocity': {'x': -5.51328706741333, 'y': 1.7042168378829956, 'z': 0.0091552734375}, 'type': 5, 'subType': 3, 'timestamp': 1624003956.3187077}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 38.278093426958016}, 
{'id': 92, 'position': {'x': 587076.181602478, 'y': 4141585.6391305923, 'z': -1.2026772499084473}, 'theta': 2.8842830667296937, 'velocity': {'x': -18.811323165893555, 'y': 4.9478559494018555, 'z': 0.12853145599365234}, 'length': 4.705558776855469, 'width': 2.080930471420288, 'height': 1.771530270576477, 'polygonPointList': [{'x': 587078.1921467582, 'y': 4141584.03418486, 'z': -1.2026772499084473}, {'x': 587078.7217012714, 'y': 4141586.0466072494, 'z': -1.2026772499084473}, {'x': 587074.1710581979, 'y': 4141587.2440763246, 'z': -1.2026772499084473}, {'x': 587073.6415036847, 'y': 4141585.2316539353, 'z': -1.2026772499084473}], 'trackingTime': 1.4399999678134918, 'type': 5, 'timestamp': 1624003956.3187077, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': -0.0762939453125, 'y': 1.0776519775390625, 'z': 1.2731552124023438}, 'anchorPoint': {'x': 587076.181602478, 'y': 4141585.6391305923, 'z': -1.2026772499084473}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 92, 'position': {'x': 587076.181602478, 'y': 4141585.6391305923, 'z': -1.2026772499084473}, 'theta': 2.8842830667296937, 'length': 4.705558776855469, 'width': 2.080930471420288, 'height': 1.771530270576477, 'velocity': {'x': -18.811323165893555, 'y': 4.9478559494018555, 'z': 0.12853145599365234}, 'type': 5, 'subType': 3, 'timestamp': 1624003956.3187077}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 42.29075117600384}]}}, 

{'timestamp': 1624003956418707712, 
'Ego': {'size': {'length': 4.7, 'width': 2.06}, 
'pose': {'position': {'x': 587061.3109407425, 'y': 4141628.6425094604, 'z': -0.7402487993240356}, 'orientation': {'qx': 0.006273551844060421, 'qy': 0.012600654736161232, 'qz': -0.9915356040000916, 'qw': -0.12907052040100098}, 'linear_velocity': {'x': 3.2396987080574036e-05, 'y': -3.517814911901951e-05, 'z': -2.460743417032063e-06}, 'linear_acceleration': {'x': -0.0, 'y': 0.0, 'z': 0.0}, 'angular_velocity': {'x': -0.0, 'y': 0.0, 'z': 0.0}, 'heading': -1.8295630439635833, 'linear_acceleration_vrf': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'angular_velocity_vrf': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'euler_angles': {'x': 0.02337066151111511, 'y': 6.267486456635538, 'z': 2.882520320417825}}}, 
'truth': {'minDistToEgo': 30.21764481163889, 'nearestGtObs': 85, 'obsList': 
[{'id': 85, 'position': {'x': 587058.3737802505, 'y': 4141594.232498169, 'z': -1.1657720804214478}, 'theta': 1.2242865689265159, 'velocity': {'x': 3.738309621810913, 'y': 10.258866310119629, 'z': 0.15239715576171875}, 'length': 4.061402797698975, 'width': 1.8944153785705566, 'height': 1.4395885467529297, 'polygonPointList': [{'x': 587056.7932101226, 'y': 4141592.644181852, 'z': -1.1657720804214478}, {'x': 587058.5750286459, 'y': 4141592.0008060453, 'z': -1.1657720804214478}, {'x': 587059.9543503785, 'y': 4141595.8208144857, 'z': -1.1657720804214478}, {'x': 587058.1725318552, 'y': 4141596.4641902926, 'z': -1.1657720804214478}], 'trackingTime': 8.099999818950891, 'type': 5, 'timestamp': 1624003956.4187076, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': -1.4400482177734375, 'y': 0.667572021484375, 'z': -0.011920928955078125}, 'anchorPoint': {'x': 587058.3737802505, 'y': 4141594.232498169, 'z': -1.1657720804214478}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 85, 'position': {'x': 587058.3737802505, 'y': 4141594.232498169, 'z': -1.1657720804214478}, 'theta': 1.2242865689265159, 'length': 4.061402797698975, 'width': 1.8944153785705566, 'height': 1.4395885467529297, 'velocity': {'x': 3.738309621810913, 'y': 10.258866310119629, 'z': 0.15239715576171875}, 'type': 5, 'subType': 3, 'timestamp': 1624003956.4187076}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 30.21764481163889}, 
{'id': 93, 'position': {'x': 587096.8969421387, 'y': 4141576.587843418, 'z': -1.3368782997131348}, 'theta': 2.8828183281414965, 'velocity': {'x': -17.1644229888916, 'y': 4.505156993865967, 'z': 0.05049705505371094}, 'length': 4.566516876220703, 'width': 2.0909385681152344, 'height': 1.3560072183609009, 'polygonPointList': [{'x': 587098.8366467288, 'y': 4141574.992907192, 'z': -1.3368782997131348}, {'x': 587099.371709362, 'y': 4141577.0142266406, 'z': -1.3368782997131348}, {'x': 587094.9572375485, 'y': 4141578.182779644, 'z': -1.3368782997131348}, {'x': 587094.4221749153, 'y': 4141576.1614601957, 'z': -1.3368782997131348}], 'trackingTime': 0.25999999418854713, 'type': 5, 'timestamp': 1624003956.4187076, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': -2.841949462890625, 'y': -1.8504142761230469, 'z': -0.2980232238769531}, 'anchorPoint': {'x': 587096.8969421387, 'y': 4141576.587843418, 'z': -1.3368782997131348}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 93, 'position': {'x': 587096.8969421387, 'y': 4141576.587843418, 'z': -1.3368782997131348}, 'theta': 2.8828183281414965, 'length': 4.566516876220703, 'width': 2.0909385681152344, 'height': 1.3560072183609009, 'velocity': {'x': -17.1644229888916, 'y': 4.505156993865967, 'z': 0.05049705505371094}, 'type': 5, 'subType': 3, 'timestamp': 1624003956.4187076}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 59.37731858090436}, 
{'id': 89, 'position': {'x': 587057.6895780563, 'y': 4141587.130384445, 'z': -1.2528719902038574}, 'theta': 2.841005101454499, 'velocity': {'x': -7.755756855010986, 'y': 2.4024975299835205, 'z': 0.014579296112060547}, 'length': 4.061402797698975, 'width': 1.8944153785705566, 'height': 1.4395885467529297, 'polygonPointList': [{'x': 587059.3487777225, 'y': 4141585.6243940867, 'z': -1.2528719902038574}, {'x': 587059.9096788685, 'y': 4141587.433869002, 'z': -1.2528719902038574}, {'x': 587056.0303783902, 'y': 4141588.6363748037, 'z': -1.2528719902038574}, {'x': 587055.4694772442, 'y': 4141586.8268998885, 'z': -1.2528719902038574}], 'trackingTime': 2.699999939650297, 'type': 5, 'timestamp': 1624003956.4187076, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': -20.44677734375, 'y': 11.835098266601562, 'z': 0.05245208740234375}, 'anchorPoint': {'x': 587057.6895780563, 'y': 4141587.130384445, 'z': -1.2528719902038574}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 89, 'position': {'x': 587057.6895780563, 'y': 4141587.130384445, 'z': -1.2528719902038574}, 'theta': 2.841005101454499, 'length': 4.061402797698975, 'width': 1.8944153785705566, 'height': 1.4395885467529297, 'velocity': {'x': -7.755756855010986, 'y': 2.4024975299835205, 'z': 0.014579296112060547}, 'type': 5, 'subType': 3, 'timestamp': 1624003956.4187076}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 38.09160449113671}, 
{'id': 92, 'position': {'x': 587074.3056821823, 'y': 4141586.132214546, 'z': -1.1845736503601074}, 'theta': 2.8838734725572124, 'velocity': {'x': -18.810083389282227, 'y': 4.970458030700684, 'z': 0.2746105194091797}, 'length': 4.705558776855469, 'width': 2.080930471420288, 'height': 1.771530270576477, 'polygonPointList': [{'x': 587076.3155690414, 'y': 4141584.526445681, 'z': -1.1845736503601074}, {'x': 587076.8459475687, 'y': 4141586.5386510123, 'z': -1.1845736503601074}, {'x': 587072.2957953232, 'y': 4141587.737983411, 'z': -1.1845736503601074}, {'x': 587071.765416796, 'y': 4141585.72577808, 'z': -1.1845736503601074}], 'trackingTime': 1.5399999655783176, 'type': 5, 'timestamp': 1624003956.4187076, 'pointCloudList': [], 'dropsList': [], 'acceleration': {'x': 0.6151199340820312, 'y': 1.8215179443359375, 'z': 3.223419189453125}, 'anchorPoint': {'x': 587074.3056821823, 'y': 4141586.132214546, 'z': -1.1845736503601074}, 'bbox2d': {'xmin': 0.0, 'ymin': 0.0, 'xmax': 0.0, 'ymax': 0.0}, 'subType': 3, 'measurementsList': [{'sensorId': 'velodyne128', 'id': 92, 'position': {'x': 587074.3056821823, 'y': 4141586.132214546, 'z': -1.1845736503601074}, 'theta': 2.8838734725572124, 'length': 4.705558776855469, 'width': 2.080930471420288, 'height': 1.771530270576477, 'velocity': {'x': -18.810083389282227, 'y': 4.970458030700684, 'z': 0.2746105194091797}, 'type': 5, 'subType': 3, 'timestamp': 1624003956.4187076}], 'heightAboveGround': nan, 'positionCovarianceList': [], 'velocityCovarianceList': [], 'accelerationCovarianceList': [], 'distToEgo': 41.32356110361513}]}}]










Spawn(position=Vector(-50.3399963378906, -1.03600025177002, -9.03000640869141), rotation=Vector(0, 104.823379516602, 0), destinations=[Transform(position=Vector(388.676696777344, -7.97211790084839, 90.3788909912109), rotation=Vector(0.173002451658249, 16.0349941253662, 357.940002441406)), Transform(position=Vector(369.055389404297, -7.81147289276123, -117.672096252441), rotation=Vector(1.0330046415329, 105.672996520996, 359.923004150391))])

Transform(position=Vector(-50.3399963378906, 0, -9.03000640869141), rotation=Vector(0, 0, 0))

GpsData(latitude=37.417360169898, longitude=-122.016132757902, northing=4141627.33999634, easting=587060.969993591, altitude=-1.03600025177002, orientation=0)






[Spawn(position=Vector(-50.3399963378906, -1.03600025177002, -9.03000640869141), rotation=Vector(0, 104.823379516602, 0), 
  destinations=[Transform(position=Vector(388.676696777344, -7.97211790084839, 90.3788909912109), rotation=Vector(0.173002451658249, 16.0349941253662, 357.940002441406)), Transform(position=Vector(369.055389404297, -7.81147289276123, -117.672096252441), rotation=Vector(1.0330046415329, 105.672996520996, 359.923004150391))]), 
Spawn(position=Vector(386.800048828125, -7.73000001907349, 106.700073242188), rotation=Vector(0, 191.806182861328, 0), 
  destinations=[Transform(position=Vector(369.055389404297, -7.81147289276123, -117.672096252441), rotation=Vector(1.0330046415329, 105.672996520996, 359.923004150391)), Transform(position=Vector(-40.4599990844727, -1.0900000333786, -5.19000005722046), rotation=Vector(1.0330046415329, 285, 359.923004150391))])]
