# -*- coding: utf-8 -*-
"""
@author: Yi Zhang
@contact: zhangyi_aero@hotmail.com
@time: 11/26/2022 2:56 PM
"""

from numpy import sin, pi, cos, ones_like

import warnings
from src.tools.frozen import Frozen


class CrazyMeshCurvatureWarning(UserWarning):
    pass


def crazy(mf, bounds=None, c=0):
    """"""
    esd = mf.esd

    if bounds is None:
        bounds = [(0, 1) for _ in range(esd)]
    else:
        assert len(bounds) == esd, f"bounds={bounds} dimensions wrong."

    rm0 = _MesPyRegionCrazyMapping(bounds, c, esd)

    if esd == 2:
        region_map = {
            0: ['Upper', 'Down', 'Left', 'Right'],    # region #0
        }
    elif esd == 3:
        region_map = {
            0: ['North', 'South', 'West', 'East', 'Back', 'Front'],   # region #0
        }
    else:
        raise NotImplementedError()

    mapping_dict = {
        0: rm0.mapping,  # region #0
    }

    Jacobian_matrix_dict = {
        0: rm0.Jacobian_matrix
    }

    if c == 0:
        mtype = 'Linear'
        for lb, ub in bounds:
            mtype += '-{}'.format('%.8f' % (ub-lb))
    else:
        mtype = None

    mtype_dict = {
        0: mtype
    }

    return region_map, mapping_dict, Jacobian_matrix_dict, mtype_dict


class _MesPyRegionCrazyMapping(Frozen):

    def __init__(self, bounds, c, esd):
        super().__init__()
        for i, bs in enumerate(bounds):
            assert len(bs) == 2 and all([isinstance(_, (int, float)) for _ in bs]), f"bounds[{i}]={bs} is illegal."
            lb, up = bs
            assert lb < up, f"bounds[{i}]={bs} is illegal."
        assert isinstance(c, (int, float)), f"={c} is illegal, need to be a int or float. Ideally in [0, 0.3]."

        if not (0 <= c <= 0.3):
            warnings.warn(f"c={c} is not good. Ideally, c in [0, 0.3].", CrazyMeshCurvatureWarning)

        self._bounds = bounds
        self._c = c
        self._esd = esd
        self._freeze()

    def mapping(self, *rst):
        """ `*rst` be in [0, 1]. """
        assert len(rst) == self._esd, f"amount of inputs wrong."

        if self._esd == 2:

            r, s = rst
            a, b = self._bounds[0]
            c, d = self._bounds[1]
            if self._c == 0:
                x = (b - a) * r + a
                y = (d - c) * s + c
            else:
                x = (b - a) * (r + 0.5 * self._c * sin(2 * pi * r) * sin(2 * pi * s)) + a
                y = (d - c) * (s + 0.5 * self._c * sin(2 * pi * r) * sin(2 * pi * s)) + c
            return x, y

        elif self._esd == 3:
            r, s, t = rst
            a, b = self._bounds[0]
            c, d = self._bounds[1]
            e, f = self._bounds[2]

            if self._c == 0:
                x = (b - a) * r + a
                y = (d - c) * s + c
                z = (f - e) * t + e

            else:
                x = (b - a) * (r + 0.5 * self._c *
                               sin(2 * pi * r) *
                               sin(2 * pi * s) *
                               sin(2 * pi * t)) + a
                y = (d - c) * (s + 0.5 * self._c *
                               sin(2 * pi * r) *
                               sin(2 * pi * s) *
                               sin(2 * pi * t)) + c
                z = (f - e) * (t + 0.5 * self._c *
                               sin(2 * pi * r) *
                               sin(2 * pi * s) *
                               sin(2 * pi * t)) + e

            return x, y, z

        else:
            raise NotImplementedError()

    def Jacobian_matrix(self, *rst):
        """ r, s, t be in [0, 1]. """
        assert len(rst) == self._esd, f"amount of inputs wrong."

        if self._esd == 2:
            r, s = rst
            
            a, b = self._bounds[0]
            c, d = self._bounds[1]
            xr = (b - a) + (b - a) * 2 * pi * 0.5 * self._c * cos(2 * pi * r) * sin(2 * pi * s)
            xs = (b - a) * 2 * pi * 0.5 * self._c * sin(2 * pi * r) * cos(2 * pi * s)
            yr = (d - c) * 2 * pi * 0.5 * self._c * cos(2 * pi * r) * sin(2 * pi * s)
            ys = (d - c) + (d - c) * 2 * pi * 0.5 * self._c * sin(2 * pi * r) * cos(2 * pi * s)
            return ((xr, xs),
                    (yr, ys))

        elif self._esd == 3:

            r, s, t = rst
            a, b = self._bounds[0]
            c, d = self._bounds[1]
            e, f = self._bounds[2]

            if self._c == 0:
                xr = (b - a) * ones_like(r)  # have to do this to make it an array.
                xs = 0  # np.zeros_like(r)
                xt = 0
    
                yr = 0
                ys = (d - c) * ones_like(r)
                yt = 0
    
                zr = 0
                zs = 0
                zt = (f - e) * ones_like(r)
            else:
                xr = (b - a) + (b - a) * 2 * pi * 0.5 * self._c * cos(2 * pi * r) * sin(2 * pi * s) * sin(
                    2 * pi * t)
                xs = (b - a) * 2 * pi * 0.5 * self._c * sin(2 * pi * r) * cos(2 * pi * s) * sin(
                    2 * pi * t)
                xt = (b - a) * 2 * pi * 0.5 * self._c * sin(2 * pi * r) * sin(2 * pi * s) * cos(
                    2 * pi * t)
    
                yr = (d - c) * 2 * pi * 0.5 * self._c * cos(2 * pi * r) * sin(2 * pi * s) * sin(
                    2 * pi * t)
                ys = (d - c) + (d - c) * 2 * pi * 0.5 * self._c * sin(2 * pi * r) * cos(2 * pi * s) * sin(
                    2 * pi * t)
                yt = (d - c) * 2 * pi * 0.5 * self._c * sin(2 * pi * r) * sin(2 * pi * s) * cos(
                    2 * pi * t)
    
                zr = (f - e) * 2 * pi * 0.5 * self._c * cos(2 * pi * r) * sin(2 * pi * s) * sin(
                    2 * pi * t)
                zs = (f - e) * 2 * pi * 0.5 * self._c * sin(2 * pi * r) * cos(2 * pi * s) * sin(
                    2 * pi * t)
                zt = (f - e) + (f - e) * 2 * pi * 0.5 * self._c * sin(2 * pi * r) * sin(2 * pi * s) * cos(
                    2 * pi * t)
    
            return [(xr, xs, xt),
                    (yr, ys, yt),
                    (zr, zs, zt)]
