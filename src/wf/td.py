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


class TemporalDiscretization(Frozen):
    """"""

    def __init__(self, wf):
        """"""
        self._wf = wf
        self._initialize_odes()
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


if __name__ == '__main__':
    # python src/wf/temporalDiscretization.py
    pass