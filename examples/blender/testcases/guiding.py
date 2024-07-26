test_case_description = {
    "title" : "Guiding tests in Blender/Cycles",
    "short" : "Comparing path tracing with and without path guiding using Blender's Cycles renderer.",
    "long" : "This test compares ."
}
common_parameters = {
    "render.engine" : 'CYCLES',
    "cycles.device" : 'CPU',
    "cycles.use_adaptive_sampling" : False, 
    "cycles.time_limit" : 0.0,

    #Advanced
    "cycles.min_light_bounces" : 16,
    "cycles.min_transparent_bounces" : 16,
    "cycles.light_sampling_threshold" : 0.0,
    #Light Paths
    "cycles.max_bounces" : 16,
    "cycles.diffuse_bounces" : 16,
    "cycles.glossy_bounces" : 16,
    "cycles.transmission_bounces" : 16,
    "cycles.volume_bounces" : 16,
    "cycles.transparent_max_bounces" : 16,
    #Guiding
    "cycles.use_guiding" : False,
    "cycles.use_deterministic_guiding" : True,
    "cycles.use_surface_guiding" : True,
    "cycles.surface_guiding_probability" : 0.5,
    "cycles.use_volume_guiding" : True,
    "cycles.volume_guiding_probability" : 0.5,
    "cycles.guiding_distribution_type" : "PARALLAX_AWARE_VMM",

    #Clamping
    "cycles.sample_clamp_direct" : 0.0,
    "cycles.sample_clamp_indirect" : 0.0,

    #Caustics
    "cycles.blur_glossy" : 0.0,
    "cycles.caustics_reflective" : True,
    "cycles.caustics_refractive" : True,

    "cycles.use_denoising" : False,
    "cycles.use_adaptive_sampling" : False,
    "cycles.pixel_filter_type" : 'BOX',
}

test_cases = {
    "no-guiding-no-lbvh" : {
        "parameters" : {
            "cycles.use_guiding" : False,
            "cycles.use_light_tree" : False,
        },
        "description" : "Guided Path tracer",
    },
    "no-guiding-lbvh" : {
        "parameters" : {
            "cycles.use_guiding" : False,
            "cycles.use_light_tree" : True,
        },
        "description" : "Guided Path tracer",
    },
    "guiding-no-lbvh" : {
        "parameters" : {
            "cycles.use_guiding" : True,
            "cycles.use_light_tree" : False,
        },
        "description" : "Guided Path tracer",
    },
    "guiding-lbvh" : {
        "parameters" : {
            "cycles.use_guiding" : True,
            "cycles.use_light_tree" : True,
        },
        "description" : "Guided Path tracer",
    },
}
