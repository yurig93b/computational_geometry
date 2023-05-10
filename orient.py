import numpy as np

ORIENT_CCW = 1
ORIENT_CW = -1
ORIENT_COLL = 0

def orient(p1, p2, p3, p4):
    mat = np.matrix([[1, 1, 1, 1],
                     [p1.x, p2.x, p3.x, p4.x],
                     [p1.y, p2.y, p3.y, p4.y],
                     [p1.z, p2.z, p3.z, p4.z]])

    det = np.linalg.det(mat)

    if det > 0:
        return ORIENT_CCW
    elif det < 0:
        return ORIENT_CW

    return ORIENT_COLL

