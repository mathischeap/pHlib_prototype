# -*- coding: utf-8 -*-
"""
pH-lib@RAM-EEMCS-UT
created at: 2/16/2023 4:24 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')

from src.tools.frozen import Frozen
from src.PDEs.interpreter import Interpreter

class Expression(Frozen):
    """

    Parameters
    ----------
    interpreter :
    expression : str, list, tuple
        str or a list (tuple) of str. Each str represent an equation.

    """

    def __init__(self, interpreter, expression):
        """"""
        assert interpreter.__class__ is Interpreter, f"I need a instance of class <Interpreter>."
        if isinstance(expression, str):
            assert len(expression) > 0, "cannot be empty expression."
            expression = [expression, ]
        else:
            for i, exp in enumerate(expression):
                assert isinstance(exp, str), f"expression[{i}] is not a string."
                assert len(exp) > 0, f"expression[{i}] is empty."

        self._parse_expression(expression)

        self._freeze()

    def _parse_expression(self, expression):
        """"""
        print(expression)


if __name__ == '__main__':
    # python src/PDEs/expression.py
    time_derivative_u2 = None,
    convective_term = None,
    codifferential_P3 = None,
    w1 = None
    d_star_u2 = None
    d_u2 = None

    sc = (
        [time_derivative_u2, 'dudt',   r'\dfrac{\partial u^2}{\partial t}'],
        [convective_term,    'wXu',    r'\omega^1\wedge\star u^2 '],
        [codifferential_P3,  'dsP3',   r'\mathrm{d}^\ast P^3'],
        [w1,                 'omega',  r'\omega^1'],
        [d_star_u2,          'dsu2',   r'\mathrm{d}^{\ast}u^2'],
        [d_u2,               'du2',    r'\mathrm{d}u^2']
    )
    it = Interpreter(sc)
    # it.list()

    exp = [
        'dudt + wXu + dsP3 = 0',
        'omega = dsu2',
        'du2 = 0'
    ]

    ep = Expression(it, exp)

