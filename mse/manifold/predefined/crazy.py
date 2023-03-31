# -*- coding: utf-8 -*-
"""
@author: Yi Zhang
@contact: zhangyi_aero@hotmail.com
@time: 11/26/2022 2:56 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')

from mse.manifold.predefined.main import RegionMapping


udg = [[1, ], ]


def crazy(mf, bounds=None, c=0):
    """"""
    assert mf.udg == udg, f"mf.udg={mf.udg} is not allowed for 'crazy' region mapping."
    esd = mf.esd

    if bounds is None:
        bounds = [(0, 1) for _ in range(esd)]
    else:
        pass
