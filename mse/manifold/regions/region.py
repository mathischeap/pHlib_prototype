# -*- coding: utf-8 -*-
"""
pH-lib@RAM-EEMCS-UT
created at: 4/3/2023 5:46 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')
from src.tools.frozen import Frozen


class MseManifoldRegion(Frozen):
    """"""

    def __init__(self, regions, i, name, mapping):
        """
        Parameters
        ----------
        regions :
            The group of regions this region belong to.
        i :
            This is the ith region in the regions of a manifolds
        name :
            This region is named after `rn`
        mapping:
            A mapping that maps the reference region into this region.
        """
        self._i = i
        self._name = name
        self._mapping = mapping


    def __repr__(self):
        """"""
        super_repr = super().__repr__().split('object')[1]
        return f"<MseManifoldRegion of " + self._name + super_repr


if __name__ == '__main__':
    # mpiexec -n 4 python 

    pass
