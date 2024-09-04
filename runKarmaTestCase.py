import renderer.karma.KarmaRenderer as KarmaRenderer
import utils.TestCaseHelper as TestCaseHelper
import utils.SceneHelper as SceneHelper

import utils.ResultsViewer as ResultsViewer

# name of the Hydra delegate
houdini_dir = "/opt/hfs20.5/"
# path to store the results
results_dir = "./karma-results/render"
# path to store the post-processed results and the HTML viewer
viewer_output_dir = "./karma-viewers/render"

# Loading the test case descriptions from a file
testCases = TestCaseHelper.loadTestCases("examples/karma/testcases/render")
testCaseDescription = TestCaseHelper.loadTestCaseDescription("examples/karma/testcases/render")

# Loading the scenes to run the test cases (e.g., usdhydra-scenes can be a folder or a soft link to it)
[scenes, scenes_dir] = SceneHelper.loadScenes("usdhydra-scenes/scenesconfig") 

print("scenes_dir ",scenes_dir)
scenes_dir = "/home/sherholz/Develop-Arnold/openpgl-scripts/usdhydra-scenes/"
# Setup the Hydra renderer
karma = KarmaRenderer.KarmaRenderer(houdini_dir, results_dir, scenes_dir)

#for each scene and each scene variant
for scene, scene_variants, resolution, camera in scenes:
    for variant in scene_variants:
        #run each test case defined in the test cases file
        for testCase in testCases:    
            karma.runTestCase(scene, variant, resolution, camera, testCase, spp = 64)

#after running all test cases for all scenes prepare the results in an interactive HTML viewer 
viewer = ResultsViewer.ResultsViewer("./utils/webviewer")
viewer.generateHTMLS(viewer_output_dir, results_dir, scenes_dir, scenes, testCaseDescription, testCases, showReference=False, perScene=False)