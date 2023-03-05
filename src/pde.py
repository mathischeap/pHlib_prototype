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
    "text.latex.preamble": r"\usepackage{amsmath, amssymb}",
})
matplotlib.use('TkAgg')
from src.wf.term import inner
from src.wf.main import WeakFormulation


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

    @staticmethod
    def _check_expression(expression):
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

    @staticmethod
    def _filter_interpreter(interpreter):
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
        indi_dict = dict()
        sign_dict = dict()
        form_dict = dict()
        ind_dict = dict()
        indexing = dict()
        for i, equation in enumerate(expression):

            equation = equation.replace(' ', '')  # remove all spaces
            equation = equation.replace('-', '+-')  # let all terms be connected by +

            indi_dict[i] = ([], [])  # for left terms and right terms of ith equation
            sign_dict[i] = ([], [])  # for left terms and right terms of ith equation
            form_dict[i] = ([], [])  # for left terms and right terms of ith equation
            ind_dict[i] = ([], [])  # for left terms and right terms of ith equation

            k = 0
            for j, lor in enumerate(equation.split('=')):
                local_terms = lor.split('+')

                for loc_term in local_terms:
                    if loc_term == '' or loc_term == '-':  # found empty terms, just ignore.
                        pass
                    else:
                        if loc_term == '0':
                            pass
                        else:
                            if loc_term[0] == '-':
                                assert loc_term[1:] in interpreter, f"found term {loc_term[1:]} not interpreted."
                                indi = loc_term[1:]
                                sign = '-'
                                form = interpreter[loc_term[1:]]
                            else:
                                assert loc_term in interpreter, f"found term {loc_term} not interpreted"
                                indi = loc_term
                                sign = '+'
                                form = interpreter[loc_term]

                            indi_dict[i][j].append(indi)
                            sign_dict[i][j].append(sign)
                            form_dict[i][j].append(form)
                            if j == 0:
                                index = str(i) + '-' + str(k)
                            elif j == 1:
                                index = str(i) + '-' + str(k)
                            else:
                                raise Exception()
                            k += 1
                            indexing[index] = (indi, sign, form)
                            ind_dict[i][j].append(index)

        self._indi_dict = indi_dict
        self._sign_dict = sign_dict
        self._form_dict = form_dict
        self._ind_dict = ind_dict
        self._indexing = indexing

        self._expression = expression
        self._interpreter = interpreter

        elementary_forms = list()
        mesh = None
        for i in self._form_dict:
            for terms in self._form_dict[i]:
                for term in terms:
                    if term == 0:
                        pass
                    else:
                        elementary_forms.extend(term._elementary_forms)
                        if mesh is None:
                            mesh = term.mesh
                        else:
                            assert mesh == term.mesh, f"mesh dis-match."

        self._elementary_forms = set(elementary_forms)
        self._mesh = mesh

    @property
    def mesh(self):
        """"""
        return self._mesh

    def print_representations(self, indexing=False):
        """"""
        indicator = ''
        symbolic = ''
        number_equations = len(self._indi_dict)
        for i in self._indi_dict:
            for t, terms in enumerate(self._indi_dict[i]):
                if len(terms) == 0:
                    indicator += '0'
                    symbolic += '0'
                else:
                    for j, term in enumerate(terms):
                        term = r'\text{\texttt{' + term + '}}'
                        if indexing:
                            index = self._ind_dict[i][t][j].replace('-', r'\text{-}')
                            term = r'\underbrace{'+ term + r'}_{' + \
                                   rf"{index}" + '}'
                        else:
                            pass
                        sign = self._sign_dict[i][t][j]
                        form = self._form_dict[i][t][j]
                        form_sym_repr = form._sym_repr
                        if indexing:
                            index = self._ind_dict[i][t][j].replace('-', r'\text{-}')
                            form_sym_repr = r'\underbrace{'+ form_sym_repr + r'}_{' + \
                                   rf"{index}" + '}'
                        else:
                            pass

                        if j == 0:
                            if sign == '+':
                                indicator += term
                                symbolic += form_sym_repr
                            elif sign == '-':
                                indicator += '-' + term
                                symbolic += '-' + form_sym_repr
                            else:
                                raise Exception()
                        else:
                            indicator += ' ' + sign + ' ' + term
                            symbolic += ' ' + sign + ' ' + form_sym_repr

                if t == 0:
                    indicator += ' &= '
                    symbolic += ' &= '
            if i < number_equations - 1:
                indicator += r' \\ '
                symbolic += r' \\ '
            else:
                pass
        indicator = r"$\left\lbrace\begin{aligned}" + indicator + r"\end{aligned}\right.$"
        symbolic = r"$\left\lbrace\begin{aligned}" + symbolic + r"\end{aligned}\right.$"

        if self._unknowns is None:
            ef_text = list()
            for ef in self._elementary_forms:
                ef_text.append(ef._sym_repr)
            ef_text = r'$' + r', '.join(ef_text) + r'$'
        else:
            ef_text_unknowns = list()
            ef_text_others = list()
            for ef in self._unknowns:
                ef_text_unknowns.append(ef._sym_repr)
            for ef in self._elementary_forms:
                if ef in self._unknowns:
                    pass
                else:
                    ef_text_others.append(ef._sym_repr)
            ef_text_unknowns = r'unknowns: $' + r', '.join(ef_text_unknowns) + r'$'
            ef_text_others = r'others: $' + r', '.join(ef_text_others) + r'$'
            ef_text = ef_text_unknowns + '\n' + ef_text_others

        if indexing:
            length = max([len(i) for i in indicator.split(r'\\')]) / 20
            height = 2 * len(self._form_dict) * 1.5
        else:
            length = max([len(i) for i in indicator.split(r'\\')]) / 15
            height = 2 * len(self._form_dict) * 0.75
        fig, ax = plt.subplots(figsize=(length, height))
        fig.patch.set_visible(False)
        ax.axis('off')
        table = ax.table(cellText=[[indicator, ], [symbolic, ], [ef_text, ]],
                         rowLabels=['expression', 'symbolic', 'elementary forms'], rowColours='gcy',
                         colLoc='left', loc='center', cellLoc='left')
        if indexing:
            table.scale(1, 5*len(self._form_dict))
        else:
            table.scale(1, 2.25*len(self._form_dict))
        table.set_fontsize(20)
        fig.tight_layout()
        plt.show()

    def __len__(self):
        """How many equations we have?"""
        return len(self._form_dict)

    def __getitem__(self, item):
        return self._indexing[item]

    def __iter__(self):
        """"""
        for i in self._ind_dict:
            for lri in self._ind_dict[i]:
                for index in lri:
                    yield index

    @property
    def elementary_forms(self):
        """Return a set of root forms that this equation involves."""
        return self._elementary_forms

    @property
    def unknowns(self):
        """"""
        return self._unknowns

    @unknowns.setter
    def unknowns(self, unknowns):
        """"""
        if self._unknowns is not None:
            f"unknowns exists; not allowed to change them."

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

    def test_with(self, test_spaces, test_method='L2', sym_repr=None):
        """return a weak formulation."""
        if not isinstance(test_spaces, (list, tuple)):
            test_spaces = [test_spaces, ]
        else:
            pass
        _test_spaces = list()
        for i, obj in enumerate(test_spaces):
            if obj.__class__.__name__ == 'Form':
                _test_spaces.append(obj.space)
            else:
                assert obj._is_space(), f"test_spaces[{i}] is not a space."
                _test_spaces.append(obj)
        assert len(_test_spaces) == len(self), \
            f"pde has {len(self)} equations, so I need {len(self)} test spaces."

        tfs = list()
        for i, ts in enumerate(test_spaces):
            unknown = None  # in case not found an unknown, will raise Error.
            for unknown in self.unknowns:
                unknown_space = unknown.space
                if ts == unknown_space:
                    break
                else:
                    unknown = None

            if sym_repr is None:
                if unknown is None:  # we do not find an unknown which is in the same space as the test form.
                    sr = r"\underline{\tau}_" + str(i)
                else:
                    assert unknown.is_root(), f"a trivial check."
                    sr = unknown._sym_repr
                    _base = sr.split('^')[0].split('_')[0]
                    sr = sr.replace(_base, r'\underline{' + _base + '}')
            else:
                assert len(sym_repr) == len(test_spaces), \
                    f"We have {len(test_spaces)} test forms, so we need {len(test_spaces)} syb_repr. " \
                    f"Now we receive {len(sym_repr)}."

                sr = sym_repr[i]

            tf = ts.make_form(sr, f'{i}th-test-form')
            tfs.append(tf)

        term_dict = dict()
        for i in self._form_dict:   # ith equation
            term_dict[i] = ([], [])
            for j, terms in enumerate(self._form_dict[i]):
                for k, term in enumerate(terms):
                    if term == 0:
                        raw_weak_term = 0
                    else:
                        raw_weak_term = inner(term, tfs[i], method=test_method)
                    term_dict[i][j].append(raw_weak_term)

        wf = WeakFormulation(term_sign_dict=(term_dict, self._sign_dict), test_forms=tfs)
        wf.unknowns = self.unknowns
        return wf


if __name__ == '__main__':
    # python src/PDEs.py
    import __init__ as ph
    # import phlib as ph
    ph.config.set_embedding_space_dim(3)
    manifold = ph.manifold(3)
    mesh = ph.mesh(manifold)

    ph.space.set_mesh(mesh)
    O0 = ph.space.new('Omega', 0, p=3)
    O1 = ph.space.new('Omega', 1, p=3)
    O2 = ph.space.new('Omega', 2, p=3)
    O3 = ph.space.new('Omega', 3, p=3)

    w = O1.make_form(r'\omega^1', "vorticity1")
    u = O2.make_form(r'u^2', r"velocity2")
    f = O2.make_form(r'f^2', r"body-force")
    P = O3.make_form(r'P^3', r"total-pressure3")

    # ph.list_spaces()
    # ph.list_forms(globals())

    wXu = w.wedge(ph.Hodge(u))

    dsP = ph.codifferential(P)
    dsu = ph.codifferential(u)
    du = ph.d(u)

    du_dt = ph.time_derivative(u)

    # ph.list_forms(globals())
    # du_dt.print_representations()

    exp = [
        'du_dt + wXu - dsP = f',
        'w = dsu',
        'du = 0',
    ]
    #
    # interpreter = {
    #     'du_dt': du_dt,
    #     'wXu': wXu,
    #     'dsP': dsP,
    #     'f': f,
    #     'w': w,
    #     'dsu': dsu,
    #     'du': du,
    # }

    pde = ph.pde(exp, globals())
    pde.unknowns = [u, w, P]
    # pde.print_representations(indexing=True)
    rwf = pde.test_with([O2, O1, O3])
    # rwf.print_representations(indexing=True)
    # # ph.list_forms(globals())
    # # print(mesh.boundary().boundary())
    # for i in rwf:
    #     if rwf[i][1] == 0:
    #         pass
    #     else:
    #         print(rwf[i][1]._simple_patterns)
