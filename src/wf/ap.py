# -*- coding: utf-8 -*-
"""
@author: Yi Zhang
@contact: zhangyi_aero@hotmail.com
@time: 11/26/2022 2:56 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')
import matplotlib.pyplot as plt
import matplotlib
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "DejaVu Sans",
    "text.latex.preamble": r"\usepackage{amsmath, amssymb}",
})
matplotlib.use('TkAgg')

from src.tools.frozen import Frozen


class AlgebraicProxy(Frozen):
    """"""

    def __init__(self, wf):
        self._parse_terms(wf)
        self._wf = wf
        self._bc = wf._bc
        self._freeze()

    def _parse_terms(self, wf):
        """"""
        wf_td = wf._term_dict
        wf_sd = wf._sign_dict
        term_dict = dict()   # the terms for the AP equation
        sign_dict = dict()   # the signs for the AP equation
        ind_dict = dict()
        indexing = dict()

        for i in wf_td:
            term_dict[i] = ([], [])
            sign_dict[i] = ([], [])
            ind_dict[i] = ([], [])
            k = 0
            for j, terms in enumerate(wf_td[i]):
                for m, term in enumerate(terms):
                    old_sign = wf_sd[i][j][m]
                    try:
                        ap, new_sign = term.ap()
                        new_sign = self._parse_sign(new_sign, old_sign)
                    except NotImplementedError:
                        ap = term
                        new_sign = old_sign

                    index = str(i) + '-' + str(k)
                    k += 1
                    indexing[index] = (ap, new_sign)
                    ind_dict[i][j].append(index)
                    term_dict[i][j].append(ap)
                    sign_dict[i][j].append(new_sign)

        self._term_dict = term_dict
        self._sign_dict = sign_dict
        self._indexing = indexing
        self._ind_dict = ind_dict

    @staticmethod
    def _parse_sign(s0, s1):
        """parse sign"""
        return '+' if s0 == s1 else '-'

    def pr(self, indexing=True):
        """Print the representations"""
        seek_text = self._wf._mesh.manifold._manifold_text()
        # if self.unknowns is None:
        #     seek_text += r'for $\left('
        #     form_sr_list = list()
        #     space_sr_list = list()
        #     for ef in self._efs:
        #         if ef not in self._test_forms:
        #             form_sr_list.append(rf' {ef._sym_repr}')
        #             space_sr_list.append(rf"{ef.space._sym_repr}")
        #         else:
        #             pass
        #     seek_text += ','.join(form_sr_list)
        #     seek_text += r'\right) \in '
        #     seek_text += r'\times '.join(space_sr_list)
        #     seek_text += '$, \n'
        # else:
        #     given_text = r'for'
        #     for ef in self._efs:
        #         if ef not in self.unknowns and ef not in self._test_forms:
        #             given_text += rf' ${ef._sym_repr} \in {ef.space._sym_repr}$, '
        #     if given_text == r'for':
        #         seek_text += r'seek $\left('
        #     else:
        #         seek_text += given_text + '\n'
        #         seek_text += r'seek $\left('
        #     form_sr_list = list()
        #     space_sr_list = list()
        #     for un in self.unknowns:
        #         form_sr_list.append(rf' {un._sym_repr}')
        #         space_sr_list.append(rf"{un.space._sym_repr}")
        #     seek_text += ','.join(form_sr_list)
        #     seek_text += r'\right) \in '
        #     seek_text += r'\times '.join(space_sr_list)
        #     seek_text += '$, such that\n'
        symbolic = ''
        number_equations = len(self._term_dict)
        for i in self._term_dict:
            for t, terms in enumerate(self._term_dict[i]):
                if len(terms) == 0:
                    symbolic += '0'
                else:

                    for j, term in enumerate(terms):
                        sign = self._sign_dict[i][t][j]
                        term = self._term_dict[i][t][j]

                        term_sym_repr = term._sym_repr

                        if indexing:
                            index = self._ind_dict[i][t][j].replace('-', r'\text{-}')
                            term_sym_repr = r'\underbrace{' + term_sym_repr + r'}_{' + \
                                rf"{index}" + '}'
                        else:
                            pass

                        if j == 0:
                            if sign == '+':
                                symbolic += term_sym_repr
                            elif sign == '-':
                                symbolic += '-' + term_sym_repr
                            else:
                                raise Exception()
                        else:
                            symbolic += ' ' + sign + ' ' + term_sym_repr

                if t == 0:
                    symbolic += ' &= '

            # symbolic += r'\quad &&\forall ' + self._test_forms[i]._sym_repr + r'\in ' + \
            #     self._test_spaces[i]._sym_repr

            if i < number_equations - 1:
                symbolic += r',\\'
            else:
                symbolic += '.'

        symbolic = r"$\left\lbrace\begin{aligned}" + symbolic + r"\end{aligned}\right.$"

        if indexing:
            figsize = (12, 3 * len(self._term_dict))
        else:
            figsize = (12, 3 * len(self._term_dict))

        plt.figure(figsize=figsize)
        plt.axis([0, 1, 0, 1])
        plt.axis('off')
        plt.text(0.05, 0.5, seek_text + '\n' + symbolic, ha='left', va='center', size=15)
        plt.tight_layout()
        plt.show()


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
    # td.average('1-1', a3, ['k-1', 'k'])
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
            # 1: '3, 0 = 2, 1, 4',
        }
    )

    ph.space.finite(3)

    (a3 @ td.ts['k']).ap(r"\vec{\alpha}")

    ap = wf.ap()

    # ap.pr()
