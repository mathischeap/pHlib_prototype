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
    """"""
    return Manifold(*args,  **kwargs)


class Manifold(Frozen):
    """"""

    def __init__(
            self, ndim,
            symbolic_representation=None,
            undirected_graph=None,   # the undirected graph representation of this manifold
            # add other representations here.
    ):
        """"""
        embedding_space_ndim = get_embedding_space_dim()
        assert ndim % 1 == 0 and 0 <= ndim <= embedding_space_ndim, \
            f"manifold ndim={ndim} is wrong. Is should be an integer and be in range [0, {embedding_space_ndim}]. " \
            f"You change change the dimensions of the embedding space using function `config.set_embedding_space_dim`."
        self._ndim = ndim
        if symbolic_representation is None:
            number_existing_manifolds = len(_global_manifolds)
            while 1:
                symbolic_representation = r'\mathcal{M}_{' + str(number_existing_manifolds) + '}'
                if symbolic_representation in _global_manifolds:
                    number_existing_manifolds += 1
                else:
                    break
        else:
            assert isinstance(symbolic_representation, str) and len(symbolic_representation)>0, \
                f"symbolic_representation must be str of length > 0."

        assert symbolic_representation not in _global_manifolds, \
            f"Manifold symbolic representation is illegal, pls specify a symbolic representation other than " \
            f"{set(_global_manifolds.keys())}"
        _global_manifolds[symbolic_representation] = self
        self._symbolic_representation = symbolic_representation

        self._undirected_graph = undirected_graph  # if it has an undirected_graph representation.

        self._freeze()

    @property
    def n(self):
        return get_embedding_space_dim()

    @property
    def ndim(self):
        """The dimensions of this manifold."""
        return self._ndim

    @property
    def undirected_graph(self):
        """the undirected graph representation of this manifold."""
        return self._undirected_graph

    def __repr__(self):
        """"""
        super_repr = super().__repr__().split('object')[-1]
        return f'<Manifold {self._symbolic_representation}' + super_repr  # this must be unique.


if __name__ == '__main__':
    # python src/manifold.py
    import __init__ as ph

    m1 = ph.manifold(3)
    print(m1)
