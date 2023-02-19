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
from src.config import _global_variables


class SpaceBase(Frozen):
    """"""

    def __init__(self, mesh):
        """"""
        self._mesh = mesh

    @property
    def mesh(self):
        """"""
        return self._mesh

    @property
    def n(self):
        """"""
        return _global_variables['space_dim']
