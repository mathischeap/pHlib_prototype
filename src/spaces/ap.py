# -*- coding: utf-8 -*-
"""
pH-lib@RAM-EEMCS-UT
created at: 3/20/2023 5:17 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')

from src.spaces.main import _default_mass_matrix_reprs
from src.spaces.main import _default_d_matrix_reprs
from src.spaces.main import _default_wedge_vector_repr
from src.algebra.array import _global_root_arrays, _array
from src.spaces.operators import d


def _parse_l2_inner_product_mass_matrix(s0, s1, d0, d1):
    """"""
    assert s0 == s1, f"spaces do not match."

    if s0.__class__.__name__ == 'ScalarValuedFormSpace' and s1.__class__.__name__ == 'ScalarValuedFormSpace':
        sym, lin = _default_mass_matrix_reprs['Omega']
        assert d0 is not None and d1 is not None, f"space is not finite."
        sym += rf"^{s0.k}"
        for lr in _global_root_arrays:
            existing_m = _global_root_arrays[lr]
            if existing_m._sym_repr == sym:
                sym += r"_{" + str((d0, d1)) + "}"
                break
            else:
                continue

        lin = lin.replace('{n}', str(s0.n))
        lin = lin.replace('{k}', str(s0.k))
        lin = lin.replace('({d0},{d1})', str((d0, d1)))

        return _array(sym, lin, (s0._sym_repr + '-' + str(d0), s1._sym_repr + '-' + str(d1)))

    else:
        raise NotImplementedError()


def _parse_d_matrix(s0, d0):
    """"""
    if s0.__class__.__name__ == 'ScalarValuedFormSpace':
        assert d0 is not None, f"space is not finite."
        sym, lin = _default_d_matrix_reprs['Omega']

        ds = d(s0)

        lin = lin.replace('{n}', str(s0.n))
        lin = lin.replace('{k}', str(s0.k))
        lin = lin.replace('{d}', str(d0))
        sym += r"^{" + str((s0.k+1, s0.k)) + r"}"

        return _array(sym, lin, (ds._sym_repr + '-' + str(d0), s0._sym_repr + '-' + str(d0)))

    else:
        raise NotImplementedError()


def _parse_wedge_vector(f0, s1, d1):
    """

    Parameters
    ----------
    f0 :
        It is f0 dependent. So do not use s0.
    s1
    d1

    Returns
    -------

    """
    s0 = f0.space
    if s0.__class__.__name__ == 'ScalarValuedFormSpace' and s1.__class__.__name__ == 'ScalarValuedFormSpace':
        assert d1 is not None, f"space is not finite."
        sym, lin = _default_wedge_vector_repr['Omega']

        print(sym, lin)
    else:
        raise NotImplementedError()
