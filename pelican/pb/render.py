"""Cycles render configuration."""
import bpy


def setup(scene, res=(1920, 1080), samples=48, pct=100, fps=24, motion_blur=True,
          noise_threshold=0.03, preview=False):
    r = scene.render
    r.engine = 'CYCLES'
    r.resolution_x, r.resolution_y = res
    r.resolution_percentage = pct
    r.fps = fps
    r.film_transparent = False
    r.use_persistent_data = True
    r.use_motion_blur = motion_blur
    r.motion_blur_shutter = 0.5
    r.image_settings.file_format = 'PNG'
    r.image_settings.color_depth = '16'
    r.image_settings.compression = 15

    c = scene.cycles
    c.device = 'CPU'
    c.samples = samples
    c.use_adaptive_sampling = True
    c.adaptive_threshold = noise_threshold
    c.adaptive_min_samples = 0
    c.use_denoising = True
    c.denoiser = 'OPENIMAGEDENOISE'
    c.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
    c.denoising_prefilter = 'ACCURATE'
    c.denoising_quality = 'HIGH'
    c.adaptive_min_samples = 4
    c.max_bounces = 6
    c.diffuse_bounces = 2
    c.glossy_bounces = 2
    c.transmission_bounces = 4
    c.volume_bounces = 0
    c.transparent_max_bounces = 6
    c.caustics_reflective = False
    c.caustics_refractive = False
    c.blur_glossy = 1.0
    c.sample_clamp_indirect = 6.0
    c.sample_clamp_direct = 0.0
    c.use_light_tree = True
    c.light_sampling_threshold = 0.01
    c.motion_blur_position = 'CENTER'
    c.film_exposure = 1.0
    c.pixel_filter_type = 'BLACKMAN_HARRIS'
    c.filter_width = 1.5
    c.seed = 7
    c.use_animated_seed = True
    c.texture_limit_render = 'OFF'
    try:
        c.use_auto_tile = True
        c.tile_size = 1024
    except AttributeError:
        pass
    if preview:
        c.samples = max(4, samples)
        c.denoising_prefilter = 'FAST'

    vs = scene.view_settings
    vs.view_transform = 'AgX'
    vs.look = 'AgX - Medium High Contrast'
    vs.exposure = 0.0
    vs.gamma = 1.0
    scene.display_settings.display_device = 'sRGB'
    scene.sequencer_colorspace_settings.name = 'sRGB'

    if scene.world is not None:
        scene.world.cycles.sampling_method = 'MANUAL'
        scene.world.cycles.sample_map_resolution = 256
    # decorative glows are seen, not used as light sources
    for m in bpy.data.materials:
        if m.name in ('Building', 'LanternGlass', 'Bulb', 'LampEmit', 'Reflector'):
            m.cycles.emission_sampling = 'NONE'
    for ob in bpy.data.objects:
        if ob.name in ('Ocean', 'OceanFar', 'Deck', 'PierStructure', 'Railings', 'Town', 'Hills',
                       'Beach', 'Headland'):
            ob.cycles.use_motion_blur = False
    vl = scene.view_layers[0]
    vl.use_pass_mist = True
    vl.use_pass_z = True
