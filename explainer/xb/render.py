"""Cycles settings for vertical (9:16) explainer shorts."""
import bpy


def setup(scene, res=(1080, 1920), samples=12, fps=24, motion_blur=True, noise_threshold=0.04):
    r = scene.render
    r.engine = 'CYCLES'
    r.resolution_x, r.resolution_y = res
    r.resolution_percentage = 100
    r.fps = fps
    r.use_motion_blur = motion_blur
    r.motion_blur_shutter = 0.5
    r.use_persistent_data = True
    r.film_transparent = False
    c = scene.cycles
    c.device = 'CPU'
    c.samples = samples
    c.use_adaptive_sampling = True
    c.adaptive_threshold = noise_threshold
    c.adaptive_min_samples = 4
    c.use_denoising = True
    c.denoiser = 'OPENIMAGEDENOISE'
    c.denoising_input_passes = 'RGB_ALBEDO_NORMAL'
    c.denoising_prefilter = 'ACCURATE'
    c.denoising_quality = 'BALANCED'
    c.max_bounces = 6
    c.diffuse_bounces = 2
    c.glossy_bounces = 2
    c.transmission_bounces = 4
    c.transparent_max_bounces = 8
    c.volume_bounces = 0
    c.sample_clamp_indirect = 8.0
    c.use_light_tree = True
    c.use_auto_tile = False
    c.blur_glossy = 0.5
    scene.view_settings.view_transform = 'AgX'
    scene.view_settings.look = 'AgX - Medium High Contrast'
    scene.view_settings.exposure = 0.0
    r.image_settings.file_format = 'PNG'
    r.image_settings.color_depth = '8'


def world(scene, color=(0.05, 0.045, 0.04), strength=1.0):
    w = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
    scene.world = w
    w.use_nodes = True
    bg = w.node_tree.nodes.get('Background')
    bg.inputs[0].default_value = (*color, 1.0)
    bg.inputs[1].default_value = strength
    return w


def cheap_emitters(keep=('LampShade',)):
    """Emissive surfaces that only need to glow, not light the scene, skip light sampling (big speed-up
    for skin that turns emissive under x-ray and for large backdrops)."""
    for m in bpy.data.materials:
        if m.name not in keep:
            m.cycles.emission_sampling = 'NONE'
