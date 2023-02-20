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


def list_forms(variable_range=None):
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

        cell_text.append([r'\texttt{' + str(var_name)  + '}',
                          rf"${form.space._symbolic_representation}$",
                          f"${form._symbolic_representation}$",
                          form._linguistic_representation,
                          form.is_root()])

    if len(cell_text) == 0:
        return
    else:
        pass

    fig, ax = plt.subplots(figsize=(14, 2 + len(cell_text) * 1.2))
    fig.patch.set_visible(False)
    ax.axis('off')
    table = ax.table(cellText=cell_text, loc='center',
                     colLabels=[col_name_0, 'space', 'symbolic', 'linguistic', 'is_root()'],
                     colLoc='left', colColours='rgmcy',
                     cellLoc='left', colWidths=[0.15,0.125, 0.125, 0.375, 0.075])
    table.scale(1, 4)
    fig.tight_layout()
    plt.show()


class Form(Frozen):
    """"""

    def __init__(self, space, symbolic_representation, linguistic_representation, is_root):
        self._space = space
        self._symbolic_representation = symbolic_representation
        self._linguistic_representation = linguistic_representation
        self._is_root = is_root
        self._cochain = Cochain(self)  # initialize an empty cochain for this form.
        _global_forms[id(self)] = self
        self._freeze()

    def print_representations(self):
        """"""
        my_id = r'\texttt{' + str(id(self)) + '}'
        plt.figure(figsize=(2 + len(self._symbolic_representation)/4, 4))
        plt.axis([0, 1, 0, 5])
        plt.text(0, 4.5, f'form id: {my_id}', ha='left', va='center', size=15)
        plt.text(0, 3.5, f'spaces: ${self.space._symbolic_representation}$', ha='left', va='center', size=15)
        plt.text(0, 2.5, 'symbolic : ' + f"${self._symbolic_representation}$", ha='left', va='center', size=15)
        plt.text(0, 1.5, 'linguistic : ' + self._linguistic_representation, ha='left', va='center', size=15)
        plt.text(0, 0.5, f'is_root: {self.is_root()}' , ha='left', va='center', size=15)
        plt.axis('off')
        plt.show()

    def is_root(self):
        """"""
        return self._is_root

    @property
    def space(self):
        """"""
        return self._space

    def __repr__(self):
        return super().__repr__()   # TODO: to be customized.


class Cochain(Frozen):
    """"""

    def __init__(self, form):
        """"""
        self._form = form
        self._local = None  # element-wise cochain; 2d data.
        self._global = None  # The cochain as a 1d vector. So ith entry refer to the value of #i dof.
        self._freeze()

    @property
    def local(self):
        """element-wise cochain; 2d data; 1-axis refers to number of mesh elements; 2-axis refers to local numbering of
        dofs."""
        return self._local

    @local.setter
    def local(self, local_cochain):
        """"""

    @property
    def global_(self):
        """The cochain as a 1d vector. The ith entry refers to the value of #i dof."""
        return self._global

    @global_.setter
    def global_(self, global_cochain):
        """"""


from src.spaces.operators import wedge as space_wedge
from src.spaces.operators import Hodge as space_Hodge
from src.spaces.operators import d as space_d
from src.spaces.operators import codifferential as space_codifferential


def wedge(f1, f2):
    """"""
    s1 = f1.space
    s2 = f2.space

    wedge_space = space_wedge(s1, s2)   # if this is not possible, return NotImplementedError

    lr_term1 = f1._linguistic_representation
    lr_term2 = f2._linguistic_representation
    lr_operator = r"\emph{ wedge }"


    sr_term1 = f1._symbolic_representation
    sr_term2 = f2._symbolic_representation
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
    linguistic_representation = lr_term1 + lr_operator + lr_term2
    symbolic_representation = sr_term1 + sr_operator + sr_term2

    f = Form(
        wedge_space,               # space
        symbolic_representation,   # symbolic representation
        linguistic_representation,
        False,
    )

    # TODO: deal with the cochain of the new form

    return f


def Hodge(f):
    """Metric Hodge of a form."""
    Hs = space_Hodge(f.space)

    lr = f._linguistic_representation
    sr = f._symbolic_representation

    if f.is_root():
        lr = r"\emph{Hodge of }" + lr
        sr = r"\star " + sr
    else:
        lr = r"\emph{Hodge of }[" + lr + ']'
        sr = r"\star \left(" + sr + r"\right)"

    f = Form(
        Hs,               # space
        sr,   # symbolic representation
        lr,
        False,
    )

    # TODO: deal with the cochain of the new form

    return f


def d(f):
    """Metric Hodge of a form."""
    ds = space_d(f.space)

    lr = f._linguistic_representation
    sr = f._symbolic_representation

    if f.is_root():
        lr = r"\emph{exterior derivative of }" + lr
        sr = r"\mathrm{d}" + sr
    else:
        lr = r"\emph{exterior derivative of }[" + lr + ']'
        sr = r"\mathrm{d}\left(" + sr + r"\right)"

    f = Form(
        ds,               # space
        sr,   # symbolic representation
        lr,
        False,
    )

    # TODO: deal with the cochain of the new form

    return f


def codifferential(f):
    """Metric Hodge of a form."""
    ds = space_codifferential(f.space)

    lr = f._linguistic_representation
    sr = f._symbolic_representation

    if f.is_root():
        lr = r"\emph{codifferential of }" + lr
        sr = r"\mathrm{d}^\ast " + sr
    else:
        lr = r"\emph{codifferential of }[" + lr + ']'
        sr = r"\mathrm{d}^\ast\left(" + sr + r"\right)"

    f = Form(
        ds,               # space
        sr,   # symbolic representation
        lr,
        False,
    )

    # TODO: deal with the cochain of the new form

    return f


if __name__ == '__main__':
    # python src/form.py
    import __init__ as ph
