# -*- coding: utf-8 -*-
"""
@author: Yi Zhang
@contact: zhangyi_aero@hotmail.com
@time: 11/26/2022 2:56 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')


from src.config import get_space_dim
from src.spaces.main import add, set_mesh


def wedge(s1, s2):
    """"""
    if s1.__class__.__name__ == 'ScalarValuedFormSpace' and s2.__class__.__name__ == 'ScalarValuedFormSpace':

        assert s1.mesh == s2.mesh, f"two entries have different meshes."

        k = s1.k
        l = s2.k

        assert k + l <= get_space_dim()

        set_mesh(s1.mesh)   # let the `space.mesh` become the current mesh.
        return add('Omega', k+l, s1.N + s2.N)

    else:
        raise NotImplementedError()


def Hodge(s):
    """A not well-defined one"""
    if s.__class__.__name__ == 'ScalarValuedFormSpace':
        n = get_space_dim()
        set_mesh(s.mesh)   # let the `space.mesh` become the current mesh.
        return add('Omega', n-s.k, s.N)
    else:
        raise NotImplementedError()


def d(space):
    """the range of exterior derivative operator on `space`."""
    if space.__class__.__name__ == 'ScalarValuedFormSpace':
        assert space.k < get_space_dim(), f'd of top-form is 0.'
        set_mesh(space.mesh)   # let the `space.mesh` become the current mesh.
        return add('Omega', space.k+1, space.N)
    else:
        raise NotImplementedError()


def codifferential(space):
    """the range of exterior derivative operator on `space`."""
    if space.__class__.__name__ == 'ScalarValuedFormSpace':
        assert space.k > 0, f'd of 0-form is 0.'
        set_mesh(space.mesh)   # let the `space.mesh` become the current mesh.
        return add('Omega', space.k-1, space.N)
    else:
        raise NotImplementedError()


if __name__ == '__main__':
    # python src/spaces/operators.py

    import __init__ as hp

    mesh = hp.mesh.static(None)
    hp.space.set_mesh(mesh)

    H1 = hp.space.add('Omega', k=1, N=1)
    H2 = hp.space.add('Omega', k=2, N=1)
    H3 = hp.space.add('Omega', k=3, N=1)

    # w = H1.generate_instance('\omega^1', "vorticity1")
    # u = H2.generate_instance('u^2', "velocity2")
    # f = H2.generate_instance('f^2', "body-force2")
    # P = H3.generate_instance('P^3', "total-pressure3")

    wXu = wedge(H1, H2).make_form('\omega^1', "vorticity1")
    dH2 = d(H2)
    du2 = dH2.make_form(r'\mathrm{d}u^2', "d-velocity")
    #
    du2.print_representations()

