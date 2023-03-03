# -*- coding: utf-8 -*-
"""
pH-lib@RAM-EEMCS-UT
created at: 3/2/2023 3:06 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')

from src.tools.frozen import Frozen
from src.spaces.main import new
from src.form import _global_forms, _global_form_variables
from src.form import codifferential, d

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
        assert f1.space._quasi_equal(f2.space), f"spaces dis-match."   # mesh consistence checked here.
        self._f1 = f1
        self._f2 = f2
        self._mesh = f1.mesh

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

        self._elementary_forms = set()
        self._elementary_forms.update(f1._elementary_forms)
        self._elementary_forms.update(f2._elementary_forms)
        self._freeze()

    def __repr__(self):
        """"""
        super_repr = super().__repr__().split('object')[1]
        return '<L2IP ' + self._sym_repr + f'{super_repr}'

    @property
    def mesh(self):
        return self._mesh

    def _integration_by_parts(self):
        """"""
        if '(codifferential sf, sf)' in self._simple_patterns:
            _global_form_variables['update_cache'] = False
            # we found the sf by testing all existing forms, this is bad. Update this in the future.
            bf = None
            for form_id in _global_forms:
                form = _global_forms[form_id]
                try:
                    ds_f = codifferential(form)
                except:
                    continue
                else:
                    if ds_f._sym_repr == self._f1._sym_repr:
                        bf = form
                        break
                    else:
                        pass

            assert bf is not None, f"something is wrong, we do not found the base form " \
                                   f"(codifferential of base form = f1)."

            _global_form_variables['update_cache'] = True

            term1 = L2InnerProductTerm(bf, d(self._f2))

            partial_mesh = self.mesh.boundary()

            boundary_space = new('Omega', bf.space.k-1, bf.space.p, mesh=partial_mesh)





        else:
            raise Exception(f"Cannot apply integration by parts to this term.")



simple_patterns = {
    '(codifferential sf, sf)',
}


def _simpler_pattern_examiner(f1, f2):
    """"""
    s1 = f1.space
    s2 = f2.space
    if s1.__class__.__name__ == 'ScalarValuedFormSpace' and s2.__class__.__name__ == 'ScalarValuedFormSpace':
        return _simpler_pattern_examiner_scalar_valued_forms(f1, f2)
    else:
        raise NotImplementedError()

def _simpler_pattern_examiner_scalar_valued_forms(f1, f2):
    """"""
    patterns = list()
    if f1._sym_repr[:15] == r'\mathrm{d}^\ast':
        patterns.append('(codifferential sf, sf)')

    return tuple(patterns)
