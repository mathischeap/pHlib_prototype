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
from src.config import get_embedding_space_dim

_global_meshes = dict()  # we monitor all meshes to avoid that we use the same representation for different meshes.
_global_mesh_variables =  {
    'last_mesh': '',
}

def mesh(*args, **kwargs):
    return Mesh(*args, **kwargs)


def _list_meshes():
    """"""
    print('\n Existing meshes:')
    print('{:>15} | {}'.format('symbolic', 'abstract'))
    for rp in _global_meshes:
        abstract = _global_meshes[rp].is_abstract()
        print('{:>15} | {}'.format(rp, abstract))


class Mesh(Frozen):   #
    """"""

    def __init__(self, manifold, symbolic_representation=None):
        """

        Parameters
        ----------
        manifold
        symbolic_representation :
            We can customize the symbolic_representation of the mesh.
        """
        assert manifold.__class__.__name__ == 'Manifold', f"I need a manifold."
        self._manifold = manifold

        if symbolic_representation is None:
            number_existing_meshes = len(_global_meshes)
            while 1:
                symbolic_representation = r'\mathcal{T}_{' + str(number_existing_meshes) + '}'
                if symbolic_representation in _global_meshes:
                    number_existing_meshes += 1
                else:
                    break
        else:
            assert isinstance(symbolic_representation, str) and len(symbolic_representation)>0, \
                f"symbolic_representation must be a str of length > 0."
        assert symbolic_representation not in _global_meshes, \
            f"Manifold symbolic representation is illegal, pls specify a symbolic representation other than " \
            f"{set(_global_meshes.keys())}"
        _global_meshes[symbolic_representation] = self
        _global_mesh_variables['last_mesh'] = symbolic_representation
        self._symbolic_representation = symbolic_representation
        self._freeze()

    @property
    def n(self):
        """"""
        return get_embedding_space_dim()

    @property
    def ndim(self):
        """"""
        return self._manifold.ndim

    def __hash__(self):
        """This has to be updated later on. Same hash means the meshes are exactly the same. Cannot use
        symbolic_representation for the hash as two differently named meshes can be equal to each other.
        """
        raise NotImplementedError()

    def __eq__(self, other):
        """"""
        if self is other:
            return True
        else:
            return hash(self) == hash(other)

    def __repr__(self):
        """"""
        super_repr = super().__repr__().split('object')[-1]
        return '<Mesh ' + self._symbolic_representation + super_repr  # this will be unique.
