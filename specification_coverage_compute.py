import logging
import shutil
import sys
import warnings

from monitor import Monitor
import os
import json
from EXtraction import ExtractAll
from AssertionExtraction import SingleAssertion
from natsort import  natsorted

def newlist(parent_list, list1):
    new_element = [element for element in list1 if element not in parent_list]
    return new_element


if __name__ == "__main__":

    normal_spec = True

    # scenario_direct = 'test_cases/final/'
    scenario_direct = 'test_cases/final/'
    test_rounds = ['random_2/'] #'random_2/', 'random_3/', 'random_4/', 'random_5/'
    # test_rounds = ['random_3/', 'random_4/', 'random_5/']
    for test_round in test_rounds:
        result_direct = '/run/user/1001/gvfs/smb-share:server=synology_nas.local,share=zhouyuan/' + test_round
        logging_file = result_direct + '/normal_spec.log'
        file_handler = logging.FileHandler(logging_file, mode='w')
        stdout_handler = logging.StreamHandler(sys.stdout)
        logging.basicConfig(level=logging.INFO, handlers=[stdout_handler, file_handler],
                            format='%(asctime)s, %(levelname)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
        scenario_names = os.listdir(result_direct)
        scenario_names = natsorted(scenario_names)
        scenario_names = ['intersection1', 'intersection2', 'intersection3', 'intersection4', 'intersection5', 'lanechange1', 'lanechange3', 'overtaking1']
        # scenario_names = ['overtaking1'] #, 'lanechange2', 'lanechange3', 'overtaking1']
        for scenario_name in scenario_names:
            scenario_file = scenario_direct + scenario_name + '.txt'
            isGroundTruth = True
            extracted_script = ExtractAll(scenario_file, isGroundTruth)
            scenario_spec = extracted_script.Get_Specifications()
            all_agents = extracted_script.Get_AllAgents()

            covered_predicates = []
            failure_predicates = []

            # log_direct = result_direct + scenario_name + '/coverage_spec'
            # if not os.path.exists(log_direct):
            #     os.makedirs(log_direct)
            logging.info("Current Round: {}, Current Scenario: {}".format(test_round, scenario_name))
            data_direct = result_direct + scenario_name + '/results/' + scenario_name + '/new_results/'
            try:
                data_files = os.listdir(data_direct)
                data_files = natsorted(data_files)
                for file in data_files:
                    if file.endswith('.json'):
                        with open(data_direct + file) as f:
                            data = json.load(f)
                            scenario_name = data['ScenarioName']
                            single_spec = SingleAssertion(scenario_spec[scenario_name][0], "san_francisco")
                            if len(data['trace']) > 1:
                                monitor = Monitor(data, single_spec)
                                value2 = monitor.continuous_monitor()
                                logging.info("Current data file: {}, Fitness Value: {}".format(file, value2))
                                # if not normal_spec:
                                if value2 < 0:
                                    coverage_rate, coverage_predicate, failure_predicates = monitor.coverage_monitor()
                                    new_predicate = newlist(covered_predicates, coverage_predicate)
                                    if len(new_predicate):
                                        covered_predicates = covered_predicates + new_predicate
                                    logging.info("Current data file: {}, coverage rate: {}".format(file, coverage_rate))
                            else:
                                warnings.warn("Wrong Execution of {}".format(file))
            except FileNotFoundError:
                pass
            logging.info("\n All possible failure predicates: {}\n".format(failure_predicates))
            logging.info("Covered predicate: {}\n".format(covered_predicates))
            logging.info("Final specification coverage rate: {}/{}\n".format(len(covered_predicates), len(failure_predicates)))
            # print(("Final specification coverage rate: {}/{}\n".format(len(covered_predicates), len(failure_predicates))))




    #
    # direct = 'random_3/intersection1/data/'
    # arr = os.listdir(direct)
    # covered_predicates = []
    # for file in arr:
    #     with open(direct + file) as f:
    #         data = json.load(f)
    #         scenario_name = data['ScenarioName']
    #         single_spec = SingleAssertion(scenario_spec[scenario_name][0], "san_francisco")
    #         monitor = Monitor(data, single_spec)
    #         value2 = monitor.continuous_monitor()
    #         if value2 < 0:
    #             coverage_rate, coverage_predicate, failure_predicates = monitor.coverage_monitor()
    #             new_predicate = newlist(covered_predicates, coverage_predicate)
    #             if len(new_predicate):
    #                 covered_predicates = covered_predicates + new_predicate
    # final_rate = len(covered_predicates)/len(failure_predicates)
    # print(final_rate)
    # print(covered_predicates)
    # print(failure_predicates)
