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

from src.form.operators import wedge

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
            assert isinstance(sym_repr, str), \
                f"sym_repr must be a str of length > 0."
            assert ' ' not in sym_repr, f"root form symbolic represent cannot have space."  # this is important
            # make sure it does not confuse operator lin repr
            assert len(sym_repr) > 0, \
                f"sym_repr must be a str of length > 0."
            for form_id in _global_forms:
                form = _global_forms[form_id]
                assert sym_repr != form._sym_repr, \
                    f"root form symbolic representation={sym_repr} is taken. Pls use another one."
                assert lin_repr != form._lin_repr, \
                    f"root form linguistic representation={lin_repr} is taken. Pls use another one."
            assert 'emph' not in lin_repr, f"A safety check, almost trivial."
            assert lin_repr[:8] == r"\textsf{" and lin_repr[-1] == r'}', \
                f"root form linguistic representation = {lin_repr} illegal, it be must be of form " + r"\textsf{...}."
            _net_lin_repr = lin_repr[8:-1]
            if '@' in _net_lin_repr:
                assert _net_lin_repr.count('@') == 1, f"trivial check!"
                _pure_lin_repr = _net_lin_repr.split('@')[0]
            else:
                _pure_lin_repr = _net_lin_repr
            _pure_lin_repr = _pure_lin_repr.replace('-', '')
            assert _pure_lin_repr.isalnum(), rf'lin_repr={lin_repr} illegal. ' + \
                                             "In {} (and before @ if existing), " \
                                             "it must only have letters, numbers and '-'."
        else:
            pass

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
        self._freeze()

    def print_representations(self):
        """Print this form with matplotlib and latex."""
        my_id = r'\texttt{' + str(id(self)) + '}'
        if self._pAti_form['base_form'] is None:
            pti_text = ''
        else:
            base_form, ats, ati = self._pAti_form['base_form'], self._pAti_form['ats'], self._pAti_form['ati']
            pti_text = rf"\\(${base_form._sym_repr}$ at abstract time instant ${ati._sym_repr}$,\\"
            pti_text += r"i.e. \textsf{" + rf"t['{ati.k}']" + r"} of abstract time sequence: "
            pti_text += rf"${ats._lin_repr}$.)"
        plt.figure(figsize=(3 + len(self._sym_repr)/4, 4))
        plt.axis([0, 1, 0, 5])
        plt.text(0, 4.5, f'form id: {my_id}', ha='left', va='center', size=15)
        plt.text(0, 3.5, f'spaces: ${self.space._sym_repr}$', ha='left', va='center', size=15)
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
        if isinstance(other, (int, tuple)):
            num_str = str(other)
            lr = self._lin_repr
            sr = self._sym_repr
            if self.is_root():
                lr = lr + r" \emph{divided by} (" + num_str + ")"
            else:
                lr = '[' + lr + ']' + r" \emph{divided by} (" + num_str + ")"
            sr = r"\dfrac{" + sr + r"}{" + num_str + "}"
            f = Form(
                self.space,  # space
                sr,          # symbolic representation
                lr,          # linguistic representation
                False,       # not a root-form anymore.
                self._elementary_forms,
                self.orientation,
            )
            return f

        elif other.__class__.__name__ == 'AbstractTimeInterval':
            ati = other
            ati_sr = ati._sym_repr
            ati_lr = ati._lin_repr
            lr = self._lin_repr
            sr = self._sym_repr

            if self.is_root():
                lr = lr + r" \emph{divided by} (" + ati_lr + ")"
            else:
                lr = '[' + lr + ']' + r" \emph{divided by} (" + ati_lr + ")"
            sr = r"\dfrac{" + sr + r"}{" + ati_sr + "}"
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
        """"""
        if ati.__class__.__name__ == 'AbstractTimeInstant':
            assert self.is_root(), f"Can only evaluate a root form at an abstract time instant."
            k = ati.k
            sym_repr = self._sym_repr
            lin_repr = self._lin_repr[:-1]
            sym_repr = r"\left." + sym_repr + r"\right|^{(" + k + ')}'
            lin_repr += "@" + ati._lin_repr + "}"

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

            return ftk
        else:
            raise NotImplementedError(f"Cannot evaluate {self} at {ati}.")
