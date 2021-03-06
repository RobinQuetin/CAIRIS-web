import unittest
import sys
from tests.AssetTests import AssetTests
from tests.CImportTests import CImportTests
from tests.DependencyTests import DependencyTests
from tests.EnvironmentTests import EnvironmentTests
from tests.GoalTests import GoalTests
from tests.MisuseCaseTests import MisuseCaseTests
from tests.ProjectTests import ProjectTests
from tests.RequirementTests import RequirementTests
from tests.ResponseTests import ResponseTests
from tests.RiskTests import RiskTests
from tests.RoleTests import RoleTests
from tests.ThreatTests import ThreatTests
from tests.UploadTests import UploadTests
from tests.UserTests import UserTests
from tests.VulnerabilityTests import VulnerabilityTests

__author__ = 'Robin Quetin'

tests_dict = {
    'asset': [0, AssetTests],
    'dependency': [0, DependencyTests],
    'environment': [0, EnvironmentTests],
    'goal': [0, GoalTests],
    'import': [0, CImportTests],
    'misusecase': [0, MisuseCaseTests],
    'project': [0, ProjectTests],
    'requirement': [0, RequirementTests],
    'response': [0, ResponseTests],
    'risk': [0, RiskTests],
    'role': [0, RoleTests],
    'threat': [0, ThreatTests],
    'upload': [0, UploadTests],
    'vulnerability': [0, VulnerabilityTests],
    'user': [0, UserTests]
}


def enable_tests(tests):
    for test in tests:
        if test in tests_dict.keys():
            tests_dict[test][0] = 1
        else:
            print('Unrecognized test: %s' % test)

if __name__ == '__main__':
    if len(sys.argv) > 0:
        test_args = '--tests='
        needs_parsing = False

        for arg in sys.argv:
            assert isinstance(arg, str)
            if arg.startswith(test_args) or needs_parsing:
                tests_str = arg[len(test_args):]
                tests = tests_str.split(',')
                enable_tests(tests)

            if arg.startswith('-t'):
                needs_parsing = True

            if arg == '--all' or arg == '-a':
                for key in tests_dict:
                    tests_dict[key][0] = 1

    suite = unittest.TestSuite()

    for value in tests_dict.values():
        if value[0] == 1:
            suite.addTest(value[1])

    suite.run(None)