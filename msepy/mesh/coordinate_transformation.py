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

    def mapping(self, *xi_et_sg, regions=None):
        """"""
        if regions is None:
            regions = range(0, len(self._mesh.manifold.regions))
        elif isinstance(regions, int):
            regions = [regions]
        else:
            raise Exception(f"pls compute mapping for one region or all regions!")

        elements = self._mesh.elements
        origin = elements._origin
        delta = elements._delta
        _xyz = dict()

        _layout_cache_key = elements._layout_cache_key
        cache = dict()

        for i in regions:
            key = _layout_cache_key[i]
            if key in cache:
                ori, dta, num_local_elements = cache[key]
            else:
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
                cache[key] = ori, dta, num_local_elements

            md_ref_coo = list()
            for j, ref_coo in enumerate(xi_et_sg):
                _ = ref_coo[..., np.newaxis].repeat(num_local_elements, axis=-1)
                _ = (_ + 1) * 0.5 * dta[j] + ori[j]
                md_ref_coo.append(_)

            md_ref_coo = self._mesh.manifold.ct.mapping(*md_ref_coo, regions=i)[i]
            _xyz[i] = md_ref_coo

        if len(regions) == 1:
            return _xyz[0]
        else:
            xyz = [list() for _ in range(len(_xyz[0]))]
            for i in regions:
                for j, region_axis_value in enumerate(_xyz[i]):  # axis_value, elements
                    xyz[j].append(region_axis_value)
                del _xyz[i]
            for j, _ in enumerate(xyz):
                xyz[j] = np.concatenate(list(_), axis=-1)

            return xyz


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

    # msepy.config(mnf)('crazy', c=0., periodic=False, bounds=[[0, 2] for _ in range(space_dim)])
    msepy.config(mnf)('backward_step')
    msepy.config(msh)([5 for _ in range(space_dim)])
    # msepy.config(msh)(([1, 2, 1], [2, 3], [1, 2, 2, 4]))

    # xi_et_sg = [np.array([-0.5, 0, 0.25, 0.5]) for _ in range(space_dim)]
    xi_et_sg = [np.linspace(-1, 1, 4) for _ in range(space_dim)]

    xyz = msh.ct.mapping(*xi_et_sg)
    print(np.shape(xyz))
