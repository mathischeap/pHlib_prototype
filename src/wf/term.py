# -*- coding: utf-8 -*-
"""
pH-lib@RAM-EEMCS-UT
created at: 3/2/2023 3:06 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')

import matplotlib.pyplot as plt
import matplotlib
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "DejaVu Sans",
    "text.latex.preamble": r"\usepackage{amsmath}"
})
matplotlib.use('TkAgg')

from src.tools.frozen import Frozen
from src.form.tools import _find_form
from src.form.operators import codifferential, d, trace, Hodge, time_derivative
from src.form.operators import _parse_related_time_derivative
from src.config import _global_operator_lin_repr_setting
from src.config import _wf_term_default_simple_patterns as _simple_patterns
from src.form.parameters import constant_scalar
_cs1 = constant_scalar(1)


class _WeakFormulationTerm(Frozen):
    """Factor multiplies the term, <f1|f2> or (f1, f2).
    """

    def __init__(self, f1, f2, factor=None):
        """"""
        self._mesh = f1.mesh
        self._f1 = f1
        self._f2 = f2
        self._factor = factor

        if factor is None:
            self._factor = _cs1
        elif isinstance(factor, (int, float)):
            self._factor = constant_scalar(factor)
        elif factor.__class__.__name__ == "ConstantScalar0Form":
            self._factor = factor
        else:
            raise NotImplementedError(f'f{factor}')

        self._simple_patterns = _simpler_pattern_examiner(f1, f2)
        for sp in self._simple_patterns:
            assert sp in _simple_patterns.values(), f"found unknown simple pattern: {sp}."
        self._efs = set()
        self._efs.update(f1.elementary_forms)
        self._efs.update(f2.elementary_forms)
        self.___sym_repr___ = None
        self.___lin_repr___ = None
        self._freeze()

    @property
    def _sym_repr(self):
        if self._factor == _cs1:
            return self.___sym_repr___
        else:
            return self._factor._sym_repr + self.___sym_repr___

    @property
    def _lin_repr(self):
        if self._factor == _cs1:
            return self.___lin_repr___
        else:
            return self._factor._sym_repr + _global_operator_lin_repr_setting['multiply'] + self.___sym_repr___

    @property
    def mesh(self):
        """The mesh."""
        return self._mesh

    @property
    def elementary_forms(self):
        return self._efs

    @staticmethod
    def _is_able_to_be_a_weak_term():
        return True

    @staticmethod
    def _is_real_number_valued():
        return True

    def print_representations(self):
        """Print the representations of this term."""
        plt.figure(figsize=(5 + len(self._lin_repr)/20, 2))
        plt.axis([0, 1, 0, 1])
        plt.text(0, 0.75, 'linguistic : ' + f"{self._lin_repr}", ha='left', va='center', size=15)
        plt.text(0, 0.25, 'symbolic : ' + f"${self._sym_repr}$", ha='left', va='center', size=15)
        plt.axis('off')
        plt.show()

    def print(self):
        """A wrapper of print_representations"""
        return self.print_representations()

    def replace(self, f, by, which='all', change_sign=False):
        """replace form `f` in this term by `by`,
        if there are more than one `f` found, apply the replacement to `which`.
        If there are 'f' in this term, which should be int or a list of int which indicating
        `f` according the sequence of `f._lin_repr` in `self._lin_repr`.
        """
        if f == 'f1':
            assert by.__class__.__name__ == 'Form' and by.space == f.space, f"Spaces do not match."
            assert self._f1.space == by.space, f"spaces do not match."
            return self.__class__(by, self._f2, factor=self._factor)

        elif f == 'f2':
            assert by.__class__.__name__ == 'Form' and by.space == f.space, f"Spaces do not match."
            assert self._f2.space == by.space, f"spaces do not match."
            return self.__class__(self._f1, by, factor=self._factor)

        elif f.__class__.__name__ == 'Form':
            assert f.space == by.space, f"spaces do not match."
            if which == 'all':
                places = {
                    'f1': 'all',
                    'f2': 'all',
                }
            else:
                raise NotImplementedError()

            f1 = self._f1
            f2 = self._f2
            factor = self._factor

            for place in places:
                if place == 'f1':
                    f1 = self._f1.replace(f, by, which=places['f1'])
                elif place == 'f2':
                    f2 = self._f2.replace(f, by, which=places['f2'])
                else:
                    raise NotImplementedError
            if change_sign:
                sign = '-'
            else:
                sign = '+'
            return sign, self.__class__(f1, f2, factor=factor)

        else:
            raise NotImplementedError()

    def reform(self, f, into, signs, which=None):
        """Split `which` `f` `into` of `signs`."""
        if f in ('f1', 'f2'):
            assert which is None, f"When specify f1 or f2, no need to set `which`."
            term_class = self.__class__
            f2 = self._f2
            if into.__class__.__name__ == 'Form':
                into = [into, ]
                assert signs in ('+', '-'), f"when give one form, sign must be in '+' or  '-'."
                signs = [signs, ]
            else:
                pass
            assert isinstance(into, (list, tuple)), f"put split objects into a list or tuple."
            assert len(into) >= 1, f"number of split objects must be equal to or larger than 1."
            assert len(into) == len(signs), f"objects and signs length dis-match."
            new_terms = list()
            for i, ifi in enumerate(into):
                assert signs[i] in ('+', '-'), f"{i}th sign = {signs[i]} is wrong."
                assert ifi.__class__.__name__ == 'Form', f"{i}th object = {ifi} is not a form."
                assert ifi.mesh == f2.mesh, f"mesh of {i}th object = {ifi.mesh} does not fit."
                # noinspection PyArgumentList
                term = term_class(ifi, f2)
                new_terms.append(term)
            return signs, new_terms

        else:
            raise NotImplementedError()


def duality_pairing(f1, f2, factor=None):
    """

    Parameters
    ----------
    f1
    f2
    factor

    Returns
    -------

    """
    s1 = f1.space
    s2 = f2.space
    if s1.__class__.__name__ == 'ScalarValuedFormSpace' and s2.__class__.__name__ == 'ScalarValuedFormSpace':
        assert s1.mesh == s2.mesh and s1.k + s2.k == s1.mesh.ndim, \
            f"cannot do duality pairing between {f1} in {s1} and {f2} in {s2}."
    else:
        raise Exception(f'cannot do duality pairing between {f1} in {s1} and {f2} in {s2}.')
    return DualityPairingTerm(f1, f2, factor=factor)


class DualityPairingTerm(_WeakFormulationTerm):
    """

    Parameters
    ----------
    f1
    f2
    """

    def __init__(self, f1, f2, factor=None):
        """

        Parameters
        ----------
        f1
        f2
        """
        s1 = f1.space
        s2 = f2.space
        if s1.__class__.__name__ == 'ScalarValuedFormSpace' and s2.__class__.__name__ == 'ScalarValuedFormSpace':
            assert s1.mesh == s2.mesh and s1.k + s2.k == s1.mesh.ndim, \
                f"cannot do duality pairing between {f1} in {s1} and {f2} in {s2}."
        else:
            raise Exception(f'cannot do duality pairing between {f1} in {s1} and {f2} in {s2}.')

        super().__init__(f1, f2, factor=factor)

        sr1 = f1._sym_repr
        sr2 = f2._sym_repr

        lr1 = f1._lin_repr
        lr2 = f2._lin_repr

        if f1.is_root():
            pass
        else:
            lr1 = rf'[{lr1}]'

        if f2.is_root():
            pass
        else:
            lr2 = rf'[{lr2}]'
        olr0, olr1, olr2 = _global_operator_lin_repr_setting['duality-pairing']
        sym_repr = rf'\left<\left.{sr1}\right|{sr2}\right>_' + r"{" + self._mesh.manifold._sym_repr + "}"
        lin_repr = olr0 + lr1 + olr1 + lr2 + olr2 + self.mesh.manifold._lin_repr
        self.___sym_repr___ = sym_repr
        self.___lin_repr___ = lin_repr

    def __repr__(self):
        """"""
        super_repr = super().__repr__().split('object')[1]
        return '<Duality Pairing ' + self._sym_repr + f'{super_repr}'


def inner(f1, f2, factor=None, method='L2'):
    """

    Parameters
    ----------
    f1
    f2
    factor
    method

    Returns
    -------

    """

    if f1.__class__.__name__ == 'Form' or f2.__class__.__name__ == 'Form':
        pass
    else:
        raise NotImplementedError()

    s1 = f1.space
    s2 = f2.space

    if s1.__class__.__name__ == 'ScalarValuedFormSpace' and s2.__class__.__name__ == 'ScalarValuedFormSpace':
        assert s1.mesh == s2.mesh and s1.k == s2.k, \
            f"cannot do inner product between {f1} in {s1} and {f2} in {s2}."
    else:
        raise Exception(f'cannot do inner product between {f1} in {s1} and {f2} in {s2}.')

    if method == 'L2':
        return L2InnerProductTerm(f1, f2, factor=factor)
    else:
        raise NotImplementedError()


class L2InnerProductTerm(_WeakFormulationTerm):
    """

    Parameters
    ----------
    f1
    f2
    """

    def __init__(self, f1, f2, factor=None):
        """

        Parameters
        ----------
        f1
        f2
        """
        s1 = f1.space
        s2 = f2.space
        if s1.__class__.__name__ == 'ScalarValuedFormSpace' and s2.__class__.__name__ == 'ScalarValuedFormSpace':
            assert s1 == s2, f"spaces dis-match."   # mesh consistence checked here.
        else:
            raise NotImplementedError()

        super().__init__(f1, f2, factor=factor)

        sr1 = f1._sym_repr
        sr2 = f2._sym_repr

        lr1 = f1._lin_repr
        lr2 = f2._lin_repr

        if f1.is_root():
            pass
        else:
            lr1 = rf'[{lr1}]'

        if f2.is_root():
            pass
        else:
            lr2 = rf'[{lr2}]'

        olr0, olr1, olr2 = _global_operator_lin_repr_setting['L2-inner-product']
        sym_repr = rf'\left({sr1},{sr2}\right)_' + r"{" + self._mesh.manifold._sym_repr + "}"
        lin_repr = olr0 + lr1 + olr1 + lr2 + olr2 + self.mesh.manifold._lin_repr

        self.___sym_repr___ = sym_repr
        self.___lin_repr___ = lin_repr

    def __repr__(self):
        """"""
        super_repr = super().__repr__().split('object')[1]
        return '<L2IP ' + self._sym_repr + f'{super_repr}'

    def _integration_by_parts(self):
        """"""
        if '(codifferential sf, sf)' in self._simple_patterns:
            # we try to find the sf by testing all existing forms, this is bad. Update this in the future.
            bf = _find_form(self._f1._lin_repr, upon=codifferential)
            assert bf is not None, f"something is wrong, we do not found the base form " \
                                   f"(codifferential of base form = f1)."
            term_manifold = L2InnerProductTerm(bf, d(self._f2))

            trace_form_1 = trace(Hodge(bf))

            trace_form_2 = trace(self._f2)

            term_boundary = duality_pairing(trace_form_1, trace_form_2)

            return (term_manifold, term_boundary), ('+', '+')

        else:
            raise Exception(f"Cannot apply integration by parts to this term.")


def _simpler_pattern_examiner(f1, f2):
    """"""
    s1 = f1.space
    s2 = f2.space
    if s1.__class__.__name__ == 'ScalarValuedFormSpace' and s2.__class__.__name__ == 'ScalarValuedFormSpace':
        return _simpler_pattern_examiner_scalar_valued_forms(f1, f2)
    else:
        return tuple()


def _simpler_pattern_examiner_scalar_valued_forms(f1, f2):
    """ """
    patterns = list()
    lin_codifferential = _global_operator_lin_repr_setting['codifferential']
    if f1._lin_repr[:len(lin_codifferential)] == lin_codifferential:
        patterns.append(_simple_patterns['(cd,)'])

    lin_td = _global_operator_lin_repr_setting['time_derivative']
    if f1._lin_repr[:len(lin_td)] == lin_td:
        bf1 = _find_form(f1._lin_repr, upon=time_derivative)
        if bf1.is_root and _parse_related_time_derivative(f2) == list():
            patterns.append(_simple_patterns['(pt,)'])

    return tuple(patterns)
