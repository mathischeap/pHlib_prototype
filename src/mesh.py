# -*- coding: utf-8 -*-
"""
@author: Yi Zhang
@contact: zhangyi_aero@hotmail.com
@time: 11/26/2022 2:56 PM
"""

from src.tools.frozen import Frozen
from src.config import _global_variables


class Mesh(Frozen):
    """"""

    def __init__(self, domain):
        """"""
        self._domain = domain
        self._freeze()

    @property
    def n(self):
        return _global_variables['space_dim']
