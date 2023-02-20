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
from src.form import Form
import matplotlib.pyplot as plt
import matplotlib
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "DejaVu Sans",
    "text.latex.preamble": r"\usepackage{amsmath}",
})
matplotlib.use('TkAgg')


class PartialDifferentialEquations(Frozen):
    """"""

    def __init__(self, expression, interpreter):
        expression = self._check_expression(expression)
        interpreter = self._filter_interpreter(interpreter)
        self._parse_expression(expression, interpreter)
        self._variables = None
        self._freeze()

    def _check_expression(self, expression):
        """"""
        if isinstance(expression, str):
            assert len(expression) > 0, "cannot be empty expression."
            expression = [expression, ]
        else:
            assert isinstance(expression, (list, tuple)), f"pls put expression in a list or tuple."
            for i, exp in enumerate(expression):
                assert isinstance(exp, str), f"expression[{i}] = {exp} is not a string."
                assert len(exp) > 0, f"expression[{i}] is empty."
        for i, equation in enumerate(expression):
            assert equation.count('=') == 1, f"expression[{i}]={equation} is wrong, can only have one '='."

        return expression

    def _filter_interpreter(self, interpreter):
        """"""
        new_interpreter = dict()
        for var_name in interpreter:
            if interpreter[var_name].__class__ is Form:
                new_interpreter[var_name] = interpreter[var_name]
            else:
                pass
        return new_interpreter

    def _parse_expression(self, expression, interpreter):
        """Keep upgrading this method to let it understand more equations."""
        term_dict = dict()
        sign_dict = dict()
        form_dict = dict()
        for i, equation in enumerate(expression):

            equation = equation.replace(' ', '')  # remove all spaces
            equation = equation.replace('-', '+-')  # let all terms be connected by +

            term_dict[i] = ([], [])  # for left terms and right terms of ith equation
            sign_dict[i] = ([], [])  # for left terms and right terms of ith equation
            form_dict[i] = ([], [])  # for left terms and right terms of ith equation

            for j, lor in enumerate(equation.split('=')):
                local_terms = lor.split('+')
                for loc_term in local_terms:
                    if loc_term == '' or loc_term == '-':  # found empty terms, just ignore.
                        pass
                    else:
                        if loc_term == '0':
                            term_dict[i][j].append('0')
                            sign_dict[i][j].append('+')
                            form_dict[i][j].append(None)
                        elif loc_term[0] == '-':
                            assert loc_term[1:] in interpreter, f"found term {loc_term[1:]} not interpreted."
                            term_dict[i][j].append(loc_term[1:])
                            sign_dict[i][j].append('-')
                            form_dict[i][j].append(interpreter[loc_term[1:]])
                        else:
                            assert loc_term in interpreter, f"found term {loc_term} not interpreted"
                            term_dict[i][j].append(loc_term)
                            sign_dict[i][j].append('+')
                            form_dict[i][j].append(interpreter[loc_term])

        self._term_dict = term_dict
        self._sign_dict = sign_dict
        self._form_dict = form_dict

        self._expression = expression
        self._interpreter = interpreter

        # TODO: below, we need to check the consistence of equations, for example, if we have k-form + l-form (k!=l).

    def print_representations(self):
        """"""
        indicator = ''
        symbolic = ''
        for i in self._term_dict:
            for t, terms in enumerate(self._term_dict[i]):
                for j, term in enumerate(terms):
                    term = r'\texttt{' + term + '}'
                    sign = self._sign_dict[i][t][j]
                    form = self._form_dict[i][t][j]
                    if form is None:
                        form_symbolic_representation = '0'
                    else:
                        form_symbolic_representation = form._symbolic_representation

                    if j == 0:
                        if sign == '+':
                            indicator += term
                            symbolic += form_symbolic_representation
                        elif sign == '-':
                            indicator += '$-$' + term
                            symbolic += '-' + form_symbolic_representation
                        else:
                            raise Exception()
                    else:
                        indicator += ' $' + sign + '$ ' + term
                        symbolic += ' ' + sign + ' ' + form_symbolic_representation

                if t == 0:
                    indicator += ' $=$ '
                    symbolic += ' = '

            indicator += '\n'
            symbolic += '\n'

        indicator = indicator[:-1]   # remove the last '\n'
        symbolic = symbolic[:-1]   # remove the last '\n'
        symbolic = symbolic.replace('\n', r' \\ ')
        symbolic = r"$\left\lbrace\begin{aligned}" + symbolic + r"\end{aligned}\right.$"
        symbolic = symbolic.replace('=', r'&=')

        length = max([len(i) for i in indicator.split('\n')]) / 10
        height = 2 * len(self._form_dict) * 0.75
        fig, ax = plt.subplots(figsize=(length, height))
        fig.patch.set_visible(False)
        ax.axis('off')
        table = ax.table(cellText=[[indicator, ], [symbolic, ]],
                         rowLabels=['expression', 'symbolic'], rowColours='gc',
                         colLoc='left', loc='center', cellLoc='left')
        table.scale(1, 2.5*len(self._form_dict))
        table.set_fontsize(20)
        fig.tight_layout()
        plt.show()

    def __len__(self):
        """How many equations we have?"""
        return len(self._form_dict)

    @property
    def variables(self):
        """"""
        return self._variables

    @variables.setter
    def variables(self, unknowns):
        """"""
        if self._variables is not None: f"variables exists; not allowed to change them."

        if len(self) == 1 and not isinstance(unknowns, (list, tuple)):
            unknowns = [unknowns, ]
        assert isinstance(unknowns, (list, tuple)), \
            f"please put variables in a list or tuple if there are more than 1 equation."
        assert len(unknowns) == len(self), \
            f"I have {len(self)} equations but receive {len(unknowns)} variables."

        for i, unknown in enumerate(unknowns):
            assert unknown.__class__ is Form and unknown.is_root(), \
                f"{i}th variable is not a root form."

        self._variables = unknowns


if __name__ == '__main__':
    # python src/PDEs.py
    from src.form import w, u, wXu, du, dsu, dsP, du_dt, f, P
    from src.form import list_forms

    exp = [
        'du_dt + wXu - dsP = f',
        'w = dsu',
        'du = 0'
    ]

    # f.print_representations()

    interpreter = {
        'du_dt' : du_dt,
        'wXu' : wXu,
        'dsP' : dsP,
        'f' : f,
        'w' : w,
        'dsu' : dsu,
        'du' : du,
    }

    pde = PartialDifferentialEquations(exp, interpreter)

    # print(111)

    list_forms(interpreter)

    pde.print_representations()

    pde.variables = [u, w, P]
