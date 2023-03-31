# -*- coding: utf-8 -*-
"""
pH-lib@RAM-EEMCS-UT
created at: 3/31/2023 2:35 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')
from src.tools.frozen import Frozen


class MseManifoldsCoordinateTransformation(Frozen):
    """"""
    def __init__(self, mf):
        self._mf = mf
        self._freeze()
