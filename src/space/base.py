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
from src.config import get_space_dim
from src.form import Form

_global_spaces = dict()

class SpaceBase(Frozen):
    """"""

    def __init__(self, mesh):
        """"""
        self._mesh = mesh
        _global_spaces[id(self)] = self

    @property
    def mesh(self):
        """"""
        return self._mesh

    @property
    def n(self):
        """"""
        return get_space_dim()

    def generate_instance(self, symbolic_representation, linguistic_representation):
        """"""
        linguistic_representation = r'\textsf{' + linguistic_representation + r'}'
        return Form(self, symbolic_representation, linguistic_representation, True)
