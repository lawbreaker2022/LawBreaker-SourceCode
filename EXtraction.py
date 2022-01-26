import copy

from parser.ast import AST, ASTDumper, Parse
from SpecExtraction import AllSpecification
from TestCaseExtraction import AllTestCase
from AssertionExtraction import AllAssertions, SingleAssertion
import json

class ExtractAll:
    def __init__(self, inputfile, isGroundTruth):
        _ast = Parse(inputfile)
        self.TestCaseObj = AllTestCase(_ast.get_scenarios(), isGroundTruth)
        self.SpecificationObj = AllAssertions(_ast.get_traces())

    def Get_TestCastINJsonList(self):
        _testcases = copy.deepcopy(self.TestCaseObj.TestCases)
        return _testcases

    def Get_AllAgents(self):
        _agent = copy.deepcopy(self.TestCaseObj.AgentNames)
        return _agent

    def Get_Specifications(self):
        _specification = copy.deepcopy(self.SpecificationObj.ScenarioSpec)
        return _specification

    def Get_AllMaps(self):
        _maps = copy.deepcopy(self.SpecificationObj.ScenarioMap)
        return _maps
    # def Get_SpecificationINScenario(self):
    #     self.SpecificationObj.scenario_specification()
    #     return self.SpecificationObj.SpecINScenario
    #
    # def Get_PerceptionSpecClass(self):
    #     self.SpecificationObj.perception_classify()
    #     return self.SpecificationObj.PerceptionSpecClass
    #
    # def Get_SafetySpecClass(self):
    #     self.SpecificationObj.safety_classify()
    #     return self.SpecificationObj.SafetySpecClass


if __name__ == "__main__":
    file = 'test_cases/input_test.txt'
    # file = 'parser_test.txt'
    isGroundTruth = True
    extracted_data = ExtractAll(file, isGroundTruth)
    agents = extracted_data.Get_AllAgents()
    print(agents)
    testcases = extracted_data.Get_TestCastINJsonList()
    spec = extracted_data.Get_Specifications()
    maps = extracted_data.Get_AllMaps()
    for i in range(len(testcases)):
        print(testcases[i])
    scenario_name = testcases[0]['ScenarioName']
    for i in range(len(spec[scenario_name])):
        print(spec[scenario_name][i])



