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

    def __init__(self):
        """"""
        self._freeze()


if __name__ == '__main__':
    # python src/weakFormulation.py
    import __init__ as ph

