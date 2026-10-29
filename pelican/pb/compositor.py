"""Compositing: aerial perspective from the mist pass, bloom, lens dispersion,
grade and vignette."""
import bpy


def _try_set(node, **kw):
    for k, v in kw.items():
        if k in node.inputs:
            node.inputs[k].default_value = v
        elif hasattr(node, k):
            setattr(node, k, v)


def setup(scene, haze=(0.62, 0.55, 0.62)):
    scene.use_nodes = True
    w = scene.world
    w.mist_settings.start = 80.0
    w.mist_settings.depth = 2200.0
    w.mist_settings.falloff = 'LINEAR'
    nt = scene.node_tree
    nt.nodes.clear()
    N, L = nt.nodes, nt.links
    rl = N.new('CompositorNodeRLayers')
    # aerial perspective on geometry only (the sky already has its own)
    depth_mask = N.new('CompositorNodeMapRange')
    _try_set(depth_mask, **{'From Min': 20000.0, 'From Max': 20001.0, 'To Min': 1.0, 'To Max': 0.0})
    depth_mask.use_clamp = True
    L.new(rl.outputs['Depth'], depth_mask.inputs[0])
    mist = N.new('CompositorNodeMath')
    mist.operation = 'MULTIPLY'
    L.new(rl.outputs['Mist'], mist.inputs[0])
    L.new(depth_mask.outputs[0], mist.inputs[1])
    fac = N.new('CompositorNodeMath')
    fac.operation = 'MULTIPLY'
    fac.inputs[1].default_value = 0.75
    L.new(mist.outputs[0], fac.inputs[0])
    hz = N.new('CompositorNodeMixRGB')
    hz.blend_type = 'MIX'
    L.new(fac.outputs[0], hz.inputs[0])
    L.new(rl.outputs['Image'], hz.inputs[1])
    hz.inputs[2].default_value = (*haze, 1.0)
    # bloom
    glare = N.new('CompositorNodeGlare')
    glare.glare_type = 'FOG_GLOW'
    _try_set(glare, quality='HIGH', threshold=1.0, size=8, mix=-0.75)
    _try_set(glare, **{'Threshold': 1.4, 'Strength': 0.22, 'Size': 0.62})
    L.new(rl.outputs['Image'], glare.inputs[0])
    # streaks for the sun / lamp highlights
    streak = N.new('CompositorNodeGlare')
    streak.glare_type = 'STREAKS'
    _try_set(streak, quality='HIGH', threshold=8.0, streaks=6, angle_offset=0.3, fade=0.86, mix=-0.93)
    _try_set(streak, **{'Threshold': 12.0, 'Strength': 0.06, 'Streaks': 6, 'Fade': 0.84})
    L.new(glare.outputs[0], streak.inputs[0])
    lens = N.new('CompositorNodeLensdist')
    _try_set(lens, use_fit=False)
    if 'Dispersion' in lens.inputs:
        lens.inputs['Dispersion'].default_value = 0.012
        lens.inputs['Distortion'].default_value = -0.008
    L.new(streak.outputs[0], lens.inputs[0])
    # grade: cool shadows, warm highlights
    cb = N.new('CompositorNodeColorBalance')
    cb.correction_method = 'LIFT_GAMMA_GAIN'
    try:
        cb.lift = (0.985, 0.99, 1.025)
        cb.gamma = (1.0, 0.995, 1.0)
        cb.gain = (1.035, 1.0, 0.985)
    except Exception:
        pass
    L.new(lens.outputs[0], cb.inputs[1])
    # vignette
    ell = N.new('CompositorNodeEllipseMask')
    _try_set(ell, width=0.92, height=0.86)
    if 'Size' in ell.inputs:
        ell.inputs['Size'].default_value = (0.92, 0.86)
    blur = N.new('CompositorNodeBlur')
    _try_set(blur, filter_type='GAUSS', size_x=260, size_y=260, use_relative=False)
    L.new(ell.outputs[0], blur.inputs[0])
    vig = N.new('CompositorNodeMapRange')
    _try_set(vig, **{'From Min': 0.0, 'From Max': 1.0, 'To Min': 0.55, 'To Max': 1.0})
    L.new(blur.outputs[0], vig.inputs[0])
    mul = N.new('CompositorNodeMixRGB')
    mul.blend_type = 'MULTIPLY'
    L.new(vig.outputs[0], mul.inputs[0])
    L.new(cb.outputs[0], mul.inputs[1])
    mul.inputs[2].default_value = (0.0, 0.0, 0.0, 1.0)
    # multiply mix: fac=1 at centre means full black?  use mix of image and image*vig instead
    mulv = N.new('CompositorNodeMixRGB')
    mulv.blend_type = 'MULTIPLY'
    mulv.inputs[0].default_value = 1.0
    L.new(cb.outputs[0], mulv.inputs[1])
    L.new(vig.outputs[0], mulv.inputs[2])
    nt.nodes.remove(mul)
    comp = N.new('CompositorNodeComposite')
    L.new(mulv.outputs[0], comp.inputs[0])
    view = N.new('CompositorNodeViewer')
    L.new(mulv.outputs[0], view.inputs[0])
    return nt
