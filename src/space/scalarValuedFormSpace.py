# -*- coding: utf-8 -*-
"""
@author: Yi Zhang
@contact: zhangyi_aero@hotmail.com
@time: 11/26/2022 2:56 PM
"""

from src.space.base import SpaceBase


class ScalarValuedFormSpace(SpaceBase):
    """"""

    def __init__(self, mesh, k):
        super().__init__(mesh)
        self._k = k
        self._freeze()

    @property
    def k(self):
        """I am k-form."""
        return self._k
