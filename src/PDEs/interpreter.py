# -*- coding: utf-8 -*-
"""
pH-lib@RAM-EEMCS-UT
created at: 2/16/2023 12:03 PM
"""
import sys
if './' not in sys.path:
    sys.path.append('./')

from src.tools.frozen import Frozen
import matplotlib.pyplot as plt
import matplotlib

class Interpreter(Frozen):
    """"""

    def __init__(self, symbolic_chart):
        """"""
        self._parse_symbolic_chart(symbolic_chart)
        self._freeze()

    def _parse_symbolic_chart(self, symbolic_chart):
        """"""
        self._symbolic_dict = dict()
        for i, term in enumerate(symbolic_chart):
            assert len(term) == 3, f"{i}th term in symbolic_chart should have 3 entries, not it has {len(term)}."
            variable, indicator, symbolic_form = term
            assert isinstance(indicator, str), f"indicator at symbolic_chart[{i}][1] = {indicator} is not a string."
            assert indicator not in self._symbolic_dict, f"indicator={indicator} is repeatedly used."
            assert indicator.isalnum(), f"inidicator={indicator} illegal, it can not have letters and numbers."
            self._symbolic_dict[indicator] = (variable, symbolic_form)

    def __getitem__(self, indicator):
        """Return the variable according to the indicator."""
        return self._symbolic_dict[indicator][0]

    def __len__(self):
        return len(self._symbolic_dict)

    def list(self):
        """list all variables."""
        plt.rcParams.update({
            "text.usetex": True,
            "font.family": "sans-serif",  # DejaVu Sans
            "text.latex.preamble": r"\usepackage{amsmath}"
        })
        matplotlib.use('TkAgg')
        cell_text = list()
        for indicator in self._symbolic_dict:
            cell_text.append([indicator, f"${self._symbolic_dict[indicator][1]}$"])
        fig, ax = plt.subplots(figsize=(5, len(self)*1))
        fig.patch.set_visible(False)
        ax.axis('off')
        ax.axis('tight')
        table = ax.table(cellText=cell_text, loc='center', fontsize=30,
                 colLabels=['indicator', 'symbol'], colLoc='left', colColours='gr',
                 cellLoc='left', colWidths=[0.3,0.7])
        table.scale(1, 5)
        table.set_fontsize(20)
        fig.tight_layout()
        plt.show()


if __name__ == '__main__':
    # python src/PDEs/interpreter.py
    time_derivative_u2 = None,
    convective_term = None,
    codifferential_P3 = None,
    w1 = None
    d_star_u2 = None
    d_u2 = None

    sc = (
        [time_derivative_u2, 'dudt',  r'\dfrac{\partial u^2}{\partial t}'],
        [convective_term,    'wXu',  r'\omega^1\wedge\star u^2 '],
        [codifferential_P3,  'dsP3',  r'\mathrm{d}^\ast P^3'],
        [w1,                 'w',  r'\omega^1'],
        [d_star_u2,          'dsu2',  r'\mathrm{d}^{\ast}u^2'],
        [d_u2,               'du2',  r'\mathrm{d}u^2']
    )
    it = Interpreter(sc)
    it.list()
