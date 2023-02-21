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


def pde(*args, **kwargs):
    """"""
    return PartialDifferentialEquations(*args, **kwargs)


class PartialDifferentialEquations(Frozen):
    """"""

    def __init__(self, expression, interpreter):
        expression = self._check_expression(expression)
        interpreter = self._filter_interpreter(interpreter)
        self._parse_expression(expression, interpreter)
        self._unknowns = None
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

        elementary_forms = list()
        for i in self._form_dict:
            for terms in self._form_dict[i]:
                for term in terms:
                    if term is not None:
                        elementary_forms.extend(term._elementary_forms)
                    else:
                        pass
        self._elementary_forms = set(elementary_forms)

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

        if self._unknowns is None:
            ef_text = list()
            for ef in self._elementary_forms:
                ef_text.append(ef._symbolic_representation)
            ef_text = r'$' + r', '.join(ef_text) + r'$'
        else:
            ef_text_unknowns = list()
            ef_text_others = list()
            for ef in self._elementary_forms:
                if ef in self._unknowns:
                    ef_text_unknowns.append(ef._symbolic_representation)
                else:
                    ef_text_others.append(ef._symbolic_representation)
            ef_text_unknowns = r'unknowns: $' + r', '.join(ef_text_unknowns) + r'$'
            ef_text_others =   r'others: $' + r', '.join(ef_text_others) + r'$'
            ef_text = ef_text_unknowns + '\n' + ef_text_others

        length = max([len(i) for i in indicator.split('\n')]) / 10
        height = 2 * len(self._form_dict) * 0.75
        fig, ax = plt.subplots(figsize=(length, height))
        fig.patch.set_visible(False)
        ax.axis('off')
        table = ax.table(cellText=[[indicator, ], [symbolic, ], [ef_text, ]],
                         rowLabels=['expression', 'symbolic', 'elementary forms'], rowColours='gcy',
                         colLoc='left', loc='center', cellLoc='left')
        table.scale(1, 2*len(self._form_dict))
        table.set_fontsize(20)
        fig.tight_layout()
        plt.show()

    def __len__(self):
        """How many equations we have?"""
        return len(self._form_dict)

    @property
    def unknowns(self):
        """"""
        return self._unknowns

    @unknowns.setter
    def unknowns(self, unknowns):
        """"""
        if self._unknowns is not None: f"unknowns exists; not allowed to change them."

        if len(self) == 1 and not isinstance(unknowns, (list, tuple)):
            unknowns = [unknowns, ]
        assert isinstance(unknowns, (list, tuple)), \
            f"please put unknowns in a list or tuple if there are more than 1 equation."
        assert len(unknowns) == len(self), \
            f"I have {len(self)} equations but receive {len(unknowns)} unknowns."

        for i, unknown in enumerate(unknowns):
            assert unknown.__class__ is Form and unknown.is_root(), \
                f"{i}th variable is not a root form."
            assert unknown in self._elementary_forms, f"{i}th variable is not an elementary form."

        self._unknowns = unknowns

    def test_with(self, test_spaces):
        """return a weak formulation."""


if __name__ == '__main__':
    # python src/PDEs.py
    import __init__ as ph

    mesh = ph.mesh.static(None)

    ph.space.set_mesh(mesh)
    # ph.list_spaces()

    O0 = ph.space.add('Omega', 0, N=3)
    O1 = ph.space.add('Omega', 1, N=3)
    O2 = ph.space.add('Omega', 2, N=3)
    O3 = ph.space.add('Omega', 3, N=3)

    w = O1.make_form(r'\omega^1', "vorticity1")
    u = O2.make_form(r'u^2', r"velocity2")
    f = O2.make_form(r'f^2', r"body-force")
    P = O3.make_form(r'P^3', r"total-pressure3")

    wXu = ph.wedge(w, ph.Hodge(u))

    dsP = ph.codifferential(P)
    dsu = ph.codifferential(u)
    du = ph.d(u)

    du_dt = ph.time_derivative(u)

    # ph.list_forms(globals())

    exp = [
        'du_dt + wXu - dsP = f',
        'w = dsu',
        'du = 0'
    ]

    # interpreter = {
    #     'du_dt' : du_dt,
    #     'wXu' : wXu,
    #     'dsP' : dsP,
    #     'f' : f,
    #     'w' : w,
    #     'dsu' : dsu,
    #     'du' : du,
    # }

    pde = ph.pde(exp, globals())

    pde.unknowns = [u, w, P]
    pde.print_representations()
