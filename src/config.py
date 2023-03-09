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


_global_lin_repr_setting = {
    # objects
    'manifold': [r'\underline{', '}'],
    'mesh': [r'\textbf{', r'}'],
    'form': [r'\textsf{', r'}'],
    'parameters': [r'\textsc{', r'}'],
    'abstract_time_sequence': [r'\textit{', r'}'],
    'abstract_time_interval': [r'\texttt{', r'}'],
    'abstract_time_instant': [r'\textsl{', r'}'],
}

_abstract_time_sequence_default_lin_repr = r'Ts'
_manifold_default_lin_repr = r'Manifold'
_mesh_default_lin_repr = r'Mesh'


def _parse_lin_repr(obj, lin_repr):
    """"""
    assert isinstance(lin_repr, str) and len(lin_repr) > 0, f"linguistic_representation must be str of length > 0."
    assert all([_ not in r"{\}" for _ in lin_repr]), f"lin_repr={lin_repr} illegal, cannot contain" + r"'{\}'."
    start, end = _global_lin_repr_setting[obj]
    return start + lin_repr + end, lin_repr


_manifold_default_sym_repr = r'\mathcal{M}'
_mesh_default_sym_repr = r'\mathfrak{M}'
_abstract_time_sequence_default_sym_repr = r'\mathtt{T}^S'
_abstract_time_interval_default_sym_repr = r'\Delta t'


def _check_sym_repr(sym_repr):
    """"""
    assert isinstance(sym_repr, str), f"sym_repr = {sym_repr} illegal, must be a string."
    pure_sym_repr = sym_repr.replace(' ', '')
    assert len(pure_sym_repr) > 0, f"sym_repr={sym_repr} illegal, it cannot be empty."
    return sym_repr


_global_operator_lin_repr_setting = {  # coded operators
    'wedge': r"\emph{wedge}",
    'Hodge': r'\emph{Hodge of}',
    'd': r'\emph{exterior-derivative of}',
    'codifferential': r'\emph{codifferential of}',
    'time_derivative': r'\emph{time-derivative of}',
    'trace': r'\emph{trace of}',
}

_global_operator_sym_repr_setting = {  # coded operators
    'wedge': r"\wedge",
    'Hodge': r'\star',
    'd': r'\mathrm{d}',
    'codifferential': r'\mathrm{d}^\ast',
    'time_derivative': r'\partial_t',
    'trace': r'\mathrm{tr}',
}
