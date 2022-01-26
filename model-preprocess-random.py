import logging
import os
import shutil
import sys

import natsort

directory0 = '/run/user/1001/gvfs/smb-share:server=synology_nas.local,share=zhouyuan/'
test_rounds = ['random_5']
scenarios = ['overtaking1'] #, 'intersection2', 'intersection3', 'intersection4','intersection5']
logging_file = directory0 + '/lanechange3_replace_new_data_file.log'
file_handler = logging.FileHandler(logging_file, mode='w')
stdout_handler = logging.StreamHandler(sys.stdout)
logging.basicConfig(level=logging.INFO, handlers=[stdout_handler, file_handler],
                        format='%(asctime)s, %(levelname)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
for test_round in test_rounds:
    for scenario in scenarios:
        logging.info("current test round: {}, current scenario: {}".format(test_round, scenario))
        first_select_directory = directory0 + test_round + '/' + scenario + '/results/'
        files = os.listdir(first_select_directory)
        files = natsort.natsorted(files)
        first_selected_json_files = []
        for file in files:
            if file.endswith('.json'):
                first_selected_json_files.append(file)
        second_select_directory = directory0 + test_round + '/' + scenario + '/results/' + scenario + '/data/'
        second_files = os.listdir(second_select_directory)
        second_files = natsort.natsorted(second_files)
        for i in range(len(second_files)):
            original_index = first_selected_json_files[i].split(sep='-')[0]
            logging.info("original data file index: {}".format(original_index))
            new_file = original_index + '-' + second_files[i]
            shutil.copyfile(second_select_directory + second_files[i], directory0 + test_round + '/' + scenario + '/new_data/' + new_file)
            if os.path.exists(directory0 + test_round + '/' + scenario + '/new_data/' + first_selected_json_files[i]):
                os.remove(directory0 + test_round + '/' + scenario + '/new_data/' + first_selected_json_files[i])


