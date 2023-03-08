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
from src.config import _mesh_default_sym_repr
from src.config import _check_sym_repr
from src.config import _parse_lin_repr
from src.config import _mesh_default_lin_repr

_global_meshes = dict()  # we monitor all meshes to avoid that we use the same representation for different meshes.


def mesh(manifold):
    """A wrapper of the Mesh class."""
    return Mesh(manifold)


def _list_meshes():
    """"""
    print('\n Existing meshes:')
    print('{:>15} | {}'.format('symbolic', 'abstract'))
    for rp in _global_meshes:
        abstract = _global_meshes[rp].is_abstract()
        print('{:>15} | {}'.format(rp, abstract))


class Mesh(Frozen):   # Mesh -
    """"""

    def __init__(self, manifold, sym_repr=None, lin_repr=None):
        """

        Parameters
        ----------
        manifold
        sym_repr :
            We can customize the sym_repr of the mesh.
        """
        assert manifold.__class__.__name__ == 'Manifold', f"I need a manifold."
        self._manifold = manifold

        if sym_repr is None:
            number_existing_meshes = len(_global_meshes)
            base_repr = _mesh_default_sym_repr
            if number_existing_meshes == 0:
                sym_repr = base_repr
            else:
                sym_repr = base_repr + r'_{' + str(number_existing_meshes) + '}'
        else:
            pass
        sym_repr = _check_sym_repr(sym_repr)

        if lin_repr is None:
            base_repr = _mesh_default_lin_repr
            number_existing_meshes = len(_global_meshes)

            if number_existing_meshes == 0:
                lin_repr = base_repr
            else:
                lin_repr = base_repr + str(number_existing_meshes)

        assert sym_repr not in _global_meshes, \
            f"Manifold symbolic representation is illegal, pls specify a symbolic representation other than " \
            f"{set(_global_meshes.keys())}"

        for _ in _global_meshes:
            _m = _global_meshes[_]
            assert lin_repr != _m._lin_repr
        lin_repr, pure_lin_repr = _parse_lin_repr('mesh', lin_repr)

        self._sym_repr = sym_repr
        self._lin_repr = lin_repr
        self._pure_pure_lin_repr = pure_lin_repr
        _global_meshes[sym_repr] = self

        self._boundary = None
        self._interface = None
        self._inclusion = None
        self._freeze()

    @property
    def ndim(self):
        """"""
        return self._manifold.ndim

    def __repr__(self):
        """"""
        super_repr = super().__repr__().split('object')[-1]
        return '<Mesh ' + self._sym_repr + super_repr  # this will be unique.

    @property
    def manifold(self):
        """The manifold this mesh is based on."""
        return self._manifold

    def boundary(self):
        """Give a mesh of dimensions (n-1) on the boundary manifold."""
        if self._boundary is None:
            manifold_boundary = self.manifold.boundary()
            if manifold_boundary.__class__.__name__ == 'Manifold':
                self._boundary = Mesh(
                    manifold_boundary,
                    sym_repr=r'\eth' + self._sym_repr,
                    lin_repr=r'boundary-of-' + self._pure_pure_lin_repr
                )
                self._boundary._inclusion = self
            elif manifold_boundary.__class__.__name__ == 'NullManifold':
                self._boundary = NullMesh(manifold_boundary)
            else:
                raise NotImplementedError()
        return self._boundary

    def inclusion(self):
        """Give the mesh of dimensions (n+1) on the inclusion manifold."""
        return self._inclusion


class NullMesh(Frozen):
    """A mesh that is constructed upon a null manifold."""

    def __init__(self, null_manifold):
        self._null_manifold = null_manifold
        self._freeze()

    @property
    def ndim(self):
        return self._null_manifold.ndim
