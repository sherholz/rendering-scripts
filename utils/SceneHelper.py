import os, sys, importlib

def loadScenes(scenes_cfg):
    testCases = []
    sys.path.append(os.path.dirname(scenes_cfg))
    scenesCfg = importlib.import_module(os.path.basename(scenes_cfg))
    if scenesCfg.scenes_directory.startswith("$HERE$"):
        scenesCfg.scenes_directory = scenesCfg.scenes_directory.replace("$HERE$", os.path.dirname(scenes_cfg))
    return [scenesCfg.scenes, scenesCfg.scenes_directory]