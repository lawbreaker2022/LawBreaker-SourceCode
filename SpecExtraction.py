from typing import Union, Any, List, Dict
from TestCaseExtraction import AllTestCase
from parser.ast import AST, ASTDumper, Parse
from parser.ast.assertion.assertion import AtomPredicate, KuoHaoWithGeneral, NotWithGeneral, GeneralAssertionWithTemporalOperator, GeneralAssertionWithUnitl, AndWithGeneral, OrWithGeneral, DeriveWithGeneral
from exception import AgentCompareError, ScenarioTraceMatchError, TrafficReferenceTraceError, SafetyAssertionError
import exception
import sys
import json
from TracePreprocess import Trace
from ast import literal_eval


class SingleTraceSpecExtract:
    def __init__(self, TraceSpec, agents):
        self.trace_name = TraceSpec.get_name()
        self.scenario_name = TraceSpec.get_scenario().get_name()
        self.perception_assert = TraceSpec.get_detection_assertions()
        self.safety_assert = TraceSpec.get_safety_assertions()
        self.intersection_assert = TraceSpec.get_intersection_assertions()
        self.road_assert = TraceSpec.get_speed_constraint_assertions()
        self.perception_specification = []
        self.safety_specification = []
        self.agents = agents[self.scenario_name]

    def perception_spec(self) -> List[Dict[str, Union[List, List[str]]]]:
        _perception_assert_list = self.perception_assert
        _perception_assert_len = len(_perception_assert_list)
        perception_specification = []
        for _i in range(_perception_assert_len):
            _perception_assert = _perception_assert_list[_i].get_assertions()  # DetectionAssertion
            element = {'visible': [], 'checking': []}
            # print(_perception_assert[0].get_agent_ground_distance().get_agent_ground_truth().get_agent().get_name())
            for _j in range(len(_perception_assert)):
                _agent_assert = _perception_assert[_j]   # AgentVisibleDetectionAssertion, AgentErrorDetectionAssertion, TrafficDetectionAssertion
                # _agent_assert_str = str(_agent_assert)
                # compare = re.finditer(r'[<>=]+', _agent_assert_str)
                # for i in compare:
                #     compare_opt = i.group(0)
                #     left_str = _agent_assert_str.split(compare_opt)[0]
                #     right_str = _agent_assert_str.split(compare_opt)[1]
                try:
                    # _agent_assert is AgentVisibleDetectionAssertion
                    sensing_range = _agent_assert.get_sensing_range()
                    distance_property = _agent_assert.get_agent_ground_distance()
                    ego_name = distance_property.get_ego_state().get_name()
                    agent_name = distance_property.get_agent_ground_truth().get_agent().get_name()
                    if agent_name not in self.agents:
                        raise exception.SpecAgentError(
                            'The agent {} is not defined in scenario {}'.format(agent_name, self.scenario_name))
                    element['visible'] = [agent_name, sensing_range]
                    # print('ego name: {}, agent name: {}'.format(ego_name, agent_name))
                    # print('ego time: {}, agent time: {}'.format(ego_time, agent_time))
                    # print("visible")
                except AttributeError:
                    try:
                        # _agent_assert is AgentErrorDetectionAssertion
                        perception_threshold = _agent_assert.get_error_threshold()
                        error_property = _agent_assert.get_agent_error()
                        agent_name_perception = error_property.get_agent_state().get_agent().get_name()
                        agent_name_truth = error_property.get_agent_ground_truth().get_agent().get_name()
                        if agent_name_perception != agent_name_truth:
                            raise AgentCompareError("Only the same agent can be compared.")
                        elif agent_name_perception not in self.agents:
                            raise exception.SpecAgentError(
                                'The agent {} is not defined in scenario {}'.format(agent_name_perception, self.scenario_name))
                        element['checking'] = [agent_name_perception, perception_threshold]
                    except AttributeError:
                        try:
                            # _agent_assert is TrafficDetectionAssertion
                            left_trace = _agent_assert.get_left_trace().get_name()
                            right_trace = _agent_assert.get_right_trace().get_name()
                            if left_trace != right_trace:
                                raise TrafficReferenceTraceError('The left trace is: {}, while the right trace is: {}'.format(left_trace, right_trace))
                            element['checking'] = ['traffic']
                        except AttributeError:
                            print("No match")
            perception_specification.append(element)
        self.perception_specification = perception_specification
        return perception_specification

    def safety_spec(self) -> List[Dict[str, List]]:
        safety_spec_list = self.safety_assert
        len_safety_spec = len(safety_spec_list)
        safety_specification = []
        for _i in range(len_safety_spec):
            safety_spec = safety_spec_list[_i].get_assertions()
            safety_element = {'visible': [], 'perception': [], 'safety': []}
            for _j in range(len(safety_spec)):
                autom_spec = safety_spec[_j]
                try:
                    agent_name = autom_spec.get_agent_ground_distance().get_agent_ground_truth().get_agent().get_name()
                    if agent_name not in self.agents:
                        raise exception.SpecAgentError(
                            'The agent {} is not defined in scenario {}'.format(agent_name, self.scenario_name))
                    sensing_range = autom_spec.get_sensing_range()
                    safety_element['visible'] = [agent_name, sensing_range]
                except AttributeError:
                    try:
                        agent_name_perception = autom_spec.get_agent_error().get_agent_state().get_agent().get_name()
                        agent_name_truth = autom_spec.get_agent_error().get_agent_ground_truth().get_agent().get_name()
                        if agent_name_perception != agent_name_truth:
                            raise AgentCompareError("Only the same agent can be compared.")
                        elif agent_name_perception not in self.agents:
                            raise exception.SpecAgentError(
                                'The agent {} is not defined in scenario {}'.format(agent_name_perception,
                                                                                    self.scenario_name))
                        perception_error = autom_spec.get_error_threshold()
                        safety_element['perception'] = [agent_name_perception, perception_error]
                    except AttributeError:
                        try:
                            safet_radius = autom_spec.get_safety_radius()
                            agent_name = autom_spec.get_agent_state().get_agent().get_name()
                            if agent_name not in self.agents:
                                raise exception.SpecAgentError(
                                    'The agent {} is not defined in scenario {}'.format(agent_name, self.scenario_name))
                            safety_element['safety'] = [agent_name, safet_radius]
                        except AttributeError:
                            raise SafetyAssertionError('The safety assertion {} is wrong.'.format(safety_spec_list[i].get_name()))
            safety_specification.append(safety_element)
        self.safety_specification = safety_specification
        return safety_specification


class AllSpecification:
    def __init__(self, tracelist, scenario_agents):
        self.traces = tracelist
        self.SpecINScenario = {}
        self.PerceptionSpecClass = []
        self.SafetySpecClass = []
        self.AllAgents = scenario_agents

        self.ScenarioSpec = {}

    def Get_all_general_specification(self):
        general_specification = {}
        for _i in range(len(self.traces)):
            _trace = self.traces[_i]
            _related_scneario_name = _trace.get_scenario().get_name()
            if _trace.has_assertion():
                self.ScenarioSpec[_related_scneario_name] = []
                temp = _trace.get_general_assertions()
                for _j in range(len(temp)):
                    _assertion = temp[_j].get_assertion()
                    self.ScenarioSpec[_related_scneario_name].append(_assertion)


    def scenario_specification(self)  -> Dict[Any, Dict[str, List]]:
        '''
        Returns: {'scenario0': {'perception specs': [{'visible': ['npc1', 50.0], 'checking': ['npc1', 0.1]},
                                                     {'visible': ['npc2', 50.0], 'checking': ['npc2', 0.1]},
                                                     {'visible': [], 'checking': ['traffic']}
                                                    ],
                                'safety specs': [{'visible': ['npc1', 50.0], 'perception': ['npc1', 0.1], 'safety': ['npc1', 0.1]},
                                                 {'visible': ['npc2', 50.0], 'perception': ['npc2', 0.1], 'safety': ['npc2', 0.1]}
                                                ]
                                }
                ,
                'scenario1': {'perception specs': [{'visible': ['npc1', 50.0], 'checking': ['npc1', 0.1]}
                                                  ],
                              'safety specs': [{'visible': ['npc1', 50.0], 'perception': ['npc1', 0.1], 'safety': ['npc1', 0.1]}
                                              ]
                             }
                }

        '''
        spec_scenario = {}
        for _i in range(len(self.traces)):
            _trace = self.traces[_i]
            if _trace.has_assertion():
                _single_trace_spec = SingleTraceSpecExtract(_trace, self.AllAgents)
                _single_trace_spec.perception_spec()
                _single_trace_spec.safety_spec()
                spec_scenario[_single_trace_spec.scenario_name] = \
                    {'perception specs': _single_trace_spec.perception_specification,
                     'safety specs': _single_trace_spec.safety_specification}
                # spec_scenario.append({'scenario name': _single_trace_spec.scenario_name,
                #                       'perception specs': _single_trace_spec.perception_specification,
                #                       'safety specs': _single_trace_spec.safety_specification})
        self.SpecINScenario = spec_scenario
        return spec_scenario

    def perception_classify(self) -> Dict[str, set]:
        '''

        Returns: {"{'visible': ['npc1', 50.0], 'checking': ['npc1', 0.1]}": {'scenario0', 'scenario1'},
                  "{'visible': ['npc2', 50.0], 'checking': ['npc2', 0.1]}": {'scenario0'},
                  "{'visible': [], 'checking': ['traffic']}": {'scenario0'}
                }

        '''
        perception_class = {}
        for _i in range(len(self.traces)):
            _trace = self.traces[_i]
            if _trace.has_assertion():
                _trace_spec = SingleTraceSpecExtract(_trace, self.AllAgents)
                _trace_spec.perception_spec()
                for _j in range(len(_trace_spec.perception_specification)):
                    _single_perception = _trace_spec.perception_specification[_j]
                    if str(_single_perception) in perception_class.keys():
                        perception_class[str(_single_perception)].add(_trace_spec.scenario_name)
                    else:
                        perception_class[str(_single_perception)] = {_trace_spec.scenario_name}
        self.PerceptionSpecClass = perception_class
        return perception_class

    def safety_classify(self) -> Dict[str, set]:
        '''

        Returns: {"{'visible': ['npc1', 50.0], 'perception': ['npc1', 0.1], 'safety': ['npc1', 0.1]}": {'scenario0', 'scenario1'},
                  "{'visible': ['npc2', 50.0], 'perception': ['npc2', 0.1], 'safety': ['npc2', 0.1]}": {'scenario0'}
                }

        '''
        safety_class = {}
        for _i in range(len(self.traces)):
            _trace = self.traces[_i]
            if _trace.has_assertion():
                _trace_spec = SingleTraceSpecExtract(_trace, self.AllAgents)
                _trace_spec.safety_spec()
                for _j in range(len(_trace_spec.safety_specification)):
                    _single_safety = _trace_spec.safety_specification[_j]
                    if str(_single_safety) in safety_class.keys():
                        safety_class[str(_single_safety)].add(_trace_spec.scenario_name)
                    else:
                        safety_class[str(_single_safety)] = {_trace_spec.scenario_name}
        self.SafetySpecClass = safety_class
        return safety_class


class GeneralAssertion:
    def __init__(self, spec_trace):
        self.spec_trace_list = spec_trace
        self.ScenarioSpec = dict()
        self.scenario_names = []
        self.auto_predicate = []

    def get_all_general_specification(self):
        for _i in range(len(self.spec_trace_list)):
            _trace = self.spec_trace_list[_i]
            _related_scenario_name = _trace.get_scenario().get_name()
            self.scenario_names.append(_related_scenario_name)
            if _trace.has_assertion():
                self.ScenarioSpec[_related_scenario_name] = []
                temp = _trace.get_general_assertions()
                for _j in range(len(temp)):
                    _assertion = temp[_j].get_assertion()
                    self.ScenarioSpec[_related_scenario_name].append(_assertion)

    def get_specifications_one_scenario(self, scenario_name):
        if scenario_name in self.scenario_names:
            return self.ScenarioSpec[scenario_name]


class SingleSpecification:
    def __init__(self, one_specification):
        self.specification = None
        self.auto_predicate_variables = []
        self.auto_predicate_variable_mapping = dict()
        self.auto_predicate_No = 0

    def get_specifiaction_type(self, one_specification):
        if isinstance(one_specification, AtomPredicate):
            self.auto_predicate_No += 1
            left_statement = one_specification.get_atom_statement_left()
            right_statement = one_specification.get_atom_statement_right()


            var_predicate = "p" + str(self.auto_predicate_No)
            self.auto_predicate_variables.append(var_predicate)
        elif isinstance(one_specification, KuoHaoWithGeneral):
            pass
        elif isinstance(one_specification, NotWithGeneral):
            pass
        elif isinstance(one_specification, GeneralAssertionWithTemporalOperator):
            pass
        elif isinstance(one_specification, GeneralAssertionWithUnitl):
            pass
        elif isinstance(one_specification, AndWithGeneral):
            pass
        elif isinstance(one_specification, OrWithGeneral):
            pass
        elif isinstance(one_specification, DeriveWithGeneral):
            pass
        else:
            raise exception.AssertionTypeError("Wrong type of assertion!")






if __name__ == "__main__":
    input_file = 'input_test.txt'
    ast_ = Parse(input_file)
    scenario_list = ast_.get_scenarios()
    trace_list = ast_.get_traces()
    test_cases = AllTestCase(scenario_list, isGroundTruth=True)
    TestCase = test_cases.TestCases[0]
    scenario_name = TestCase['ScenarioName']
    agent_name = TestCase['AgentNames']

    specification_obj = GeneralAssertion(trace_list)
    specification_obj.get_all_general_specification()
    specification = specification_obj.get_specification_one_scenario(scenario_name)
    spec_NO = len(specification)
    for i in range(spec_NO):
        single_spec = specification[i]
        a = isinstance(single_spec, GeneralAssertionWithTemporalOperator)
        print(a)





