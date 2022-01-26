import os
import sys
from natsort import natsorted

directory0 = '/run/user/1001/gvfs/smb-share:server=synology_nas.local,share=zhouyuan/'

test_rounds = ['random_1/', 'random_2/', 'random_3/', 'random_4/', 'random_5/']
test_scenarios = ['intersection1/', 'intersection2/', 'intersection3/', 'intersection4/', 'intersection5/']

coverage_list_round_scenario = []

for test_round in test_rounds:
    coverage_list = []
    for test_scenario in test_scenarios:
        log_file = directory0 + test_round + test_scenario + 'coverage_spec/test.log'
        read_log = open(log_file, 'r')
        Lines = read_log.readlines()
        coverage = Lines[-1].split(sep=':')[-1]
        # print("Current Round: {}, Current Scenario: {}".format(test_round, test_scenario))
        coverage_list.append(coverage)
    print(coverage_list)
    # coverage_list_round_scenario.append(coverage_list)



