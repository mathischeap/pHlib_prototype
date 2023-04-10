# -*- coding: utf-8 -*-

import sys

if './' not in sys.path:
    sys.path.append('./')
from src.tools.frozen import Frozen


class MsePyRegionCoordinateTransformation(Frozen):
    """"""

    def __init__(self, mapping, Jacobian_matrix, mtype):

        self._mapping = mapping
        if Jacobian_matrix is None:
            raise NotImplementedError(f"Implement a numerical Jacobian_matrix")
        else:
            self._Jacobian_matrix = Jacobian_matrix
        self.mtype = mtype  # if it is None, we will set a unique one.
        self._freeze()

    @property
    def mapping(self):
        """"""
        return self._mapping

    @property
    def Jacobian_matrix(self):
        """"""
        return self._Jacobian_matrix

    @property
    def mtype(self):
        """"""
        return self._mtype

    @mtype.setter
    def mtype(self, mtp):
        """"""
        if mtp is None:
            indicator = 'unique'
            parameters = None
        else:
            assert isinstance(mtp, dict), f"mtype must be a dict."
            indicator = mtp['indicator']
            parameters = mtp['parameters']
        mtp = _MsePyRegionMtype(indicator, parameters)
        self._mtype = mtp


class _MsePyRegionMtype(Frozen):
    """"""
    def __init__(self, indicator, parameters):
        assert indicator in (
            'unique',  # `parameters` is a the unique id.
            'Linear',  # regular box in Cartesian system.
                       # `parameters` is a list of region length along each axis.
        ), f"indicator = {indicator} is illegal."
        if parameters is None:
            parameters = id(self)
        else:
            pass
        self._indicator = indicator
        self._parameters = parameters
        self._signature = self._indicator + ":" + str(self._parameters)
        self._freeze()

    @property
    def signature(self):
        """"""
        return self._signature

    def __eq__(self, other):
        """"""
        if other.__class__ is not _MsePyRegionMtype:
            return False
        else:
            return self.signature == other.signature
