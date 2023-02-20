# -*- coding: utf-8 -*-
"""
pH-lib@RAM-EEMCS-UT
created at: 2/20/2023 4:36 PM
"""
from src.spaces.operators import wedge as space_wedge
from src.form import wedge as form_wedge

from src.spaces.operators import Hodge as space_Hodge
from src.form import Hodge as form_Hodge

from src.spaces.operators import d as space_d
from src.form import d as form_d

from src.spaces.operators import codifferential as space_codifferential
from src.form import codifferential as form_codifferential


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


def d(obj):
    """"""
    try:
        return space_d(obj)
    except NotImplementedError:
        pass

    try:
        return form_d(obj)
    except NotImplementedError:
        pass

    raise NotImplementedError()


def codifferential(obj):
    """"""
    try:
        return space_codifferential(obj)
    except NotImplementedError:
        pass

    try:
        return form_codifferential(obj)
    except NotImplementedError:
        pass

    raise NotImplementedError()