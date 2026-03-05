#!/usr/bin/env python3
# Apache License, Version 2.0


import argparse
import pathlib
import sys
import json

def disableRenderLayers(view_layer, visible_layers=[]):
    layerList = [
        'z',
        'mist',
        'position',
        'normal',
        'vector',
        'uv',
        'object_index',
        'debug_sample_count',
        'diffuse_direct',
        'diffuse_indirect',
        'diffuse_color',
        'glossy_direct',
        'glossy_indirect',
        'glossy_color',
        'transmission_direct',
        'transmission_indirect',
        'transmission_color',
        'volume_direct',
        'volume_indirect',
        'emit',
        'environment',
        'shadow',
        'shadow_catcher',
        'ambient_occlusion',
        'subsurface_color',
        'subsurface_direct',
        'subsurface_indirect',
        ]

    for layer in layerList:
        if(hasattr(view_layer, "use_pass_"+layer)):
            setattr(view_layer, "use_pass_"+layer, False)
    if(hasattr(view_layer.cycles, "denoising_store_passes")):
        setattr(view_layer.cycles, "denoising_store_passes", False)	

    view_layer.name = "Cycles"

    if len(visible_layers) == 0:
        if(hasattr(view_layer, "use_pass_"+ "combined")):
            setattr(view_layer, "use_pass_"+ "combined", True)	

    else:
        for layer in visible_layers:
            print()
            if layer == "denoising_store_passes":
                if(hasattr(view_layer.cycles, "denoising_store_passes")):
                    setattr(view_layer.cycles, "denoising_store_passes", True)
            else:
                if(hasattr(view_layer, "use_pass_"+layer)):
                    setattr(view_layer, "use_pass_"+layer, True)	

class ArgumentParserForBlender(argparse.ArgumentParser):
    """
    This class is identical to its superclass, except for the parse_args
    method (see docstring). It resolves the ambiguity generated when calling
    Blender from the CLI with a python script, and both Blender and the script
    have arguments. E.g., the following call will make Blender crash because
    it will try to process the script's -a and -b flags:
    >>> blender --python my_script.py -a 1 -b 2

    To bypass this issue this class uses the fact that Blender will ignore all
    arguments given after a double-dash ('--'). The approach is that all
    arguments before '--' go to Blender, arguments after go to the script.
    The following calls work fine:
    >>> blender --python my_script.py -- -a 1 -b 2
    >>> blender --python my_script.py --
    """

    def _get_argv_after_doubledash(self):
        """
        Given the sys.argv as a list of strings, this method returns the
        sublist right after the '--' element (if present, otherwise returns
        an empty list).
        """
        try:
            idx = sys.argv.index("--")
            return sys.argv[idx+1:] # the list after '--'
        except ValueError as e: # '--' not in the list:
            return []

    # overrides superclass
    def parse_args(self):
        """
        This method is expected to behave identically as in the superclass,
        except that the sys.argv list will be pre-processed using
        _get_argv_after_doubledash before. See the docstring of the class for
        usage examples and details.
        """
        return super().parse_args(args=self._get_argv_after_doubledash())

parser = ArgumentParserForBlender()


parser.add_argument("-j", "--json",
                    help="JSON file for the test case")
args = parser.parse_args()

TESTCASEJSON = args.json

f = open(TESTCASEJSON)
testcase_parameters = json.load(f)

import bpy

scene = bpy.context.scene

visible_layers=testcase_parameters["visible_layers"]
scene.render.image_settings.file_format = 'OPEN_EXR'
if len(visible_layers) > 0:
    scene.render.image_settings.media_type = 'MULTI_LAYER_IMAGE'
else:
    scene.render.image_settings.media_type = 'IMAGE'

view_layer = bpy.context.view_layer
disableRenderLayers(view_layer, visible_layers)

scene.use_nodes = False

for parameter in testcase_parameters:
      print(parameter, " = ", testcase_parameters[parameter])
      if parameter.startswith("cycles."):
        cycles_parameter = parameter.replace("cycles.","")
        setattr(scene.cycles, cycles_parameter, testcase_parameters[parameter])
      elif parameter.startswith("render."):
        render_parameter = parameter.replace("render.","")
        setattr(scene.render, render_parameter, testcase_parameters[parameter])

bpy.ops.render.render(write_still=True)
