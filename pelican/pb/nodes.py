"""Tiny DSL for building shader node trees from Python.

    m, n = new_material("Paint")
    noise = n.node('ShaderNodeTexNoise', Scale=40.0)
    bsdf = n.principled(base=(0.1, 0.4, 0.4), roughness=noise.outputs['Fac'])
    n.out(bsdf)

Input values may be constants or output sockets (which get linked).
"""
import bpy


class Nodes:
    def __init__(self, tree):
        self.tree = tree
        self.nodes = tree.nodes
        self.links = tree.links
        self._x = 0

    def node(self, kind, _name=None, _props=None, **inputs):
        nd = self.nodes.new(kind)
        if _name:
            nd.name = nd.label = _name
        nd.location = (self._x, 0)
        self._x += 200
        for k, val in (_props or {}).items():
            setattr(nd, k, val)
        for k, val in inputs.items():
            self.set(nd, k, val)
        return nd

    def set(self, nd, key, val):
        if isinstance(key, int):
            sock = nd.inputs[key]
        else:
            sock = nd.inputs.get(key)
            if sock is None:
                key2 = key.replace('_', ' ')
                sock = nd.inputs.get(key2)
            if sock is None:
                raise KeyError(f"{nd.bl_idname} has no input {key!r}: "
                               f"{[s.name for s in nd.inputs]}")
        if isinstance(val, bpy.types.NodeSocket):
            self.links.new(val, sock)
        elif isinstance(val, bpy.types.Node):
            self.links.new(val.outputs[0], sock)
        else:
            if isinstance(val, (tuple, list)) and len(val) == 3 and sock.type == 'RGBA':
                val = (*val, 1.0)
            sock.default_value = val
        return sock

    def link(self, a, b):
        if isinstance(a, bpy.types.Node):
            a = a.outputs[0]
        if isinstance(b, bpy.types.Node):
            b = b.inputs[0]
        self.links.new(a, b)

    # ---- convenience wrappers -------------------------------------------
    def math(self, op, a, b=None, c=None, clamp=False):
        nd = self.node('ShaderNodeMath', _props=dict(operation=op, use_clamp=clamp))
        self.set(nd, 0, a)
        if b is not None:
            self.set(nd, 1, b)
        if c is not None:
            self.set(nd, 2, c)
        return nd.outputs[0]

    def vmath(self, op, a, b=None, scale=None):
        nd = self.node('ShaderNodeVectorMath', _props=dict(operation=op))
        self.set(nd, 0, a)
        if b is not None:
            self.set(nd, 1, b)
        if scale is not None:
            self.set(nd, 'Scale', scale)
        out = 'Value' if op in ('DOT_PRODUCT', 'LENGTH', 'DISTANCE') else 'Vector'
        return nd.outputs[out]

    def mix(self, fac, a, b, blend='MIX', dtype='RGBA', clamp=False):
        nd = self.node('ShaderNodeMix', _props=dict(data_type=dtype, blend_type=blend,
                                                    clamp_result=clamp))
        if dtype == 'RGBA':
            self.set(nd, 0, fac)
            self.set(nd, 6, a)
            self.set(nd, 7, b)
            return nd.outputs[2]
        if dtype == 'FLOAT':
            self.set(nd, 0, fac)
            self.set(nd, 2, a)
            self.set(nd, 3, b)
            return nd.outputs[0]
        self.set(nd, 0, fac)
        self.set(nd, 4, a)
        self.set(nd, 5, b)
        return nd.outputs[1]

    def ramp(self, fac, stops, interp='LINEAR'):
        nd = self.node('ShaderNodeValToRGB')
        cr = nd.color_ramp
        cr.interpolation = interp
        while len(cr.elements) > len(stops):
            cr.elements.remove(cr.elements[-1])
        while len(cr.elements) < len(stops):
            cr.elements.new(0.5)
        for el, (pos, col) in zip(cr.elements, stops):
            el.position = pos
            if isinstance(col, (int, float)):
                col = (col, col, col, 1.0)
            elif len(col) == 3:
                col = (*col, 1.0)
            el.color = col
        self.set(nd, 'Fac', fac)
        return nd.outputs['Color']

    def maprange(self, val, a, b, c=0.0, d=1.0, clamp=True, interp='LINEAR'):
        nd = self.node('ShaderNodeMapRange', _props=dict(clamp=clamp, interpolation_type=interp))
        self.set(nd, 'Value', val)
        self.set(nd, 'From Min', a)
        self.set(nd, 'From Max', b)
        self.set(nd, 'To Min', c)
        self.set(nd, 'To Max', d)
        return nd.outputs['Result']

    def texcoord(self, which='Object'):
        if not hasattr(self, '_tc'):
            self._tc = self.node('ShaderNodeTexCoord')
        return self._tc.outputs[which]

    def attr(self, name, out='Fac', kind='GEOMETRY'):
        nd = self.node('ShaderNodeAttribute', _props=dict(attribute_name=name, attribute_type=kind))
        return nd.outputs[out]

    def mapping(self, vec, loc=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        nd = self.node('ShaderNodeMapping', Vector=vec, Location=loc, Rotation=rot, Scale=scale)
        return nd.outputs[0]

    def noise(self, vec=None, scale=5.0, detail=2.0, rough=0.5, dist=0.0, dims='3D', w=None):
        nd = self.node('ShaderNodeTexNoise', _props=dict(noise_dimensions=dims),
                       Scale=scale, Detail=detail, Roughness=rough, Distortion=dist)
        if vec is not None:
            self.set(nd, 'Vector', vec)
        if w is not None:
            self.set(nd, 'W', w)
        return nd

    def voronoi(self, vec=None, scale=5.0, feature='F1', metric='EUCLIDEAN', rand=1.0, dims='3D'):
        nd = self.node('ShaderNodeTexVoronoi', _props=dict(feature=feature, distance=metric,
                                                           voronoi_dimensions=dims),
                       Scale=scale, Randomness=rand)
        if vec is not None:
            self.set(nd, 'Vector', vec)
        return nd

    def wave(self, vec=None, scale=5.0, dist=0.0, detail=2.0, kind='BANDS', axis='X',
             profile='SIN', dscale=1.0):
        nd = self.node('ShaderNodeTexWave', _props=dict(wave_type=kind, bands_direction=axis,
                                                        wave_profile=profile),
                       Scale=scale, Distortion=dist, Detail=detail)
        nd.inputs['Detail Scale'].default_value = dscale
        if vec is not None:
            self.set(nd, 'Vector', vec)
        return nd

    def bump(self, height, strength=0.2, distance=0.01, normal=None):
        nd = self.node('ShaderNodeBump', Strength=strength, Distance=distance, Height=height)
        if normal is not None:
            self.set(nd, 'Normal', normal)
        return nd.outputs['Normal']

    def principled(self, base=(0.8, 0.8, 0.8), roughness=0.5, metallic=0.0, **kw):
        nd = self.node('ShaderNodeBsdfPrincipled')
        self.set(nd, 'Base Color', base)
        self.set(nd, 'Roughness', roughness)
        self.set(nd, 'Metallic', metallic)
        alias = {
            'normal': 'Normal', 'ior': 'IOR', 'alpha': 'Alpha',
            'sss': 'Subsurface Weight', 'sss_radius': 'Subsurface Radius',
            'sss_scale': 'Subsurface Scale', 'spec': 'Specular IOR Level',
            'coat': 'Coat Weight', 'coat_rough': 'Coat Roughness',
            'coat_normal': 'Coat Normal', 'sheen': 'Sheen Weight',
            'sheen_rough': 'Sheen Roughness', 'sheen_tint': 'Sheen Tint',
            'emission': 'Emission Color', 'emission_strength': 'Emission Strength',
            'transmission': 'Transmission Weight', 'aniso': 'Anisotropic',
            'aniso_rot': 'Anisotropic Rotation', 'tangent': 'Tangent',
            'thin_film': 'Thin Film Thickness', 'spec_tint': 'Specular Tint',
            'coat_tint': 'Coat Tint',
        }
        for k, val in kw.items():
            self.set(nd, alias.get(k, k), val)
        return nd

    def out(self, surface, volume=None, displacement=None):
        o = self.node('ShaderNodeOutputMaterial')
        self.link(surface if isinstance(surface, bpy.types.NodeSocket) else surface.outputs[0],
                  o.inputs['Surface'])
        if volume is not None:
            self.link(volume, o.inputs['Volume'])
        if displacement is not None:
            self.link(displacement, o.inputs['Displacement'])
        return o


def new_material(name):
    m = bpy.data.materials.get(name)
    if m is not None:
        bpy.data.materials.remove(m)
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    m.node_tree.nodes.clear()
    return m, Nodes(m.node_tree)


def simple_material(name, base, roughness=0.5, metallic=0.0, **kw):
    m, n = new_material(name)
    n.out(n.principled(base=base, roughness=roughness, metallic=metallic, **kw))
    m.diffuse_color = (*base[:3], 1.0) if len(base) == 3 else base
    return m
