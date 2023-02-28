# -*- coding: utf-8 -*-
"""Global configuring variables and methods.

@author: Yi Zhang
@contact: zhangyi_aero@hotmail.com
@time: 11/26/2022 2:56 PM
"""

_global_variables = {
    'embedding_space_dim': 3,
}


def set_embedding_space_dim(ndim):
    """"""
    _global_variables['embedding_space_dim'] = ndim


def get_embedding_space_dim():
    """"""
    return _global_variables['embedding_space_dim']
