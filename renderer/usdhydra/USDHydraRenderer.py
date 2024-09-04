import os
import copy

#usdrecord ./usdhydra-scenes/pool/pool.usd --renderer 'Karma CPU' --colorCorrectionMode disabled --camera Camera --imageWidth 1920 test.exr

class USDHydraRenderer:
    def __init__(self, hydra_delegate, results_dir, scenes_dir, deps_dir = None):
        self.hydra_delegate = hydra_delegate
        self.results_dir = results_dir
        self.scenes_dir = scenes_dir
        self.deps_dir = deps_dir

        #os.environ['LD_LIBRARY_PATH'] = os.environ['LD_LIBRARY_PATH'] + ":" + self.mitsuba_install_dir + ":" + self.mitsuba_install_dir +"/lib" + ":" + self.mitsuba_install_dir +"/lib64"
        
        #if self.deps_dir:
        #    os.environ['LD_LIBRARY_PATH'] = os.environ['LD_LIBRARY_PATH'] + ":" + self.deps_dir +"/lib" + ":" + self.deps_dir +"/lib64"
        #os.environ['PATH'] = os.environ['PATH'] + ":" + self.mitsuba_install_dir + ":" + self.mitsuba_install_dir +"/bin"

        make_safe_dir(self.results_dir)

    def runTestCase(self, scene, scene_variant, resolution, camera, test_case, max_component_value = 0, spp = 64):
        make_safe_dir(self.results_dir + "/" + scene + scene_variant)
        parameters = copy.deepcopy(test_case.parameters)

        for parameter in parameters:
            value = parameters[parameter]
            if isinstance(value, str):
                if "$SCENE$" in value:
                    parameters[parameter] = value.replace("$SCENE$", self.results_dir + "/" + scene + scene_variant + "/" + scene + scene_variant)
                    print(value)
                    print(parameters[parameter])

        if not parameters.__contains__("sampleCount"):
            parameters["sampleCount"] = spp
        if not parameters.__contains__("maxComponentValue") and max_component_value > 0:
            parameters["maxComponentValue"] = max_component_value
        
        parameters["width"] = resolution[0]
        parameters["height"] = resolution[1]
        #parameterString = extractParameters(parameters)
        sceneFileName = self.scenes_dir + scene +"/" + scene + scene_variant + ".usd"

        outFile = self.results_dir + "/" + scene + scene_variant + "/" + scene + scene_variant + "-" + test_case.name + ".exr"
        #usdrecord ./usdhydra-scenes/pool/pool.usd --renderer 'Karma CPU' --colorCorrectionMode disabled --camera Camera --imageWidth 1920 test.exr


        command = "usdrecord"
        command += " " + sceneFileName
        command += " --renderer " + "'" + self.hydra_delegate + "' "
        command += " --colorCorrectionMode disabled "
        command += " --camera " + camera + " "
        command += " --imageWidth " + str(resolution[0])
        #command += " " + parameterString
        #command += " --spp " + str(spp)
        command += " " + str(outFile)
        #command += " > " + outFile.replace(".exr", ".log")
        print(command)
        os.system(command)


    def run(self, sceneFile, outfile, spp = 64):
        command = "pbrt"
        command += " " + sceneFile
        command += " --spp " + str(spp)
        command += " --outfile " + str(outfile)
        command += " > " + outfile.replace(".exr", ".log")
        print(command)
        os.system(command)

def make_safe_dir(folderName):
    if not os.path.exists(folderName):
        os.makedirs(folderName)


def extractParameters(parameters):
    parameterString = ""

    for parameter in  parameters:
        parameterString += "-D " + str(parameter) + "=" + str(parameters[parameter]) + " "       
    return parameterString

def run(sceneFile, outfile, spp = 64):
    command = "mitsuba"
    command += " " + sceneFile
    command += " -o " + str(outfile)
    command += " > " + outfile.replace(".exr", ".log")
    print(command)
    os.system(command)