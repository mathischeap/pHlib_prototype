# -*- coding: utf-8 -*-
"""
@author: Yi Zhang
@contact: zhangyi_aero@hotmail.com
@time: 11/26/2022 2:56 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')
from src.tools.frozen import Frozen
from typing import List
import matplotlib.pyplot as plt
import matplotlib
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "DejaVu Sans",
    "text.latex.preamble": r"\usepackage{amsmath}"
})
matplotlib.use('TkAgg')

_global_forms = dict()
_global_form_variables = {
    'update_cache': True
}


def _find_form(rp, upon=None):
    """Find a form according to symbolic_representation or linguistic_representation.

    If we do not find such a form, we return None. Otherwise, we return the first found one.

    If upon is None, we seek the form whose either `sym_repr` or `lin_repr` is equal to `rp`.

    If upon is not None:
        If upon in _operators:
            We seek the form for which `upon(form)._sym_repr` or `upon(form)._lin_repr` is equal to `rp`.

    """
    _global_form_variables['update_cache'] = False  # during this process, we do not cache the intermediate forms.
    if upon is None:
        the_one = None
        for form_id in _global_forms:
            form = _global_forms[form_id]
            if form._sym_repr == rp or form._lin_repr == rp:
                the_one = form
                break
            else:
                pass

    else:
        if upon in _operators:
            the_one = None
            for form_id in _global_forms:
                form = _global_forms[form_id]
                try:
                    operator_of_f = upon(form)
                except:
                    continue
                else:
                    if operator_of_f._sym_repr == rp or operator_of_f._lin_repr == rp:
                        the_one = form
                        break
                    else:
                        pass
        else:
            raise NotImplementedError()
    _global_form_variables['update_cache'] = True  # turn on cache! Very important!
    return the_one


def _list_forms(variable_range=None):
    """"""
    if variable_range is None:
        col_name_0 = 'form id'
    else:
        col_name_0 = 'variable name'

    if variable_range is None and len(_global_forms) >= 8:
        for form_id in _global_forms:
            form = _global_forms[form_id]
            print('--->', form_id, '|', form._sym_repr, '=', form._lin_repr)
    else:
        cell_text = list()
        for form_id in _global_forms:
            form = _global_forms[form_id]

            if variable_range is None:
                var_name = form_id
            else:
                var_name = list()
                for var in variable_range:
                    if variable_range[var] is form:
                        var_name.append(var)

                if len(var_name) == 0:  # a form is not involved in the variable_range.
                    continue
                elif len(var_name) == 1:
                    var_name = var_name[0]
                else:
                    var_name = ','.join(var_name)

            cell_text.append([r'\texttt{' + str(var_name) + '}',
                              rf"${form.space._sym_repr}$",
                              f"${form._sym_repr}$",
                              form._lin_repr,
                              form.is_root()])

        if len(cell_text) == 0:
            return
        else:
            pass

        fig, ax = plt.subplots(figsize=(16, (1 + len(cell_text))))
        fig.patch.set_visible(False)
        ax.axis('off')
        table = ax.table(cellText=cell_text, loc='center',
                         colLabels=[col_name_0, 'space', 'symbolic', 'linguistic', 'is_root()'],
                         colLoc='left', colColours='rgmcy',
                         cellLoc='left', colWidths=[0.15, 0.125, 0.125, 0.375, 0.075])
        table.scale(1, 8)
        table.set_fontsize(50)
        fig.tight_layout()
        plt.show()


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
        self._pAti_form: List = [None, None, None]  # (father_form, abstract_time_instant)
        self._freeze()

    def print_representations(self):
        """Print this form with matplotlib and latex."""
        my_id = r'\texttt{' + str(id(self)) + '}'
        if self._pAti_form == [None, None, None]:
            pAti_text = ''
        else:
            father_form, ts, ati = self._pAti_form
            pAti_text = rf"\\(${father_form._sym_repr}$ at abstract time instant ${ati._sym_repr}$,\\"
            pAti_text += r"i.e. \textsf{" + rf"t['{ati.k}']" + r"} of abstract time sequence: "
            pAti_text += rf"${ts._lin_repr}$.)"
        plt.figure(figsize=(3 + len(self._sym_repr)/4, 4))
        plt.axis([0, 1, 0, 5])
        plt.text(0, 4.5, f'form id: {my_id}', ha='left', va='center', size=15)
        plt.text(0, 3.5, f'spaces: ${self.space._sym_repr}$', ha='left', va='center', size=15)
        plt.text(0, 2.5, rf'\noindent symbolic : ' + f"${self._sym_repr}$" + pAti_text, ha='left', va='center', size=15)
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

    # @property
    # def _abstract_forms(self):
    #     """All abstract forms of self in a dictionary."""
    #     return self._abf
    #

    def evaluate_at(self, ats):
        """"""
        if ats.__class__.__name__ == 'AbstractTimeInstant':
            assert self.is_root(), f"Can only evaluate a root form at an abstract time instant."
            k = ats.k
            sym_repr = self._sym_repr
            lin_repr = self._lin_repr[:-1]
            sym_repr = r"\left." + sym_repr + r"\right|^{(" + k + ')}'
            lin_repr += "@" + ats._lin_repr + "}"

            ftk = Form(
                self._space,
                sym_repr, lin_repr,
                self._is_root,
                None,    # elementary_forms
                self._orientation,
            )
            ftk._pAti_form[0] = self
            ftk._pAti_form[1] = ats.time_sequence
            ftk._pAti_form[2] = ats

            return ftk
        else:
            raise NotImplementedError(f"Cannot evaluate {self} at {ats}.")


from src.spaces.operators import wedge as space_wedge
from src.spaces.operators import Hodge as space_Hodge
from src.spaces.operators import d as space_d
from src.spaces.operators import codifferential as space_codifferential


def wedge(f1, f2):
    """f1 wedge f2"""
    s1 = f1.space
    s2 = f2.space

    wedge_space = space_wedge(s1, s2)   # if this is not possible, return NotImplementedError

    lr_term1 = f1._lin_repr
    lr_term2 = f2._lin_repr
    lr_operator = r" \emph{wedge} "

    sr_term1 = f1._sym_repr
    sr_term2 = f2._sym_repr
    sr_operator = r'\wedge '

    if f1.is_root():
        pass
    else:
        lr_term1 = '[' + lr_term1 + ']'
        sr_term1 = r'\left(' + sr_term1 + r'\right)'
    if f2.is_root():
        pass
    else:
        lr_term2 = '[' + lr_term2 + ']'
        sr_term2 = r'\left(' + sr_term2 + r'\right)'
    lin_repr = lr_term1 + lr_operator + lr_term2
    sym_repr = sr_term1 + sr_operator + sr_term2

    elementary_forms = set()
    elementary_forms.update(f1._elementary_forms)
    elementary_forms.update(f2._elementary_forms)

    if f1.orientation == f2.orientation:
        orientation = f1.orientation
    else:
        orientation = 'None'

    f = Form(
        wedge_space,               # space
        sym_repr,   # symbolic representation
        lin_repr,
        False,
        elementary_forms,
        orientation,
    )

    return f


def Hodge(f):
    """Metric Hodge of a form."""
    hs = space_Hodge(f.space)

    lr = f._lin_repr
    sr = f._sym_repr

    if f.is_root():
        lr = r"\emph{Hodge of} " + lr
        sr = r"\star " + sr
    else:
        lr = r"\emph{Hodge of} [" + lr + ']'
        sr = r"\star \left(" + sr + r"\right)"

    if f.orientation == 'inner':
        orientation = 'outer'
    elif f.orientation == 'outer':
        orientation = 'inner'
    else:
        orientation = 'None'
    f = Form(
        hs,               # space
        sr,   # symbolic representation
        lr,
        False,
        f._elementary_forms,
        orientation,
    )

    return f


def d(f):
    """Metric Hodge of a form."""
    ds = space_d(f.space)

    lr = f._lin_repr
    sr = f._sym_repr

    if f.is_root():
        lr = r"\emph{exterior-derivative of} " + lr
        sr = r"\mathrm{d}" + sr
    else:
        lr = r"\emph{exterior-derivative of} [" + lr + ']'
        sr = r"\mathrm{d}\left(" + sr + r"\right)"

    f = Form(
        ds,               # space
        sr,   # symbolic representation
        lr,
        False,
        f._elementary_forms,
        f.orientation,
    )

    return f


def codifferential(f):
    """Metric Hodge of a form."""
    ds = space_codifferential(f.space)

    lr = f._lin_repr
    sr = f._sym_repr

    if f.is_root():
        lr = r"\emph{codifferential of} " + lr
        sr = r"\mathrm{d}^\ast " + sr
    else:
        lr = r"\emph{codifferential of} [" + lr + ']'
        sr = r"\mathrm{d}^\ast\left(" + sr + r"\right)"

    f = Form(
        ds,               # space
        sr,   # symbolic representation
        lr,
        False,
        f._elementary_forms,
        f.orientation,
    )

    return f


def time_derivative(f):
    """The time derivative operator."""
    if f.__class__.__name__ != 'Form':
        raise NotImplementedError(f"time_derivative on {f} is not implemented or even not possible at all.")
    else:
        pass

    lr = f._lin_repr
    sr = f._sym_repr

    if f.is_root():
        lr = r"\emph{time-derivative of} " + lr
        sr = r"\partial_t " + sr
    else:
        lr = r"\emph{time-derivative of} [" + lr + ']'
        sr = r"\partial_t\left(" + sr + r"\right)"

    tdf = Form(
        f.space,
        sr,
        lr,
        False,
        f._elementary_forms,
        f.orientation,
    )

    return tdf


from src.spaces.operators import trace as space_trace


def trace(f):
    """The trace operator."""
    trf_space = space_trace(f.space)

    lr = f._lin_repr
    sr = f._sym_repr

    if f.is_root():
        lr = r"\emph{trace of} " + lr
        sr = r"\mathrm{tr}" + sr
    else:
        lr = r"\emph{trace of} [" + lr + ']'
        sr = r"\mathrm{tr}\left(" + sr + r"\right)"

    f = Form(
        trf_space,               # space
        sr,   # symbolic representation
        lr,
        False,
        f._elementary_forms,
        f.orientation,
    )

    return f


_operators = (  # coded operators
    Hodge,
    d,
    codifferential,
    time_derivative,
    trace,
)
