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
from mse.manifold.regions.main import MseManifoldRegions
from mse.manifold.coordinate_transformation import MseManifoldsCoordinateTransformation
from mse.manifold.predefined.main import RegionMapping


_global_mse_manifolds = dict()  # cache all MseManifolds, keys are sym_repr of abstract manifold.


def config(mf, arg, **kwargs):
    """"""
    assert mf.__class__ is MseManifold, f"I can only config MseManifold instance. Now I get {mf}."
    assert mf._regions is None, f"manifold {mf} already have region configurations. Change it may lead to error."

    mf._regions = MseManifoldRegions(mf)  # initialize the regions.

    if isinstance(arg, str):  # use predefined mappings

        predefined_path = '.'.join(str(RegionMapping).split(' ')[1][1:-2].split('.')[:-2]) + '.' + arg
        _module = import_module(predefined_path)
        region_map, region_mapping_dict = getattr(_module, arg)(mf, **kwargs)

        for i in region_mapping_dict:
            assert region_mapping_dict[i].__class__ is RegionMapping, f"{i}th region mapping is not a valid one."

        mf.regions._parse_regions_from_region_map_and_mapping_dict(region_map, region_mapping_dict)

    else:
        raise NotImplementedError()

        # else:  # give particular mappings for each region in a list or tuple.
        #
        #     region_mapping_dict = dict()
        #     assert isinstance(arg, (list, tuple)), f"pls put region mappings in list or tuple."
        #     assert len(mf.udg) == len(arg), f"I have {len(mf.udg)} regions, but {len(arg)} mappings provided."
        #     for i, mapping in enumerate(arg):
        #         rmi = RegionMapping()
        #         rmi.mapping = mapping
        #         region_mapping_dict[i] = rmi

        # at this stage, regions are number named! we will name the region during the initialization of regions.


class MseManifold(Frozen):
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
        return f"<MseManifold " + self._abstract._sym_repr + super_repr

    @property
    def abstract(self):
        return self._abstract

    @property
    def udg(self):
        """un-directed graph representation of this manifold.

        If it is not None, it is a 2d topological matrix (containing only 0 and 1).
        """
        return self._abstract.udg

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
            self._ct = MseManifoldsCoordinateTransformation(self)
        return self._ct

    @property
    def regions(self):
        return self._regions


if __name__ == '__main__':
    # mpiexec -n 4 python 

    pass
