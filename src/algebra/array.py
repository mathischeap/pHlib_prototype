# -*- coding: utf-8 -*-
"""
pH-lib@RAM-EEMCS-UT
created at: 3/21/2023 2:35 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')

from src.tools.frozen import Frozen
from src.config import _parse_lin_repr
from src.config import _non_root_lin_sep, _transpose_text
from src.form.parameters import constant_scalar
_cs1 = constant_scalar(1)


_global_root_arrays = dict()  # using pure_lin_repr as cache keys


def _array(sym_repr, pure_lin_repr, shape, symmetric=None, transposed=None):
    """"""
    if pure_lin_repr in _global_root_arrays:
        return _global_root_arrays[pure_lin_repr]
    else:
        lin_repr, pure_lin_repr = _parse_lin_repr('array', pure_lin_repr)
        aa = AbstractArray(sym_repr, lin_repr, shape, symmetric=symmetric, transposed=transposed)
        aa._pure_lin_repr = pure_lin_repr
        _global_root_arrays[pure_lin_repr] = aa
        return aa


class AbstractArray(Frozen):
    """"""

    def __init__(self, sym_repr, lin_repr, shape, symmetric=None, transposed=None):
        """"""
        self._sym_repr = sym_repr
        self._lin_repr = lin_repr
        self._pure_lin_repr = None
        assert isinstance(shape, tuple), f"pls put shape in a tuple."
        self._shape = shape
        self._symmetric = symmetric    # True or False only for 2-d array
        self._transposed = transposed  # True or False only for 2-d array
        self._freeze()

    def is_root(self):
        return False if self._pure_lin_repr is None else True

    @property
    def shape(self):
        return self._shape

    def _shape_text(self):
        if self.ndim == 2 and self.shape[1] == 1:
            return r'\mathbb{R}^{\#_{dof}' + self.shape[0] + r"}"
        else:
            raise NotImplementedError()

    def __repr__(self):
        """repr"""
        super_repr = super().__repr__().split('object')[1]
        return f"<AbstractArray {self._lin_repr} of shape {self.shape}" + super_repr

    @property
    def ndim(self):
        return len(self.shape)

    @property
    def T(self):
        """Transpose."""
        assert self.ndim == 2, f"Only 2d array has T property."

        if self._symmetric:
            return self
        else:
            pass

        if self._transposed:

            sym = self._sym_repr
            trans_text = r'\right)}^\mathsf{T}'
            if sym[-len(trans_text):] == trans_text:
                sym_repr = sym[7:-len(trans_text)]
            else:
                sym_repr = sym[1:-12]

            lin_repr = self._lin_repr.split(_transpose_text)[0]

        else:

            if self.is_root():
                sym_repr = r'{' + self._sym_repr + r'}^\mathsf{T}'
            else:
                sym_repr = r'{\left(' + self._sym_repr + r'\right)}^\mathsf{T}'

            lin_repr = self._lin_repr + _transpose_text

        shape = (self._shape[1], self._shape[0])
        return AbstractArray(
            sym_repr,
            lin_repr,
            shape,
            transposed=True,
        )

    def _partial_t(self):
        sym_repr = r'\partial_t ' + self._sym_repr
        lin_repr = self._lin_repr
        return AbstractArray(
            sym_repr,
            lin_repr,
            self.shape,
        )

    def __matmul__(self, other):
        """self @ other"""
        if other.__class__.__name__ == 'AbstractArray':

            s_shape = self.shape
            o_shape = other.shape
            assert s_shape[-1] == o_shape[0], f"Cannot do @ between {self} and {other}."

            sym_repr = self._sym_repr + other._sym_repr
            lin_repr = self._lin_repr + '@' + other._lin_repr
            shape = s_shape[:-1] + o_shape[1:]
            return AbstractArray(
                sym_repr,
                lin_repr,
                shape,
            )

        else:
            raise NotImplementedError()

    def __rmul__(self, other):
        """other * self."""
        if isinstance(other, (int, float)):
            other = constant_scalar(other)
        else:
            pass

        if other == _cs1:
            return self
        else:
            sym = self._sym_repr
            lin = self._lin_repr
            osr, olr = other._sym_repr, other._lin_repr
            if other.is_root():
                sym = osr + sym
                lin = olr + lin
            else:
                sym = osr + sym
                lin = _non_root_lin_sep[0] + olr + _non_root_lin_sep[1] + lin

            return self.__class__(sym, lin, self.shape)
