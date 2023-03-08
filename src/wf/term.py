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
from src.form.operators import _parse_related_time_derivative, _implemented_operators


class _WeakFormulationTerm(Frozen):
    """Factor multiplies the term, <f1|f2> or (f1, f2).
    """

    def __init__(self, mesh, f1, f2, factor=None):
        """"""
        self._mesh = mesh
        self._f1 = f1
        self._f2 = f2
        self._factor = factor

        if factor is None:
            self._factor_sym_repr = None
            self._factor_lin_repr = None
        elif isinstance(factor, (int, float)):
            self._factor_sym_repr = str(factor)
            self._factor_lin_repr = rf"({str(factor)})"

        self._simple_patterns = _simpler_pattern_examiner(f1, f2)
        for sp in self._simple_patterns:
            assert sp in simple_patterns, f"found unknown simple pattern: {sp}."
        self._elementary_forms = set()
        self._elementary_forms.update(f1._elementary_forms)
        self._elementary_forms.update(f2._elementary_forms)
        self._sym_repr = None
        self._lin_repr = None
        self._freeze()

    @property
    def mesh(self):
        """The mesh."""
        return self._mesh

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

    # def replace(self, f, by, which='all'):
    #     """replace form `f` in this term by `by`,
    #     if there are more than one `f` found, apply the replacement to `which`.
    #     If there are 'f' in this term, which should be int or a list of int which indicating
    #     `f` according the sequence of `f._lin_repr` in `self._lin_repr`.
    #     """
    #     raise NotImplementedError()

    def split(self, f, into, signs, which=None):
        """Split `which` `f` `into`."""
        if f in ('f1', 'f2'):
            assert which is None, f"When specify f1 or f2, no need to set `which`."
            term_class = self.__class__
            f2 = self._f2
            assert isinstance(into, (list, tuple)), f"put split objects into a list or tuple."
            assert len(into) > 1, f"number of split objects must be larger than 1."
            assert len(into) == len(signs), f"objects and signs length dis-match."
            new_terms = list()
            for i, ifi in enumerate(into):
                assert signs[i] in ('+', '-'), f"{i}th sign = {signs[i]} is wrong."
                assert ifi.__class__.__name__ == 'Form', f"{i}th object = {ifi} is not a form."
                assert ifi.mesh == f2.mesh, f"mesh of {i}th object = {ifi.mesh} does not fit."
                # noinspection PyArgumentList
                term = term_class(ifi, f2)
                new_terms.append(term)
            return new_terms, signs

        else:
            raise NotImplementedError()


def duality_pairing(f1, f2):
    """

    Parameters
    ----------
    f1
    f2

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
    return DualityPairingTerm(f1, f2)


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
        f2.print_representations()

        s1 = f1.space
        s2 = f2.space
        if s1.__class__.__name__ == 'ScalarValuedFormSpace' and s2.__class__.__name__ == 'ScalarValuedFormSpace':
            assert s1.mesh == s2.mesh and s1.k + s2.k == s1.mesh.ndim, \
                f"cannot do duality pairing between {f1} in {s1} and {f2} in {s2}."
        else:
            raise Exception(f'cannot do duality pairing between {f1} in {s1} and {f2} in {s2}.')

        super().__init__(f1.mesh, f1, f2, factor=factor)

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

        sym_repr = rf'\left<\left.{sr1}\right|{sr2}\right>_' + r"{" + self._mesh.manifold._sym_repr + "}"
        lin_repr = r"\emph{duality-pairing between} " + lr1 + r' \emph{and} ' + lr2
        lin_repr += r" \emph{over} " + self.mesh.manifold._lin_repr
        self._sym_repr = sym_repr
        self._lin_repr = lin_repr

    def __repr__(self):
        """"""
        super_repr = super().__repr__().split('object')[1]
        return '<Duality Pairing ' + self._sym_repr + f'{super_repr}'


def inner(f1, f2, method='L2'):
    """

    Parameters
    ----------
    f1
    f2
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
        return L2InnerProductTerm(f1, f2)
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

        super().__init__(f1.mesh, f1, f2, factor=factor)

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

        sym_repr = rf'\left({sr1},{sr2}\right)_' + r"{" + self._mesh.manifold._sym_repr + "}"
        lin_repr = r"\emph{L2-inner-product between} " + lr1 + r' \emph{and} ' + lr2
        lin_repr += r" \emph{over} " + self.mesh.manifold._lin_repr

        self._sym_repr = sym_repr
        self._lin_repr = lin_repr

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


simple_patterns = {   # use only str to represent a pattern.
    '(partial_t root-sf, sf)',
    '(codifferential sf, sf)',
}


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
    if f1._lin_repr[:24] == _implemented_operators['codifferential']:
        patterns.append('(codifferential sf, sf)')

    if f1._lin_repr[:25] == _implemented_operators['time_derivative']:
        bf1 = _find_form(f1._lin_repr, upon=time_derivative)
        if bf1.is_root and _parse_related_time_derivative(f2) == list():
            patterns.append('(partial_t root-sf, sf)')

    return tuple(patterns)
