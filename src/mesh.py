# -*- coding: utf-8 -*-
"""
@author: Yi Zhang
@contact: zhangyi_aero@hotmail.com
@time: 11/26/2022 2:56 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')

from src.tools.frozen import Frozen
from src.config import _global_variables

_global_meshes = dict()  # we monitor all meshes to avoid that we use the same representation for different meshes.


def static(*args, **kwargs):
    return StaticMesh(*args, **kwargs)


def adaptive(*args, **kwargs):
    return StaticMesh(*args, **kwargs)


def moving(*args, **kwargs):
    return StaticMesh(*args, **kwargs)


class StaticMesh(Frozen):   #
    """"""

    def __init__(self, domain, symbolic_representation=None):
        """

        Parameters
        ----------
        domain
        symbolic_representation :
            We can customize the symbolic_representation of the mesh.
        """
        self._domain = domain

        if symbolic_representation is None:
            symbolic_representation = r"\mathcal{T}_" + f"{len(_global_meshes)}"
        else:
            raise NotImplementedError()

        assert symbolic_representation not in _global_meshes, \
            f"mesh symbolic_representation {symbolic_representation} is used."
        self._symbolic_representation = symbolic_representation
        self._freeze()

    @property
    def n(self):
        """"""
        return _global_variables['space_dim']

    def __hash__(self):
        """This has to be updated later on. Same hash means the meshes are exactly the same. Cannot use
        symbolic_representation for the hash.
        """
        return hash(('mesh', self.n))

    def __eq__(self, other):
        """"""
        if self is other:
            return True
        else:
            return hash(self) == hash(other)

    def __repr__(self):
        """"""
        return 'StaticMesh:' + self._symbolic_representation # this will be unique.


class AdaptiveMesh(StaticMesh):
    """"""


class MovingMesh(StaticMesh):
    """"""


if __name__ == '__main__':
    # python src/mesh.py
    import __init__ as ph

    mesh = ph.mesh.static(None)
    print(mesh == mesh)
