test_case_description = {
    "title" : "Guiding tests in PBRT",
    "short" : "Comparing path tracing with and without path guiding using PBRT's guidedvolpath integrator.",
    "long" : "This test compares ."
}

common_parameters = {
    "integrator": "guidedvolpath",
    "maxdepth" : ["integer", 20],
    "minrrdepth" : ["integer", 20],
    "usenee" : ["bool", True],
    "surfaceguiding" : ["bool", False],
    "volumeguiding" : ["bool", False],
}

test_cases = {
        "volume_surface_guiding" : {
        "parameters" : {
            "surfaceguiding" : ["bool", True],
            "volumeguiding" : ["bool", True],
        },
        "description" : "Guided Path tracer",
    }
}
