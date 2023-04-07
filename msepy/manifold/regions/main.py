# -*- coding: utf-8 -*-
"""
pH-lib@RAM-EEMCS-UT
created at: 3/31/2023 2:29 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')
from src.tools.frozen import Frozen
from msepy.manifold.regions.region import MsePyManifoldRegion
from msepy.manifold.regions.rct import MsePyRegionCoordinateTransformation


class MseManifoldRegions(Frozen):
    """"""

    def __init__(self, mf):
        """"""
        # no need to do any check. It should be done already! We only access this class through `config`
        self._mf = mf
        self._regions = dict()
        self._map = None   # normally, only regions of the highest dimensional manifold has a region map.
        self._freeze()

    def _parse_regions_from_region_map(
            self,
            region_map,
            mapping_dict,
            Jacobian_matrix_dict,
            mtype_dict
    ):
        assert self._regions == dict(), f"Change regions will be dangerous!"
        for i in region_map:

            mapping = mapping_dict[i]
            if Jacobian_matrix_dict is None:
                Jacobian_matrix = None
            else:
                Jacobian_matrix = Jacobian_matrix_dict[i]
            mtype = mtype_dict[i]
            rct = MsePyRegionCoordinateTransformation(mapping, Jacobian_matrix, mtype)
            region = MsePyManifoldRegion(self, i, rct)
            self._regions[i] = region

        self._map = region_map  # ***

    @property
    def map(self):
        """normally, only regions of the highest dimensional manifold has a region map.

        Return `None` if the regions of this manifold has no region map. For example, these boundary manifolds. We
        can locate these manifolds by access its location indicator, for example. It a boundary manifolds has
        6 faces of a 3d cube.
        """
        return self._map  # ***

    def __repr__(self):
        """"""
        super_repr = super().__repr__().split('object')[1]
        return f"<Regions of " + self._mf.__repr__() + super_repr

    def __iter__(self):
        """go through all region index. Remember, a region does not have a name."""
        for ri in self._regions:
            yield ri

    def __getitem__(self, ri):
        """Retrieve a region through its index."""
        return self._regions[ri]

    def __len__(self):
        """How many regions I have?"""
        return len(self._regions)

    def __contains__(self, i):
        """check if `i` is a valid region index."""
        return i in self._regions


if __name__ == '__main__':
    # mpiexec -n 4 python 

    pass
