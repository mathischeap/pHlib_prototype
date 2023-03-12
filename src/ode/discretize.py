# -*- coding: utf-8 -*-
"""
pH-lib@RAM-EEMCS-UT
created at: 3/10/2023 3:11 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')

from src.tools.frozen import Frozen
from src.config import _wf_term_default_simple_patterns as simple_patterns
from src.form.tools import _find_form
from src.form.operators import time_derivative
from src.pde import PartialDifferentialEquations
import warnings


class ExistingAbstractTimeInstantWarning(UserWarning):
    pass


class OrdinaryDifferentialEquationDiscretize(Frozen):
    """Ordinary Differential Equation Discretize"""

    def __init__(self, ode):
        """"""
        self._ode = ode
        self._ats = None
        self._at_instants = dict()
        self._at_intervals = dict()
        self._eq_terms = dict()
        self._unknown = None
        self._freeze()

    @property
    def time_sequence(self):
        """The time sequence this discretization is working on."""
        return self._ats

    @time_sequence.setter
    def time_sequence(self, ts):
        """Set the time sequence of this discretization."""
        assert ts.__class__.__name__ == 'AbstractTimeSequence', f"I need an abstract time sequence object."
        self._ats = ts

    def set_time_sequence(self, ts):
        """The method of setting time sequence."""
        self.time_sequence = ts

    def define_abstract_time_instants(self, *atis):
        """For example, atis = ('k-1', 'k-0.5', 'k')."""
        assert self.time_sequence is not None, f"set the abstract time sequence first."
        for i, k in enumerate(atis):
            if k in self._at_instants:
                warnings.warn(f"Abstract time instant {k} already exists", ExistingAbstractTimeInstantWarning)
            else:
                assert isinstance(k, str), f"{i}th abstract time instant {k} is not a string. pls use only str."
                self._at_instants[k] = self.time_sequence[k]

    def _get_abstract_time_interval(self, ks, ke):
        """make time interval [ati0, ati1]"""
        assert isinstance(ks, str) and isinstance(ke, str), f"must use string for abstract time instant."
        assert ks in self._at_instants, f"time instant {ks} is not defined"
        assert ke in self._at_instants, f"time instant {ke} is not defined"
        key = str([ks, ke])
        if key in self._at_intervals:
            return self._at_intervals[key]
        else:
            ks = self._at_instants[ks]
            ke = self._at_instants[ke]
            ati = self.time_sequence.make_time_interval(ks, ke)
            self._at_intervals[key] = ati
            return ati

    def differentiate(self, index, ks, ke, degree=1):
        """Differentiate a term at time interval [ati0, ati1] using a Gauss integrator of degree 1."""
        if isinstance(index, int):
            index = str(index)
        else:
            pass
        term = self._ode[index]
        pattern = term[2]
        ptm = term[1]
        dt = self._get_abstract_time_interval(ks, ke)
        if degree == 1:
            if pattern == simple_patterns['(pt,)']:
                bf1 = _find_form(ptm._f1._lin_repr, upon=time_derivative)
                bf1_ks = bf1.evaluate_at(dt.start)
                bf1_ke = bf1.evaluate_at(dt.end)
                bf2 = ptm._f2
                bf1_ks_divided_by_dt = bf1_ks / dt
                bf1_ke_divided_by_dt = bf1_ke / dt
                diff_term1 = ('+', ptm.__class__(bf1_ke_divided_by_dt, bf2))
                diff_term2 = ('-', ptm.__class__(bf1_ks_divided_by_dt, bf2))
                self._eq_terms[index] = (diff_term1, diff_term2)
                self._unknown = bf1_ke
            else:
                raise NotImplementedError()

        else:
            raise NotImplementedError()

    # def

    def __call__(self):
        """return the resulting weak formulation (of one single equation of course.)"""
        terms = ([], [])
        signs = ([], [])
        new_term_sign = self._eq_terms
        for index in self._ode:
            every_thing_about_this_term = self._ode[index]
            l_o_r = self._ode._parse_index(index)[0]
            if index in new_term_sign:
                original_sign = every_thing_about_this_term[0]
                for sign_term in new_term_sign[index]:
                    sign, term = sign_term
                    sign = self._parse_sign(original_sign, sign)
                    terms[l_o_r].append(term)
                    signs[l_o_r].append(sign)
            else:
                terms[l_o_r].append(every_thing_about_this_term[1])
                signs[l_o_r].append(every_thing_about_this_term[0])
        signs_dict = {0: signs}
        terms_dict = {0: terms}
        equation = PartialDifferentialEquations(terms_and_signs_dict=(terms_dict, signs_dict))
        equation.unknowns = self._unknown
        return equation

    @staticmethod
    def _parse_sign(sign1, sign2):
        """-- = +, ++ = +, +- = -, -+ = - sign."""
        return '+' if sign1 == sign2 else '-'


if __name__ == '__main__':
    # python src/ode/discretize.py
    import __init__ as ph
    # import phlib as ph
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

    pde.print_representations()

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
    # wf.print_representations()

    i = 0
    terms = wf._term_dict[i]
    signs = wf._sign_dict[i]
    ode_i = ph.ode(terms_and_signs=[terms, signs])
    ode_i.constant_elementary_forms = wf.test_forms[0]
    # ode_i.print_representations()

    ts1 = ph.time_sequence()
    td = ode_i.discretize

    td.time_sequence = ts1
    td.define_abstract_time_instants('k-1', 'k-0.5', 'k')
    td.differentiate(0, 'k-1', 'k')

    eq = ode_i.discretize()
    print(eq)
    eq.print_representations()
    # ph.list_forms(globals())
