# -*- coding: utf-8 -*-
"""
@author: Yi Zhang
@contact: zhangyi_aero@hotmail.com
@time: 11/26/2022 2:56 PM
"""

import os
absolute_path = os.path.dirname(__file__)
import sys
if absolute_path not in sys.path:
    sys.path.append(absolute_path)

__version__ = '0.0.0'

about = ''

from src.form import list_forms
from src.spaces.main import _list_spaces as list_spaces

import src.config as config


import src.mesh as mesh

import src.spaces.main as space


from src.operators import inner, wedge, Hodge, d, codifferential, time_derivative


from src.PDEs import pde
