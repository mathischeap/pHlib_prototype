# -*- coding: utf-8 -*-
"""
@author: Yi Zhang
@contact: zhangyi_aero@hotmail.com
@time: 11/26/2022 2:56 PM
"""
from src.form.operators import _parse_related_time_derivative
from src.form.main import _global_root_forms_lin_dict
from src.form.operators import time_derivative, d
from src.config import _global_operator_lin_repr_setting
from src.config import _wf_term_default_simple_patterns as _simple_patterns
from src.form.tools import _find_form
from src.config import _non_root_lin_sep
from src.spaces.ap import _parse_l2_inner_product_mass_matrix
from src.spaces.ap import _parse_d_matrix


def _inner_simpler_pattern_examiner_scalar_valued_forms(factor, f0, f1):
    """ """
    if factor.__class__.__name__ == 'ConstantScalar0Form':
        # (codifferential sf, sf) -------------------------------------------
        lin_codifferential = _global_operator_lin_repr_setting['codifferential']
        if f0._lin_repr[:len(lin_codifferential)] == lin_codifferential:
            return _simple_patterns['(cd,)'], None

        # (partial_time_derivative of root-sf, sf) --------------------------
        lin_td = _global_operator_lin_repr_setting['time_derivative']
        if f0._lin_repr[:len(lin_td)] == lin_td:
            bf0 = _find_form(f0._lin_repr, upon=time_derivative)
            if bf0.is_root and _parse_related_time_derivative(f1) == list():
                return _simple_patterns['(pt,)'], {
                    'rsf0': bf0,   # root-scalar-form-0
                    'rsf1': f1,    # root-scalar-form-1
                }

        # (root-sf, root-sf) ------------------------------------------------
        if f0.is_root() and f1.is_root():
            return _simple_patterns['(rt,rt)'], {
                    'rsf0': f0,   # root-scalar-form-0
                    'rsf1': f1,   # root-scalar-form-1
                }
        else:
            pass

        # (d of root-sf, root-sf) -------------------------------------------
        lin_d = _global_operator_lin_repr_setting['d']
        if f0._lin_repr[:len(lin_d)] == lin_d:
            bf0 = _find_form(f0._lin_repr, upon=d)
            if bf0 is None:
                pass
            elif bf0.is_root() and f1.is_root():
                return _simple_patterns['(d,)'], {
                    'rsf0': bf0,   # root-scalar-form-0
                    'rsf1': f1,    # root-scalar-form-1
                }
            else:
                pass

        # (root-sf, d of root-sf) -------------------------------------------
        lin_d = _global_operator_lin_repr_setting['d']
        if f1._lin_repr[:len(lin_d)] == lin_d:
            bf1 = _find_form(f1._lin_repr, upon=d)
            if bf1 is None:
                pass
            elif f0.is_root() and bf1.is_root():
                return _simple_patterns['(,d)'], {
                    'rsf0': f0,   # root-scalar-form-0
                    'rsf1': bf1,    # root-scalar-form-1
                }
            else:
                pass

        return '', None

    else:
        raise NotImplementedError(f'Not implemented for factor={factor}')


def _dp_simpler_pattern_examiner_scalar_valued_forms(factor, f0, f1):
    """ """
    if factor.__class__.__name__ == 'ConstantScalar0Form':
        lin_tr = _global_operator_lin_repr_setting['trace']
        lin_hodge = _global_operator_lin_repr_setting['Hodge']

        lin = lin_tr + _non_root_lin_sep[0] + lin_hodge
        if f0._lin_repr[:len(lin)] == lin and \
                f0._lin_repr[-len(_non_root_lin_sep[1]):] == _non_root_lin_sep[1] and \
                f1._lin_repr[:len(lin_tr)] == lin_tr:

            bf0_lr = f0._lin_repr[len(lin):-len(_non_root_lin_sep[1])]
            bf1_lr = f1._lin_repr[len(lin_tr):]

            if bf0_lr in _global_root_forms_lin_dict and bf1_lr in _global_root_forms_lin_dict:
                bf0 = _global_root_forms_lin_dict[bf0_lr]
                bf1 = _global_root_forms_lin_dict[bf1_lr]

                return _simple_patterns['<tr star, star>'], {
                    'rsf0': bf0,   # root-scalar-form-0
                    'rsf1': bf1,   # root-scalar-form-1
                }
            else:
                pass
        else:
            pass

        return '', None
    else:
        raise NotImplementedError(f'Not implemented for factor={factor}')


from src.tools.frozen import Frozen


class _SimplePatternAPParser(Frozen):
    """"""

    def __init__(self, wft):
        """"""
        self._wft = wft
        self._freeze()

    def __call__(self):
        """"""
        sp = self._wft._simple_pattern
        if sp == '':
            raise NotImplementedError(f"We do not have an pattern for term {self._wft}.")
        else:
            if sp == _simple_patterns['(pt,)']:
                return self._parse_reprs_pt()
            elif sp == _simple_patterns['(rt,rt)']:
                return self._parse_reprs_rt_rt()
            elif sp == _simple_patterns['(d,)']:
                return self._parse_reprs_d_()
            elif sp == _simple_patterns['(,d)']:
                return self._parse_reprs__d()
            elif sp == _simple_patterns['<tr star, star>']:
                return self._parse_reprs_tr_star_star()
            else:
                raise NotImplementedError(f"not implemented for pattern = {sp}")

    def _parse_reprs_pt(self):
        """"""
        spk = self._wft.___simple_pattern_keys___
        bf0 = spk['rsf0']
        d0 = bf0._degree
        s0 = self._wft._f0.space
        s1 = self._wft._f1.space
        d1 = self._wft._f1._degree
        mass_matrix = _parse_l2_inner_product_mass_matrix(s0, s1, d0, d1)

        v0 = bf0.ap().T
        v1 = self._wft._f1.ap()
        pv0 = v0._partial_t()

        term = pv0 @ mass_matrix @ v1
        return TermAlgebraicProxy(term), '+'


    def _parse_reprs_rt_rt(self):
        """"""
        f0, f1 = self._wft._f0, self._wft._f1
        s0 = f0.space
        s1 = f1.space
        d0 = f0._degree
        d1 = f1._degree
        mass_matrix = _parse_l2_inner_product_mass_matrix(s0, s1, d0, d1)
        v0 = f0.ap().T
        v1 = f1.ap()
        term = v0 @ mass_matrix @ v1
        return TermAlgebraicProxy(term), '+'

    def _parse_reprs_d_(self):
        """"""
        spk = self._wft.___simple_pattern_keys___
        bf0 = spk['rsf0']
        d0 = bf0._degree
        s0 = self._wft._f0.space
        s1 = self._wft._f1.space
        d1 = self._wft._f1._degree
        mass_matrix = _parse_l2_inner_product_mass_matrix(s0, s1, d0, d1)
        d_matrix = _parse_d_matrix(bf0.space, d0)

        v0 = bf0.ap().T
        v1 = self._wft._f1.ap()

        term = v0 @ d_matrix.T @ mass_matrix @ v1
        return TermAlgebraicProxy(term), '+'

    def _parse_reprs__d(self):
        """"""
        s0 = self._wft._f0.space
        d0 = self._wft._f0._degree

        spk = self._wft.___simple_pattern_keys___
        bf1 = spk['rsf1']
        d1 = bf1._degree
        s1 = self._wft._f1.space
        mass_matrix = _parse_l2_inner_product_mass_matrix(s0, s1, d0, d1)
        d_matrix = _parse_d_matrix(bf1.space, d1)

        v0 = self._wft._f0.ap().T
        v1 = bf1.ap()

        term = v0 @ mass_matrix @ d_matrix @ v1
        return TermAlgebraicProxy(term), '+'

    def _parse_reprs_tr_star_star(self):
        """"""



class TermAlgebraicProxy(Frozen):
    """It is basically a wrapper of a (1, 1) abstract array."""

    def __init__(self, term):
        """"""
        assert term.shape == (1, 1), f"term shape = {term.shape} wrong."
        self._sym_repr = term._sym_repr
        self._lin_repr = term._lin_repr
        self._freeze()

    def __repr__(self):
        """repr"""
        super_repr = super().__repr__().split('object')[1]
        return f"<TermAlgebraicProxy {self._sym_repr}" + super_repr
