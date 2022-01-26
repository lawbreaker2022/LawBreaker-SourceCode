import os
from natsort import natsorted
import shutil


def new_select_bug_test_cases_all(direct, folder):
    file_directory = direct + folder + '/new_results/'
    files = os.listdir(file_directory)
    files = natsorted(files)
    result_folder = direct + folder + '/infeasible/'
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)
    log_file = direct + folder + '/test.log'
    read_log = open(log_file, 'r')
    Lines = read_log.readlines()
    for i in range(len(Lines)):
        line = Lines[i]
        if 'Running Predefined Test Case' in line:
            index = int(line.split(sep=':')[-1]) + 1
            line1 = Lines[i+1]
            if i+2 < len(Lines):
                line2 = Lines[i+2]
            if "Fitness Value" in line1:
                fitness = float(line1.split(sep=":")[-1])
                if -20 <= fitness < -3.5:
                    print(index)
                    for file in files:
                        file_index = int(file.split(sep='-')[0])
                        if file_index == index:
                            shutil.copyfile(file_directory + file, result_folder + file)
                            if os.path.exists(file_directory + file):
                                os.remove(file_directory + file)
                        elif index < file_index:
                            break
            elif "Fitness Value" in line2:
                fitness = float(line2.split(sep=":")[-1])
                if -20 <= fitness < -3.5:
                    print(index)
                    for file in files:
                        file_index = int(file.split(sep='-')[0])
                        if file_index == index:
                            shutil.copyfile(file_directory + file, result_folder + file)
                            if os.path.exists(file_directory + file):
                                os.remove(file_directory + file)
                        elif index < file_index:
                            break




if __name__ == "__main__":



    # test_number = ['ga_1/', 'ga_2/', 'ga_3/', 'ga_4/']
    # test_number = ['random_1/', 'random_2/', 'random_3/', 'random_4/', 'random_5/']
    # 'intersection1', 'intersection2', 'intersection3', 'intersection4', 'intersection5',
    # 'lanechange1', 'lanechange3', 'overetaking1'
    # test_number = ['ga_1/', 'ga_2/', 'ga_3/', 'ga_4/', 'ga_5/',  'random_2/', 'random_3/', 'random_4/', 'random_5/']
    test_number = ['ga_4/', 'ga_5/']
    test_scenarios = ['lanechange3']
    for number in test_number:
        for test_scenario in test_scenarios:
            print('Current round: {}, scenario: {}'.format(number, test_scenario))
            direct = '/run/user/1001/gvfs/smb-share:server=synology_nas.local,share=zhouyuan/' + number + test_scenario + '/results/'
            new_select_bug_test_cases_all(direct, test_scenario)






