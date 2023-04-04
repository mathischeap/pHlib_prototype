# -*- coding: utf-8 -*-
"""
pH-lib@RAM-EEMCS-UT
created at: 3/31/2023 2:29 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')
from src.tools.frozen import Frozen
from mse.manifold.regions.region import MseManifoldRegion


class MseManifoldRegions(Frozen):
    """"""

    def __init__(self, mf):
        """"""
        # no need to do any check. It should be done already! We only access this class through `config`
        self._mf = mf
        self._map = None
        self._regions = dict()
        self._freeze()

    def __repr__(self):
        """"""
        super_repr = super().__repr__().split('object')[1]
        return f"<Regions of " + self._mf.__repr__() + super_repr

    def _parse_regions_from_region_map_and_mapping_dict(self, region_map, mapping_dict):
        assert self._regions == dict(), f"Change regions will be dangerous!"
        for i in mapping_dict:
            mp = mapping_dict[i]
            rn = self._mf.abstract._sym_repr + r':R_{' + str(i) + r'}'
            region = MseManifoldRegion(self, i, rn, mp)
            self._regions[i] = region
        self._map = region_map

    def __iter__(self):
        """go through all region index."""
        for ri in self._regions:
            yield ri

    def __getitem__(self, ri):
        """Retrieve a region through its index."""
        return self._regions[ri]


if __name__ == '__main__':
    # mpiexec -n 4 python 

    pass
