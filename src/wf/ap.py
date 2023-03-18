# -*- coding: utf-8 -*-
"""
@author: Yi Zhang
@contact: zhangyi_aero@hotmail.com
@time: 11/26/2022 2:56 PM
"""
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




if __name__ == '__main__':
    pass
