# -*- coding: utf-8 -*-
"""
pH-lib@RAM-EEMCS-UT
created at: 3/8/2023 12:05 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')

from src.tools.frozen import Frozen
from typing import Dict
import matplotlib.pyplot as plt
import matplotlib
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "DejaVu Sans",
    "text.latex.preamble": r"\usepackage{amsmath}"
})
matplotlib.use('TkAgg')

from src.config import _parse_lin_repr
from src.form.operators import wedge
from src.config import _check_sym_repr
from src.form.parameters import constant_scalar
from src.config import _global_operator_lin_repr_setting

_global_forms = dict()
_global_form_variables = {
    'update_cache': True
}


class Form(Frozen):
    """The form class."""

    def __init__(
            self, space,
            sym_repr, lin_repr,
            is_root,
            elementary_forms,
            orientation,
    ):
        assert isinstance(is_root, bool), f"is_root must be bool."
        self._space = space

        if is_root:  # we check the `sym_repr` only for root forms.
            lin_repr, self._pure_lin_repr = _parse_lin_repr('form', lin_repr)
            for form_id in _global_forms:
                form = _global_forms[form_id]
                assert sym_repr != form._sym_repr, \
                    f"root form symbolic representation={sym_repr} is taken. Pls use another one."
                assert lin_repr != form._lin_repr, \
                    f"root form linguistic representation={lin_repr} is taken. Pls use another one."
        else:
            self._pure_lin_repr = None

        sym_repr = _check_sym_repr(sym_repr)
        self._sym_repr = sym_repr
        self._lin_repr = lin_repr
        self._is_root = is_root
        if is_root is True:
            if elementary_forms is None:
                elementary_forms = [self, ]
            else:
                _ = list(elementary_forms)
                assert _[0] is self, f"A root form must have self as its elementary_form."
        else:
            assert elementary_forms is not None, f"must provide elementary forms for a non-root form."
            if elementary_forms .__class__.__name__ == 'Form':
                elementary_forms = [elementary_forms, ]
            else:
                assert isinstance(elementary_forms, (list, tuple, set)) and \
                    all([f.__class__.__name__ == 'Form' for f in elementary_forms]), \
                    f'pls set only forms and put them in a list or tuple or set.'
        self._elementary_forms = set(elementary_forms)

        assert orientation in ('inner', 'outer', 'i', 'o', None, 'None'), \
            f"orientation={orientation} is wrong, must be one of ('inner', 'outer', 'i', 'o', None)."
        if orientation == 'i':
            orientation = 'inner'
        elif orientation == 'o':
            orientation = 'outer'
        elif orientation is None:
            orientation = 'None'
        else:
            pass
        self._orientation = orientation
        if _global_form_variables['update_cache']:  # cache it
            _global_forms[id(self)] = self
        else:
            pass
        self._pAti_form: Dict = {
            'base_form': None,
            'ats': None,
            'ati': None
        }
        self._abstract_forms = dict()   # the abstract forms based on this form.
        self._freeze()

    def print_representations(self):
        """Print this form with matplotlib and latex."""
        my_id = r'\texttt{' + str(id(self)) + '}'
        if self._pAti_form['base_form'] is None:
            pti_text = ''
        else:
            base_form, ats, ati = self._pAti_form['base_form'], self._pAti_form['ats'], self._pAti_form['ati']
            pti_text = rf"\\(${base_form._sym_repr}$ at abstract time instant ${ati._sym_repr}$"
        space_text = f'spaces: ${self.space._sym_repr}$'
        space_text += rf"\ \ \ \ on ({self.mesh._lin_repr})"
        plt.figure(figsize=(3 + len(self._sym_repr)/4, 4))
        plt.axis([0, 1, 0, 5])
        plt.text(0, 4.5, f'form id: {my_id}', ha='left', va='center', size=15)
        plt.text(0, 3.5, space_text, ha='left', va='center', size=15)
        plt.text(0, 2.5, rf'\noindent symbolic : ' + f"${self._sym_repr}$" + pti_text, ha='left', va='center', size=15)
        plt.text(0, 1.5, 'linguistic : ' + self._lin_repr, ha='left', va='center', size=15)
        root_text = rf'is_root: {self.is_root()}'
        plt.text(0, 0.5, root_text, ha='left', va='center', size=15)
        plt.axis('off')
        plt.show()

    def __repr__(self):
        """"""
        super_repr = super().__repr__().split('object')[-1]
        return '<Form ' + self._sym_repr + super_repr  # this will be unique.

    @property
    def orientation(self):
        """The orientation of this form."""
        return self._orientation

    def is_root(self):
        """Return True this form is a root form."""
        return self._is_root

    @property
    def space(self):
        """The space this form is in."""
        return self._space

    @property
    def mesh(self):
        """The mesh this form is on."""
        return self.space.mesh

    def wedge(self, other):
        """Return a form representing `self` wedge `other`."""
        return wedge(self, other)

    def __neg__(self):
        """- self"""
        raise NotImplementedError()

    def __add__(self, other):
        """self + other"""
        raise NotImplementedError()

    def __sub__(self, other):
        """self-other"""
        raise NotImplementedError()

    def __mul__(self, other):
        """self * other"""
        raise NotImplementedError()

    def __rmul__(self, other):
        """other * self"""
        raise NotImplementedError()

    def __truediv__(self, other):
        """self / other"""
        operator_lin = _global_operator_lin_repr_setting['divided']
        if isinstance(other, (int, tuple)):
            cs = constant_scalar(other)
            return self / cs

        elif other.__class__.__name__ == 'AbstractTimeInterval':
            ati = other
            return self / ati._as_scalar()

        elif other.__class__.__name__ == 'ConstantScalar0Form':
            lr = self._lin_repr
            sr = self._sym_repr
            cs = other
            if self.is_root():
                lr = lr + operator_lin + cs._lin_repr
            else:
                lr = '[' + lr + ']' + operator_lin + cs._lin_repr
            sr = r"\dfrac{" + sr + r"}{" + cs._sym_repr + "}"
            f = Form(
                self.space,  # space
                sr,          # symbolic representation
                lr,          # linguistic representation
                False,       # not a root-form anymore.
                self._elementary_forms,
                self.orientation,
            )
            return f

        else:
            raise NotImplementedError(f"form divided by <{other.__class__.__name__}> is not implemented.")

    def evaluate_at(self, ati):
        """evaluate_at"""
        if ati.__class__.__name__ == 'AbstractTimeInstant':
            assert self.is_root(), f"Can only evaluate a root form at an abstract time instant."
            sym_repr = self._sym_repr
            lin_repr = self._pure_lin_repr
            sym_repr = r"\left." + sym_repr + r"\right|^{(" + ati.k + ')}'
            lin_repr += "@" + ati._pure_lin_repr

            if lin_repr in self._abstract_forms:   # we cache it, this is very important.
                pass
            else:
                ftk = Form(
                    self._space,
                    sym_repr, lin_repr,
                    self._is_root,
                    None,    # elementary_forms
                    self._orientation,
                )
                ftk._pAti_form['base_form'] = self
                ftk._pAti_form['ats'] = ati.time_sequence
                ftk._pAti_form['ati'] = ati
                self._abstract_forms[lin_repr] = ftk

            return self._abstract_forms[lin_repr]

        else:
            raise NotImplementedError(f"Cannot evaluate {self} at {ati}.")
