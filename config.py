import  json

file_name = "config.json"
with open(file_name) as f:
    agent_list = json.load(f)
    npc_list = agent_list['vehicle']
    pedestrian_list = agent_list['pedestrian']
    map_list = agent_list['map']
    ego_list = agent_list['ego']
    weather_list = agent_list['weather']

def get_npc_list():
    return npc_list

def get_pedestrian_list():
    return pedestrian_list

def get_map_list():
    return map_list

def get_ego_list():
    return ego_list

def get_weather_list():
    return weather_list
