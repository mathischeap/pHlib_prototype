# -*- coding: utf-8 -*-
"""
@author: Yi Zhang
@contact: zhangyi_aero@hotmail.com
@time: 2/18/2023 10:18 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')
from tools.frozen import Frozen
import matplotlib.pyplot as plt
import matplotlib
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "DejaVu Sans",
    "text.latex.preamble": r"\usepackage{amsmath}",
})
matplotlib.use('TkAgg')
from src.form import inner


class RawWeakFormulation(Frozen):
    """"""

    def __init__(self, pde, test_spaces, test_method='L2'):
        """"""
        self._pde = pde
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
        assert len(_test_spaces) == len(pde), \
            f"pde has {len(pde)} equations, so I need {len(pde)} test spaces."
        self._test_spaces = _test_spaces
        self._parse_test_forms()
        self._test_method = test_method
        self._parse_weak_terms()
        self._freeze()

    @property
    def mesh(self):
        return self._pde.mesh

    @property
    def pde(self):
        return self._pde

    @property
    def unknowns(self):
        return self._pde.unknowns

    def _parse_test_forms(self):
        """"""
        pde_unknowns = self.pde.unknowns
        tfs = list()
        for i, ts in enumerate(self._test_spaces):
            unknown = None  # in case not found a unknown, will raise Error.
            for unknown in pde_unknowns:
                unknown_space = unknown.space
                if ts == unknown_space:
                    break
                else:
                    unknown = None

            if unknown is None:  # we do not find an unknown which is in the same space as the test form.
                sr = r"\underline{\tau}_" + str(i)
            else:
                assert unknown.is_root(), f"a trivial check."
                sr = unknown._symbolic_representation
                _base = sr.split('^')[0].split('_')[0]
                sr = sr.replace(_base, r'\underline{' + _base + '}')

            tf = ts.make_form(sr, f'{i}th-test-form')
            tfs.append(tf)

        self._test_forms = tfs

    def _parse_weak_terms(self):
        """"""
        term_dict = dict()

        form_dict = self.pde._form_dict

        for i in form_dict:   # ith equation
            term_dict[i] = ([], [])
            for j, terms in enumerate(form_dict[i]):
                for term in terms:
                    if term is None:
                        raw_weak_term = 0
                    else:
                        raw_weak_term = inner(term, self._test_forms[i], method=self._test_method)
                    term_dict[i][j].append(raw_weak_term)

        self._term_dict = term_dict
        self._sign_dict = self.pde._sign_dict

    def print_representations(self):
        """"""
        seek_text = 'Seek $\left('
        form_sr_list = list()
        space_sr_list = list()
        for un in self.unknowns:
            form_sr_list.append(rf' {un._symbolic_representation}')
            space_sr_list.append(rf"{un.space._symbolic_representation}")
        seek_text += ','.join(form_sr_list)
        seek_text += r'\right) \in '
        seek_text += r'\times '.join(space_sr_list)
        seek_text += r'$, such that\\'
        symbolic = ''
        for i in self._term_dict:
            for t, terms in enumerate(self._term_dict[i]):
                for j, term in enumerate(terms):
                    sign = self._sign_dict[i][t][j]
                    term = self._term_dict[i][t][j]

                    if term == 0:
                        term_symbolic_representation = '0'
                    else:
                        term_symbolic_representation = term._symbolic_representation

                    if j == 0:
                        if sign == '+':
                            symbolic += term_symbolic_representation
                        elif sign == '-':
                            symbolic += '-' + term_symbolic_representation
                        else:
                            raise Exception()
                    else:
                        symbolic += ' ' + sign + ' ' + term_symbolic_representation

                if t == 0:
                    symbolic += ' = '
            symbolic += r'\quad &&\forall' + self._test_forms[i]._symbolic_representation + r'\in ' + \
                        self._test_spaces[i]._symbolic_representation
            symbolic += ',\n'

        symbolic = symbolic[:-2]   # remove the last '\n'
        symbolic += '.'
        symbolic = symbolic.replace('\n', r' \\ ')
        symbolic = r"$\left\lbrace\begin{aligned}" + symbolic + r"\end{aligned}\right.$"
        symbolic = symbolic.replace('=', r'&=')

        fig, ax = plt.subplots(figsize=(14, len(self._term_dict)))
        fig.patch.set_visible(False)
        ax.axis('off')
        table = ax.table(cellText=[[seek_text + symbolic, ], ],
                         rowLabels=['symbolic', ], rowColours='gcy',
                         colLoc='left', loc='center', cellLoc='left')
        table.scale(1, 3 * len(self._term_dict))
        table.set_fontsize(20)
        fig.tight_layout()
        plt.show()






class WeakFormulation(Frozen):
    """"""



if __name__ == '__main__':
    # python src/weakFormulation.py
    import __init__ as ph
