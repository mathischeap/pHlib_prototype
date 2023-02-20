# -*- coding: utf-8 -*-
"""
@author: Yi Zhang
@contact: zhangyi_aero@hotmail.com
@time: 11/26/2022 2:56 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')
from src.mesh import Mesh

from src.config import get_space_dim
from src.space.scalarValuedFormSpace import ScalarValuedFormSpace


def wedge(s1, s2):
    """"""
    if s1.__class__ is ScalarValuedFormSpace and s2.__class__ is ScalarValuedFormSpace:

        assert s1.mesh == s2.mesh, f"two entries have different meshes."

        k = s1.k
        l = s2.k

        assert k + l <= get_space_dim()

        return ScalarValuedFormSpace(s1.mesh, k+l, s1.N + s2.N)


if __name__ == '__main__':
    # python src/space/operators.py

    mesh = Mesh(None)
    H1 = ScalarValuedFormSpace(mesh, 1, 1)
    H2 = ScalarValuedFormSpace(mesh, 2, 1)
    H3 = ScalarValuedFormSpace(mesh, 3, 1)

    # w = H1.generate_instance('\omega^1', "vorticity1")
    # u = H2.generate_instance('u^2', "velocity2")
    # f = H2.generate_instance('f^2', "body-force2")
    # P = H3.generate_instance('P^3', "total-pressure3")


    wXu = wedge(H1, H2).generate_instance('\omega^1', "vorticity1")

    wXu.print_representations()
