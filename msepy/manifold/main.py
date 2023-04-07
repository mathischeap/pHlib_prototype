# -*- coding: utf-8 -*-
"""
pH-lib@RAM-EEMCS-UT
created at: 3/30/2023 7:02 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')
from importlib import import_module
from src.tools.frozen import Frozen
from src.config import get_embedding_space_dim
from msepy.manifold.regions.main import MseManifoldRegions
from msepy.manifold.coordinate_transformation import MsePyManifoldsCoordinateTransformation


_global_mse_manifolds = dict()  # cache all MseManifolds, keys are sym_repr of abstract manifold.


def config(mf, arg, **kwargs):
    """"""
    assert mf.__class__ is MsePyManifold, f"I can only config MseManifold instance. Now I get {mf}."
    assert mf._regions is None, f"manifold {mf} already have region configurations. Change it may lead to error."

    mf._regions = MseManifoldRegions(mf)  # initialize the regions.

    if isinstance(arg, str):  # use predefined mappings
        predefined_path = '.'.join(str(MsePyManifold).split(' ')[1][1:-2].split('.')[:-2]) + \
                          '.predefined.' + arg
        _module = import_module(predefined_path)
        region_map, mapping_dict, Jacobian_matrix_dict, mtype_dict = getattr(_module, arg)(mf, **kwargs)

        mf.regions._parse_regions_from_region_map(
            region_map,
            mapping_dict,
            Jacobian_matrix_dict,
            mtype_dict
        )

        assert mf.regions.map is not None, f"predefined manifold only config manifold with region map."

    else:
        raise NotImplementedError()

    assert mf.regions._regions is not None, f"we need to set regions for the manifold by this `config` function."


class MsePyManifold(Frozen):
    """"""

    def __init__(self, abstract_manifold):
        """"""
        self._abstract = abstract_manifold
        self._ct = None
        self._regions = None
        _global_mse_manifolds[abstract_manifold._sym_repr] = self
        self._freeze()

    def __repr__(self):
        super_repr = super().__repr__().split('object')[1]
        return f"<{self.__class__.__name__} " + self._abstract._sym_repr + super_repr

    @property
    def abstract(self):
        return self._abstract

    @property
    def ndim(self):
        """The dimensions of this manifold (Not the embedding space dimensions!)"""
        return self._abstract.ndim

    @property
    def esd(self):
        """embedding space dimensions."""
        return get_embedding_space_dim()

    @property
    def ct(self):
        if self._ct is None:
            self._ct = MsePyManifoldsCoordinateTransformation(self)
        return self._ct

    @property
    def regions(self):
        """"""
        assert self._regions is not None, f"regions of {self} is not configured, config it through `msepy.config`"
        return self._regions


if __name__ == '__main__':
    # mpiexec -n 4 python
    pass
