import os
import copy
import json
import pathlib

class BlenderRenderer:
    def __init__(self, blender_install_dir, results_dir, scenes_dir):
        self.blender_install_dir = blender_install_dir
        self.results_dir = results_dir
        self.scenes_dir = scenes_dir

        make_safe_dir(self.results_dir)
    
    def runTestCase(self, scene, scene_variant, resolution, test_case, spp = 64, deleteTestCaseJSON=True, renderLayers=[]):
        make_safe_dir(self.results_dir + "/" + scene + scene_variant)

        outFile = self.results_dir + "/" + scene + scene_variant + "/" + scene + scene_variant + "-" + test_case.name + ".exr"
        
        scriptFolder = pathlib.Path(__file__).parent.resolve()

        parameters = copy.deepcopy(test_case.parameters)
        for parameter in parameters:
            value = parameters[parameter]
            if isinstance(value, str):
                if "$SCENE$" in value:
                    parameters[parameter] = value.replace("$SCENE$", self.results_dir + "/" + scene + scene_variant + "/" + scene + scene_variant)
        
        parameters["render.filepath"] = outFile

        parameters["render.resolution_percentage"] = 100
        parameters["render.resolution_x"] = resolution[0]
        parameters["render.resolution_y"] = resolution[1]

        if not parameters.__contains__("cycles.samples"):
            parameters["cycles.samples"] = spp

        parameters["visible_layers"] = renderLayers
        testCaseFile = self.results_dir + "/" + scene + scene_variant + "/" + scene + scene_variant + "-" + test_case.name + ".json"
        with open(testCaseFile, 'w') as f:
            json.dump(parameters, f, indent=4)

        sceneFile = self.scenes_dir + scene +"/" + scene + scene_variant + ".blend"

        command = self.blender_install_dir + "/blender"
        command += " --background" 
        command += " " + sceneFile
        command += " -P " + str(scriptFolder) + "/RunBlenderTestCase.py"
        command += " -- "
        command += " -j " + testCaseFile
        command += " > " + outFile.replace(".exr", ".log")
        print(command)
        os.system(command)
        
        if deleteTestCaseJSON and os.path.isfile(testCaseFile):
            os.remove(testCaseFile)
        
    """
    def run(self, sceneFile, outfile, spp = 64):
        command = self.blender_install_dir + "/blender"
        command += " --background" 
        command += " " + sceneFile
        command += "-P blender/RunBlenderTestCase.py"
        command += " -- "
        command += " -s " + str(spp)
        command += " -b " + str(20)
        command += " -g"
        print(command)
        os.system(command)
    """

    def getRenderLayerNames(self, render_layers):
        prefix = "Cycles"
        render_layer_names = []
        for layer in render_layers:
            if layer == "denoising_store_passes":
                render_layer_names.append(prefix + "." + "Denoising Albedo")
                render_layer_names.append(prefix + "." + "Denoising Depth")
                render_layer_names.append(prefix + "." + "Denoising Normal")
                #render_layer_names.append(prefix + "." + "Denoising Roughness")
                #render_layer_names.append(prefix + "." + "Denoising Specular Albedo")
            elif layer == "combined":
                render_layer_names.append(prefix + "." + "Combined")
            elif layer == "diffuse_color":
                render_layer_names.append(prefix + "." + "Diffuse Color")
            elif layer == "glossy_color":
                render_layer_names.append(prefix + "." + "Glossy Color")
        # TODO: Need to add other AOV naming transitions 
        return render_layer_names

def make_safe_dir(folderName):
    if not os.path.exists(folderName):
        os.makedirs(folderName)