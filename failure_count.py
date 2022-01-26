import os
from natsort import natsorted
import glob

def fitness_counter(directory, scenario):
    log_file = directory + scenario + 'test.log'
    read_log = open(log_file, 'r')
    Lines = read_log.readlines()
    failure_number = 0
    for i in range(len(Lines)):
        line = Lines[i]
        if 'Fitness Value' in line:
            fitness = float(line.split(sep=":")[-1])
            if fitness < 0:
                failure_number += 1
    return failure_number


def first_failure(directory, scenario):
    original_json_files = []
    for file in os.listdir(directory):
        if file.endswith(".json"):
            original_json_files.append(file)
    original_json_files = natsorted(original_json_files)

    log_file = directory + scenario + 'test.log'
    read_log = open(log_file, 'r')
    Lines = read_log.readlines()
    test_number = 0
    index = 0
    for i in range(len(Lines)):
        line = Lines[i]
        if 'Fitness Value' in line:
            fitness = float(line.split(sep=":")[-1])
            if fitness <=-0.5:
                original_file = original_json_files[test_number]
                index = int(original_file.split(sep="-")[0])
                break
            test_number += 1
    return index


if __name__ == "__main__":
    directory0 = '/run/user/1001/gvfs/smb-share:server=synology_nas.local,share=zhouyuan/'
    # directories = ['ga_1/', 'ga_2/', 'ga_3/', 'ga_4/', 'ga_5/', 'random_1/', 'random_2/', 'random_3/', 'random_4/', 'random_5/']
    directories = ['random_1/']
    scenarios = ['lanechange1/']
    failure_number_list = []
    for scenario in scenarios:
        for directory in directories:
            current_directory = directory0 + directory + scenario + 'results/'
            failure_number = fitness_counter(current_directory, scenario)
            failure_number_list.append(failure_number)
    print(failure_number_list)

    first_failure_list = []
    for scenario in scenarios:
        for directory in directories:
            current_directory = directory0 + directory + scenario + 'results/'
            index = first_failure(current_directory, scenario)
            first_failure_list.append(index)

    print(first_failure_list)


