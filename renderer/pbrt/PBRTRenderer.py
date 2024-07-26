import os
import copy

class PBRTRenderer:
    def __init__(self, pbrt_install_dir, results_dir, scenes_dir):
        self.pbrt_install_dir = pbrt_install_dir
        self.results_dir = results_dir
        self.scenes_dir = scenes_dir

        os.environ['LD_LIBRARY_PATH'] = os.environ['LD_LIBRARY_PATH'] + ":" + self.pbrt_install_dir +"lib"
        os.environ['PATH'] = os.environ['PATH'] + ":" + self.pbrt_install_dir +"bin"

        make_safe_dir(self.results_dir)

    def runTestCase(self, scene, scene_variant, resolution, test_case, spp = 64, stats = False, usedGuidedGBuffer = False):
        make_safe_dir(self.results_dir + "/" + scene + scene_variant)

        outFile = self.results_dir + "/" + scene + scene_variant + "/" + scene + scene_variant + "-" + test_case.name + ".exr"

        parameters = copy.deepcopy(test_case.parameters)
        for parameter in parameters:
            value = parameters[parameter][1]
            if isinstance(value, str):
                if "$SCENE$" in value:
                    parameters[parameter][1] = value.replace("$SCENE$", self.results_dir + "/" + scene + scene_variant + "/" + scene + scene_variant)
                    #print(value)
                    #print(parameters[parameter][1])
        
        integratorString = extractIntegrator(parameters)
        filmString = extractFilm(resolution, parameters, scene + scene_variant + "-" + test_case.name + ".exr", usedGuidedGBuffer = usedGuidedGBuffer)
        tmpTestCaseFileName = self.scenes_dir + scene +"/" + scene + scene_variant + "-"+ test_case.name + ".pbrt"
        
        tmpSceneFile = open(tmpTestCaseFileName,"w")
        tmpSceneFile.write(filmString)
        tmpSceneFile.write("\n")
        tmpSceneFile.write(integratorString)
        tmpSceneFile.write("\n")
        tmpSceneFile.write("Include \"" + scene + scene_variant + "_auto.pbrt" + "\"")
        tmpSceneFile.write("\n")
        tmpSceneFile.close()

        command = "pbrt"
        command += " " + tmpTestCaseFileName
        if stats:
            command += " --stats "
        #command += " --nthreads " + str(1)
        command += " --spp " + str(spp)
        command += " --outfile " + str(outFile)
        command += " > " + outFile.replace(".exr", ".log")
        print(command)
        os.system(command)

        if os.path.isfile(tmpTestCaseFileName):
            os.remove(tmpTestCaseFileName)

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

def extractFilm(resolution, parameters, outputFileName, usedGuidedGBuffer = False):
    filmString = ""
    if not usedGuidedGBuffer:
        filmString += "Film " +"\"rgb\"" + "\n"
    else:
        filmString += "Film " +"\"guidedgbuffer\"" + "\n"
    
    filmString += "\"string filename\" " + "\"" + outputFileName +"\""+ "\n"
    filmString += "\"integer xresolution\" ["+ str(resolution[0]) + "]" + "\n"
    filmString += "\"integer yresolution\" ["+ str(resolution[1]) + "]" + "\n"
    if parameters.__contains__("maxcomponentvalue"):
        filmString += "\"float maxcomponentvalue\" ["+ str(parameters["maxcomponentvalue"][1]) + "]" + "\n"
    return filmString

def extractIntegrator(parameters):
    integratorString = ""

    integratorString += "Integrator \"" + parameters["integrator"] + "\"\n"
    for parameter in  parameters:
        if parameter != "integrator" and parameter != "maxcomponentvalue":
            if str(parameters[parameter][0]) == "bool":
                integratorString += "\t" + "\"" + str(parameters[parameter][0]) + " " + str(parameter) + "\" " +  str(parameters[parameter][1]).lower() + "\n"
            elif str(parameters[parameter][0]) == "string":
                integratorString += "\t" + "\"" + str(parameters[parameter][0]) + " " + str(parameter) + "\" \"" +  str(parameters[parameter][1]) + "\"\n"
            else:
                integratorString += "\t" + "\"" + str(parameters[parameter][0]) + " " + str(parameter) + "\" " +  str(parameters[parameter][1]) + "\n"
    return integratorString

def run(sceneFile, outfile, spp = 64):
    command = "pbrt"
    command += " " + sceneFile
    command += " --spp " + str(spp)
    command += " --outfile " + str(outfile)
    command += " > " + outfile.replace(".exr", ".log")
    print(command)
    os.system(command)