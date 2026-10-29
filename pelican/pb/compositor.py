"""Compositing: bloom, sun streaks, lens dispersion and a colour grade.
(Vignette and film grain are applied at encode time with ffmpeg.)"""
import bpy


def _try_set(node, **kw):
    for k, v in kw.items():
        if k in node.inputs:
            node.inputs[k].default_value = v
        elif hasattr(node, k):
            setattr(node, k, v)


def setup(scene):
    scene.use_nodes = True
    nt = scene.node_tree
    nt.nodes.clear()
    N, L = nt.nodes, nt.links
    rl = N.new('CompositorNodeRLayers')
    # bloom
    glare = N.new('CompositorNodeGlare')
    glare.glare_type = 'FOG_GLOW'
    _try_set(glare, quality='MEDIUM')
    _try_set(glare, **{'Threshold': 1.4, 'Strength': 0.22, 'Size': 0.62})
    L.new(rl.outputs['Image'], glare.inputs[0])
    # streaks for the sun / lamp highlights
    streak = N.new('CompositorNodeGlare')
    streak.glare_type = 'STREAKS'
    _try_set(streak, quality='MEDIUM')
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
    comp = N.new('CompositorNodeComposite')
    L.new(cb.outputs[0], comp.inputs[0])
    return nt
