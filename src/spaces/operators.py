# -*- coding: utf-8 -*-
"""
@author: Yi Zhang
@contact: zhangyi_aero@hotmail.com
@time: 11/26/2022 2:56 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')

from src.spaces.main import new


def wedge(s1, s2):
    """"""
    if s1.__class__.__name__ == 'ScalarValuedFormSpace' and s2.__class__.__name__ == 'ScalarValuedFormSpace':

        assert s1.mesh == s2.mesh, f"two entries have different meshes."

        k = s1.k
        l = s2.k

        assert k + l <= s1.mesh.ndim

        return new('Omega', k + l, s1.p + s2.p, mesh=s1.mesh)

    else:
        raise NotImplementedError()


def Hodge(s):
    """A not well-defined one"""
    if s.__class__.__name__ == 'ScalarValuedFormSpace':
        n = s.mesh.ndim
        return new('Omega', n - s.k, s.p, mesh=s.mesh)
    else:
        raise NotImplementedError()


def d(space):
    """the range of exterior derivative operator on `space`."""
    if space.__class__.__name__ == 'ScalarValuedFormSpace':
        assert space.k < space.mesh.ndim, f'd of top-form-space: {space} is 0.'
        return new('Omega', space.k + 1, space.p, mesh=space.mesh)
    else:
        raise NotImplementedError()


def codifferential(space):
    """the range of exterior derivative operator on `space`."""
    if space.__class__.__name__ == 'ScalarValuedFormSpace':
        assert space.k > 0, f'd of 0-form is 0.'
        return new('Omega', space.k - 1, space.p, mesh=space.mesh)
    else:
        raise NotImplementedError(f"codifferential of {space} is not implemented or not even possible.")


def trace(space):
    if space.__class__.__name__ == 'ScalarValuedFormSpace':
        mesh = space.mesh
        assert 0 <= space.k < mesh.ndim, f"Cannot do trace on {space}."
        boundary_mesh = mesh.boundary()
        return new('Omega', space.k, space.p, mesh = boundary_mesh)

    else:
        raise NotImplementedError(f"trace of {space} is not implemented or not even possible.")
