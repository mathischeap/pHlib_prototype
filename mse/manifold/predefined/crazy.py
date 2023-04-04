# -*- coding: utf-8 -*-
"""
@author: Yi Zhang
@contact: zhangyi_aero@hotmail.com
@time: 11/26/2022 2:56 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')
from src.tools.frozen import Frozen

from mse.manifold.predefined.main import RegionMapping
import numpy as np

import warnings


class CrazyMeshCurvatureWarning(UserWarning):
    pass


def crazy(mf, bounds=None, c=0):
    """"""
    esd = mf.esd

    rm0 = RegionMapping()
    rm0.mapping = _CrazyMapping(bounds, c, esd)

    region_mapping_dict = {
        0: rm0,
    }

    if esd == 2:
        region_map = (
            ['Upper', 'Down', 'Left', 'Right'],
        )
    elif esd == 3:
        region_map = (
            ['North', 'South', 'West', 'East', 'Back', 'Front'],
        )
    else:
        raise NotImplementedError()

    return region_map, region_mapping_dict


class _CrazyMapping(Frozen):

    def __init__(self, bounds, c, esd):
        if bounds is None:
            bounds = [(0, 1) for _ in range(esd)]
        else:
            assert len(bounds) == esd, f"bounds={bounds} dimensions wrong."
        for i, bs in enumerate(bounds):
            assert len(bs) == 2 and all([isinstance(_, (int, float)) for _ in bs]), f"bounds[{i}]={bs} is illegal."
            lb, up = bs
            assert lb < up, f"bounds[{i}]={bs} is illegal."
        assert isinstance(c, (int, float)), f"={c} is illegal, need to be a int or float. Ideally in [0, 0.3]."

        if not (0 <= c <= 0.3):
            warnings.warn(f"c={c} is not good. Ideally, c in [0, 0.3].", CrazyMeshCurvatureWarning)

        self.bounds = bounds
        self.c = c
        self.esd = esd
        self._freeze()

    def __call__(self, *rst):
        """ `*rst` be in [0, 1]. """
        assert len(rst) == self.esd, f"amount of inputs wrong."

        if self.esd == 2:

            r, s = rst
            a, b = self.bounds[0]
            c, d = self.bounds[1]
            if self.c == 0:
                x = (b - a) * r + a
                y = (d - c) * s + c
            else:
                x = (b - a) * (r + 0.5 * self.c * np.sin(2 * np.pi * r) * np.sin(2 * np.pi * s)) + a
                y = (d - c) * (s + 0.5 * self.c * np.sin(2 * np.pi * r) * np.sin(2 * np.pi * s)) + c
            return x, y

        elif self.esd == 3:
            r, s, t = rst
            a, b = self.bounds[0]
            c, d = self.bounds[1]
            e, f = self.bounds[2]

            if self.c == 0:
                x = (b - a) * r + a
                y = (d - c) * s + c
                z = (f - e) * t + e

            else:
                x = (b - a) * (r + 0.5 * self.c *
                               np.sin(2 * np.pi * r) *
                               np.sin(2 * np.pi * s) *
                               np.sin(2 * np.pi * t)) + a
                y = (d - c) * (s + 0.5 * self.c *
                               np.sin(2 * np.pi * r) *
                               np.sin(2 * np.pi * s) *
                               np.sin(2 * np.pi * t)) + c
                z = (f - e) * (t + 0.5 * self.c *
                               np.sin(2 * np.pi * r) *
                               np.sin(2 * np.pi * s) *
                               np.sin(2 * np.pi * t)) + e

            return x, y, z

        else:
            raise NotImplementedError()
