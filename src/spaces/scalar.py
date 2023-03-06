# -*- coding: utf-8 -*-
"""
@author: Yi Zhang
@contact: zhangyi_aero@hotmail.com
@time: 11/26/2022 2:56 PM
"""

from src.spaces.base import SpaceBase


class ScalarValuedFormSpace(SpaceBase):
    """
    Parameters
    ----------
    mesh :
    k :
        k-form spaces
    p :
        The degree of the fintie element spaces.

    Examples
    --------

    """

    def __init__(self, mesh, k, p):
        """"""
        super().__init__(mesh)
        assert isinstance(k, int) and 0 <= k <= mesh.ndim, f" k={k} illegal on {mesh}."
        self._k = k
        assert isinstance(p, int) and p >= 1, f"basis function degree p = {p} is wrong."
        self._p = p
        self._sym_repr = r"\Omega^{(" + str(self.k) + r')}' + rf"_{self.p}({mesh._sym_repr})"
        self._freeze()

    @property
    def k(self):
        """I am k-form."""
        return self._k

    @property
    def p(self):
        """Basis function degree."""
        return self._p

    def __repr__(self):
        """By construction, it will be unique."""
        super_repr = super().__repr__().split('object')[-1]
        return f'<Space {self._sym_repr}' + super_repr
