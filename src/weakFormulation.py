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


class WeakFormulation(Frozen):
    """"""

    def __init__(self, term_dict, sign_dict):
        """"""
        self._term_dict = term_dict
        self._sign_dict = sign_dict
        self._freeze()


if __name__ == '__main__':
    # python src/weak_formulation.py
    pass
