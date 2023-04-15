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
        regions = self._mesh.manifold.regions
        _xyz = dict()

        for i in regions:
            oi = origin[i]
            di = delta[i]
            assert len(xi_et_sg) == len(oi) == self._mesh.ndim, f"I need {len(oi)} reference coordinates."
            length = [len(_) for _ in oi]
            if self._mesh.ndim == 1:   # 1-d mapping
                ox = oi[0]
                dx = di[0]
                ori = [ox]
                dta = [dx]
            elif self._mesh.ndim == 2:   # 2-d mapping
                ox = np.tile(oi[0], length[1])
                dx = np.tile(di[0], length[1])
                oy = np.repeat(oi[1], length[0])
                dy = np.repeat(di[1], length[0])
                ori = [ox, oy]
                dta = [dx, dy]
            elif self._mesh.ndim == 3:    # 3-d mapping
                ox = np.tile(np.tile(oi[0], length[1]), length[2])
                dx = np.tile(np.tile(di[0], length[1]), length[2])
                oy = np.tile(np.repeat(oi[1], length[0]), length[2])
                dy = np.tile(np.repeat(di[1], length[0]), length[2])
                oz = np.repeat(np.repeat(oi[2], length[1]), length[0])
                dz = np.repeat(np.repeat(di[2], length[1]), length[0])
                ori = [ox, oy, oz]
                dta = [dx, dy, dz]
            else:
                raise NotImplementedError()

            num_local_elements = np.prod(length)
            md_ref_coo = list()
            for j, ref_coo in enumerate(xi_et_sg):
                _ = ref_coo[..., np.newaxis].repeat(num_local_elements, axis=-1)
                _ = (_ + 1) * 0.5 * dta[j] + ori[j]
                md_ref_coo.append(_)

            _xyz[i] = self._mesh.manifold.ct.mapping(*md_ref_coo, regions=i)[i]

        xyz = [_xyz[0][_] for _ in range(self._mesh.ndim)]
        for i in regions:
            if i != 0:
                x_y_z = _xyz[i]
                for j, _ in enumerate(xyz):
                    xyz[j] = np.stack((_, x_y_z[j]), axis=-1)

        return xyz


if __name__ == '__main__':
    # python msepy/mesh/coordinate_transformation.py
    import __init__ as ph

    space_dim = 3
    ph.config.set_embedding_space_dim(space_dim)

    manifold = ph.manifold(space_dim)
    mesh = ph.mesh(manifold)

    msepy, obj = ph.fem.apply('msepy', locals())

    mnf = obj['manifold']
    msh = obj['mesh']

    msepy.config(mnf)('crazy', c=0., periodic=False, bounds=[[0, 2] for _ in range(space_dim)])
    # msepy.config(msh)([5 for _ in range(space_dim)])
    msepy.config(msh)(([1, 2, 1], [2, 3], [1, 2, 2, 4]))

    # xi_et_sg = [np.array([-0.5, 0, 0.25, 0.5]) for _ in range(space_dim)]
    xi_et_sg = [np.linspace(-1, 1, 3) for _ in range(space_dim)]

    xyz = msh.ct.mapping(*xi_et_sg)
    print(np.shape(xyz))
