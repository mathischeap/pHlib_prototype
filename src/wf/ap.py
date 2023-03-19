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


class AlgebraicProxy(Frozen):
    """"""

    def __init__(self, wf):
        self._parse_terms(wf)
        self._freeze()

    def _parse_terms(self, wf):
        """"""
        wf_td = wf._term_dict
        wf_sd = wf._sign_dict

        for i in wf_td:
            for j, terms in enumerate(wf_td[i]):
                for k, term in enumerate(terms):
                    old_sign = wf_sd[i][j][k]
                    ap, new_sign = term._ap()
                    print(ap, new_sign)
    @staticmethod
    def _parse_sign(s0, s1):
        """parse sign"""
        return '+' if s0 == s1 else '-'





if __name__ == '__main__':
    # python src/wf/ap.py
    import __init__ as ph

    samples = ph.samples

    oph = samples.pde_canonical_pH(n=3, p=3)[0]
    a3, b2 = oph.unknowns

    wf = oph.test_with(oph.unknowns, sym_repr=[r'v^3', r'u^2'])
    wf = wf.derive.integration_by_parts('1-1')
    # wf.pr(indexing=True)

    td = wf.td
    td.set_time_sequence()  # initialize a time sequence

    td.define_abstract_time_instants('k-1', 'k-1/2', 'k')
    td.differentiate('0-0', 'k-1', 'k')
    td.average('0-1', b2, ['k-1', 'k'])

    td.differentiate('1-0', 'k-1', 'k')
    td.average('1-1', a3, ['k-1', 'k'])
    td.average('1-2', a3, ['k-1/2'])
    dt = td.time_sequence.make_time_interval('k-1', 'k')

    wf = td()
    wf.unknowns = [a3 @ td.time_sequence['k'], b2 @ td.time_sequence['k']]
    wf = wf.derive.split('0-0', 'f0',
                         [a3 @ td.ts['k'], a3 @ td.ts['k-1']],
                         ['+', '-'],
                         factors=[1/dt, 1/dt])
    wf = wf.derive.split('0-2', 'f0',
                         [ph.d(b2 @ td.ts['k-1']), ph.d(b2 @ td.ts['k'])],
                         ['+', '+'],
                         factors=[1/2, 1/2])
    wf = wf.derive.split('1-0', 'f0',
                         [b2 @ td.ts['k'], b2 @ td.ts['k-1']],
                         ['+', '-'],
                         factors=[1/dt, 1/dt])
    wf = wf.derive.split('1-2', 'f0',
                         [a3 @ td.ts['k-1'], a3 @ td.ts['k']],
                         ['+', '+'],
                         factors=[1/2, 1/2])
    wf = wf.derive.rearrange(
        {
            0: '0, 3 = 1, 2',
            1: '3, 0 = 2, 1, 4',
        }
    )

    ph.space.finite(3)

    ap = wf.ap

    wf.pr()