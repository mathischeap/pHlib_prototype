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
    lengths = list()
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
                          str(form.space),
                          f"${form.symbolic_representation}$",
                          form.linguistic_representation,
                          form.isroot()])
        lengths.append(len(form.symbolic_representation)/10 + len(form.linguistic_representation)/5)

    fig, ax = plt.subplots(figsize=(max(lengths), len(cell_text) * 1.2))
    fig.patch.set_visible(False)
    ax.axis('off')
    table = ax.table(cellText=cell_text, loc='center',
                     colLabels=[col_name_0, 'space', 'symbolic', 'linguistic', 'isroot'],
                     colLoc='left', colColours='rgbcy',
                     cellLoc='left', colWidths=[0.15,0.15, 0.15, 0.35, 0.05])
    table.scale(1, 5)
    table.set_fontsize(20)
    fig.tight_layout()
    plt.show()


class Form(Frozen):
    """"""

    def __init__(self, space, symbolic_representation, linguistic_representation, isroot):
        self._space = space
        self._symbolic_representation = symbolic_representation
        self._linguistic_representation = linguistic_representation
        self._isroot = isroot
        _global_forms[id(self)] = self
        self._freeze()

    def print_representations(self):
        """"""
        my_id = r'\texttt{' + str(id(self)) + '}'
        plt.figure(figsize=(2 + len(self.symbolic_representation)/4, 4))
        plt.axis([0, 1, 0, 5])
        plt.text(0, 4.5, f'id: {my_id}', ha='left', va='center', size=15)
        plt.text(0, 3.5, f'space: {self.space}', ha='left', va='center', size=15)
        plt.text(0, 2.5, 'symbolic : ' + f"${self.symbolic_representation}$", ha='left', va='center', size=15)
        plt.text(0, 1.5, 'linguistic : ' + self.linguistic_representation, ha='left', va='center', size=15)
        plt.text(0, 0.5, f'isroot: {self.isroot()}' , ha='left', va='center', size=15)
        plt.axis('off')
        plt.show()

    def isroot(self):
        """"""
        return self._isroot

    @property
    def space(self):
        """"""
        return self._space

    @property
    def symbolic_representation(self):
        """"""
        return self._symbolic_representation

    @property
    def linguistic_representation(self):
        """"""
        return self._linguistic_representation

    def __repr__(self):
        return super().__repr__()   # TODO: to be customized.


w = Form(None, r'\omega^1', r"\textsf{vorticity1}", True)
u = Form(None, r'u^2', r"\textsf{velocity2}", True)
wXu = Form(None, r'\omega^1\wedge\star u^2', r'\textsf{vorticity1} \emph{cross-product} (\emph{Hodge} \textsf{velocity2})', False)
du_dt = Form(None, r'\dfrac{\partial u^2}{\partial t}', r'\emph{time-derivative-of} \textsf{velocity2}', False)
dsP = Form(None, r'\mathrm{d}^\ast P^3', r"\emph{codifferential-of} \textsf{total-pressure3}", False)
dsu = Form(None, r'\mathrm{d}^{\ast}u^2', r"\emph{codifferential-of} \textsf{velocity2}", False)
du = Form(None, r'\mathrm{d}u^2', r"\emph{exterior-derivative-of} \textsf{velocity2}", False)


if __name__ == '__main__':
    # python src/form.py
    pass
    # wXu.print_representations()
    # du_dt.print_representations()
    # dsP.print_representations()
    # dsu.print_representations()
    # du.print_representations()
