test_case_description = {
    "title" : "Guiding tests in PBRT",
    "short" : "Comparing path tracing with and without path guiding using PBRT's guided integrator.",
    "long" : "This test compares ."
}

common_parameters = {
    "karma:global:causticsenable" : ["bool", True],
    "karma:global:causticsroughnessclamp" : ["float", 0.001],

    "karma:object:causticsenable" : ["bool", True],
    "karma:object:causticsroughnessclamp" : ["float", 0.001],

    "karma:global:colorlimit" : ["float", 1000.0],
    "karma:global:colorlimitindirect" : ["float", 1000.0],
    "karma:global:convergence_mode" : ["int", 0],
    
    "karma:object:diffuselimit" : ["int", 15],
    "karma:object:reflectlimit" : ["int", 15],
    "karma:object:diffuselimit" : ["int", 15],
    "karma:object:refractlimit" : ["int", 15],

    "karma:global:diffuselimit" : ["int", 15],
    "karma:global:reflectlimit" : ["int", 15],
    "karma:global:diffuselimit" : ["int", 15],
    "karma:global:refractlimit" : ["int", 15],

    "karma:global:russianroulette_cutoff" : ["int", 15],
    "karma:object:russianroulette_cutoff" : ["int", 15],
}

test_cases = {
    "pt-no-guiding" : {
        "parameters" : {
            "karma:global:guiding_enable" : ["bool", False],
            "karma:global:guiding_samples" : ["int", 0],
        },
        "description" : "Standard Path tracer",
    },

    "pt-surfaceguiding" : {
        "parameters" : {
            "karma:global:guiding_enable" : ["bool", True],
            "karma:global:guiding_samples" : ["int", 0],
        },
        "description" : "Standard Path tracer",
    },
}