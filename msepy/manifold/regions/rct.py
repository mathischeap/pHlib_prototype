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

        self._mtype = mtype
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
