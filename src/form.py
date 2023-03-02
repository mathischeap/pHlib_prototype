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
import matplotlib.pyplot as plt
import matplotlib
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "DejaVu Sans",
    "text.latex.preamble": r"\usepackage{amsmath}"
})
matplotlib.use('TkAgg')

_global_forms = dict()


def _list_forms(variable_range=None):
    """"""
    if variable_range is None:
        col_name_0 = 'form id'
    else:
        col_name_0 = 'variable name'

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
    """"""

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
            sym_repr = sym_repr.replace(' ', '')
            assert len(sym_repr) > 0, \
                f"sym_repr must be a str of length > 0."
            for form_id in _global_forms:
                form = _global_forms[form_id]
                assert sym_repr != form._sym_repr, \
                    f"form symbolic representation={sym_repr} is taken. Pls use another one."
        else:
            pass

        self._sym_repr = sym_repr
        self._lin_repr = lin_repr
        self._is_root = is_root
        if is_root is True:
            assert elementary_forms is None, f"pls do not provide elementary forms for a root form."
            elementary_forms = [self, ]
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
        _global_forms[id(self)] = self
        self._freeze()

    def print_representations(self):
        """"""
        my_id = r'\texttt{' + str(id(self)) + '}'
        plt.figure(figsize=(2 + len(self._sym_repr)/4, 4))
        plt.axis([0, 1, 0, 5])
        plt.text(0, 4.5, f'form id: {my_id}', ha='left', va='center', size=15)
        plt.text(0, 3.5, f'spaces: ${self.space._sym_repr}$', ha='left', va='center', size=15)
        plt.text(0, 2.5, 'symbolic : ' + f"${self._sym_repr}$", ha='left', va='center', size=15)
        plt.text(0, 1.5, 'linguistic : ' + self._lin_repr, ha='left', va='center', size=15)
        plt.text(0, 0.5, f'is_root: {self.is_root()}' , ha='left', va='center', size=15)
        plt.axis('off')
        plt.show()

    def __repr__(self):
        """"""
        super_repr = super().__repr__().split('object')[-1]
        return '<Form ' + self._sym_repr + super_repr  # this will be unique.

    @property
    def orientation(self):
        """"""
        return self._orientation

    def is_root(self):
        """"""
        return self._is_root

    @property
    def space(self):
        """"""
        return self._space

    @property
    def mesh(self):
        """"""
        return self.space.mesh


    def wedge(self, other):
        return wedge(self, other)


from src.spaces.operators import wedge as space_wedge
from src.spaces.operators import Hodge as space_Hodge
from src.spaces.operators import d as space_d
from src.spaces.operators import codifferential as space_codifferential


def wedge(f1, f2):
    """"""
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
    Hs = space_Hodge(f.space)

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
        Hs,               # space
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
        lr = r"\emph{exterior derivative of} " + lr
        sr = r"\mathrm{d}" + sr
    else:
        lr = r"\emph{exterior derivative of} [" + lr + ']'
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
    """"""
    if f.__class__.__name__ != 'Form':
        raise NotImplementedError()
    else:
        pass

    lr = f._lin_repr
    sr = f._sym_repr

    if f.is_root():
        lr = r"\emph{time derivative of} " + lr
        sr = r"\partial_t " + sr
    else:
        lr = r"\emph{time derivative of} [" + lr + ']'
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
