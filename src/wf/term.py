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
from src.form import _find_form
from src.form import codifferential, d, trace, Hodge


class _WeakFormulationTerm(Frozen):
    """"""

    def __init__(self, mesh, f1, f2):
        """"""
        self._mesh = mesh
        self._f1 = f1
        self._f2 = f2
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
        plt.figure(figsize=(2 + len(self._sym_repr)/10, 2))
        plt.axis([0, 1, 0, 1])
        plt.text(0, 0.5, 'symbolic : ' + f"${self._sym_repr}$", ha='left', va='center', size=15)
        plt.axis('off')
        plt.show()

    def _replace(self, f, by, which='all'):
        """replace `f` by `by`, if there are more than one `f` found, apply the replacement to `which`."""



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
    return DualityPairing(f1, f2)


class DualityPairing(_WeakFormulationTerm):
    """

    Parameters
    ----------
    f1
    f2
    """

    def __init__(self, f1, f2):
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

        super().__init__(f1.mesh, f1, f2)

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

        self._sym_repr = rf'\left<\left.{sr1}\right|{sr2}\right>_' + r"{" + self._mesh.manifold._sym_repr + "}"
        self._lin_repr = r"\emph{duality pairing between} " + lr1 + r' \emph{and} ' + lr2

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

    def __init__(self, f1, f2):
        """

        Parameters
        ----------
        f1
        f2
        """
        s1 = f1.space
        s2 = f2.space
        if s1.__class__.__name__ == 'ScalarValuedFormSpace' and s2.__class__.__name__ == 'ScalarValuedFormSpace':
            assert s1.mesh == s2.mesh and s1.k == s2.k, f"spaces dis-match."   # mesh consistence checked here.
        else:
            raise NotImplementedError()

        super().__init__(f1.mesh, f1, f2)

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

        self._sym_repr = rf'\left({sr1},{sr2}\right)_' + r"{" + self._mesh.manifold._sym_repr + "}"
        self._lin_repr = r"\emph{L2 inner product between} " + lr1 + r' \emph{and} ' + lr2

    def __repr__(self):
        """"""
        super_repr = super().__repr__().split('object')[1]
        return '<L2IP ' + self._sym_repr + f'{super_repr}'

    def _integration_by_parts(self):
        """"""
        if '(codifferential sf, sf)' in self._simple_patterns:
            # we try to find the sf by testing all existing forms, this is bad. Update this in the future.
            bf = _find_form(self._f1._sym_repr, upon=codifferential)
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
    if f1._sym_repr[:15] == r'\mathrm{d}^\ast':
        patterns.append('(codifferential sf, sf)')

    if f1._sym_repr[:10] == r'\partial_t':
        bf1 = _find_form(f1._sym_repr[11:])  # use 11 as there is a space between `\partial_t` and root form sym_repr.
        if bf1.is_root and r'\partial_t' not in f2._sym_repr:
            patterns.append('(partial_t root-sf, sf)')

    return tuple(patterns)
