# -*- coding: utf-8 -*-
"""
pH-lib@RAM-EEMCS-UT
created at: 3/2/2023 3:06 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')

from src.tools.frozen import Frozen


def inner(f1, f2, method='L2'):
    """"""

    if f1.__class__.__name__ == 'Form' or f2.__class__.__name__ == 'Form':
        pass
    else:
        raise NotImplementedError()

    s1 = f1.space
    s2 = f2.space

    if s1._quasi_equal(s2):
        pass
    else:
        raise Exception(f'cannot do inner product between {s1} and {s2}.')

    if method == 'L2':
        return L2InnerProductTerm(f1, f2)
    else:
        raise NotImplementedError()


class L2InnerProductTerm(Frozen):
    """"""

    def __init__(self, f1, f2):
        """"""

        assert f1.space._quasi_equal(f2.space), f"spaces dis-match."
        self._f1 = f1
        self._f2 = f2

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

        self._sym_repr = rf'\left({sr1},{sr2}\right)_' + r"{L^2}"
        self._lin_repr = r"\emph{L2 inner product between} " + lr1 + r' \emph{and} ' + lr2
        self._simple_patterns = _simpler_pattern_examiner(f1, f2)

        self._freeze()

    def __repr__(self):
        """"""
        super_repr = super().__repr__().split('object')[1]
        return '<L2IP ' + self._sym_repr + f'{super_repr}'


simpler_patterns = {
    '(codifferential sf, sf)',
}


def _simpler_pattern_examiner(f1, f2):
    s1 = f1.space
    s2 = f2.space
    if s1.__class__.__name__ == 'ScalarValuedFormSpace' and s2.__class__.__name__ == 'ScalarValuedFormSpace':
        return _simpler_pattern_examiner_scalar_valued_forms(f1, f2)
    else:
        raise NotImplementedError()

def _simpler_pattern_examiner_scalar_valued_forms(f1, f2):
    patterns = list()
    if f1._sym_repr[:15] == r'\mathrm{d}^\ast':
        patterns.append('(codifferential sf, sf)')

    return tuple(patterns)


