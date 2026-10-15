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
    "no_guiding" : {
        "parameters" : {

        },
        "description" : "Standard Path tracer",
    },
    "surface_guiding_RIS" : {
        "parameters" : {
            "enableguiding" : ["bool", True],
            "surfaceguidingtype" : ["string", "ris"],
        },
        "description" : "Guided Path tracer",
    },
    "surface_guiding_MIS" : {
        "parameters" : {
            "enableguiding" : ["bool", True],
            "surfaceguidingtype" : ["string", "mis"],
            
        },
        "description" : "Guided Path tracer",
    }
}