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
        Left = list()
        Right = list()
        for equation in expression:
            equation = equation.replace(' ', '')  # remove all spaces
            left, right = equation.split('=')  # we already checked there is only one '=' in it


        self._expression = expression
        self._symbolic_representation = None  # TODO: to be continued.


    def print_equations(self):
        """"""
        for equation in self._expression:
            print(equation)





if __name__ == '__main__':
    # python src/PDEs.py
    from src.form import w, u, wXu, du, dsu, dsP, du_dt, f
    from src.form import list_forms

    exp = [
        'du_dt + wXu - dsP = f',
        'w = dsu',
        'du = 0'
    ]

    # du_dt.print_representations()

    pde = PartialDifferentialEquations(exp, globals())

    # list_forms(globals())

    # pde.print_equations()
