# -*- coding: utf-8 -*-
"""
@author: Yi Zhang
@contact: zhangyi_aero@hotmail.com
@time: 11/26/2022 2:56 PM
"""

from src.spaces.base import SpaceBase
from src.config import get_space_dim


class ScalarValuedFormSpace(SpaceBase):
    """
    Parameters
    ----------
    mesh :
    k :
        k-form spaces
    N :
        The degree of the fintie element spaces.

    Examples
    --------

    """

    def __init__(self, mesh, k, N):
        """"""
        super().__init__(mesh)
        assert isinstance(k, int) and 0 <= k <= get_space_dim(), f" k wrong"
        self._k = k
        assert isinstance(N, int) and N >= 1, f"N wrong"
        self._N = N
        self._symbolic_representation = rf"\Omega^{self.k}({mesh._symbolic_representation};{self.N})"
        self._freeze()

    @property
    def k(self):
        """I am k-form."""
        return self._k

    @property
    def N(self):
        return self._N

    def __repr__(self):
        """By construction, it will be unique."""
        return 'Space:' + rf"\Omega^{self.k}({self.mesh.__repr__()};{self.N})"

    def _quasi_equal(self, other):
        """"""
        if other is self:
            return True
        else:
            if other.__class__.__name__ != 'ScalarValuedFormSpace':
                return False
            else:
                return other.mesh == self.mesh and other.k == self.k
