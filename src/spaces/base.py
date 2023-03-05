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

    def make_form(self, sym_repr, lin_repr, orientation='outer'):
        """"""
        assert isinstance(sym_repr, str), f"symbolic representation must be a str."
        assert isinstance(lin_repr, str), f"symbolic representation must be a str."
        if lin_repr[:8] == r"\textsf{":
            pass
        else:
            lin_repr = r'\textsf{' + lin_repr + r'}'
        return Form(
            self, sym_repr, lin_repr,
            True,  # is_root
            None,  # elementary_forms
            orientation
        )

    def __eq__(self, other):
        """"""
        return self.__repr__() == other.__repr__()

    @staticmethod
    def _is_space():
        """A private tag."""
        return True
