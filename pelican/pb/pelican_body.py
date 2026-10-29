"""Pelican body/neck/head surface from a signed distance field."""
import numpy as np

from . import pose as P
from . import sdf


def body_field(Pts):
    e = lambda d: sdf.ellipsoid(Pts, d['c'], d['r'], d['R'])
    body = e(P.BODY)
    body = sdf.smin(body, e(P.BELLY), 0.06)
    body = sdf.smin(body, e(P.CHEST), 0.07)
    body = sdf.smin(body, e(P.BACK), 0.05)
    body = sdf.smin(body, e(P.TAIL), 0.05)
    for s in (1, -1):
        th = dict(P.THIGH)
        c = np.array(th['c'], dtype=float)
        c[1] *= s
        th['c'] = c
        body = sdf.smin(body, e(th), 0.04)
    neck = sdf.tube(Pts, P.NECK_PTS, P.NECK_R)
    d = sdf.smin(body, neck, 0.07)
    head = e(P.HEAD)
    head = sdf.smin(head, e(P.FOREHEAD), 0.025)
    head = sdf.smin(head, e(P.CHEEK), 0.02)
    head = sdf.smin(head, e(P.NAPE), 0.03)
    # shallow eye socket groove + brow ridge
    for s in (1, -1):
        eye = np.array(P.EYE)
        eye[1] *= s
        sock = sdf.ellipsoid(Pts, eye + np.array([0.0, 0.004 * s, 0.0]), (0.014, 0.008, 0.011))
        head = sdf.smax(head, -sock, 0.008)
    # flatten the bill-base so the bill seats nicely
    d = sdf.smin(d, head, 0.035)
    return d


def build_body_mesh(step=0.0034):
    lo = np.array([-0.02, -0.19, 0.46])
    hi = np.array([0.76, 0.19, 1.16])
    Pts, axes = sdf.grid(lo, hi, step)
    field = body_field(Pts.reshape(-1, 3)).reshape(Pts.shape[:3])
    verts, faces = sdf.polygonize(field, axes, step)
    verts = sdf.laplacian_smooth(verts, faces, iterations=6)
    return verts, faces
