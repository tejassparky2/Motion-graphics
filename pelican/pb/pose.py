"""Rest pose of the pelican in bike space (+X forward, +Z up, metres).

The bird is modelled directly in its riding pose; the rig only adds motion.
"""
import math

import numpy as np

from .sdf import rot_y

DEG = math.pi / 180

SADDLE = np.array([0.268, 0.0, 0.546])

# ---- torso ------------------------------------------------------------------
BODY = dict(c=(0.322, 0, 0.700), r=(0.300, 0.150, 0.135), R=rot_y(-18 * DEG))
BELLY = dict(c=(0.300, 0, 0.655), r=(0.220, 0.132, 0.100), R=rot_y(-10 * DEG))
CHEST = dict(c=(0.528, 0, 0.770), r=(0.102, 0.116, 0.112), R=rot_y(-10 * DEG))
BACK = dict(c=(0.330, 0, 0.765), r=(0.240, 0.130, 0.085), R=rot_y(-18 * DEG))
TAIL = dict(c=(0.082, 0, 0.615), r=(0.112, 0.070, 0.045), R=rot_y(-15 * DEG))
THIGH = dict(c=(0.322, 0.088, 0.620), r=(0.070, 0.050, 0.062), R=rot_y(-10 * DEG))

# ---- neck & head --------------------------------------------------------------
NECK_PTS = np.array([[0.540, 0, 0.825], [0.566, 0, 0.898], [0.557, 0, 0.958],
                     [0.562, 0, 1.012], [0.598, 0, 1.054], [0.642, 0, 1.075]])
NECK_R = np.array([0.060, 0.047, 0.040, 0.036, 0.035, 0.038])

HEAD = dict(c=(0.662, 0, 1.084), r=(0.066, 0.038, 0.042), R=rot_y(8 * DEG))
FOREHEAD = dict(c=(0.693, 0, 1.100), r=(0.044, 0.027, 0.025), R=rot_y(14 * DEG))
CHEEK = dict(c=(0.682, 0, 1.064), r=(0.050, 0.034, 0.029), R=rot_y(8 * DEG))
NAPE = dict(c=(0.622, 0, 1.086), r=(0.048, 0.035, 0.038), R=None)

BILL_BASE = np.array([0.723, 0.0, 1.080])
BILL_PITCH = -12 * DEG
BILL_LEN = 0.370
BILL_DIR = np.array([math.cos(BILL_PITCH), 0, math.sin(BILL_PITCH)])
BILL_UP = np.array([-math.sin(BILL_PITCH), 0, math.cos(BILL_PITCH)])
EYE = np.array([0.697, 0.0325, 1.090])
EYE_R = 0.0072
THROAT = np.array([0.592, 0.0, 1.010])
JAW_HINGE = np.array([0.676, 0.0, 1.058])

# ---- wings (L side; mirror y for R) ------------------------------------------
SHOULDER = np.array([0.505, 0.108, 0.805])
ELBOW = np.array([0.400, 0.160, 0.700])
WRIST = np.array([0.585, 0.222, 0.770])     # recomputed from the grip at build time
HAND_TIP = np.array([0.665, 0.240, 0.740])

# ---- legs (L side) ------------------------------------------------------------
KNEE = np.array([0.322, 0.086, 0.605])       # hidden inside the body plumage
SHIN_LEN = 0.292                             # tibiotarsus (feathered down to near the ankle)
TARSUS_LEN = 0.196                           # tarsometatarsus


def mirror(p):
    q = np.array(p, dtype=float).copy()
    q[..., 1] *= -1
    return q
