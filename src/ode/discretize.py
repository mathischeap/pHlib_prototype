# -*- coding: utf-8 -*-
"""
pH-lib@RAM-EEMCS-UT
created at: 3/10/2023 3:11 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')

from src.tools.frozen import Frozen
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
        self._afterward_terms = dict()
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


    def _differentiate(self, index, ks, ke, degree=1):
        """Differentiate a term at time interval [ati0, ati1] using a Gauss integrator of degree 1."""
        term = self._ode[index]
        dt = self._get_abstract_time_interval(ks, ke)
        if degree == 1:
            pattern = term[2]
            if pattern == '(partial_t root-sf, sf)':
                print('cool')
        else:
            raise NotImplementedError()


    def __call__(self):
        """return the resulting weak formulation (of one single equation of course.)"""

        # print(self._ode._pterm)
        # print(self._ode._signs)
        return self._afterward_terms   # you'd better check that it is None before using it. -.-




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
    td._differentiate(0, 'k-1', 'k')

    wf = ode_i.discretize()
    print(wf)
