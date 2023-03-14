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
from src.tools.time_sequence import AbstractTimeSequence


class TemporalDiscretization(Frozen):
    """"""

    def __init__(self, wf):
        """"""
        self._wf = wf
        self._initialize_odes()
        self._ats = None
        self._freeze()

    def _initialize_odes(self):
        """Initialize odes."""
        from src.ode.main import ode, OrdinaryDifferentialEquationError
        # must import locally here to avoid a circular import

        wf = self._wf
        valid_ode = dict()
        for i in wf._term_dict:
            terms = wf._term_dict[i]
            signs = wf._sign_dict[i]

            try:

                v_ode = ode(terms_and_signs=[terms, signs])

            except OrdinaryDifferentialEquationError:
                pass
            else:
                valid_ode[i] = v_ode

        self._valid_ode = valid_ode


    def __getitem__(self, item):
        """Return the ode."""
        return self._valid_ode[item]

    def __call__(self, *args, **kwargs):
        """"""
        return self._wf.__class__

    @property
    def time_sequence(self):
        """The time sequence this discretization is working on."""
        return self._ats

    def set_time_sequence(self, ts=None):
        """The method of setting time sequence.

        Note that each wf only use one time sequence. If your time sequence is complex, you should carefully design
        it.
        """
        if ts is None:  # make a new one
            ts = AbstractTimeSequence()
        else:
            pass
        assert ts.__class__.__name__ == 'AbstractTimeSequence', f"I need an abstract time sequence object."
        self._ats = ts

if __name__ == '__main__':
    # python src/wf/td.py

    import __init__ as ph
    # import phlib as ph
    # ph.config.set_embedding_space_dim(3)
    manifold = ph.manifold(3)
    mesh = ph.mesh(manifold)

    ph.space.set_mesh(mesh)
    O0 = ph.space.new('Omega', 0)
    O1 = ph.space.new('Omega', 1)
    O2 = ph.space.new('Omega', 2)
    O3 = ph.space.new('Omega', 3)

    # ph.list_spaces()
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

    # ph.list_forms(globals())

    exp = [
        'du_dt - dsP = f',
        'w = dsu',
        'du = 0',
    ]
    pde = ph.pde(exp, globals())
    pde.unknowns = [u, w, P]
    # pde.print_representations(indexing=True)

    wf = pde.test_with([O2, O1, O3], sym_repr=[r'v^2', r'w^1', r'q^3'])

    wf = wf.derive.integration_by_parts('0-1')
    wf = wf.derive.integration_by_parts('1-1')

    wf = wf.derive.rearrange(
        {
            0: '0, 1 = 3, 2',
            1: '1, 0 = 2',
            2: ' = 0',
        }
    )
    wf.print()

    td = wf.td
    td.set_time_sequence()
