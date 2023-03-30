# -*- coding: utf-8 -*-
"""
@author: Yi Zhang
@contact: zhangyi_aero@hotmail.com
@time: 11/26/2022 2:56 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')
from src.tools.frozen import Frozen


class MseMesh(Frozen):
    """"""
    def __init__(self, abstract_mesh):
        self._abstract = abstract_mesh
        self._freeze()

    @property
    def abstract(self):
        return self._abstract
