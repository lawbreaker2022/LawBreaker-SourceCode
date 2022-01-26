import os
from natsort import natsorted
import shutil


def new_select_bug_test_cases_all(direct, folder):
    if 'intersection' in folder:
        threshold = 0
    else:
        threshold = 0
    # threshold = -50
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
            # if threshold < fitness < 0:
                print(case_number)
                # copy recording
                for file in recording_files:
                    file_index = int(file.split(sep='-')[0])
                    if case_number == file_index:
                        shutil.copyfile(recording_folder + file, result_folder + file)
                    elif case_number < file_index:
                        break
                # copy data
                for file in data_files:
                    file_index = int(file.split(sep='-')[0])
                    if case_number == file_index:
                        shutil.copyfile(data_folder + file, result_folder + file)
                        break



if __name__ == "__main__":



    # test_number = ['ga_1/', 'ga_2/', 'ga_3/', 'ga_4/']
    # test_number = ['random_1/', 'random_2/', 'random_3/', 'random_4/', 'random_5/']
    # 'intersection1', 'intersection2', 'intersection3', 'intersection4', 'intersection5',
    # 'lanechange1', 'lanechange3', 'overetaking1'
    # test_number = ['ga_1/', 'ga_2/', 'ga_3/', 'ga_4/', 'ga_5/',  'random_2/', 'random_3/', 'random_4/', 'random_5/']
    test_number = ['ga_3/']
    test_scenarios = ['intersection1']
    for number in test_number:
        for test_scenario in test_scenarios:
            print('Current round: {}, scenario: {}'.format(number, test_scenario))
            direct = '/run/user/1001/gvfs/smb-share:server=synology_nas.local,share=zhouyuan/' + number + test_scenario + '/results/'
            new_select_bug_test_cases_all(direct, test_scenario)






