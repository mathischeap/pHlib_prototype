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

_global_manifolds = dict()


def manifold(*args,  **kwargs):
    """A function wrapper of the Manifold class."""
    return Manifold(*args,  **kwargs)


class Manifold(Frozen):
    """"""

    def __init__(
            self, ndim,
            sym_repr=None,
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
            number_existing_manifolds = len(_global_manifolds)
            while 1:
                if number_existing_manifolds == 0:
                    sym_repr = r'\mathcal{M}'
                    break
                else:
                    sym_repr = r'\mathcal{M}_{' + str(number_existing_manifolds) + '}'
                    if sym_repr in _global_manifolds:
                        number_existing_manifolds += 1
                    else:
                        break
        else:
            pass
        assert isinstance(sym_repr, str), f"sym_repr must be a str of length > 0."
        assert ' ' not in sym_repr, f"manifold symbolic representation cannot contain space."
        assert len(sym_repr) > 0, f"sym_repr must be a str of length > 0."

        assert sym_repr not in _global_manifolds, \
            f"Manifold symbolic representation is illegal, pls specify a symbolic representation other than " \
            f"{set(_global_manifolds.keys())}"

        _global_manifolds[sym_repr] = self
        self._sym_repr = sym_repr

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
