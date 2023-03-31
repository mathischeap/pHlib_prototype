# -*- coding: utf-8 -*-
"""
pH-lib@RAM-EEMCS-UT
created at: 3/30/2023 6:19 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')

from mse.manifold.main import MseManifold, _global_mse_manifolds
from mse.mesh.main import MseMesh

__all__ = [
    '_parse_manifolds',
    '_parse_meshes',
    '_parse_spaces',
    '_parse_root_forms',
    '_parse',

    'config',
]


def _parse_manifolds(abstract_manifolds):
    """"""
    keys = list(_global_mse_manifolds.keys())
    for mf_sym_repr in keys:  # when ever we do this, we actually clear all existing manifolds.
        del _global_mse_manifolds[mf_sym_repr]
    for sym in abstract_manifolds:
        assert sym not in _global_mse_manifolds
        MseManifold(abstract_manifolds[sym])  # this will automatically cache the manifold to `_global_mse_manifolds`
    return _global_mse_manifolds


def _parse_meshes(abstract_meshes):
    """"""
    meshes = dict()
    for sym in abstract_meshes:
        am = abstract_meshes[sym]
        m = MseMesh(am)
        meshes[sym] = m
    return meshes


def _parse_spaces(abstract_spaces):
    """"""


def _parse_root_forms(abstract_rfs):
    """"""


def _parse(obj):
    """"""

from mse.manifold.main import config as _mf_config


def config(obj, *args,  **kwargs):
    if obj.__class__ is MseManifold:
        return _mf_config(obj, *args, **kwargs)
    else:
        raise NotImplementedError()
