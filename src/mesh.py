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

_global_meshes = dict()  # we monitor all meshes to avoid that we use the same representation for different meshes.


def mesh(*args, **kwargs):
    """A wrapper of the Mesh class."""
    return Mesh(*args, **kwargs)


def _list_meshes():
    """"""
    print('\n Existing meshes:')
    print('{:>15} | {}'.format('symbolic', 'abstract'))
    for rp in _global_meshes:
        abstract = _global_meshes[rp].is_abstract()
        print('{:>15} | {}'.format(rp, abstract))


class Mesh(Frozen):   # Mesh -
    """"""

    def __init__(self, manifold, sym_repr=None):
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
            while 1:
                if number_existing_meshes == 0:
                    sym_repr = r'\mathfrak{M}'
                    break
                else:
                    sym_repr = r'\mathfrak{M}_{' + str(number_existing_meshes) + '}'
                    if sym_repr in _global_meshes:
                        number_existing_meshes += 1
                    else:
                        break
        else:
            assert isinstance(sym_repr, str), \
                f"sym_repr must be a str of length > 0."
            sym_repr = sym_repr.replace(' ', '')
            assert len(sym_repr) > 0, \
                f"sym_repr must be a str of length > 0."

        assert sym_repr not in _global_meshes, \
            f"Manifold symbolic representation is illegal, pls specify a symbolic representation other than " \
            f"{set(_global_meshes.keys())}"

        _global_meshes[sym_repr] = self
        self._sym_repr = sym_repr
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

    def boundary(self, sym_repr=None):
        """Give a mesh of dimensions (n-1) on the boundary manifold."""
        if self._boundary is None:
            manifold_boundary = self.manifold.boundary()
            if manifold_boundary.__class__.__name__ == 'Manifold':
                if sym_repr is None:
                    sym_repr = r'\eth' + self._sym_repr
                else:
                    pass
                self._boundary = Mesh(
                    manifold_boundary,
                    sym_repr
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
