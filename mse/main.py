# -*- coding: utf-8 -*-
"""
pH-lib@RAM-EEMCS-UT
created at: 3/30/2023 6:19 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')

from mse.manifold import MseManifolds
from mse.mesh.main import MseMesh


def parse_manifolds(abstract_manifolds):
    """"""
    manifolds = dict()
    for sym in abstract_manifolds:
        am = abstract_manifolds[sym]
        m = MseManifolds(am)
        manifolds[sym] = m
    return manifolds


def parse_meshes(abstract_meshes):
    """"""
    meshes = dict()
    for sym in abstract_meshes:
        am = abstract_meshes[sym]
        m = MseMesh(am)
        meshes[sym] = m
    return meshes


def parse_spaces(abstract_spaces):
    """"""

def parse_root_forms(abstract_rfs):
    """"""

def parse(obj):
    """"""
