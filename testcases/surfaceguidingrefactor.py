test_case_description = {
    "title" : "Guiding tests in PBRT",
    "short" : "Comparing path tracing with and without path guiding using PBRT's guided integrator.",
    "long" : "This test compares ."
}

common_parameters = {
    "integrator": "guidedpath",
    "maxdepth" : ["integer", 15],
    "minrrdepth" : ["integer", 5],
    "usenee" : ["bool", True],
    "enableguiding" : ["bool", False],
}

test_cases = {
    "surface_guiding_refactor" : {
        "parameters" : {
            "enableguiding" : ["bool", True],
            "surfaceguidingtype" : ["string", "mis"],
            
        },
        "description" : "Guided Path tracer",
    }
}