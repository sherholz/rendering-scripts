# rendering-scripts
A selection of scripts to run and evaluate rendering experiments supporting different renderers.

# Dependencies

``` bash
pip install simpleimageio opencv-python numpy
```

# Examples

## Mitsuba

``` bash
PYTHONPATH=$PYTHONPATH:$PWD python3 ./examples/mitsuba/runMitsubaReferenceTestCase.py
```

## PBRT

``` bash
PYTHONPATH=$PYTHONPATH:$PWD python3 ./examples/pbrt/runPBRTSurfaceGuidingTestCase.py
```

## SideFX Blender

``` bash
PYTHONPATH=$PYTHONPATH:$PWD python3 ./examples/blender/runBlenderGuidingTestCase.py
```

## SideFX Karma

``` bash
PYTHONPATH=$PYTHONPATH:$PWD python3 ./examples/karma/runKarmaGuidingTestCase.py
```
