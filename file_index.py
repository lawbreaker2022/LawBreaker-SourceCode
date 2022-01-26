import os
from natsort import natsorted


def index_result(direct):
    sub_folders = os.listdir(direct)
    sub_folders = natsorted(sub_folders)
    sub_folders = ['lanechange3']
    for folder in sub_folders:
        sub_folder = direct + folder + '/results/'
        files = os.listdir(sub_folder)
        files = natsorted(files)
        json_index = 0
        record_index = 0
        current_file = ""
        for file in files:
            old_file = sub_folder + file
            if 'json' in file:
                json_index += 1
                new_name = sub_folder + str(json_index) + '-' + file
                os.rename(old_file, new_name)
            else:
                file_same = file[0:-5]
                if file_same != current_file:
                    current_file = file_same
                    record_index += 1
                new_name = sub_folder + str(record_index) + '-' + file
                os.rename(old_file, new_name)

def index_recording(directory, scenario):
    # sub_folders = os.listdir(direct)
    # sub_folders = natsorted(sub_folders)
    # sub_folders = ['lanechange3', 'overtaking1']
    # # sub_folders = ['intersection1', 'intersection2', 'intersection3', 'intersection4', 'intersection5', 'lanechange1',
    # #                'lanechange3', 'lanechange2']
    # for folder in sub_folders:
    sub_folder = directory + scenario + '/recording/'
    files = os.listdir(sub_folder)
    files = natsorted(files)
    record_index = 0
    current_file = ""
    for file in files:
        old_file = sub_folder + file
        file_same = file[0:-5]
        if file_same != current_file:
            current_file = file_same
            record_index += 1
        new_name = sub_folder + str(record_index) + '-' + file
        os.rename(old_file, new_name)


def index_data(directory, scenario):
    # sub_folders = os.listdir(direct)
    # sub_folders = natsorted(sub_folders)
    # sub_folders = ['lanechange3', 'overtaking1']
    # for folder in sub_folders:
    sub_folder = directory + scenario + '/data/'
    files = os.listdir(sub_folder)
    files = natsorted(files)
    for i in range(len(files)):
        old_file = sub_folder + files[i]
        new_name = sub_folder + str(i+1) + '-' + files[i]
        os.rename(old_file, new_name)


def re_index_data(directory, scenario):
    # sub_folders = os.listdir(direct)
    # sub_folders = natsorted(sub_folders)
    # sub_folders = ['overtaking1']
    # for folder in sub_folders:
    sub_folder = directory + scenario + '/recording/'
    files = os.listdir(sub_folder)
    files = natsorted(files)
    for i in range(len(files)):
        old_file = sub_folder + files[i]
        split_list = files[i].split(sep='-')
        n = len(split_list[0])
        new_name = files[i][n+1:]
        new_name = sub_folder + new_name
        os.rename(old_file, new_name)

def re_index_customized(direct):
    sub_folders = os.listdir(direct)
    sub_folders = sorted(sub_folders)
    sub_folders = ['lanechange1']
    for folder in sub_folders:
        sub_folder = direct + folder + '/results/'
        files = os.listdir(sub_folder)
        files = sorted(files)
        for i in range(len(files)):
            if 'test' in files[i]:
                old_file = sub_folder + files[i]
                split_list = files[i].split(sep='-')
                n = len(split_list[0])
                new_name = files[i][n+1:]
                new_name = sub_folder + new_name
                os.rename(old_file, new_name)


if __name__ == '__main__':
    # round_direct = '/run/user/1001/gvfs/smb-share:server=synology_nas.local,share=zhouyuan/ga_2/'
    # index_data(round_direct)
    # index_recording(round_direct)

    # re_index_customized(round_direct)
    # index_result(round_direct)

    # round_direct = '/run/user/1001/gvfs/smb-share:server=synology_nas.local,share=zhouyuan/ga_1/overtaking1/results/'
    # index_data(round_direct)
    # index_recording(round_direct)

    # 'ga_1/', 'ga_2/', 'ga_3/', 'ga_4/', 'ga_5/'
    # test_number = ['random_1/', 'random_2/', 'random_3/', 'random_4/', 'random_5/']
    # 'intersection1', 'intersection2', 'intersection3', 'intersection4', 'intersection5',
    # 'lanechange1', 'lanechange3', 'overtaking1'
    # test_number = ['coverage_1/', 'coverage_2/', 'coverage_3/']
    # test_scenarios = ['intersection1', 'intersection2', 'intersection3', 'intersection4', 'intersection5','lanechange1','lanechange2','lanechange3','overtaking1']
    # test_number = ['ga_1/', 'ga_2/', 'ga_3/', 'ga_4/', 'ga_5/', 'random_1/', 'random_2/', 'random_3/', 'random_4/', 'random_5/']
    # test_number = ['random_5/']
    # test_scenarios = ['intersection1', 'intersection2', 'intersection3', 'intersection4', 'intersection5','lanechange1','lanechange2','lanechange3', 'overtaking1']
    test_number = ['ga_3/']
    test_scenarios = ['intersection1']
    for number in test_number:
        for test_scenario in test_scenarios:
            # print("Current test round: {}, scearion: {}".format(number, test_scenario))
            direct = '/run/user/1001/gvfs/smb-share:server=synology_nas.local,share=zhouyuan/' + number + test_scenario + '/results/'
            index_data(direct, test_scenario)
            index_recording(direct, test_scenario)
            # re_index_data(direct, test_scenario)

