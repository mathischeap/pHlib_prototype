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
from src.form.tools import _find_form
import matplotlib.pyplot as plt
import matplotlib
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "DejaVu Sans",
    "text.latex.preamble": r"\usepackage{amsmath, amssymb}",
})
matplotlib.use('TkAgg')


def ode(*args, **kwargs):
    """"""
    return OrdinaryDifferentialEquation(*args, **kwargs)


class OrdinaryDifferentialEquationError(Exception):
    """Raise when we try to define new attribute for a frozen object."""


class OrdinaryDifferentialEquation(Frozen):
    """ODE about t only. Only deal with real number valued terms."""

    def __init__(self, expression=None, terms_and_signs=None):
        """"""
        if expression is None:
            assert terms_and_signs is not None, f"must provide one of `expression` or `term_sign_dict`."
            self._parse_terms_and_signs(terms_and_signs)
        elif terms_and_signs is None:
            self._parse_expression(expression)
        else:
            raise Exception(f'Pls provide only one of `expression` or `term_sign_dict`.')
        self._constant_elementary_forms = set()
        self._analyze_terms()
        self._freeze()

    def _parse_terms_and_signs(self, terms_and_signs):
        """"""
        terms, signs = terms_and_signs
        assert len(terms) == len(signs) == 2, f"terms, signs length wrong, must be 2 " \
                                              f"(representing left and right terms)."

        left_terms, right_terms = terms
        left_signs, right_signs = signs

        if not isinstance(left_terms, (list, tuple)):
            left_terms = [left_terms, ]
        if not isinstance(right_terms, (list, tuple)):
            right_terms = [right_terms, ]
        if not isinstance(left_signs, (list, tuple)):
            left_signs = [left_signs, ]
        if not isinstance(right_signs, (list, tuple)):
            right_signs = [right_signs, ]

        assert len(left_terms) == len(left_signs), f"left terms length is not equal to left signs length."
        assert len(right_terms) == len(right_signs), f"right terms length is not equal to right signs length."

        partial_t_orders = ([], [])
        partial_t_terms = ([], [])
        other_terms = ([], [])
        pattern = ([], [])

        elementary_forms = set()
        number_valid_terms = 0
        for i, terms in enumerate([left_terms, right_terms]):
            for j, term in enumerate(terms):
                sign = signs[i][j]
                assert sign in ('+', '-'), rf"sign[{i}][{j}] = {sign} is wrong."
                assert term._is_real_number_valued(), f"{j}th term in left terms is not real number valued."
                elementary_forms.update(term._elementary_forms)
                valid_pattern, order = None, None
                for sp in term._simple_patterns:
                    if sp in self._recognized_pattern():
                        assert valid_pattern is None, f"find more than 1 valid pattern for term {term}."
                        valid_pattern = sp
                        order = self._recognized_pattern()[sp]
                if valid_pattern is None:  # this is not a partial t term.
                    partial_t_orders[i].append(None)
                    partial_t_terms[i].append(None)
                    other_terms[i].append(term)
                    pattern[i].append(None)
                else:
                    number_valid_terms += 1
                    partial_t_orders[i].append(order)
                    partial_t_terms[i].append(term)
                    other_terms[i].append(None)
                    pattern[i].append(valid_pattern)

        if number_valid_terms == 0:
            raise OrdinaryDifferentialEquationError(f"It is not a valid ODE.")
        else:
            pass
        self._signs = signs
        self._order = partial_t_orders
        self._pterm = partial_t_terms
        self._other = other_terms
        self._pattern = pattern
        self._elementary_forms = elementary_forms

    def _parse_expression(self, expression):
        """"""
        raise NotImplementedError(f"must set `sign`, `_order`, `pterm`, `_other`, "
                                  f"`_pattern` `_elementary_forms` properties.")

    @classmethod
    def _recognized_pattern(cls):
        """"""
        return {
            # pattern name                : order
            '(partial_t root-sf, sf)': 1,  # inner product of time-derivative of a root-s-form and another s-form.
        }

    def _analyze_terms(self):
        """"""
        _about = list()
        overall_order = list()
        k = 0
        indexing = dict()
        ind = ([], [])
        for i, terms in enumerate(self._pterm):
            for j, term in enumerate(terms):
                if term is not None:
                    overall_order.append(self._order[i][j])
                    pattern = self._pattern[i][j]
                    assert pattern is not None, f"trivial check."
                    if pattern == '(partial_t root-sf, sf)':
                        f1 = term._f1
                        f1_lin_repr = f1._lin_repr
                        rf_lin_repr = r'\textsf{' + f1_lin_repr.split(r'\textsf{')[1]
                        rf = _find_form(rf_lin_repr)
                        _about.append(rf)
                    else:
                        raise NotImplementedError()

                else:
                    term = self._other[i][j]

                index = str(k)
                indexing[index] = (self._signs[i][j], term)
                ind[i].append(index)
                k += 1

        _about = list(set(_about))
        assert len(_about) == 1, f"this ode should only about a single root-form."
        self._about = _about[0]
        self._overall_order = max(overall_order)
        self._ind = ind
        self._indexing = indexing

    def __repr__(self):
        super_repr = super().__repr__().split('object')[1]
        ele_form_repr = set([form._sym_repr for form in self._elementary_forms])
        return f"<ODE of {self._about._sym_repr} for {ele_form_repr}" + super_repr

    def __contains__(self, index):
        return index in self._indexing

    def __getitem__(self, index):
        return self._indexing[index]

    def __iter__(self):
        """Iter"""
        for index in self._indexing:
            yield index

    @property
    def elementary_forms(self):
        """The elementary forms."""
        return self._elementary_forms

    @property
    def constant_elementary_forms(self):
        """constant_elementary_forms"""
        return self._constant_elementary_forms

    @constant_elementary_forms.setter
    def constant_elementary_forms(self, cef):
        """"""
        if not isinstance(cef, (list, tuple)):
            cef = [cef, ]
        else:
            pass
        for f in cef:
            assert f in self.elementary_forms, f"f={f} is not an elementary form."
            self._constant_elementary_forms = set(cef)

    def print_representations(self, indexing=True):
        """print_representations"""
        sym = 'elementary forms: '
        for ef in self.elementary_forms:
            sym += rf'${ef._sym_repr}$, '
        if len(self.constant_elementary_forms) > 0:
            sym += '(constant: '
            for cef in self.constant_elementary_forms:
                sym += rf"${cef._sym_repr}$, "
            sym = sym[:-2] + '):'
        else:
            sym = sym[:-2] + ':'

        sym += r'\\\\$'
        for i, terms in enumerate(self._pterm):
            if len(terms) == 0:
                sym += '0'
            else:
                for j, term in enumerate(terms):
                    ptm = term
                    otm = self._other[i][j]
                    sign = self._signs[i][j]
                    if j == 0 and sign == '+':
                        sign = ''

                    if ptm is None:
                        sym_term = otm._sym_repr
                    else:
                        sym_term = ptm._sym_repr

                    if indexing:
                        index = self._ind[i][j]
                        sym_term = r"\underbrace{" + sym_term + '}_{' + index + '}'
                    else:
                        pass

                    sym += sign + sym_term

            if i == 0:
                sym += '='

        sym += '$'
        figsize = (14, 8)
        fig, ax = plt.subplots(figsize=figsize)
        fig.patch.set_visible(False)
        ax.axis('off')
        table = ax.table(cellText=[[sym, ], ],
                         rowLabels=['symbolic', ], rowColours='gcy',
                         colLoc='left', loc='center', cellLoc='left')

        table.scale(1, 8)
        table.set_fontsize(20)
        fig.tight_layout()
        plt.show()


if __name__ == '__main__':
    # python src/ode/main.py
    import __init__ as ph
    # import phlib as ph
    # ph.config.set_embedding_space_dim(3)
    manifold = ph.manifold(3)
    mesh = ph.mesh(manifold)
    ph.space.set_mesh(mesh)
    O1 = ph.space.new('Omega', 1)
    O2 = ph.space.new('Omega', 2)
    O3 = ph.space.new('Omega', 3)
    # ph.list_meshes()
    w = O1.make_form(r'\omega^1', "vorticity1")
    u = O2.make_form(r'u^2', "velocity2")
    f = O2.make_form(r'f^2', "body-force")
    P = O3.make_form(r'P^3', "total-pressure3")
    wXu = w.wedge(ph.Hodge(u))
    dsP = ph.codifferential(P)
    dsu = ph.codifferential(u)
    du = ph.d(u)
    du_dt = ph.time_derivative(u)
    exp = [
        'du_dt + wXu - dsP = f',
        'w = dsu',
        'du = 0',
    ]
    pde = ph.pde(exp, globals())
    pde.unknowns = [u, w, P]
    wf = pde.test_with([O2, O1, O3], sym_repr=[r'v^2', r'w^1', r'q^3'])
    wf = wf.derive.integration_by_parts('0-2')
    wf = wf.derive.integration_by_parts('1-1')
    wf = wf.derive.rearrange(
        {
            0: '0, 1, 2 = 4, 3',
            1: '1, 0 = 2',
            2: ' = 0',
        }
    )
    i = 0
    terms = wf._term_dict[i]
    signs = wf._sign_dict[i]
    ode_i = ph.ode(terms_and_signs=[terms, signs])
    ode_i.constant_elementary_forms = wf.test_forms[0]
    # ode_i.print_representations()

    term0 = ode_i['0'][1]
    ats = ph.time_sequence()
    dt = ats.make_time_interval('k-1', 'k')   # dt = t[k] - t[k-1/2]
    # term0.print_representations()

    u_km1 = u.evaluate_at(dt.start)
    u_k = u.evaluate_at(dt.end)
    # print(dt._lin_repr, dt._sym_repr)
    # print(dt.start._lin_repr)
    # u_km1.print_representations()

    u_km1_dt = u_km1 / dt
    u_k_dt = u_k / dt
    # ut.print_representations()

    new_terms, signs = term0.split('f1', [u_km1_dt, u_k_dt], ['-', '+'])
    new_terms[0].print_representations()
    new_terms[1].print_representations()
