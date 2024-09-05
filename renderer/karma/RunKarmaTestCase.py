import hou
import sys
import json
from pxr import Usd, Sdf

#print("Script arguments", sys.argv)

settings = stage.GetPrimAtPath("/Render/RenderSettings")
print(settings)

#if settings == None:
# TODO    

if len(sys.argv) > 1:
    f = open(sys.argv[1])
    testcase_parameters = json.load(f)
    #print(testcase_parameters)
    for parameter in testcase_parameters:
        [ptype, pvalue] = testcase_parameters[parameter]
        if ptype == "int":
            attr = settings.CreateAttribute(parameter, Sdf.ValueTypeNames.Int)
            attr.Set(int(pvalue))
        elif ptype == "float":
            attr = settings.CreateAttribute(parameter, Sdf.ValueTypeNames.Float)
            attr.Set(float(pvalue))
        elif ptype == "bool":
            attr = settings.CreateAttribute(parameter, Sdf.ValueTypeNames.Bool)
            attr.Set(bool(pvalue))
        else:
            print("Unknown parameter type: parameter = ", parameter, "\t type = ", ptype, "\t value = ", str(pvalue))


