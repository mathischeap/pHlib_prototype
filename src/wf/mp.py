# -*- coding: utf-8 -*-
"""
pH-lib@RAM-EEMCS-UT
created at: 3/24/2023 2:53 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')


from src.tools.frozen import Frozen


class MatrixProxy(Frozen):
    """"""

    def __init__(self, ap):
        """"""
        self._wf = ap._wf
        self._ap = ap
        self._left_terms = self._parse_left_right('left')
        self._right_terms = self._parse_left_right('right')
        self._freeze()

    def _parse_left_right(self, side):
        """"""
        if side == 'left':
            j = 0
        elif side == 'right':
            j = 1
        else:
            raise Exception()
        sign_dict = self._ap._sign_dict
        term_dict = self._ap._term_dict
        signs = dict()  # left or right signs
        terms = dict()  # left or right terms
        for i in sign_dict:  # ith equation
            signs[i] = sign_dict[i][j]
            terms[i] = term_dict[i][j]

        self._parse_signs_terms(signs, terms)

    def _parse_signs_terms(self, signs, terms):
        """"""
        num_unknown_terms = 0
        num_unknowns = len(self._ap.unknowns)

        blocks = tuple([tuple([list() for _ in range(num_unknowns)]) for _ in range(len(signs))])
        others = tuple([list() for _ in range(len(signs))])
        bs = tuple([tuple([list() for _ in range(num_unknowns)]) for _ in range(len(signs))])
        os = tuple([list() for _ in range(len(signs))])

        # print(num_unknowns, self._ap.unknowns)

        for i in signs:
            for j, sign in enumerate(signs[i]):
                term = terms[i][j]
                test_vector = self._ap.test_vectors[i]
                if term.__class__.__name__ == 'TermLinearAlgebraicProxy':
                    tlr = term._lin_repr
                    assert test_vector.T._lin_repr in tlr, "test vector must be present."
                    factor_lin_repr = tlr.split(test_vector.T._lin_repr)[0]
                    print(factor_lin_repr, len(factor_lin_repr))
                else:
                    others[i].append(term)
                    os[i].append(sign)

        # print(others, os)


class BlockMatrix(Frozen):
    """"""
    def __init__(self):

        self._freeze()


class BlockColVector(Frozen):
    """"""
    def __init__(self):

        self._freeze()
