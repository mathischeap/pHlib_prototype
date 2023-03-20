# -*- coding: utf-8 -*-
"""
pH-lib@RAM-EEMCS-UT
created at: 3/20/2023 5:17 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')

from src.tools.frozen import Frozen
from src.config import _parse_lin_repr


def _parse_matrix_ap_of(wft):
    """

    Parameters
    ----------
    wft
    Returns
    -------

    """
    if wft.__class__.__name__ == 'L2InnerProductTerm':
        _parse_scalar_valued_form_mass_matrix(wft._f0, wft._f1)
    else:
        raise NotImplementedError(f"wft={wft}")


_global_matrix = dict()  # we use lin_repr as keys as lin_repr is dependent to f.lin_repr.


def _parse_scalar_valued_form_mass_matrix(f0, f1):
    """"""
    # print(f0, f1)

# def _parse_root_form_ap_col_vec(sym_repr, lin_repr):
#     """"""
#     assert lin_repr not in _global_matrix, f"Cannot be because we cache the ap of root-forms."
#     cv = ColVec(sym_repr, lin_repr)
#     _global_matrix[lin_repr] = cv
#     return cv
#
#
# class ColVec(Frozen):
#     """column vector."""
#     def __init__(self, sym_repr, lin_repr):
#         self._sym_repr = sym_repr
#         lin_repr, pure_lin_repr = _parse_lin_repr('matrix', lin_repr)
#         self._lin_repr = lin_repr
#         self._pure_lin_repr = pure_lin_repr
#         self._freeze()
#
#     def __repr__(self):
#         """repr"""
#         super_repr = super().__repr__().split('object')[1]
#         return f"<ColVec {self._lin_repr}" + super_repr
