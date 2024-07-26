import renderer.blender.BlenderRenderer as BlenderRenderer
import utils.TestCaseHelper as TestCaseHelper
import utils.SceneHelper as SceneHelper

import utils.ResultsViewer as ResultsViewer

# path to the Blender installation (e.g., folder or a soft link to it)
blender_dir = "./blender-renderer/"

# path to store the results
results_dir = "./blender-results/guiding"
# path to store the post-processed results and the HTML viewer
viewer_output_dir = "./blender-viewers/guiding"

# Loading the test case descriptions from a file
testCases = TestCaseHelper.loadTestCases("examples/blender/testcases/guiding")
testCaseDescription = TestCaseHelper.loadTestCaseDescription("examples/blender/testcases/guiding")

# Loading the scenes to run the test cases (e.g., blender-scenes can be a folder or a soft link to it)
[scenes, scenes_dir] = SceneHelper.loadScenes("blender-scenes/scenesconfig") 

# Setup the Blender renderer
blender = BlenderRenderer.BlenderRenderer(blender_dir, results_dir, scenes_dir)

#for each scene and each scene variant
for scene, scene_variants, resolution in scenes:
    for variant in scene_variants:
        #run each test case defined in the test cases file
        for testCase in testCases:    
            blender.runTestCase(scene, variant, resolution, testCase, spp = 16, deleteTestCaseJSON=True)

#after running all test cases for all scenes prepare the results in an interactive HTML viewer 
viewer = ResultsViewer.ResultsViewer("./utils/webviewer")
viewer.generateHTMLS(viewer_output_dir, results_dir, scenes_dir, scenes, testCaseDescription, testCases, showReference=False, perScene=False)

