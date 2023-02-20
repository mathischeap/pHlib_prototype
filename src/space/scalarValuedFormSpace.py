# -*- coding: utf-8 -*-
"""
@author: Yi Zhang
@contact: zhangyi_aero@hotmail.com
@time: 11/26/2022 2:56 PM
"""

from src.space.base import SpaceBase
from src.config import get_space_dim


class ScalarValuedFormSpace(SpaceBase):
    """
    Parameters
    ----------
    mesh
    k :
        k-form space
    N :
        The degree of the fintie element space.
    """

    def __init__(self, mesh, k, N):
        """"""
        super().__init__(mesh)
        assert isinstance(k, int) and 0 <= k <= get_space_dim(), f" k wrong"
        self._k = k
        assert isinstance(N, int) and N >= 1, f"N wrong"
        self._N = N
        self._symbolic_representation = rf"$\Omega^{self.k}({self.N})$"
        self._freeze()

    @property
    def k(self):
        """I am k-form."""
        return self._k

    @property
    def N(self):
        return self._N
