import renderer.mitsuba.MitsubaRenderer as MitsubaRenderer
import utils.TestCaseHelper as TestCaseHelper
import utils.SceneHelper as SceneHelper

import utils.ResultsViewer as ResultsViewer

# path to the Mitsuba installation (dist) folder (e.g., folder or a soft link to it)
mts_dir = "./mitsuba-renderer/"
# optional: path to the Mitsuba dependency folder (e.g., folder or a soft link to it)
mts_deps = "./mitsuba-deps/"

# path to store the results
results_dir = "./mitsuba-results/guiding"
# path to store the post-processed results and the HTML viewer
viewer_output_dir = "./mitsuba-viewers/guiding"

# Loading the test case descriptions from a file
testCases = TestCaseHelper.loadTestCases("examples/mitsuba/testcases/references")
testCaseDescription = TestCaseHelper.loadTestCaseDescription("examples/mitsuba/testcases/references")

# Loading the scenes to run the test cases (e.g., pbrt-scenes can be a folder or a soft link to it)
[scenes, scenes_dir] = SceneHelper.loadScenes("mitsuba-scenes/scenesconfig") 

# Setup the Mitsuba renderer
mts = MitsubaRenderer.MitsubaRenderer(mts_dir, results_dir, scenes_dir, deps_dir = mts_deps)

#for each scene and each scene variant
for scene, scene_variants, resolution in scenes:
    for variant in scene_variants:
        #run each test case defined in the test cases file
        for testCase in testCases:    
            mts.runTestCase(scene, variant, resolution, testCase, spp = 16)

#after running all test cases for all scenes prepare the results in an interactive HTML viewer 
viewer = ResultsViewer.ResultsViewer("./utils/webviewer")
viewer.generateHTMLS(viewer_output_dir, results_dir, scenes_dir, scenes, testCaseDescription, testCases, showReference=False, perScene=False)