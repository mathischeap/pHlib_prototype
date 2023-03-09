# -*- coding: utf-8 -*-
"""
pH-lib@RAM-EEMCS-UT
created at: 3/8/2023 3:37 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')

from src.tools.frozen import Frozen
from src.config import _parse_lin_repr
from src.config import _check_sym_repr

_global_parameters = dict()


def constant_scalar(*args):
    """constant scalar"""
    num_args = len(args)

    if num_args == 1:
        arg = args[0]
        if isinstance(arg, (int, float)):
            sym_repr, lin_repr = str(arg), str(arg)
            is_real = True
        else:
            raise NotImplementedError()

    elif num_args == 2:
        sym_repr, lin_repr = args
        assert isinstance(sym_repr, str), f"symbolic representation must be a str."
        assert isinstance(lin_repr, str), f"symbolic representation must be a str."
        is_real = False
    else:
        raise NotImplementedError()

    # --- now we have gotten sym_repr, lin_repr and is_real ------
    assert all([_ is not None for _ in (sym_repr, lin_repr)])
    sym_repr = _check_sym_repr(sym_repr)
    lin_repr, pure_lin_repr = _parse_lin_repr('parameters', lin_repr)
    for pid in _global_parameters:
        p = _global_parameters[pid]
        if lin_repr == p._lin_repr and sym_repr == p._sym_repr:
            return p
        else:
            continue

    for pid in _global_parameters:
        p = _global_parameters[pid]
        assert lin_repr != p._lin_repr, f"lin_repr={lin_repr} is taken."
        assert sym_repr != p._sym_repr, f"sym_repr={sym_repr} is taken."
    assert isinstance(is_real, bool), f"Almost trivial check."
    cs = ConstantScalar0Form(
        sym_repr,
        lin_repr,
        pure_lin_repr,
        is_real,
        True,  # is_root, generate root obj only.
    )
    _global_parameters[id(cs)] = cs
    return cs


class ConstantScalar0Form(Frozen):
    """It is actually a special scalar valued 0-form. But since it is so special,
    we do not wrapper it with a Form class
    """

    def __init__(
            self,
            sym_repr,
            lin_repr,
            pure_lin_repr,
            is_real,
            is_root,
    ):
        """"""
        self._sym_repr = sym_repr
        self._lin_repr = lin_repr
        self._pure_lin_repr = pure_lin_repr
        self._is_real = is_real
        self._is_root = is_root
        self._freeze()

    def print_representations(self):
        """print representations"""
        print(self._sym_repr, self._lin_repr)

    def __repr__(self):
        """repr"""
        real_text = 'real' if self.is_real() else 'abstract'
        super_repr = super().__repr__().split('object')[1]
        return f"<ConstantScalar0Form {real_text} {(self._sym_repr, self._lin_repr)}" + super_repr

    def is_real(self):
        r"""Return True if it is a real number in \mathbb{R}."""
        return self._is_real

    def is_root(self):
        """Return True if I am a root obj."""
        return self._is_root

    def __add__(self, other):
        """self + other"""

    def __radd__(self, other):
        """other + self """


if __name__ == '__main__':
    # python src/form/parameters.py
    import __init__ as ph

    Rn = ph.constant_scalar('R', "Rn")
    print(Rn)
    Rs = ph.constant_scalar(2)
    print(Rs)
