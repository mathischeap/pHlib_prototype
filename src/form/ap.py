# -*- coding: utf-8 -*-
"""
pH-lib@RAM-EEMCS-UT
created at: 3/20/2023 3:57 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')
from src.tools.frozen import Frozen
from src.config import _parse_lin_repr, _form_evaluate_at_repr_setting, _root_form_ap_vec_setting


def _parse_root_form_ap(f, sym_repr=None):
    """"""
    assert f.is_root(), f"safety check."
    if sym_repr is None:
        setting_sym = _root_form_ap_vec_setting['sym']
        if f._pAti_form['base_form'] is None:
            sym_repr = setting_sym[0] + f._sym_repr + setting_sym[1]
        else:
            ss = _form_evaluate_at_repr_setting['sym']
            sym_repr = f._sym_repr.split(ss[1])[0].split(ss[0])[1]
            sym_repr = setting_sym[0] + sym_repr + setting_sym[1]
            sym_repr = ss[0] + sym_repr + ss[1] + f._sym_repr.split(ss[1])[1]
    else:
        pass

    lr = f._pure_lin_repr + _root_form_ap_vec_setting['lin']

    return _parse_root_form_ap_col_vec(sym_repr, lr)


_global_col_vec = dict()  # we use lin_repr as keys as lin_repr is dependent to f.lin_repr.


def _parse_root_form_ap_col_vec(sym_repr, lin_repr):
    """"""
    assert lin_repr not in _global_col_vec, f"Cannot be because we cache the ap of root-forms."
    cv = ColVec(sym_repr, lin_repr)
    _global_col_vec[lin_repr] = cv
    return cv


class ColVec(Frozen):
    """column vector."""
    def __init__(self, sym_repr, lin_repr):
        self._sym_repr = sym_repr
        lin_repr, pure_lin_repr = _parse_lin_repr('col_vec', lin_repr)
        self._lin_repr = lin_repr
        self._pure_lin_repr = pure_lin_repr
        self._freeze()

    def __repr__(self):
        """repr"""
        super_repr = super().__repr__().split('object')[1]
        return f"<ColVec {self._lin_repr}" + super_repr
