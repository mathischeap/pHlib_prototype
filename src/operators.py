# -*- coding: utf-8 -*-
"""
pH-lib@RAM-EEMCS-UT
created at: 2/20/2023 4:36 PM
"""
from src.spaces.operators import wedge as space_wedge
from src.form import wedge as form_wedge

from src.spaces.operators import Hodge as space_Hodge
from src.form import Hodge as form_Hodge


def wedge(obj1, obj2):
    """"""
    try:
        return space_wedge(obj1, obj2)
    except NotImplementedError:
        pass

    try:
        return form_wedge(obj1, obj2)
    except NotImplementedError:
        pass

    raise NotImplementedError()


def Hodge(obj):
    """"""
    try:
        return space_Hodge(obj)
    except NotImplementedError:
        pass

    try:
        return form_Hodge(obj)
    except NotImplementedError:
        pass

    raise NotImplementedError()