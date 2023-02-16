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
        """"""
        self._symbolic_representation = None  # TODO: to be continued.

    @property
    def symbolic_representation(self):
        return self._symbolic_representation


if __name__ == '__main__':
    # python src/PDEs.py
    from src.form import w, u, wXu, du, dsu, dsP, du_dt
    from src.form import list_forms

    # wXu.print_representations()

    exp = [
        'du_dt + wXu + dsP = 0',
        'w = dsu',
        'du = 0'
    ]

    pde = PartialDifferentialEquations(exp, globals())

    # list_forms(globals())
