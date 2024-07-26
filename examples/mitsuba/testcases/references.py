test_case_description = {
    "title" : "Reference renderings using Mitsuba",
    "short" : "Rendering reference images using the guidedprogressivevolpath integrator of Mitsuba.",
    "long" : "This test compares ."
}

common_parameters = {
    "INTEGRATOR_SETTINGS": "guidedprogressivevolpath",
    "__SAMPLER__": "deterministic",
    "trainingSamples": 128,
    #"sampleCount": 32768,
    "sampleCount": 256,
    "maxdepth" :20,
    "rrDepth" : 20,
    "useNee" : True,
    "useVolumeGuiding" : False,
    "useSurfaceGuiding" : False,
}

test_cases = {
        "preparecaches" : {
            "parameters" : {
                "sampleCount": 128,
                "trainingSamples": 128,
                "savePixelEstimate" : True,
                
                "pixelEstimateFile" : "$SCENE$-est.exr",
                "saveGuidingCaches" : True,
                "guidingCachesFile" : "$SCENE$-guidingCaches.field",

                "useVolumeGuiding" : True,
                "useSurfaceGuiding" : True,
            },
            "description" : "Guided Path tracer",
        },
        "reference" : {
        "parameters" : {
            "useVolumeGuiding" : True,
            "useSurfaceGuiding" : True,
            "loadGuidingCaches" : True,
            "guidingCachesFile" : "$SCENE$-guidingCaches.field",
        },
        "description" : "Guided Path tracer",
        },  
}
