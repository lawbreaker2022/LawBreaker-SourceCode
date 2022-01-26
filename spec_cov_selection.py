import os
from natsort import natsorted
import shutil
import re

def select_bug_test_cases(direct):
    sub_folders = os.listdir(direct)
    sub_folders = natsorted(sub_folders)
    # sub_folders = ['intersection1', 'intersection2', 'intersection3', 'intersection4', 'intersection5', 'lanechange1'] #, 'lanechange3', 'overtaking1']
    # sub_folders = ['intersection1', 'intersection2', 'intersection3', 'intersection4', 'intersection5']
    for folder in sub_folders:
        print("Current Folder: {}".format(folder))
        if 'intersection' in folder:
            threshold = 0
        else:
            threshold = 0
        recording_folder = direct + folder + '/recording/'
        recording_files = os.listdir(recording_folder)
        recording_files = natsorted(recording_files)
        data_folder = direct + folder + '/data/'
        data_files = os.listdir(data_folder)
        data_files = natsorted(data_files)
        result_folder_L = direct + folder + '/results_L/'
        result_folder_M = direct + folder + '/results_M/'
        result_folder_MS = direct + folder + '/results_MS/'
        result_folder_S = direct + folder + '/results_S/'
        if not os.path.exists(result_folder_L):
            os.makedirs(result_folder_L)
        if not os.path.exists(result_folder_M):
            os.makedirs(result_folder_M)
        if not os.path.exists(result_folder_MS):
            os.makedirs(result_folder_MS)
        if not os.path.exists(result_folder_S):
            os.makedirs(result_folder_S)
        threshold_L = -15
        threshold_M = -5
        threshold_S = -1
        log_file = direct + folder + '/test.log'
        read_log = open(log_file, 'r')
        Lines = read_log.readlines()
        case_number = 1
        for i in range(len(Lines)):
            line = Lines[i]
            if 'Running Generation' in line:
                case_number += 1
                next_line = Lines[i + 2]
                if "Fitness Value" in next_line:
                    fitness = float(next_line.split(sep=":")[-1])
                    if fitness <= threshold_L:
                        # copy recording
                        for file in recording_files:
                            file_index = int(file.split(sep='-')[0])
                            if case_number == file_index:
                                shutil.copy(recording_folder + file, result_folder_L)
                            elif case_number < file_index:
                                break
                        # copy data
                        for file in data_files:
                            file_index = int(file.split(sep='-')[0])
                            if case_number == file_index:
                                shutil.copy(data_folder + file, result_folder_L)
                                break
                    elif threshold_L < fitness <= threshold_M:
                        # copy recording
                        for file in recording_files:
                            file_index = int(file.split(sep='-')[0])
                            if case_number == file_index:
                                shutil.copy(recording_folder + file, result_folder_M)
                            elif case_number < file_index:
                                break
                        # copy data
                        for file in data_files:
                            file_index = int(file.split(sep='-')[0])
                            if case_number == file_index:
                                shutil.copy(data_folder + file, result_folder_M)
                                break
                    elif threshold_M < fitness <= threshold_S:
                        # copy recording
                        for file in recording_files:
                            file_index = int(file.split(sep='-')[0])
                            if case_number == file_index:
                                shutil.copy(recording_folder + file, result_folder_MS)
                            elif case_number < file_index:
                                break
                        # copy data
                        for file in data_files:
                            file_index = int(file.split(sep='-')[0])
                            if case_number == file_index:
                                shutil.copy(data_folder + file, result_folder_MS)
                                break
                    elif threshold_S < fitness <= -threshold:
                        # copy recording
                        for file in recording_files:
                            file_index = int(file.split(sep='-')[0])
                            if case_number == file_index:
                                shutil.copy(recording_folder + file, result_folder_S)
                            elif case_number < file_index:
                                break
                        # copy data
                        for file in data_files:
                            file_index = int(file.split(sep='-')[0])
                            if case_number == file_index:
                                shutil.copy(data_folder + file, result_folder_S)
                                break
                else:
                    print(next_line)



def select_bug_test_cases_all(direct, scenarios):

    for folder in scenarios:
        print("Current Folder: {}".format(folder))
        if 'intersection' in folder:
            threshold = 0
        else:
            threshold = 0
        recording_folder = direct + folder + '/recording/'
        recording_files = os.listdir(recording_folder)
        recording_files = natsorted(recording_files)
        data_folder = direct + folder + '/data/'
        data_files = os.listdir(data_folder)
        data_files = natsorted(data_files)
        result_folder = direct + folder + '/results/'
        if not os.path.exists(result_folder):
            os.makedirs(result_folder)
        log_file = direct + folder + '/test.log'
        read_log = open(log_file, 'r')
        Lines = read_log.readlines()
        case_number = 1
        for i in range(len(Lines)):
            line = Lines[i]
            if 'Running Generation' in line:
                case_number += 1
                next_line = Lines[i + 2]
                if "Fitness Value" in next_line:
                    fitness = float(next_line.split(sep=":")[-1])
                    if fitness <= threshold:
                        # copy recording
                        for file in recording_files:
                            file_index = int(file.split(sep='-')[0])
                            if case_number == file_index:
                                command = 'cp ' + recording_folder + file + ' ' + result_folder
                                os.system(command)
                                # shutil.copyfile(recording_folder + file, result_folder + file)
                            elif case_number < file_index:
                                break
                        # copy data
                        for file in data_files:
                            file_index = int(file.split(sep='-')[0])
                            if case_number == file_index:
                                command = 'cp ' + data_folder + file + ' ' + result_folder
                                os.system(command)
                                # shutil.copyfile(data_folder + file, result_folder + file)
                                break
                else:
                    print(next_line)


def coverage_bug_test_cases_all(direct, scenarios):
    for folder in scenarios:
        print("Current Folder: {}".format(folder))
        if 'intersection' in folder:
            threshold = 0
        else:
            threshold = 0
        recording_folder = direct + folder + '/recording/'
        recording_files = os.listdir(recording_folder)
        recording_files = natsorted(recording_files)
        data_folder = direct + folder + '/data/'
        data_files = os.listdir(data_folder)
        data_files = natsorted(data_files)
        result_folder = direct + folder + '/results/'
        if not os.path.exists(result_folder):
            os.makedirs(result_folder)
        log_file = direct + folder + '/specification_coverage.log'
        read_log = open(log_file, 'r')
        Lines = read_log.readlines()
        case_number = 0
        for i in range(len(Lines)):
            line = Lines[i]
            if "Fitness Value" in line:
                case_number += 1
                fitness = float(line.split(sep=":")[-1])
                if fitness <= threshold:
                    # copy recording
                    for file in recording_files:
                        file_index = int(file.split(sep='-')[0])
                        if case_number == file_index:
                            command = 'cp ' + recording_folder + file + ' ' + result_folder
                            os.system(command)
                            # shutil.copyfile(recording_folder + file, result_folder + file)
                        elif case_number < file_index:
                            break
                    # copy data
                    for file in data_files:
                        file_index = int(file.split(sep='-')[0])
                        if case_number == file_index:
                            command = 'cp ' + data_folder + file + ' ' + result_folder
                            os.system(command)
                            # shutil.copyfile(data_folder + file, result_folder + file)
                            break



def new_select_bug_test_cases_all(direct):
    sub_folders = ['lanechange3']
    for folder in sub_folders:
        print("Current Folder: {}".format(folder))
        if 'intersection' in folder:
            threshold = 0
        else:
            threshold = 0
        recording_folder = direct + folder + '/recording/'
        recording_files = os.listdir(recording_folder)
        recording_files = natsorted(recording_files)
        data_folder = direct + folder + '/data/'
        data_files = os.listdir(data_folder)
        data_files = natsorted(data_files)
        result_folder = direct + folder + '/new_results/'
        if not os.path.exists(result_folder):
            os.makedirs(result_folder)
        log_file = direct + folder + '/test.log'
        read_log = open(log_file, 'r')
        Lines = read_log.readlines()
        case_number = 0
        for i in range(len(Lines)):
            line = Lines[i]
            if "Fitness Value" in line:
                case_number += 1
                fitness = float(line.split(sep=":")[-1])
                if fitness <= threshold:
                    print(case_number)
                    # copy recording
                    for file in recording_files:
                        file_index = int(file.split(sep='-')[0])
                        if case_number == file_index:
                            command = 'cp ' + recording_folder + file + ' ' + result_folder
                            os.system(command)
                            # shutil.copyfile(recording_folder + file, result_folder + file)
                        elif case_number < file_index:
                            break
                    # copy data
                    for file in data_files:
                        file_index = int(file.split(sep='-')[0])
                        if case_number == file_index:
                            command = 'cp ' + data_folder + file + ' ' + result_folder
                            os.system(command)
                            # shutil.copyfile(data_folder + file, result_folder + file)
                            break


def fitness_counter(direct0, directs):

    sub_folders = ['intersection1', 'intersection2', 'intersection3', 'intersection4', 'intersection5', 'lanechange1'] #, 'lanechange3', 'overtaking1']
    sub_folders = ['intersection5']
    for direct in directs:
        directory = direct0 + direct
        for folder in sub_folders:
            print("Current Folder: {}".format(folder))
            log_file = directory + folder + '/test.log'
            read_log = open(log_file, 'r')
            Lines = read_log.readlines()
            case_number = 1
            failure_number = 0
            for i in range(len(Lines)):
                line = Lines[i]
                if 'Running Generation' in line:
                    case_number += 1
                    next_line = Lines[i + 2]
                    if "Fitness Value" in next_line:
                        fitness = float(next_line.split(sep=":")[-1])
                        if fitness < 0:
                            failure_number += 1
            print("test round: {}, test scenario: {}, failure number: {}".format(direct, folder, failure_number))


def get_file_size(file):
    file_size = os.path.getsize(file)/1e6
    return file_size



if __name__ == "__main__":

    # sub_folders = os.listdir(direct)
    # sub_folders = natsorted(sub_folders)
    directory = '/run/user/1001/gvfs/smb-share:server=synology_nas.local,share=zhouyuan/coverage_4/'
    scenarios = ['intersection1', 'intersection2', 'intersection3', 'intersection4', 'intersection5', 'lanechange1', 'lanechange3', 'overtaking1']
    coverage_bug_test_cases_all(directory, scenarios)

    # file = '/media/zhouyuan/MyBookPro/zhouyuan/ga_1/intersection5/results/222-test--2021-7-2-2.6.50.rec.00000'
    # file_size = get_file_size(file)
    # print(file_size)
    #
    # direct0 = '/media/zhouyuan/MyBookPro/zhouyuan/'
    # direct = ['ga_1/', 'ga_2/', 'ga_3/', 'ga_4/', 'ga_5/', 'random_1/', 'random_2/', 'random_3/', 'random_4/', 'random_5/']
    # fitness_counter(direct0, direct)


    # direct = '/run/user/1001/gvfs/smb-share:server=synology_nas.local,share=zhouyuan/ga_1/lanechange3/results/'
    # new_select_bug_test_cases_all(direct)

    # counter, line_set = fitness_counter(direct)
    # print(counter)
    # print(line_set)




