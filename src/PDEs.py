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
    "text.latex.preamble": r"\usepackage{amsmath}"
})
matplotlib.use('TkAgg')


class PartialDifferentialEquations(Frozen):
    """"""

    def __init__(self, expression, interpreter):
        expression = self._check_expression(expression)
        interpreter = self._filter_interpreter(interpreter)
        self._parse_expression(expression, interpreter)
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

        # TODO: below, we need to check the consistence of equations, for example, if we have k-form + l-form (k!=l).

    def print_representations(self):
        """"""
        cell_text = ['', '']
        for i in self._term_dict:
            left_terms, right_terms = self._term_dict[i]
            for j, term in enumerate(left_terms):
                sign = self._sign_dict[i][0][j]
                form = self._form_dict[i][0][j]
                if j == 0:
                    if sign == '+':
                        cell_text[0] += term
                    elif sign == '-':
                        cell_text[0] += '-' + term
                    else:
                        raise Exception()
                else:
                    cell_text[0] += ' ' + sign + ' ' + term

            cell_text[0] += ' = '

            for j, term in enumerate(right_terms):
                sign = self._sign_dict[i][0][j]
                form = self._form_dict[i][0][j]
                if j == 0:
                    if sign == '+':
                        cell_text[0] += term
                    elif sign == '-':
                        cell_text[0] += '-' + term
                    else:
                        raise Exception()
                else:
                    cell_text[0] += ' ' + sign + ' ' + term

            cell_text[0] += '\n'

        cell_text[0] = cell_text[0][:-1]   # remove the last '\n'

        print(cell_text[0])


if __name__ == '__main__':
    # python src/PDEs.py
    from src.form import w, u, wXu, du, dsu, dsP, du_dt, f
    from src.form import list_forms

    exp = [
        '-du_dt + wXu - dsP = f',
        'w = dsu',
        'du = 0'
    ]

    # du_dt.print_representations()

    pde = PartialDifferentialEquations(exp, globals())

    # list_forms(globals())

    pde.print_representations()
