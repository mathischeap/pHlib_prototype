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


class TimeSequence(Frozen):
    """"""

    def __init__(self, ):

        self._freeze()



class TimeInterval(Frozen):
    """"""

    def __init__(self):

        self._freeze()


class TimeInstance(Frozen):
    """"""

    def __init__(self):

        self._freeze()


    def __repr__(self):
        """"""