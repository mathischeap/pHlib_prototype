# -*- coding: utf-8 -*-
"""
pH-lib@RAM-EEMCS-UT
created at: 2/20/2023 11:41 AM
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
    # python 
    import __init__ as ph
