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
    """TemporalDiscretization"""

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
        """Return a new weak formulation by combining all equations."""
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

    samples = ph.samples

    oph = samples.pde_canonical_pH(3, 3)[0]

    # oph.print()

    wf = oph.test_with(oph.unknowns, sym_repr=[r'v^3', r'u^2'])
    wf = wf.derive.integration_by_parts('1-1')

    wf.print()
