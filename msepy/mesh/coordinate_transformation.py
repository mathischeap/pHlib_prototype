# -*- coding: utf-8 -*-
"""
@author: Yi Zhang
@contact: zhangyi_aero@hotmail.com
"""
import sys
if './' not in sys.path:
    sys.path.append('./')

from src.tools.frozen import Frozen
import numpy as np


class MsePyMeshCoordinateTransformation(Frozen):
    """"""

    def __init__(self, mesh):
        """"""
        self._mesh = mesh
        self._freeze()

    def mapping(self, *xi_et_sg):
        """"""
        elements = self._mesh.elements
        origin = elements._origin
        delta = elements._delta


if __name__ == '__main__':
    # python msepy/mesh/coordinate_transformation.py
    import __init__ as ph

    space_dim = 2
    ph.config.set_embedding_space_dim(space_dim)

    manifold = ph.manifold(space_dim)
    mesh = ph.mesh(manifold)

    msepy, obj = ph.fem.apply('msepy', locals())

    mnf = obj['manifold']
    msh = obj['mesh']

    msepy.config(mnf)('crazy', c=0.1, periodic=False, bounds=[[0, 2] for _ in range(space_dim)])
    msepy.config(msh)([1 for _ in range(space_dim)])

    xi_et_sg = [np.array([-0.5, 0, 0.5]) for _ in range(space_dim)]

    xyz = msh.ct.mapping(*xi_et_sg)
