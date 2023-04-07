# -*- coding: utf-8 -*-
"""
pH-lib@RAM-EEMCS-UT
created at: 3/30/2023 6:19 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')
from src.tools.frozen import Frozen
from msepy.manifold.main import MsePyManifold, _global_mse_manifolds
from msepy.mesh.main import MsePyMesh
from src.config import SIZE   # MPI.SIZE


__all__ = [
    '_parse_manifolds',
    '_parse_meshes',
    '_parse_spaces',
    '_parse_root_forms',
    '_parse',

    'config',
]

def _chech_config():
    """"""
    assert SIZE == 1, f"msepy only works for single thread call (MPI.SIZE=1), now MPI.size = {SIZE}"


def _parse_manifolds(abstract_manifolds):
    """"""
    keys = list(_global_mse_manifolds.keys())
    for mf_sym_repr in keys:  # when ever we do this, we actually clear all existing manifolds.
        del _global_mse_manifolds[mf_sym_repr]
    for sym in abstract_manifolds:
        assert sym not in _global_mse_manifolds
        MsePyManifold(abstract_manifolds[sym])  # this will automatically cache the manifold to `_global_mse_manifolds`
    return _global_mse_manifolds


def _parse_meshes(abstract_meshes):
    """"""
    meshes = dict()
    for sym in abstract_meshes:
        am = abstract_meshes[sym]
        m = MsePyMesh(am)
        meshes[sym] = m
    return meshes


def _parse_spaces(abstract_spaces):
    """"""


def _parse_root_forms(abstract_rfs):
    """"""


def _parse(obj):
    """"""


from msepy.manifold.main import config as _mf_config


def config(obj):
    return _Config(obj)


class _Config(Frozen):
    """"""
    def __init__(self, obj):
        self._obj = obj

    def __call__(self, *args, **kwargs):
        if self._obj.__class__ is MsePyManifold:
            return _mf_config(self._obj, *args, **kwargs)
        else:
            raise NotImplementedError()
