# -*- coding: utf-8 -*-
"""
pH-lib@RAM-EEMCS-UT
created at: 2/20/2023 11:41 AM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')

from src.tools.frozen import Frozen
from src.config import get_embedding_space_dim
from src.config import _manifold_default_sym_repr
from src.config import _check_sym_repr
from src.config import _parse_lin_repr
from src.config import _manifold_default_lin_repr

_global_manifolds = dict()


def manifold(
        ndim,
        is_periodic=False,
        udg_repr=None
):
    """A function wrapper of the Manifold class."""
    return Manifold(ndim, is_periodic=is_periodic, udg_repr=udg_repr)


class Manifold(Frozen):
    """"""

    def __init__(
            self, ndim,
            sym_repr=None,
            lin_repr=None,
            is_periodic=False,
            udg_repr=None,   # the undirected graph representation of this manifold
            # add other representations here.
    ):
        """"""
        embedding_space_ndim = get_embedding_space_dim()
        assert ndim % 1 == 0 and 0 <= ndim <= embedding_space_ndim, \
            f"manifold ndim={ndim} is wrong. Is should be an integer and be in range [0, {embedding_space_ndim}]. " \
            f"You change change the dimensions of the embedding space using function `config.set_embedding_space_dim`."
        self._ndim = ndim
        if sym_repr is None:
            base_repr = _manifold_default_sym_repr
            number_existing_manifolds = len(_global_manifolds)

            if number_existing_manifolds == 0:
                sym_repr = base_repr
            else:
                sym_repr = base_repr + r'_{' + str(number_existing_manifolds) + '}'
        else:
            pass
        sym_repr = _check_sym_repr(sym_repr)

        if lin_repr is None:
            base_repr = _manifold_default_lin_repr
            number_existing_manifolds = len(_global_manifolds)

            if number_existing_manifolds == 0:
                lin_repr = base_repr
            else:
                lin_repr = base_repr + str(number_existing_manifolds)

        assert sym_repr not in _global_manifolds, \
            f"Manifold symbolic representation is illegal, pls specify a symbolic representation other than " \
            f"{set(_global_manifolds.keys())}"

        for _ in _global_manifolds:
            _m = _global_manifolds[_]
            assert lin_repr != _m._lin_repr
        lin_repr, pure_lin_repr = _parse_lin_repr('manifold', lin_repr)

        self._sym_repr = sym_repr
        self._lin_repr = lin_repr
        self._pure_pure_lin_repr = pure_lin_repr
        _global_manifolds[sym_repr] = self

        assert isinstance(is_periodic, bool), f"is_periodic must be bool type."
        self._is_periodic = is_periodic

        self._udg_repr = udg_repr  # if it has an udg_repr representation.
        self._boundary = None
        self._inclusion = None  # not None for boundary manifold. Will be set when initialize a boundary manifold.
        self._freeze()

    @property
    def ndim(self):
        """The dimensions of this manifold."""
        return self._ndim

    @property
    def udg_repr(self):
        """the undirected graph representation of this manifold."""
        return self._udg_repr

    def is_periodic(self):
        """"""
        return self._is_periodic

    def __repr__(self):
        """"""
        super_repr = super().__repr__().split('object')[-1]
        return f'<Manifold {self._sym_repr}' + super_repr  # this must be unique.

    def boundary(self, sym_repr=None):
        """Give a manifold of dimensions (n-1)"""
        if self._boundary is None:
            if self.ndim == 0:
                return NullManifold('Null')
            elif self.is_periodic():
                return NullManifold(self.ndim-1)
            else:
                if sym_repr is None:
                    sym_repr = r'\partial' + self._sym_repr
                else:
                    pass
                self._boundary = Manifold(
                    self.ndim-1,
                    sym_repr=sym_repr,
                    lin_repr=f'boundary-of-{self._pure_pure_lin_repr}',
                    is_periodic=True,
                )
                self._boundary._inclusion = self
        return self._boundary

    def inclusion(self):
        """"""
        return self._inclusion

    def cap(self, other, sym_repr=None):
        """return the intersection of two manifolds, i.e., return manifold := self cap other."""
        raise NotImplementedError()

    def interface(self, other, sym_repr=None):
        """return the cap of boundaries of two manifolds."""
        raise NotImplementedError()


class NullManifold(Frozen):
    """"""

    def __init__(self, ndim):
        """"""
        self._ndim = ndim
        self._freeze()

    @property
    def ndim(self):
        """"""
        return self._ndim


if __name__ == '__main__':
    # python src/manifold.py
    import __init__ as ph

    m1 = ph.manifold(3)
    m0 = m1.boundary()
    print(m0, m0.inclusion())
