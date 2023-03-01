# -*- coding: utf-8 -*-
"""
@author: Yi Zhang
@contact: zhangyi_aero@hotmail.com
@time: 11/26/2022 2:56 PM
"""

from src.tools.frozen import Frozen
from src.config import get_embedding_space_dim
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
        return get_embedding_space_dim()

    def make_form(self, symbolic_representation, linguistic_representation, orientation='outer'):
        """"""
        linguistic_representation = r'\textsf{' + linguistic_representation + r'}'
        return Form(
            self, symbolic_representation, linguistic_representation,
            True,  # is_root
            None,  # elementary_forms
            orientation
        )

    def __eq__(self, other):
        """"""
        return self.__repr__() == other.__repr__()

    def _quasi_equal(self, other):
        """equal but basis function degrees can be different."""
        raise NotImplementedError()

    @staticmethod
    def _is_space():
        """A private tag."""
        return True
