# -*- coding: utf-8 -*-
"""
pH-lib@RAM-EEMCS-UT
created at: 3/30/2023 7:02 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')
from src.tools.frozen import Frozen
from src.config import get_embedding_space_dim
from mse.manifold.regions.main import MseManifoldRegions
from mse.manifold.coordinate_transformation import MseManifoldsCoordinateTransformation


_global_mse_manifolds = dict()  # cache all MseManifolds, keys are sym_repr of abstract manifold.


def config(mf, *args, **kwargs):
    """"""
    assert mf.__class__ is MseManifold, f"I can only config MseManifold instance. Now I get {mf}."
    

class MseManifold(Frozen):
    """"""

    def __init__(self, abstract_manifold):
        """"""
        self._abstract = abstract_manifold
        self._ct = None
        self._regions = None
        _global_mse_manifolds[abstract_manifold._sym_repr] = self
        self._freeze()

    @property
    def abstract(self):
        return self._abstract

    @property
    def udg(self):
        """un-directed graph representation of this manifold.

        If it is not None, it is a 2d topological matrix (containing only 0 and 1).
        """
        return self._abstract.udg_repr

    @property
    def ndim(self):
        """The dimensions of this manifold"""
        return self._abstract.ndim

    @property
    def esd(self):
        """embedding space dimensions."""
        return get_embedding_space_dim()

    @property
    def ct(self):
        if self._ct is None:
            self._ct = MseManifoldsCoordinateTransformation(self)
        return self._ct

    @property
    def regions(self):
        return self._regions


if __name__ == '__main__':
    # mpiexec -n 4 python 

    pass
