# -*- coding: utf-8 -*-
"""
pH-lib@RAM-EEMCS-UT
created at: 3/24/2023 2:53 PM
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

from src.algebra.array import _global_root_arrays
from src.config import _parse_type_and_pure_lin_repr, _transpose_text
from src.tools.frozen import Frozen


# class MatrixProxy(Frozen):
#     """"""
#
#     def __init__(self, ap):
#         """"""
#         self._wf = ap._wf
#         self._ap = ap
#         # left base matrix block, left other vector
#         self._l_bmb, self._lov = self._parse_left_right('left')
#         # right base matrix block, right other vector
#         self._r_bmb, self._rov = self._parse_left_right('right')
#         self._l_mbs = tuple()  # left matrix blocks
#         self._r_mbs = tuple()  # right matrix blocks
#         self._freeze()
#
#     def _parse_left_right(self, side):
#         """"""
#         if side == 'left':
#             j = 0
#         elif side == 'right':
#             j = 1
#         else:
#             raise Exception()
#
#         sign_dict = self._ap._sign_dict
#         term_dict = self._ap._term_dict
#
#         bv = BlockColVector(len(sign_dict))
#
#         for i in sign_dict:  # ith equation
#             signs = sign_dict[i][j]
#             terms = term_dict[i][j]
#             for k, sign in enumerate(signs):
#                 term = terms[k]
#                 bv.add(i, term, sign)
#
#         bm, bv, ov = self._parse_block_matrix(bv, self._ap.unknowns, self._ap.test_vectors)
#         return [bm, bv], ov
#
#     def _parse_block_matrix(self, ibv, targets, test_vectors):
#         """
#         ibv = mb @ bv + ov
#         mb is a BlockMatrix, bv is a BlockColVector of the targets, and ov are other terms
#         that cannot be summarized into mb @ bv.
#
#         """
#         bv = BlockColVector(len(targets))
#         bm = BlockMatrix((ibv.shape, len(targets)))
#         ov = BlockColVector(ibv.shape)
#
#         tlr = list()
#         for i, tar in enumerate(targets):
#             tlr.append(tar._lin_repr)
#             bv.add(i, tar, '+')
#
#         for i, di in enumerate(ibv._data):
#             for j, dij in enumerate(di):
#                 sij = ibv._sign[i][j]
#                 tv = test_vectors[i]
#                 tv_trans = tv.T._lin_repr
#                 assert tv_trans in dij._lin_repr, "cannot find the test vector."
#
#                 if dij.__class__.__name__ == 'TermLinearAlgebraicProxy':
#
#                     factor, m_at_v = dij._lin_repr.split(tv_trans)
#                     elements = m_at_v.split('@')
#                     assert elements[0] == '', f"block {dij._lin_repr} is wrong."
#                     mats = elements[1:-1]
#                     check_target = elements[-1]
#
#                     if check_target in tlr:
#                         k = tlr.index(check_target)
#
#                         if len(mats) > 0:
#                             the_array = list()
#                             for m in mats:
#                                 if m[-10:] == _transpose_text:
#                                     trans = True
#                                     lr = m[:-10]
#                                 else:
#                                     trans = False
#                                     lr = m
#
#                                 what, pure_lr = _parse_type_and_pure_lin_repr(lr)
#
#                                 assert what == 'array'
#                                 if trans:
#                                     _a = _global_root_arrays[pure_lr].T
#                                 else:
#                                     _a = _global_root_arrays[pure_lr]
#
#                                 the_array.append(_a)
#
#                             if len(mats) == 1:
#                                 mt = the_array[0]
#
#                             else:
#                                 mt = the_array[0] @ the_array[1]
#                                 for ta in the_array[2:]:
#                                     mt = mt @ ta
#
#                             bm.add(i, k, mt, sij)
#
#                         else:
#                             raise NotImplementedError('Identity matrix.')
#
#                     else:
#                         ov.add(i, dij, sij)
#
#                 else:
#                     ov.add(i, dij, sij)
#
#         return bm, bv, ov
#
#     def pr(self, figsize=(12, 8)):
#         """"""
#         symbolic = ''
#         m, v = self._l_bmb
#         if m._is_empty:
#             pass
#         else:
#             symbolic += m._bm_text()
#             symbolic += v._bv_text()
#         # self._l_mbs
#
#         if self._lov._is_empty:
#             pass
#         else:
#             symbolic += '+' + self._lov._bv_text()
#
#         symbolic += '='
#         m, v = self._r_bmb
#         if m._is_empty:
#             pass
#         else:
#             symbolic += m._bm_text()
#             symbolic += v._bv_text()
#         # self._r_mbs
#         symbolic += self._rov._bv_text()
#         symbolic = r"$" + symbolic + r"$"
#
#         plt.figure(figsize=figsize)
#         plt.axis([0, 1, 0, 1])
#         plt.axis('off')
#         plt.text(0.05, 0.5, symbolic, ha='left', va='center', size=15)
#         plt.tight_layout()
#         plt.show()
#
#
# class BlockMatrix(Frozen):
#     """"""
#     def __init__(self, shape):
#         si, sj = shape
#         data = tuple()
#         sign = tuple()
#         self._shape = shape
#         for i in range(si):
#             data += (list(), )
#             sign += (list(), )
#             for j in range(sj):
#                 data[i].append(list())
#                 sign[i].append(list())
#         self._data = data
#         self._sign = sign
#         self._is_empty = True
#         self._freeze()
#
#     def add(self, i, j, term, sign):
#         """Add term to [i][j] block."""
#         assert sign in ('+', '-'), f"sign={sign} is wrong."
#         self._data[i][j].append(term)
#         self._sign[i][j].append(sign)
#         self._is_empty = False
#
#     def _bm_text(self):
#         """"""
#         symbolic = ''
#         for i, di in enumerate(self._data):
#             for j, dij in enumerate(di):
#                 for k, dij_k in enumerate(dij):
#                     term = dij_k
#                     sign = self._sign[i][j][k]
#
#                     if k == 0 and sign == '+':
#                         symbolic += term._sym_repr
#                     else:
#                         symbolic += sign + term._sym_repr
#                 if j < self._shape[1] - 1:
#                     symbolic += '&'
#             if i < self._shape[0] - 1:
#                 symbolic += r'\\'
#         symbolic = r"\begin{bmatrix}" + symbolic + r"\end{bmatrix}"
#         return symbolic
#
#     def pr(self, figsize=(10, 8)):
#         """"""
#         plt.figure(figsize=figsize)
#         plt.axis([0, 1, 0, 1])
#         plt.axis('off')
#         plt.text(0.05, 0.5, '$' + self._bm_text() + '$', ha='left', va='center', size=15)
#         plt.tight_layout()
#         plt.show()
#
#
# class BlockColVector(Frozen):
#     """"""
#     def __init__(self, shape):
#         self._shape = shape
#         data = tuple()
#         sign = tuple()
#         for i in range(shape):
#             data += (list(), )
#             sign += (list(), )
#         self._data = data
#         self._sign = sign
#         self._is_empty = True
#         self._freeze()
#
#     def add(self, i, term, sign):
#         """Add term to [i] block."""
#         assert sign in ('+', '-'), f"sign={sign} is wrong."
#         self._data[i].append(term)
#         self._sign[i].append(sign)
#         self._is_empty = False
#
#     @property
#     def shape(self):
#         return self._shape
#
#     def _bv_text(self):
#         """"""
#         symbolic = ''
#         for i, di in enumerate(self._data):
#             for j, dij in enumerate(di):
#                 sij = self._sign[i][j]
#                 if j == 0 and sij == '+':
#                     symbolic += dij._sym_repr
#                 else:
#                     symbolic += sij + dij._sym_repr
#
#             if i < self.shape - 1:
#                 symbolic += r'\\'
#
#         symbolic = r"\begin{bmatrix}" + symbolic + r"\end{bmatrix}"
#         return symbolic
#
#     def pr(self, figsize=(8, 6)):
#         """"""
#
#         plt.figure(figsize=figsize)
#         plt.axis([0, 1, 0, 1])
#         plt.axis('off')
#         plt.text(0.05, 0.5, '$' + self._bv_text() + '$', ha='left', va='center', size=15)
#         plt.tight_layout()
#         plt.show()
