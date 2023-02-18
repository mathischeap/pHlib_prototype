# -*- coding: utf-8 -*-
"""
@author: Yi Zhang
@contact: zhangyi_aero@hotmail.com
@time: 2/19/2023 10:56 AM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')
from src.tools.frozen import Frozen


class ClassName(Frozen):
    """"""

    def __init__(self, ):
        """"""
        self._freeze()


if __name__ == '__main__':
    # python src/discretizations.py
    pass
