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
import matplotlib.pyplot as plt
import matplotlib
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "DejaVu Sans",
    "text.latex.preamble": r"\usepackage{amsmath, amssymb}",
})
matplotlib.use('TkAgg')


class BlockMatrix(Frozen):
    """"""
    def __init__(self, shape):
        self._shape = shape
        self._entries = dict()
        self._signs = dict()
        for i in range(shape[0]):
            self._entries[i] = list()
            self._signs[i] = list()
            for j in range(shape[1]):
                self._entries[i].append(list())
                self._signs[i].append(list())
        self._freeze()

    def _is_empty(self):
        empty = True
        for i in self._entries:
            for en in self._entries[i]:
                if en != list():
                    return False
                else:
                    pass
        return empty

    def _add(self, i, j, term, sign):
        """"""
        assert sign in ('+', '-'), f"sign={sign} is wrong."
        if self._entries[i][j] != list():
            assert term.shape == self._entries[i][j][0].shape, f"shape dis-match."
        else:
            pass
        self._entries[i][j].append(term)
        self._signs[i][j].append(sign)

    def __call__(self, i, j):
        """"""
        return self._entries[i][j], self._signs[i][j]

    def _pr_text(self):
        """"""
        symbolic = ''
        for i in self._entries:
            entry = self._entries[i]
            for j, terms in enumerate(entry):
                if len(terms) == 0:
                    symbolic += r"\boldsymbol{0}"

                for k, term in enumerate(terms):
                    sign = self._signs[i][j][k]

                    if k == 0 and sign == '+':
                        symbolic += term._sym_repr

                    else:
                        symbolic += sign + term._sym_repr

                if j < len(entry) - 1:
                    symbolic += '&'

            if i < len(self._entries) - 1:
                symbolic += r'\\'

        symbolic = r"\begin{bmatrix}" + symbolic + r"\end{bmatrix}"
        return symbolic

    def pr(self, figsize=(12, 6)):
        """"""
        symbolic = r"$" + self._pr_text() + r"$"
        plt.figure(figsize=figsize)
        plt.axis([0, 1, 0, 1])
        plt.axis('off')
        plt.text(0.05, 0.5, symbolic, ha='left', va='center', size=15)
        plt.tight_layout()
        plt.show()


class BlockColVector(Frozen):
    """"""

    def __init__(self, shape):
        """"""
        self._shape = shape
        self._entries = tuple([list() for _ in range(shape)])
        self._signs = tuple([list() for _ in range(shape)])
        self._freeze()

    def __call__(self, i):  # work as getitem, use call to make it consistent with `BlockMatrix`.
        """"""
        return self._entries[i], self._signs[i]

    def _is_empty(self):
        empty = True
        for en in self._entries:
            if en != list():
                return False
            else:
                pass
        return empty

    def _add(self, i, term, sign):
        """"""
        assert sign in ('+', '-'), f"sign={sign} is wrong."
        if self._entries[i] != list():
            assert term.shape == self._entries[i][0].shape, f"shape dis-match."
        else:
            pass
        self._entries[i].append(term)
        self._signs[i].append(sign)

    def _pr_text(self):
        """"""
        symbolic = ''
        for i, entry in enumerate(self._entries):

            if len(entry) == 0:
                symbolic += r'\boldsymbol{0}'
            else:
                for j, term in enumerate(entry):
                    sign = self._signs[i][j]

                    if j == 0 and sign == '+':
                        symbolic += term._sym_repr

                    else:
                        symbolic += sign + term._sym_repr

            if i < len(self._entries) - 1:
                symbolic += r'\\'

        symbolic = r"\begin{bmatrix}" + symbolic + r"\end{bmatrix}"
        return symbolic

    def pr(self, figsize=(8, 6)):
        """"""
        symbolic = r"$" + self._pr_text() + r"$"
        plt.figure(figsize=figsize)
        plt.axis([0, 1, 0, 1])
        plt.axis('off')
        plt.text(0.05, 0.5, symbolic, ha='left', va='center', size=15)
        plt.tight_layout()
        plt.show()


class LinearSystem(Frozen):
    """"""

    def __init__(self, A, x, b):
        """"""
        bsp0 = len(A)
        bsp1 = None
        for i, Ai in enumerate(A):
            if i == 0:
                bsp1 = len(Ai)
            else:
                assert len(Ai) == bsp1, 'A shape wrong, must be 2-d data structure.'
            for j, Aij in enumerate(Ai):
                assert isinstance(Aij, (list, tuple)), f"pls put A[{i}][{j}] in a list or tuple."





        self._freeze()

    @property
    def bsp(self):
        """block shape."""
        return self._bsp



