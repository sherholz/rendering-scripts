import os
import copy
import json
import pathlib

class KarmaRenderer:
    def __init__(self, houdini_dir, results_dir, scenes_dir, use_xpu = False):
        self.houdini_dir = houdini_dir
        self.results_dir = results_dir
        self.scenes_dir = scenes_dir
        self.use_xpu = use_xpu

        make_safe_dir(self.results_dir)

    def runTestCase(self, scene, scene_variant, resolution, camera, test_case, max_component_value = 0, spp = 64):
        make_safe_dir(self.results_dir + "/" + scene + scene_variant)
        parameters = copy.deepcopy(test_case.parameters)

        scriptFolder = pathlib.Path(__file__).parent.resolve()
        currentFolder = pathlib.Path.cwd()

        for parameter in parameters:
            value = parameters[parameter]
            if isinstance(value, str):
                if "$SCENE$" in value:
                    parameters[parameter] = value.replace("$SCENE$", self.results_dir + "/" + scene + scene_variant + "/" + scene + scene_variant)
                    print(value)
                    print(parameters[parameter])

        #if not parameters.__contains__("karma:global:samplesperpixel"):
        #    parameters["karma:global:samplesperpixel"] = ["int",spp]
        

        testCaseFile = self.results_dir + "/" + scene + scene_variant + "/" + scene + scene_variant + "-" + test_case.name + ".json"
        with open(testCaseFile, 'w') as f:
            json.dump(parameters, f, indent=4)
        
        sceneFileName = self.scenes_dir + scene +"/" + scene + scene_variant + ".usd"

        outFile = self.results_dir + "/" + scene + scene_variant + "/" + scene + scene_variant + "-" + test_case.name + ".exr"

        command = "bash -c \""
        command += "cd "+ self.houdini_dir +" \n "
        command += "source houdini_setup_bash \n "
        command += "cd " + str(currentFolder) + " \n "
        command += "husk"
        command += " --prerender-script " + "'" + str(scriptFolder) + "/RunKarmaTestCase.py " + testCaseFile +"'"
        command += " " + sceneFileName

        if self.use_xpu:
            command += " --engine " + "xpu"
        else:
            command += " --engine " + "cpu"
        #command += " --convergence-mode " + "pathtraced"
        command += " --pixel-samples " + str(spp)
        command += " --camera " + camera + " "
        command += " -o " + str(outFile)
        command += "\""
        print(command)
        os.system(command)

    """
    def run(self, sceneFile, outfile, spp = 64):
        command = "pbrt"
        command += " " + sceneFile
        command += " --spp " + str(spp)
        command += " --outfile " + str(outfile)
        command += " > " + outfile.replace(".exr", ".log")
        print(command)
        os.system(command)
    """
def make_safe_dir(folderName):
    if not os.path.exists(folderName):
        os.makedirs(folderName)
