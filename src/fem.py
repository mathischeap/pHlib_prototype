# -*- coding: utf-8 -*-
"""
finite element setting

pH-lib@RAM-EEMCS-UT
created at: 3/30/2023 5:35 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')

from src.manifold import _global_manifolds
from src.mesh import _global_meshes
from src.spaces.main import _space_set
from src.form.main import _global_root_forms_lin_dict

import mse.main as mse


_implemented_finite_elements = {
    'mse': mse   # mimetic spectral elements
}

_setting = {
    'current_finite_elements': ''
}


_finite_elements_setup = dict()


def set(fe):
    """"""
    assert fe in _implemented_finite_elements, \
        f"fe={fe} is wrong, should be one of {_implemented_finite_elements.keys()}"

    _setting['current_finite_elements'] = fe


def get():
    """"""
    return _setting['current_finite_elements']


def apply(obj_dict, setup_name=None, cache=True):
    """"""
    if setup_name is None:
        cfe = _setting['current_finite_elements']
        num = 0
        while 1:
            setup_name = cfe + str(num)
            if setup_name not in _finite_elements_setup:
                break
            else:
                num += 1
    else:
        pass

    if setup_name in _finite_elements_setup:
        return _finite_elements_setup[setup_name]

    else:

        finite_element_main = _implemented_finite_elements[get()]

        manifolds = finite_element_main.parse_manifolds(_global_manifolds)
        meshes = finite_element_main.parse_meshes(_global_meshes)
        spaces = finite_element_main.parse_spaces(_space_set)
        root_forms = finite_element_main.parse_root_forms(_global_root_forms_lin_dict)

        new_setup = {
            'base': {
                'manifolds': manifolds,
                'meshes': meshes,
                'spaces': spaces,
                'root_forms': root_forms
            },
            'others': dict()
        }

        for obj_name in obj_dict:

            obj = obj_dict[obj_name]

            particular_obj = finite_element_main.parse(obj)
            if particular_obj is not None:
                new_setup['others'][obj_name] = particular_obj
            else:
                pass

        if cache:
            _finite_elements_setup[setup_name] = new_setup

        return new_setup



if __name__ == '__main__':
    # python src/fes.py

    import __init__ as ph

    set('mse')
    a = apply(locals())
    print(a)