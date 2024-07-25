import os, sys, importlib

class TestCase:
    def __init__(self, name, data, common_parameters):
        self.name = name
        self.parameters = mergeParameters(common_parameters, data["parameters"])
        self.description = data["description"]
        self.skipViewer = False
        if data.__contains__("skipViewer"):
            self.skipViewer = data["skipViewer"]

def loadTestCases(test_cases):
    testCases = []
    sys.path.append(os.path.dirname(test_cases))
    tcs = importlib.import_module(os.path.basename(test_cases))
    

    for test_case in tcs.test_cases: 
        testCases.append(TestCase(test_case, tcs.test_cases[test_case], tcs.common_parameters))
    return testCases

def loadTestCaseDescription(test_cases):
    sys.path.append(os.path.dirname(test_cases))
    tcs = importlib.import_module(os.path.basename(test_cases))
    return tcs.test_case_description

def mergeParameters(common_parameters, test_case_parameters):
    parameters = test_case_parameters
    for cparameter in common_parameters:
        if not parameters.__contains__(cparameter):
            parameters[cparameter] = common_parameters[cparameter]
    return parameters