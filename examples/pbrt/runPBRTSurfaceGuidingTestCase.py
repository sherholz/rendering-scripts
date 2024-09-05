import renderer.pbrt.PBRTRenderer as PBRTRenderer
import utils.TestCaseHelper as TestCaseHelper
import utils.SceneHelper as SceneHelper

import utils.ResultsViewer as ResultsViewer

# path to the PBRT installation (e.g., folder or a soft link to it)
pbrt_dir = "./pbrt-renderer/"
# path to store the results
results_dir = "./pbrt-results/surfaceguiding"
# path to store the post-processed results and the HTML viewer
viewer_output_dir = "./pbrt-viewers/surfaceguiding"

# Loading the test case descriptions from a file
testCases = TestCaseHelper.loadTestCases("examples/pbrt/testcases/surfaceguiding")
testCaseDescription = TestCaseHelper.loadTestCaseDescription("examples/pbrt/testcases/surfaceguiding")

# Loading the scenes to run the test cases (e.g., pbrt-scenes can be a folder or a soft link to it)
[scenes, scenes_dir] = SceneHelper.loadScenes("pbrt-scenes/scenesconfig") 

# Setup the PBRT renderer
pbrt = PBRTRenderer.PBRTRenderer(pbrt_dir, results_dir, scenes_dir)

#for each scene and each scene variant
for scene, scene_variants, resolution in scenes:
    for variant in scene_variants:
        #run each test case defined in the test cases file
        for testCase in testCases:    
            pbrt.runTestCase(scene, variant, resolution, testCase, spp = 64, stats = True, usedGuidedGBuffer = False)

#after running all test cases for all scenes prepare the results in an interactive HTML viewer 
viewer = ResultsViewer.ResultsViewer("./utils/webviewer")
viewer.generateHTMLS(viewer_output_dir, results_dir, scenes_dir, scenes, testCaseDescription, testCases, showReference=False, perScene=False)