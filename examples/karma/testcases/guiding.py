test_case_description = {
    "title" : "Karma Path Guiding Test",
    "short" : "Comparing path tracing with and without path guiding using SideFX's Karma renderer.",
    "long" : "In this (equal-spp) test, Karma is set up to generate unbiased, path traced rendering results (no colorlimits, caustics enabled, long diffuse, refract, and refract limits), without and with path guiding enabled."
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
        "description" : "Standard umbiased path tracer",
    },

    "pt-surfaceguiding" : {
        "parameters" : {
            "karma:global:guiding_enable" : ["bool", True],
            "karma:global:guiding_samples" : ["int", 0],
        },
        "description" : "Surface guided unbiased path tracer",
    },
}