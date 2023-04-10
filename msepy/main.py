# -*- coding: utf-8 -*-
"""
pH-lib@RAM-EEMCS-UT
created at: 3/30/2023 6:19 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')
from src.tools.frozen import Frozen
from msepy.manifold.main import MsePyManifold
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


base = {
    'manifolds': dict(),
    'meshes': dict(),
    'spaces': dict(),
    'forms': dict(),  # root-forms
}


def _chech_config():
    """"""
    assert SIZE == 1, f"msepy only works for single thread call (MPI.SIZE=1), now MPI.size = {SIZE}"


def _parse_manifolds(abstract_manifolds):
    """"""
    manifold_dict = {}
    for sym in abstract_manifolds:
        manifold = MsePyManifold(abstract_manifolds[sym])
        manifold_dict[sym] = manifold
    base['manifolds'] = manifold_dict


def _parse_meshes(abstract_meshes):
    """"""
    meshes = dict()
    for sym in abstract_meshes:
        am = abstract_meshes[sym]
        m = MsePyMesh(am)
        meshes[sym] = m
    base['meshes'] = meshes


def _parse_spaces(abstract_spaces):
    """"""


def _parse_root_forms(abstract_rfs):
    """"""


def _parse(obj):
    """"""
    if hasattr(obj, "_sym_repr"):
        sym_repr = obj._sym_repr
        if sym_repr in base['manifolds']:
            return base['manifolds'][sym_repr]
        elif sym_repr in base['meshes']:
            return base['meshes'][sym_repr]
        else:
            pass

    else:
        pass


from msepy.manifold.main import config as _mf_config
from msepy.mesh.main import config as _mh_config


def config(obj):
    return _Config(obj)


class _Config(Frozen):
    """"""
    def __init__(self, obj):
        self._obj = obj

    def __call__(self, *args, **kwargs):
        if self._obj.__class__ is MsePyManifold:
            return _mf_config(self._obj, *args, **kwargs)
        elif self._obj.__class__ is MsePyMesh:
            mesh = self._obj
            abstract_mesh = mesh.abstract
            abstract_manifold = abstract_mesh.manifold
            mnf = None
            for mnf_sr in base['manifolds']:
                mnf = base['manifolds'][mnf_sr]
                if mnf.abstract is abstract_manifold:
                    break
            assert mnf is not None, f"cannot find a valid mse-py-manifold."

            return _mh_config(self._obj, mnf, *args, **kwargs)
        else:
            raise NotImplementedError()
