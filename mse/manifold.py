# -*- coding: utf-8 -*-
"""
pH-lib@RAM-EEMCS-UT
created at: 3/30/2023 7:02 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')
from src.tools.frozen import Frozen

class MseManifolds(Frozen):
    """"""

    def __init__(self, abstract_manifold):
        """"""
        self._abstract = abstract_manifold
        self._freeze()

    @property
    def abstract(self):
        return self._abstract


if __name__ == '__main__':
    # mpiexec -n 4 python 

    pass
