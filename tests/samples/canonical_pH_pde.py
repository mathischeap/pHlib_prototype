# -*- coding: utf-8 -*-
"""
pH-lib@RAM-EEMCS-UT
created at: 3/14/2023 12:13 PM
"""
import sys

if './' not in sys.path:
    sys.path.append('./')

from src.config import set_embedding_space_dim
from src.manifold import manifold
from src.mesh import mesh
from src.pde import pde
import src.spaces.main as space


def pde_canonical_pH(n, p):
    """Generate pde representations of the canonical port-Hamiltonian systems."""
    set_embedding_space_dim(n)
    q = n + 1 - p

    m = manifold(n)
    m = mesh(m)

    space.set_mesh(m)
    O_p = space.new('Omega', p, orientation='outer')
    O_pm1 = space.new('Omega', p-1, orientation='outer')

    ap = O_p.make_form(r'\widehat{\alpha}^' + rf'{p}', 'a-p')
    bpm1 = O_pm1.make_form(r'\widehat{\beta}^{' + rf'{p-1}' + '}', 'b-pm1')

    sign1 = '+' if (-1) ** p == 1 else '-'
    sign2 = '+' if (-1) ** (p+1) == 1 else '-'

    pt_ap = ap.time_derivative()
    pt_bpm1 = bpm1.time_derivative()
    d_bpm1 = bpm1.exterior_derivative()
    ds_ap = ap.codifferential()

    outer_expression = [
        f'pt_ap = {sign1} d_bpm1',
        f'pt_bpm1 = {sign2} ds_ap'
    ]

    outer_pde = pde(outer_expression, locals())
    outer_pde._indi_dict = None  # clear this local expression
    outer_pde.unknowns = [ap, bpm1]

    inner_pde = None   # not implemented yet
    return outer_pde, inner_pde


if __name__ == '__main__':
    # python tests/samples/canonical_pH_pde.py

    pde_canonical_pH(3, 3)
